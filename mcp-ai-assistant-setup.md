# AI assistant (MCP)

Other languages: [Română](ro/mcp-ai-assistant-setup.md) · [Afrikaans](af/mcp-ai-assistant-setup.md) · [العربية](ar/mcp-ai-assistant-setup.md) · [Čeština](cs/mcp-ai-assistant-setup.md) · [Dansk](da/mcp-ai-assistant-setup.md) · [Deutsch](de/mcp-ai-assistant-setup.md) · [Español](es/mcp-ai-assistant-setup.md) · [Suomi](fi/mcp-ai-assistant-setup.md) · [Français](fr/mcp-ai-assistant-setup.md) · [हिन्दी](hi/mcp-ai-assistant-setup.md) · [Magyar](hu/mcp-ai-assistant-setup.md) · [Bahasa Indonesia](id/mcp-ai-assistant-setup.md) · [Italiano](it/mcp-ai-assistant-setup.md) · [日本語](ja/mcp-ai-assistant-setup.md) · [한국어](ko/mcp-ai-assistant-setup.md) · [Nederlands](nl/mcp-ai-assistant-setup.md) · [Polski](pl/mcp-ai-assistant-setup.md) · [Português do Brasil](pt-BR/mcp-ai-assistant-setup.md) · [Русский](ru/mcp-ai-assistant-setup.md) · [Svenska](sv/mcp-ai-assistant-setup.md) · [Kiswahili](sw/mcp-ai-assistant-setup.md) · [ไทย](th/mcp-ai-assistant-setup.md) · [Türkçe](tr/mcp-ai-assistant-setup.md) · [Українська](uk/mcp-ai-assistant-setup.md) · [Tiếng Việt](vi/mcp-ai-assistant-setup.md) · [简体中文](zh-Hans/mcp-ai-assistant-setup.md)

Licensed teams connect **OrganizeFiles.Cli** to Claude Desktop, **Cursor**, VS Code Copilot or another Model Context Protocol client, called an MCP client below. The connector is the **organize-files-mcp** Python package. It is a free download from github.com/GutRaz/organize-files-docs, in its `mcp/` folder.

**In the desktop app:** open **MCP setup…** under **Application & data** in the options column, or from the tools menu. Choose **MCP access**: **Off**, **Monitor** or **Control**. Then copy the JSON snippet. Reload MCP in the AI app after every change of level, because **Control** makes a new token each time.

**Ask the documentation assistant** "setup mcp" or "cum setez mcp" for the steps on the current system.

## MCP access levels, set in the app

The levels match three kinds of work: **read / preview / execute**.

| Level | Kind of work | What the AI can do |
|-------|--------|-------------------|
| **Off** | — | Only `organize_mcp_status`. No diagnostics and no access to the workspace. |
| **Monitor** | **Read** | Everything in Off, plus read-only diagnostics, run and job history, locks, audit checks, **`organize_capabilities`** and **`organize_workspace_snapshot`**. `organize_capabilities` lists the run modes, **`ai`** among them, the move scopes and the targets. `organize_workspace_snapshot` shows the workspace saved in the main window. No preview and no execute. |
| **Control** | **Preview** / **Execute** | Everything in Monitor, plus **`organize_create_job`**, **`organize_run_workspace`** and **`organize_remove_empty_organize_layout`**. It needs a **control token** in the MCP settings, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. **Preview** is `organize_run_workspace` when the saved workspace has **Dry run** on, so nothing is written. **Execute** is the same tool with Dry run off, so files are moved. The connector leaves out `--confirm-destructive` unless the call sets `confirm_destructive=true`, and without it the command line refuses with `confirm_destructive_required`. |

The control file is **`mcp-control.json`**, next to `automation-jobs.json` in the app's profile folder. The copied snippet does not name it, because the connector finds it in the default profile folder. Set **`ORGANIZE_FILES_MCP_CONTROL_FILE`** only when the file is somewhere else. At **Control**, the snippet also sets **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`**.

**Moving and deleting takes a second, human step.** The assistant sets its own confirmation, so text it reads could talk it into confirming. A run that is not a dry run therefore also needs a window opened in **MCP setup**, and that window closes by itself after 15 minutes. Outside it the assistant can still prepare and preview a run, but the run itself is refused. Both the control file and the window are signed with a key this installation keeps. A control file that was changed by hand, or copied from another computer, counts as Off.

## MCP tools by level

**Always, also at Off:** `organize_mcp_status`

**Monitor and Control:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide`, and `organize_run_raw_cli`, which accepts only read-only commands.

**Also in Monitor and Control:** `organize_capabilities`, which lists the run mode **`ai`** for AI and ML files, and `organize_workspace_snapshot`.

**Control only:** `organize_create_job` from the workspace or from job JSON, `organize_run_workspace` for a preview or a real run as the workspace's Dry run says, and `organize_remove_empty_organize_layout`, which removes empty layout folders inside an existing output and never creates the output folder itself.

Commands that move or delete files are always blocked through MCP outside the **Control** level. No other setting allows them.

## Command-line flags the connector uses

| Flag | Level | Purpose |
|------|-------|---------|
| `--mcp-control-status` | any | JSON with the level, the control file path and the Monitor and Control flags |
| `--mcp-capabilities` | Monitor and above | JSON list of run modes, **`ai`** among them, move scopes and targets |
| `--mcp-workspace-snapshot` | Monitor and above | The saved workspace and how it maps to a job |
| `--mcp-create-job` | Control | Create a job with `--from-workspace` or `--mcp-job-json` |
| `--mcp-run-workspace` | Control | Run the saved workspace, with `--allow-app-target` and `--mcp-control-token` |
| `--remove-empty-organize-layout` | Control | Remove empty layout folders inside an existing `--output` |
| `--confirm-destructive` | Control | Needed with `--mcp-run-workspace` for a run that moves or deletes. The connector passes it only when `confirm_destructive=true` |

## Settings in the MCP client JSON

| Setting | When |
|----------|------|
| `ORGANIZE_FILES_CLI` | Path to OrganizeFiles.Cli |
| `ORGANIZE_FILES_JOBS_FILE` | Path to `automation-jobs.json` |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | Path to `mcp-control.json`, only when it is not in the default profile folder |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | **Control** level only, from the app's snippet |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | **Control** level, for runs of the saved workspace |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | Optional. The same token the host uses for read operations |

## Windows setup

1. **Python 3.10 or newer** — run `python -V` in PowerShell. If Python is missing or older, install it from [python.org](https://www.python.org/downloads/) and tick **Add python.exe to PATH**.
2. **Download and install the connector** — download github.com/GutRaz/organize-files-docs as a ZIP, unpack it and run `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1`. The script makes a private Python environment for the connector and prints the command for the AI app.
3. **In the app:** **MCP setup…**, choose **Monitor** or **Control**, then copy the JSON.
4. **Paths:** `%LocalAppData%\OrganizeFilesCrossPlatform\` holds the jobs and `mcp-control.json`. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **Test** — run `organize_mcp_status`, then `organize_server_info`. `cliResolved` must be true and `mcpLevel` must match the app.

## macOS setup

The same steps with **python3** and `bash mcp/install-organize-files-mcp.sh`. If `python3 -V` shows 3.9 or no Python at all, first install Python from [python.org](https://www.python.org/downloads/macos/). Paths: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Linux setup

The same steps with **python3** and `bash mcp/install-organize-files-mcp.sh`. On Debian and Ubuntu, first run `sudo apt install python3-venv`. Paths: `~/.local/share/OrganizeFilesCrossPlatform/`, or `$XDG_DATA_HOME` when it is set, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## Security

- MCP runs as **the local user** of the operating system, with the same rights as the command line run by hand.
- Keep the **control token** and the **read token** secret, like passwords. Copy the JSON again after turning on Control.
- **`organize_run_workspace`** runs in the command line, not through the Run button of the app. Do not run two jobs on the same output folder at the same time.
- Examples: `mcp/examples/`.

## Runs that move or delete

`--mcp-run-workspace` needs `--confirm-destructive` for every run that is not a dry run, whether it moves, deletes or archives. Without it the command line answers `confirm_destructive_required`. The connector leaves the flag out unless the call sets `confirm_destructive=true`, which only the Control level can do. So by default the connector refuses.

## Languages

The setup answers come from the same translated guide as the Documentation window and the Guide assistant. `organize_capabilities` reports run modes and targets, not names of themes in the app.
