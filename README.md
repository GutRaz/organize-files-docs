# Organize Files public guides

This repository holds public guides for Organize Files, and the AI connector that lets an AI app work with Organize Files on the same computer.

Legal documents, such as the licence terms, the privacy policy and the third-party notices, are in [organize-files-legal](https://github.com/GutRaz/organize-files-legal).

## Guides

| Guide | What it covers |
| ----- | -------------- |
| [AI assistant and MCP](mcp-ai-assistant-setup.md) | Connecting Claude Desktop, Cursor, VS Code Copilot or another MCP app to Organize Files, in every language of the app |
| [AI connector](mcp/README.md) | The files and the install scripts of the connector |
| [Performance and tuning](performance-and-tuning.md) | Being rewritten in plain language |
| [Automation server deployment](automation-server-deployment.md) | Being rewritten in plain language |
| [Enterprise operations](automation-enterprise-operations.md) | Being rewritten in plain language |
| [Containers and Kubernetes](containers-and-kubernetes.md) | Being rewritten in plain language |

## Systems

The desktop app runs on Windows, macOS and Linux. The phone apps run on Android and iOS. The AI connector runs on Windows, macOS and Linux, on the same computer as the desktop app.

## Where the app keeps its data

| System | Folder |
| ------ | ------ |
| Windows | `%LocalAppData%\OrganizeFilesCrossPlatform\` |
| macOS | `~/Library/Application Support/OrganizeFilesCrossPlatform/` |
| Linux | `~/.local/share/OrganizeFilesCrossPlatform/`, or the same folder name under `$XDG_DATA_HOME` when it is set |
| Android and iOS | Private to the app, with no folder a person can open |

## Good to know

- Examples use placeholders such as `__REPLACE_ME__`. A real token never belongs in a shared file.
- When a guide and the app disagree, the app is the one to follow, and a note about the difference is welcome.

## Contact

Corrections and questions: <razvan.gutulov@outlook.com>
