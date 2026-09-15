"""Discover installed OrganizeFiles.Cli for customer MCP deployments."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path
from typing import Sequence


def installed_cli_candidates() -> list[Path]:
    """Return likely retail / server install locations (checked before dev repo paths)."""
    names = ("OrganizeFiles.Cli.exe", "OrganizeFiles.Cli", "organize-files-cli")
    found: list[Path] = []

    for name in names:
        which = shutil.which(name)
        if which:
            found.append(Path(which))

    install_dir = os.environ.get("ORGANIZE_FILES_INSTALL_DIR", "").strip()
    if install_dir:
        root = Path(install_dir)
        for name in names:
            found.append(root / name)
        found.append(root / "OrganizeFiles.Cli.dll")

    if sys.platform == "win32":
        program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
        program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
        for base in (program_files, program_files_x86):
            found.extend(
                [
                    Path(base) / "OrganizeFiles" / "Cli" / "OrganizeFiles.Cli.exe",
                    Path(base) / "OrganizeFiles" / "Cli" / "OrganizeFiles.Cli.dll",
                    Path(base) / "OrganizeFiles" / "JobAgent" / "OrganizeFiles.Cli.exe",
                    Path(base) / "OrganizeFiles" / "JobAgent" / "OrganizeFiles.Cli.dll",
                ]
            )
    elif sys.platform == "darwin":
        found.extend(
            [
                Path("/usr/local/bin/OrganizeFiles.Cli"),
                Path("/opt/organize-files/OrganizeFiles.Cli"),
                Path("/opt/organize-files/OrganizeFiles.Cli.dll"),
            ]
        )
        applications = Path("/Applications")
        if applications.is_dir():
            for app in applications.glob("Organize Files*.app"):
                macos = app / "Contents" / "MacOS"
                found.extend(
                    [
                        macos / "OrganizeFiles.Cli",
                        macos / "OrganizeFiles.Cli.dll",
                    ]
                )
    else:
        found.extend(
            [
                Path("/usr/local/bin/OrganizeFiles.Cli"),
                Path("/usr/bin/OrganizeFiles.Cli"),
                Path("/opt/organize-files/OrganizeFiles.Cli"),
                Path("/opt/organize-files/OrganizeFiles.Cli.dll"),
            ]
        )

    home = Path.home()
    found.extend(
        [
            home / ".local" / "bin" / "OrganizeFiles.Cli",
            home / "OrganizeFiles" / "Cli" / "OrganizeFiles.Cli",
            home / "OrganizeFiles" / "Cli" / "OrganizeFiles.Cli.dll",
        ]
    )

    deduped: list[Path] = []
    seen: set[str] = set()
    for candidate in found:
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(candidate)
    return deduped


def first_existing_cli(candidates: Sequence[Path]) -> Path | None:
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None
