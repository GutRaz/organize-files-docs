"""Run OrganizeFiles.Cli subprocesses with shared env and safety guards."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Mapping, Sequence

from organize_files_mcp.cli_discovery import installed_cli_candidates
from organize_files_mcp.mcp_control import (
    LEVEL_CONTROL,
    LEVEL_MONITOR,
    LEVEL_OFF,
    effective_level,
    load_control_state,
    resolve_control_file,
    resolve_control_token,
)


DEFAULT_TIMEOUT_SECONDS = 1200
READ_ONLY_PREFIXES = (
    "--query-runs",
    "--show-run",
    "--query-jobs",
    "--list-running",
    "--due-pass-lock-status",
    "--output-lock-status",
    "--verify-audit",
    "--tail-run-log",
    "--export-run-log",
    "--help",
    "--check-update",
)

MCP_MONITOR_PREFIXES = (
    "--mcp-control-status",
    "--mcp-capabilities",
    "--mcp-workspace-snapshot",
)

MCP_CONTROL_PREFIXES = (
    "--mcp-create-job",
    "--mcp-run-workspace",
    "--remove-empty-organize-layout",
)


class CliRunnerError(RuntimeError):
    pass


_resolved_cli_invocation: list[str] | None = None


def reset_cli_invocation_cache_for_tests() -> None:
    global _resolved_cli_invocation
    _resolved_cli_invocation = None


def resolve_cli_invocation() -> list[str]:
    """Return argv prefix to launch OrganizeFiles.Cli (dotnet dll or native exe)."""
    global _resolved_cli_invocation
    if _resolved_cli_invocation is not None:
        return list(_resolved_cli_invocation)

    explicit = os.environ.get("ORGANIZE_FILES_CLI", "").strip()
    if explicit:
        path = Path(explicit)
        if path.suffix.lower() == ".dll":
            dotnet = shutil.which("dotnet")
            if not dotnet:
                raise CliRunnerError("ORGANIZE_FILES_CLI points to a .dll but dotnet is not on PATH.")
            return _store_resolved_cli_invocation([dotnet, str(path)])
        return _store_resolved_cli_invocation([str(path)])

    saw_dll_without_dotnet = False
    for candidate in installed_cli_candidates():
        if not candidate.is_file():
            continue
        if candidate.suffix.lower() == ".dll":
            dotnet = shutil.which("dotnet")
            if dotnet:
                return _store_resolved_cli_invocation([dotnet, str(candidate)])
            saw_dll_without_dotnet = True
            continue
        return _store_resolved_cli_invocation([str(candidate)])

    for candidate in _dev_cli_candidates():
        if not candidate.is_file():
            continue
        if candidate.suffix.lower() == ".dll":
            dotnet = shutil.which("dotnet")
            if dotnet:
                return _store_resolved_cli_invocation([dotnet, str(candidate)])
            saw_dll_without_dotnet = True
            continue
        return _store_resolved_cli_invocation([str(candidate)])

    if saw_dll_without_dotnet:
        raise CliRunnerError(
            "Found OrganizeFiles.Cli.dll but dotnet is not on PATH. "
            "Install the .NET runtime or set ORGANIZE_FILES_CLI to the native executable."
        )

    raise CliRunnerError(
        "OrganizeFiles.Cli not found. Set ORGANIZE_FILES_CLI to OrganizeFiles.Cli.dll or the published executable."
    )


def _store_resolved_cli_invocation(invocation: list[str]) -> list[str]:
    global _resolved_cli_invocation
    _resolved_cli_invocation = list(invocation)
    return invocation


def _dev_cli_candidates() -> Sequence[Path]:
    here = Path(__file__).resolve()
    repo_root = here
    for _ in range(6):
        if (repo_root / "OrganizeFiles.sln").is_file():
            break
        repo_root = repo_root.parent
    else:
        repo_root = here.parents[3]

    # Prefer published/bin CLI paths. Test builds are never picked here: set ORGANIZE_FILES_CLI
    # explicitly to use one.
    return [
        repo_root / "src" / "OrganizeFiles.Cli" / "artifacts" / "linux-x64" / "OrganizeFiles.Cli.dll",
        repo_root / "src" / "OrganizeFiles.Cli" / "bin" / "Release" / "net10.0" / "OrganizeFiles.Cli.dll",
    ]


_MUTATION_ARG_PREFIXES = (
    "--run-due-jobs",
    "--run-once",
    "--run-job",
    "--stop-job",
    "--remove-job",
    "--jobs-daemon",
    "--approve-execute",
    "--approve-and-run",
    "--and-run",
    "--force-execute",
    "--execute",
    "--confirm-destructive",
    "--confirm-delete",
    "--delete-issues",
    "--delete-duplicates",
    "--export-audit",
    "--replay-webhooks",
    "--mcp-run-workspace",
    "--mcp-create-job",
    "--remove-empty-organize-layout",
)


def _normalize_cli_arg_glyphs(arg: str) -> str:
    """Map common Unicode lookalike dashes/spaces to ASCII so blocklists cannot be smuggled."""
    text = str(arg)
    for src, dst in (
        ("\u2010", "-"),  # hyphen
        ("\u2011", "-"),  # non-breaking hyphen
        ("\u2012", "-"),  # figure dash
        ("\u2013", "-"),  # en dash
        ("\u2014", "-"),  # em dash
        ("\u2212", "-"),  # minus sign
        ("\uFE63", "-"),  # small hyphen-minus
        ("\uFF0D", "-"),  # fullwidth hyphen-minus
        ("\u00A0", " "),  # nbsp
        ("\u200B", ""),  # zero-width space
        ("\u200C", ""),  # ZWNJ
        ("\u200D", ""),  # ZWJ
        ("\uFEFF", ""),  # BOM / ZWNBSP
    ):
        text = text.replace(src, dst)
    return text


def _arg_head(arg: str) -> str:
    return _normalize_cli_arg_glyphs(arg).split("=", 1)[0]


def _is_mutation_arg(arg: str) -> bool:
    head = _arg_head(arg).casefold()
    return any(head == b.casefold() or head.startswith(b.casefold()) for b in _MUTATION_ARG_PREFIXES)


def export_root() -> Path:
    """The one folder the bridge may drop exported run logs into."""
    return resolve_control_file().parent / "mcp-exports"


def _export_destination_index(args: Sequence[str]) -> int | None:
    for i, arg in enumerate(args):
        if _arg_head(arg).casefold() == "--export-run-log" and i + 2 < len(args):
            return i + 2
    return None


def resolve_confined_export_destination(args: Sequence[str]) -> Path | None:
    """
    ``--export-run-log`` names its own destination, and it reads as an observability command, so it
    sits in the read-only allowlist. Its third argument is still a path this account can write, which
    means text the assistant reads could aim a run log at a customer document, or at the key the
    control file is signed with. The command keeps working; it just cannot leave one folder.

    Returns the resolved destination, or ``None`` when the command is not present.
    """
    index = _export_destination_index(args)
    if index is None:
        return None

    raw = args[index].strip()
    if not raw:
        raise CliRunnerError("Export destination is required.")

    root = export_root()
    candidate = Path(raw).expanduser()
    try:
        resolved = (candidate if candidate.is_absolute() else root / candidate).resolve()
        root_resolved = root.resolve()
    except OSError as ex:
        raise CliRunnerError("Export destination could not be resolved.") from ex

    if resolved != root_resolved and root_resolved not in resolved.parents:
        raise CliRunnerError(
            f"Export destination must stay inside {root_resolved}. "
            "Pass a bare file name and the bridge places it there."
        )

    return resolved


def assert_read_only_args(args: Sequence[str]) -> None:
    if not args:
        raise CliRunnerError("At least one CLI argument is required.")
    head = args[0]
    level = effective_level()
    resolve_confined_export_destination(args)

    if head in MCP_CONTROL_PREFIXES:
        if level != LEVEL_CONTROL:
            raise CliRunnerError(
                f"Command {head!r} requires MCP Control level. Current level is {level!r}."
            )
        # Still reject smuggled mutation flags after a Control head.
        # Workspace run and empty-layout cleanup may append --confirm-destructive when opted in.
        for arg in args[1:]:
            if _is_mutation_arg(arg) and _arg_head(arg).casefold() != head.casefold():
                if (
                    head in {"--mcp-run-workspace", "--remove-empty-organize-layout"}
                    and _arg_head(arg).casefold() == "--confirm-destructive"
                ):
                    continue
                raise CliRunnerError(
                    f"Trailing argument {arg!r} is blocked after Control command {head!r}."
                )
        return

    if head in MCP_MONITOR_PREFIXES:
        if level not in {LEVEL_MONITOR, LEVEL_CONTROL}:
            raise CliRunnerError(
                f"Command {head!r} requires MCP Monitor or Control. Current level is {level!r}."
            )
        for arg in args[1:]:
            if _is_mutation_arg(arg):
                raise CliRunnerError(
                    f"Trailing argument {arg!r} is blocked after Monitor command {head!r}."
                )
        return

    # Fail closed: even allowlisted heads must not smuggle mutation flags later in argv.
    for arg in args[1:]:
        if _is_mutation_arg(arg):
            raise CliRunnerError(
                f"Trailing argument {arg!r} is blocked in read-only MCP mode."
            )

    if level == LEVEL_OFF:
        if head == "--help":
            return
        raise CliRunnerError(
            "MCP access is Off. Open Organize Files → Application & data → MCP setup and choose Monitor or Control."
        )

    if not any(head == prefix for prefix in READ_ONLY_PREFIXES):
        if _is_mutation_arg(head):
            raise CliRunnerError(
                f"Command {head!r} is blocked in read-only MCP mode. "
                "Set MCP Control in the app for approved workspace runs."
            )
        raise CliRunnerError(f"Command {head!r} is not in the MCP read-only allowlist.")


# Settings that must never reach the command line from an AI app's configuration. They are removed
# before every call. This file is a public download, so it keeps only the SHA-256 digest of each name.
_BLOCKED_ENV_NAME_DIGESTS = frozenset(
    {
        "66dca8bb0788f6e32fec8b178af86d233bc18c8c483d4264bcbd660f6717526e",
        "80159e437d8cfb14b5d5b42471dbdc2fa34b7cc817a2afd4c9a6bf477f53c344",
        "860d4cf544c4c52aad2a3a4a2141cb2000aa7d90cb7ad26c596d8f842235e8fc",
        "a41f589a06d4ee446de54f6e4a6311c836ff64f35ddfad3b2260fa314392146d",
        "b8f8ca7c1768e3a61a03537147ee6af241ae1d815645210765ff3833870c7610",
        "b9ea07332914967eb32a9da464c1b956aaceb54bd15c34d466e77dd5c70e95f6",
        "ba5fc432af1aba0aa0615d2e6940ad216cd85803f850d05e592099275d7e17fd",
    }
)


def _env_name_digest(name: str) -> str:
    return hashlib.sha256(name.encode("utf-8")).hexdigest()


def strip_blocked_env(env: dict[str, str]) -> dict[str, str]:
    """Drop every blocked setting from ``env`` and return it."""
    for key in [k for k in env if k.startswith("ORGANIZE_FILES_") and _env_name_digest(k) in _BLOCKED_ENV_NAME_DIGESTS]:
        env.pop(key, None)
    return env


def run_cli(
    args: Sequence[str],
    *,
    extra_env: Mapping[str, str] | None = None,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    stdin_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run the CLI with the argument guard, the confined export path and the control token.

    ``stdin_text`` feeds a job body on standard input. It exists so that path cannot drift from this
    one: the server used to have a second runner for stdin that copied the environment and stopped
    there, so creating a job from JSON reached the CLI without the control token this function
    injects, and without the export-destination confinement.
    """
    assert_read_only_args(args)

    args = list(args)
    destination = resolve_confined_export_destination(args)
    index = _export_destination_index(args)
    if destination is not None and index is not None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        # Rewrite so a bare file name cannot land wherever the CLI happens to be running from.
        args[index] = str(destination)

    cmd = resolve_cli_invocation() + list(args)
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    # Strip after the merge, so extra_env cannot put a blocked setting back.
    env = strip_blocked_env(env)

    # Tokens stay in env (ORGANIZE_FILES_MCP_READ_TOKEN / ORGANIZE_FILES_MCP_CONTROL_TOKEN).
    # CLI hosts prefer those env vars. Do not inject --read-token / --mcp-control-token into
    # argv (process-list leak). Legacy: argv still works as fallback when passed explicitly.
    control_token = resolve_control_token()
    if control_token:
        env["ORGANIZE_FILES_MCP_CONTROL_TOKEN"] = control_token

    if args and args[0] == "--mcp-run-workspace" and "--allow-app-target" not in args:
        cmd.append("--allow-app-target")

    try:
        return subprocess.run(
            cmd,
            input=stdin_text,
            capture_output=True,
            text=True,
            env=env,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as ex:
        raise CliRunnerError(f"CLI timed out after {timeout_seconds}s: {' '.join(args)}") from ex


def describe_cli_resolution() -> dict[str, str | bool | list[str] | None]:
    """Return MCP-friendly status for customer setup diagnostics."""
    explicit = os.environ.get("ORGANIZE_FILES_CLI", "").strip()
    installed = [str(p) for p in installed_cli_candidates() if p.is_file()]
    dev = [str(p) for p in _dev_cli_candidates() if p.is_file()]
    try:
        resolved = resolve_cli_invocation()
        resolved_text = " ".join(resolved)
        ok = True
    except CliRunnerError as ex:
        resolved_text = str(ex)
        ok = False

    control = load_control_state()
    level = str(control.get("level", LEVEL_OFF))
    return {
        "cliResolved": ok,
        "resolvedInvocation": resolved_text,
        "organizeFilesCliEnv": explicit or None,
        "installedCandidatesFound": installed,
        "devCandidatesFound": dev,
        "mcpLevel": level,
        "mcpControlFile": control.get("controlFile"),
        "mcpMonitorEnabled": level in {LEVEL_MONITOR, LEVEL_CONTROL},
        "mcpControlEnabled": level == LEVEL_CONTROL,
        "mcpWorkspaceControlEnabled": level == LEVEL_CONTROL,
    }


def format_cli_result(result: subprocess.CompletedProcess[str]) -> str:
    parts: list[str] = [f"exitCode={result.returncode}"]
    stdout = (result.stdout or "").strip()
    stderr = (result.stderr or "").strip()
    if stdout:
        parts.append("stdout:\n" + stdout)
    if stderr:
        parts.append("stderr:\n" + stderr)
    return "\n\n".join(parts)
