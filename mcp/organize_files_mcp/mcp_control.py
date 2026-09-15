"""Resolve MCP Off / Monitor / Control tier from the GUI-written control file."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import sys
from pathlib import Path
from typing import Any

LEVEL_OFF = "off"
LEVEL_MONITOR = "monitor"
LEVEL_CONTROL = "control"

VALID_LEVELS = frozenset({LEVEL_OFF, LEVEL_MONITOR, LEVEL_CONTROL})

SIGNING_KEY_FILE = "mcp-control.key"
SIGNING_KEY_BYTES = 32


def _verify_signature(payload: dict[str, Any], control_file: Path) -> bool:
    """True when this installation's key signed exactly these fields.

    The signed timestamp is read back verbatim rather than rebuilt, because reconstructing a .NET
    round-trip timestamp here would have to match it to the digit, and one mismatch would reject a
    tier the user really did choose.
    """
    signature = str(payload.get("signature", "") or "").strip().lower()
    if not signature:
        return False

    try:
        key = (control_file.parent / SIGNING_KEY_FILE).read_bytes()
    except OSError:
        return False
    if len(key) != SIGNING_KEY_BYTES:
        return False

    signed = "|".join(
        [
            "mcp-control",
            "v1",
            str(payload.get("version", "")),
            str(payload.get("level", "")),
            str(payload.get("controlToken", "") or ""),
            str(payload.get("signedAt", "") or ""),
        ]
    )
    expected = hmac.new(key, signed.encode("utf-8"), hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)


def resolve_control_file() -> Path:
    explicit = os.environ.get("ORGANIZE_FILES_MCP_CONTROL_FILE", "").strip()
    if explicit:
        return Path(explicit)
    return _default_control_file()


def _profile_subfolder() -> str:
    custom = os.environ.get("ORGANIZE_FILES_PROFILE_SUBFOLDER", "").strip()
    return custom if custom else "OrganizeFilesCrossPlatform"


def _default_control_file() -> Path:
    subfolder = _profile_subfolder()
    if sys.platform == "win32":
        local_app_data = os.environ.get("LOCALAPPDATA", "").strip()
        if local_app_data:
            return Path(local_app_data) / subfolder / "mcp-control.json"

    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / subfolder / "mcp-control.json"

    xdg_data = os.environ.get("XDG_DATA_HOME", "").strip()
    if xdg_data:
        return Path(xdg_data) / subfolder / "mcp-control.json"

    return Path.home() / ".local" / "share" / subfolder / "mcp-control.json"


def resolve_control_token() -> str:
    """Prefer the GUI-written control file token over a stale MCP env token."""
    file_token = str(load_control_state().get("controlToken", "") or "").strip()
    if file_token:
        return file_token
    return os.environ.get("ORGANIZE_FILES_MCP_CONTROL_TOKEN", "").strip()


def load_control_state() -> dict[str, Any]:
    path = resolve_control_file()
    if not path.is_file():
        return {
            "level": LEVEL_OFF,
            "controlToken": "",
            "controlFile": str(path),
            "loadStatus": "missing",
            "loadError": None,
        }

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {
            "level": LEVEL_OFF,
            "controlToken": "",
            "controlFile": str(path),
            "loadStatus": "invalid_json",
            "loadError": "mcp_control_file_invalid_json",
        }
    except OSError:
        return {
            "level": LEVEL_OFF,
            "controlToken": "",
            "controlFile": str(path),
            "loadStatus": "read_error",
            "loadError": "mcp_control_file_read_error",
        }

    level = str(payload.get("level", LEVEL_OFF)).strip().lower()
    if level.isdigit():
        level = {0: LEVEL_OFF, 1: LEVEL_MONITOR, 2: LEVEL_CONTROL}.get(int(level), LEVEL_OFF)
    if level not in VALID_LEVELS:
        level = LEVEL_OFF

    # Off grants nothing, so it needs no proof. Anything above it reaches tools that move and delete
    # a customer's files, and only this installation's key may authorise that.
    if level != LEVEL_OFF and not _verify_signature(payload, path):
        return {
            "level": LEVEL_OFF,
            "controlToken": "",
            "controlFile": str(path),
            "loadStatus": "signature_mismatch",
            "loadError": "mcp_control_file_signature_mismatch",
        }

    token = str(payload.get("controlToken", "") or "").strip()
    return {
        "level": level,
        "controlToken": token,
        "controlFile": str(path),
        "updatedUtc": payload.get("updatedUtc"),
        "loadStatus": "ok",
        "loadError": None,
    }


def effective_level() -> str:
    return str(load_control_state().get("level", LEVEL_OFF))


def monitor_enabled() -> bool:
    return effective_level() in {LEVEL_MONITOR, LEVEL_CONTROL}


def control_enabled() -> bool:
    return effective_level() == LEVEL_CONTROL


def describe_control_state() -> dict[str, Any]:
    state = load_control_state()
    level = state["level"]
    env_control_file = os.environ.get("ORGANIZE_FILES_MCP_CONTROL_FILE", "").strip()
    default_path = str(_default_control_file())
    env_token = os.environ.get("ORGANIZE_FILES_MCP_CONTROL_TOKEN", "").strip()
    file_token = str(state.get("controlToken", "") or "").strip()
    return {
        "level": level,
        "controlFile": state.get("controlFile"),
        "controlFileExists": Path(str(state.get("controlFile", ""))).is_file(),
        "loadStatus": state.get("loadStatus"),
        "loadError": state.get("loadError"),
        "monitorEnabled": level in {LEVEL_MONITOR, LEVEL_CONTROL},
        "controlEnabled": level == LEVEL_CONTROL,
        "updatedUtc": state.get("updatedUtc"),
        "envControlFileSet": bool(env_control_file),
        "defaultControlFile": default_path,
        "controlFileMatchesDefault": not env_control_file
        and str(state.get("controlFile", "")) == default_path,
        "envControlTokenStale": bool(env_token and file_token and env_token != file_token),
        # Prefer app/CLI --mcp-control-status (localized McpReloadToolsHint). This Python
        # fallback is English-only for hosts that never spawn the CLI status path.
        "reloadToolsHint": (
            "After changing MCP access in the app, reload MCP in the AI client. "
            "Clients that support notifications/tools/list_changed refresh automatically."
        ),
    }
