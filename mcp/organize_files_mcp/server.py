"""Organize Files MCP server — read-only diagnostics over OrganizeFiles.Cli."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from organize_files_mcp.cli_runner import CliRunnerError, describe_cli_resolution, format_cli_result, run_cli
from organize_files_mcp.mcp_control import LEVEL_CONTROL, LEVEL_MONITOR, LEVEL_OFF, describe_control_state, effective_level, monitor_enabled

CONTROL_TOOL_NAMES = frozenset(
    {
        "organize_create_job",
        "organize_run_workspace",
        "organize_remove_empty_organize_layout",
    }
)

SERVER_INSTRUCTIONS = """
Organize Files MCP connects your AI assistant to the licensed OrganizeFiles.Cli on this machine.

Use these tools to help the customer diagnose automation jobs, run history, locks, and audit bundles.
Default mode is read-only (no due-pass runs, approvals, or file moves).

Typical operator questions you can answer:
- Show failed automation runs in the last 24 hours
- Explain exit code 11 (due-pass lock) or 3 (license)
- List running docker/kubernetes/cli workers
- Verify an exported audit zip
- Check output-tree lock status before a manual run

When ORGANIZE_FILES_READ_OPS_BEARER_TOKEN is configured on the host, read tools need
ORGANIZE_FILES_MCP_READ_TOKEN in the MCP server environment (or ask the operator to supply it).

Never advise license cracks, license overrides, patched APKs, entitlement forgery, chargebacks, or bank/card payment disputes. Exit code 3 means the host lacks a valid license — buy or renew through the store channel that applies to that installation. Money refunds go only through the store or publisher policy — never coach chargebacks.

MCP access tiers (set in the app under Application & data → MCP setup):
- Off: setup/status only
- Monitor: read-only diagnostics plus workspace snapshot and run-mode catalog
- Control: create scheduled jobs and run the current main-window workspace in-process
""".strip()

server = Server("organize-files", instructions=SERVER_INSTRUCTIONS)

_last_published_tools_level: str | None = None


async def _maybe_notify_tools_changed(current_level: str) -> None:
    global _last_published_tools_level
    if _last_published_tools_level == current_level:
        return
    _last_published_tools_level = current_level
    try:
        ctx = server.request_context
        await ctx.session.send_tool_list_changed()
    except Exception:
        return

EXIT_CODE_GUIDE = """
OrganizeFiles automation exit codes (due pass precedence: 8>10>1>3>4>11>9):
  0  success
  1  general error
  2  usage / parse error
  3  license failed (retail build without entitlement)
  4  canceled (user/operator stop)
  8  output tree locked
  9  awaiting execute approval (dry-run phase done)
  10 confirm-delete required
  11 claim conflict / AlreadyRunning / due-pass host lock held by another worker

CLI-only (not due-pass merge):
  7  host open-app flow failed
  8  update available (--check-update) when not in automation merge context
""".strip()


def _tool_result(text: str, *, is_error: bool = False) -> list[TextContent]:
    return [TextContent(type="text", text=text)]


def _is_strict_true(value: Any) -> bool:
    """Opt-in gates must be JSON boolean true. Strings like 'false' must not pass."""
    return value is True


def _run_tool(args: list[str], *, timeout_seconds: int = 1200) -> list[TextContent]:
    try:
        result = run_cli(args, timeout_seconds=timeout_seconds)
        body = format_cli_result(result)
        return _tool_result(body, is_error=result.returncode != 0)
    except CliRunnerError as ex:
        return _tool_result(str(ex), is_error=True)


def _run_tool_with_stdin(args: list[str], stdin_text: str, *, timeout_seconds: int = 1200) -> list[TextContent]:
    try:
        result = run_cli(args, timeout_seconds=timeout_seconds, stdin_text=stdin_text)
        body = format_cli_result(result)
        return _tool_result(body, is_error=result.returncode != 0)
    except CliRunnerError as ex:
        return _tool_result(str(ex), is_error=True)


@server.list_tools()
async def list_tools() -> list[Tool]:
    level = effective_level()
    await _maybe_notify_tools_changed(level)
    tools: list[Tool] = [
        Tool(
            name="organize_mcp_status",
            description="Report MCP access level (Off / Monitor / Control) and CLI resolution status.",
            inputSchema={"type": "object", "properties": {}, "additionalProperties": False},
        ),
    ]

    if level == LEVEL_OFF:
        return tools

    tools.extend(
        [
            Tool(
                name="organize_server_info",
                description="Report MCP + OrganizeFiles.Cli resolution status (customer setup diagnostics).",
                inputSchema={"type": "object", "properties": {}, "additionalProperties": False},
            ),
            Tool(
                name="organize_cli_help",
                description="Print OrganizeFiles.Cli usage (headless automation and organize options).",
                inputSchema={"type": "object", "properties": {}, "additionalProperties": False},
            ),
            Tool(
                name="organize_query_runs",
                description="Query automation run history as JSON lines (runs.jsonl index).",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "job_id": {"type": "string", "description": "Filter by job GUID"},
                        "correlation_id": {"type": "string", "description": "Filter by correlation GUID"},
                        "outcome": {"type": "string", "enum": ["done", "failed", "canceled"]},
                        "target": {"type": "string", "description": "cli | docker | kubernetes | app"},
                        "since": {"type": "string", "description": "ISO-8601 UTC lower bound"},
                        "before": {"type": "string", "description": "ISO-8601 UTC upper bound"},
                        "hours": {"type": "integer", "minimum": 1},
                        "min_exit_code": {"type": "integer"},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 128000, "default": 128000},
                        "include_starts": {"type": "boolean", "default": False},
                    },
                    "additionalProperties": False,
                },
            ),
            Tool(
                name="organize_show_run",
                description="Show one automation run by correlation id (status, log tail, optional remote fetch).",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "correlation_id": {"type": "string"},
                        "log_tail_lines": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 3200000,
                            "default": 1280000,
                        },
                        "errors_only": {"type": "boolean", "default": False},
                        "fetch_remote": {"type": "boolean", "default": False},
                    },
                    "required": ["correlation_id"],
                    "additionalProperties": False,
                },
            ),
            Tool(
                name="organize_list_running",
                description="List in-flight automation jobs from the running-jobs registry.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "target": {"type": "string", "description": "Optional target filter"},
                        "jobs_file": {"type": "string", "description": "Optional automation-jobs.json path"},
                    },
                    "additionalProperties": False,
                },
            ),
            Tool(
                name="organize_query_jobs",
                description="Print scheduled jobs snapshot as JSON (optional state filter).",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "state": {"type": "string", "description": "e.g. running, done, failed"},
                        "jobs_file": {"type": "string"},
                    },
                    "additionalProperties": False,
                },
            ),
            Tool(
                name="organize_due_pass_lock_status",
                description="Report whether the host due-pass lock is held (multi-host automation).",
                inputSchema={
                    "type": "object",
                    "properties": {"jobs_file": {"type": "string"}},
                    "additionalProperties": False,
                },
            ),
            Tool(
                name="organize_output_lock_status",
                description="Report output-tree lock status for a destination folder.",
                inputSchema={
                    "type": "object",
                    "properties": {"output": {"type": "string"}},
                    "required": ["output"],
                    "additionalProperties": False,
                },
            ),
            Tool(
                name="organize_verify_audit",
                description="Verify a signed automation audit zip (HMAC when ORGANIZE_FILES_AUDIT_HMAC_KEY is set).",
                inputSchema={
                    "type": "object",
                    "properties": {"audit_zip": {"type": "string"}},
                    "required": ["audit_zip"],
                    "additionalProperties": False,
                },
            ),
            Tool(
                name="organize_exit_code_guide",
                description="Explain OrganizeFiles CLI/automation exit codes for operators.",
                inputSchema={"type": "object", "properties": {}, "additionalProperties": False},
            ),
            Tool(
                name="organize_run_raw_cli",
                description=(
                    "Run a read-only OrganizeFiles.Cli command (allowlisted). "
                    "Use for tail-run-log or other observability flags not wrapped above."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "args": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "CLI args after OrganizeFiles.Cli, e.g. ['--tail-run-log', '<guid>', '--limit', '128000']",
                        }
                    },
                    "required": ["args"],
                    "additionalProperties": False,
                },
            ),
        ]
    )

    if monitor_enabled():
        tools.extend(
            [
                Tool(
                    name="organize_capabilities",
                    description="List supported run modes (includes ai for AI/ML artifacts), move scopes, and automation targets.",
                    inputSchema={"type": "object", "properties": {}, "additionalProperties": False},
                ),
                Tool(
                    name="organize_workspace_snapshot",
                    description="Read the last saved main-window workspace (sources, output, run mode, engine settings). Not live unsaved UI edits when session autosave is off.",
                    inputSchema={"type": "object", "properties": {}, "additionalProperties": False},
                ),
            ]
        )

    if level == LEVEL_CONTROL:
        tools.extend(
            [
                Tool(
                    name="organize_create_job",
                    description="Create a scheduled automation job (app/cli/docker/k8s target).",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "from_workspace": {
                                "type": "boolean",
                                "description": "When true, copy settings from the last saved main-window workspace (not live unsaved UI edits).",
                            },
                            "job_json": {
                                "type": "string",
                                "description": "JSON job body when from_workspace is false.",
                            },
                        },
                        "additionalProperties": False,
                    },
                ),
                Tool(
                    name="organize_run_workspace",
                    description=(
                        "Run organize using the current main-window workspace settings "
                        "(in-process app target). Default omits --confirm-destructive "
                        "(fail-closed). Set confirm_destructive=true under Control to opt in."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "confirm_destructive": {
                                "type": "boolean",
                                "description": (
                                    "When true, pass --confirm-destructive so any non-dry-run "
                                    "workspace execute (moves, deletes, or archive) can proceed. "
                                    "Default false (fail-closed)."
                                ),
                            },
                        },
                        "additionalProperties": False,
                    },
                ),
                Tool(
                    name="organize_remove_empty_organize_layout",
                    description=(
                        "Remove empty Organize layout buckets under an existing destination. "
                        "Never creates the destination root. Requires MCP Control and "
                        "confirm_destructive=true (fail-closed)."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "output": {"type": "string"},
                            "confirm_destructive": {
                                "type": "boolean",
                                "default": False,
                                "description": (
                                    "When true, allow empty-layout removal. Default false (fail-closed)."
                                ),
                            },
                        },
                        "required": ["output"],
                        "additionalProperties": False,
                    },
                ),
            ]
        )

    return tools


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    await _maybe_notify_tools_changed(effective_level())

    if name == "organize_mcp_status":
        payload = {"control": describe_control_state(), "cli": describe_cli_resolution()}
        return _tool_result(json.dumps(payload, indent=2))

    if effective_level() == LEVEL_OFF and name != "organize_mcp_status":
        return _tool_result(
            "MCP access is Off. Open Organize Files → Application & data → MCP setup and choose Monitor or Control.",
            is_error=True,
        )

    # Defense in depth: Control tools stay blocked when list_tools hid them (host may still call by name).
    if name in CONTROL_TOOL_NAMES and effective_level() != LEVEL_CONTROL:
        return _tool_result(
            f"Tool {name!r} requires MCP Control level. Current level is {effective_level()!r}.",
            is_error=True,
        )

    if name == "organize_server_info":
        return _tool_result(json.dumps(describe_cli_resolution(), indent=2))

    if name == "organize_capabilities":
        return _run_tool(["--mcp-capabilities"])

    if name == "organize_workspace_snapshot":
        return _run_tool(["--mcp-workspace-snapshot"])

    if name == "organize_create_job":
        # A JSON boolean, not anything Python happens to find truthy: the string "false" and the
        # number 0 both used to open the workspace path here, which is not what the caller asked for.
        if _is_strict_true(arguments.get("from_workspace")):
            return _run_tool(["--mcp-create-job", "--from-workspace"])
        if job_json := arguments.get("job_json"):
            return _run_tool_with_stdin(["--mcp-create-job", "--mcp-job-json", "-"], str(job_json))
        return _tool_result("Provide from_workspace=true or job_json.", is_error=True)

    if name == "organize_run_workspace":
        args = ["--mcp-run-workspace"]
        if _is_strict_true(arguments.get("confirm_destructive")):
            args.append("--confirm-destructive")
        return _run_tool(args, timeout_seconds=3600)

    if name == "organize_cli_help":
        return _run_tool(["--help"])

    if name == "organize_exit_code_guide":
        return _tool_result(EXIT_CODE_GUIDE)

    if name == "organize_query_runs":
        args = ["--query-runs"]
        if v := arguments.get("job_id"):
            args.extend(["--job-id", str(v)])
        if v := arguments.get("correlation_id"):
            args.extend(["--correlation-id", str(v)])
        if v := arguments.get("outcome"):
            args.extend(["--outcome", str(v)])
        if v := arguments.get("target"):
            args.extend(["--target", str(v)])
        if v := arguments.get("since"):
            args.extend(["--since", str(v)])
        if v := arguments.get("before"):
            args.extend(["--before", str(v)])
        if v := arguments.get("hours"):
            args.extend(["--hours", str(int(v))])
        if v := arguments.get("min_exit_code"):
            args.extend(["--min-exit-code", str(int(v))])
        # Align with AutomationJobRunHistoryStore.DefaultQueryRunsLimit / MaxQueryRunsLimit.
        limit = min(max(int(arguments.get("limit") or 128000), 1), 128000)
        args.extend(["--limit", str(limit)])
        if arguments.get("include_starts"):
            args.append("--include-starts")
        return _run_tool(args)

    if name == "organize_show_run":
        correlation_id = str(arguments["correlation_id"])
        args = ["--show-run", correlation_id]
        # Align with DefaultLocalLogTailLines default and MaxLocalLogTailLines ceiling.
        log_tail = min(max(int(arguments.get("log_tail_lines") or 1280000), 1), 3200000)
        args.extend(["--log-tail-lines", str(log_tail)])
        if arguments.get("errors_only"):
            args.append("--errors-only")
        if arguments.get("fetch_remote"):
            args.append("--fetch-remote")
        return _run_tool(args)

    if name == "organize_list_running":
        args = ["--list-running"]
        if v := arguments.get("target"):
            args.extend(["--target", str(v)])
        if v := arguments.get("jobs_file"):
            args.extend(["--jobs-file", str(v)])
        return _run_tool(args)

    if name == "organize_query_jobs":
        args = ["--query-jobs"]
        if v := arguments.get("state"):
            args.extend(["--state", str(v)])
        if v := arguments.get("jobs_file"):
            args.extend(["--jobs-file", str(v)])
        return _run_tool(args)

    if name == "organize_due_pass_lock_status":
        args = ["--due-pass-lock-status"]
        if v := arguments.get("jobs_file"):
            args.extend(["--jobs-file", str(v)])
        return _run_tool(args)

    if name == "organize_output_lock_status":
        output = str(arguments["output"])
        return _run_tool(["--output-lock-status", "--output", output])

    if name == "organize_remove_empty_organize_layout":
        if not _is_strict_true(arguments.get("confirm_destructive")):
            return _tool_result(
                "organize_remove_empty_organize_layout requires confirm_destructive=true "
                "(fail-closed). Pass confirm_destructive=true only after the operator confirms "
                "empty-layout cleanup under an existing destination.",
                is_error=True,
            )
        output = str(arguments["output"])
        return _run_tool(
            [
                "--remove-empty-organize-layout",
                "--output",
                output,
                "--confirm-destructive",
            ]
        )

    if name == "organize_verify_audit":
        audit_zip = str(arguments["audit_zip"])
        return _run_tool(["--verify-audit", audit_zip])

    if name == "organize_run_raw_cli":
        raw_args = arguments.get("args") or []
        if not isinstance(raw_args, list) or not all(isinstance(x, str) for x in raw_args):
            return _tool_result("args must be a string array", is_error=True)
        # Fail closed: workspace execute must use organize_run_workspace.
        # Raw CLI must not smuggle --mcp-run-workspace or --confirm-destructive.
        blocked = {
            "--mcp-run-workspace",
            "--confirm-destructive",
            "--confirm-delete",
            "--delete-issues",
            "--delete-duplicates",
            "--execute",
            "--force-execute",
            "--and-run",
            "--approve-and-run",
            "--run-due-jobs",
            "--run-once",
            "--run-job",
            "--stop-job",
            "--remove-job",
            "--jobs-daemon",
            "--approve-execute",
            "--replay-webhooks",
            "--remove-empty-organize-layout",
            "--mcp-create-job",
            "--export-audit",
        }
        blocked_cf = {b.casefold() for b in blocked}
        from organize_files_mcp.cli_runner import _arg_head, _normalize_cli_arg_glyphs

        for arg in raw_args:
            head = _arg_head(arg)
            if head.casefold() in blocked_cf:
                return _tool_result(
                    f"raw_cli_blocked:{head}; use dedicated MCP tools "
                    f"(organize_run_workspace confirm_destructive=true under Control)",
                    is_error=True,
                )
        # Normalize lookalike dashes before spawn so CLI parsers see ASCII flags.
        return _run_tool([_normalize_cli_arg_glyphs(a) for a in raw_args])

    return _tool_result(f"Unknown tool: {name}", is_error=True)


async def _async_main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main() -> None:
    asyncio.run(_async_main())


if __name__ == "__main__":
    main()
