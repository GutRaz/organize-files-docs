# Organize Files AI connector

This folder holds the connector that lets an AI app, such as Claude Desktop, Cursor or VS Code Copilot, work with Organize Files on the same computer. It uses the Model Context Protocol, called MCP below.

The full steps, in every language of the app, are in the app itself: open **Documentation** and read the chapter **AI assistant (MCP)**.

## What is needed

- Organize Files, with its command line tool **OrganizeFiles.Cli**.
- Python 3.10 or newer. The install script checks this and says what to install when it is missing.

## Install

Download this repository as a ZIP and unpack it. Then run the script for the system, from this folder.

Windows, in PowerShell or a command prompt:

```powershell
powershell -ExecutionPolicy Bypass -File Install-OrganizeFilesMcp.ps1
```

Windows does not run a downloaded script by its name alone, so the command asks PowerShell to run this one script as it is.

macOS and Linux, in a terminal:

```bash
bash install-organize-files-mcp.sh
```

The script makes a Python environment just for the connector, installs the connector there, checks that it loads and prints the full path of that environment's Python. The Python already on the computer is not changed. Run the script again later to update the connector.

When Python is missing or too old, the script says what to install and stops. On Debian and Ubuntu it can ask for one more package, for example `sudo apt install python3-venv`.

To put the environment in another folder, set `ORGANIZE_FILES_MCP_HOME` before running the script.

## Connect the AI app

1. In Organize Files, open **MCP setup…** and choose **Monitor** or **Control**.
2. Copy the JSON the app shows into the MCP settings of the AI app.
3. In `command`, put the full Python path the install script printed.
4. Reload MCP in the AI app, or restart the AI app.

Examples: `examples/claude-desktop.json` and `examples/cursor-mcp.json`.

## Check

Ask the AI app to run `organize_mcp_status`, then `organize_server_info`. `cliResolved` must be true.

## Remove

1. Delete the environment folder. On Windows it is `%LOCALAPPDATA%\OrganizeFilesMcp\venv`. On macOS and Linux it is `~/.local/share/organize-files-mcp`.
2. Remove the `organize-files` entry from the MCP settings of the AI app.

## Safety

- The connector has the same rights as the user who starts the AI app.
- Keep the tokens in the JSON secret, like passwords.
- Moving or deleting files needs the **Control** level and a window that a person opens in **MCP setup**. That window closes by itself after 15 minutes.
