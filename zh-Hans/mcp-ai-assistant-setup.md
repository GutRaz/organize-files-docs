# 人工智能助手（MCP）

获得许可的团队将 **OrganizeFiles.Cli** 连接到 Claude Desktop、**Cursor**、VS Code Copilot 或其他 Model Context Protocol 客户端，下文称为 MCP 客户端。连接器是 Python 包 **organize-files-mcp**。可从 github.com/GutRaz/organize-files-docs 的 `mcp/` 文件夹免费下载。

**在桌面应用中：** 在选项列的 **应用与数据** 下或工具菜单中打开 **MCP 设置...**。选择 **MCP访问**：**关闭**、**监视** 或 **控制**。然后复制 JSON 片段。每次更改级别后，请在 AI 应用中重新加载 MCP，因为 **控制** 每次都会生成新的令牌。

**向文档助手提问** “setup mcp” 或 “cum setez mcp”，即可获得当前系统上的步骤。

## 在应用中设置的 MCP 访问级别

级别对应三类工作：**读取 / 预览 / 执行**。

| 级别 | 工作类型 | AI 能做什么 |
|-------|--------|-------------------|
| **关闭** | — | 仅 `organize_mcp_status`。没有诊断，也不能访问工作区。 |
| **监视** | **读取** | 包括关闭级别的全部内容，另加只读诊断、运行和任务历史、锁、审核检查、**`organize_capabilities`** 和 **`organize_workspace_snapshot`**。`organize_capabilities` 列出运行模式，其中包括 **`ai`**，还列出移动范围和目标。`organize_workspace_snapshot` 显示主窗口中保存的工作区。没有预览，也没有执行。 |
| **控制** | **预览** / **执行** | 包括监视级别的全部内容，另加 **`organize_create_job`**、**`organize_run_workspace`** 和 **`organize_remove_empty_organize_layout`**。需要在 MCP 设置中提供 **控制令牌** `ORGANIZE_FILES_MCP_CONTROL_TOKEN`。**预览** 是指保存的工作区开启 **试运行** 时的 `organize_run_workspace`，因此不会写入任何内容。**执行** 是指关闭试运行时的同一工具，因此文件会被移动。除非调用设置了 `confirm_destructive=true`，否则连接器不会加上 `--confirm-destructive`，而没有这个标志时，命令行会以 `confirm_destructive_required` 拒绝。 |

控制文件是 **`mcp-control.json`**，位于应用配置文件夹中 `automation-jobs.json` 的旁边。复制的片段不写出这个文件，因为连接器会在默认配置文件夹中自行找到这个文件。只有当文件位于其他位置时，才设置 **`ORGANIZE_FILES_MCP_CONTROL_FILE`**。在 **控制** 级别，片段还会设置 **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`**。

**移动和删除需要第二个由人完成的步骤。** 助手会自行设置确认，因此助手读到的文本可能诱使助手确认。所以不是试运行的运行还需要在 **MCP 设置** 中打开的时间窗口，该窗口会在 15 分钟后自动关闭。在窗口之外，助手仍可准备并预览一次运行，但运行本身会被拒绝。控制文件和该窗口都用本安装持有的密钥签名。手动修改过的控制文件，或从其他计算机复制来的控制文件，都按关闭处理。

## 按级别划分的 MCP 工具

**始终可用，关闭级别也可用：** `organize_mcp_status`

**监视和控制：** `organize_server_info`、`organize_cli_help`、`organize_query_runs`、`organize_show_run`、`organize_list_running`、`organize_query_jobs`、`organize_due_pass_lock_status`、`organize_output_lock_status`、`organize_verify_audit`、`organize_exit_code_guide`，以及只接受只读命令的 `organize_run_raw_cli`。

**监视和控制中还有：** 为 AI 和 ML 文件列出运行模式 **`ai`** 的 `organize_capabilities`，以及 `organize_workspace_snapshot`。

**仅控制：** 从工作区或任务 JSON 创建任务的 `organize_create_job`，按工作区的试运行设置进行预览或真实运行的 `organize_run_workspace`，以及删除现有输出中的空布局文件夹、但从不创建输出文件夹本身的 `organize_remove_empty_organize_layout`。

移动或删除文件的命令，在 **控制** 级别之外始终会被 MCP 阻止。其他任何设置都不能允许这些命令。

## 连接器使用的命令行标志

| 标志 | 级别 | 用途 |
|------|-------|---------|
| `--mcp-control-status` | 任意 | 包含级别、控制文件路径以及监视和控制标记的 JSON |
| `--mcp-capabilities` | 监视及以上 | 运行模式、其中的 **`ai`**、移动范围和目标的 JSON 列表 |
| `--mcp-workspace-snapshot` | 监视及以上 | 保存的工作区，以及工作区如何对应到一个任务 |
| `--mcp-create-job` | 控制 | 使用 `--from-workspace` 或 `--mcp-job-json` 创建任务 |
| `--mcp-run-workspace` | 控制 | 使用 `--allow-app-target` 和 `--mcp-control-token` 运行保存的工作区 |
| `--remove-empty-organize-layout` | 控制 | 删除现有 `--output` 中的空布局文件夹 |
| `--confirm-destructive` | 控制 | 与 `--mcp-run-workspace` 一起用于会移动或删除的运行。连接器只在 `confirm_destructive=true` 时传递这个标志 |

## MCP 客户端 JSON 中的设置

| 设置 | 何时 |
|----------|------|
| `ORGANIZE_FILES_CLI` | OrganizeFiles.Cli 的路径 |
| `ORGANIZE_FILES_JOBS_FILE` | `automation-jobs.json` 的路径 |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | `mcp-control.json` 的路径，仅当文件不在默认配置文件夹中时 |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | 仅 **控制** 级别，来自应用的片段 |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | **控制** 级别，用于运行保存的工作区 |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | 可选。与主机读取操作所用的令牌相同 |

## Windows 设置

1. **Python 3.10 或更新版本** — 在 PowerShell 中运行 `python -V`。如果没有 Python 或版本较旧，请从 [python.org](https://www.python.org/downloads/) 安装，并勾选 **Add python.exe to PATH**。
2. **下载并安装连接器** — 以 ZIP 形式下载 github.com/GutRaz/organize-files-docs，解压后运行 `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1`。脚本会为连接器创建专用的 Python 环境，并打印给 AI 应用使用的命令。
3. **在应用中：** 打开 **MCP 设置...**，选择 **监视** 或 **控制**，然后复制 JSON。
4. **路径：** `%LocalAppData%\OrganizeFilesCrossPlatform\` 中保存任务和 `mcp-control.json`。Cursor：`%USERPROFILE%\.cursor\mcp.json`。Claude：`%APPDATA%\Claude\claude_desktop_config.json`。VS Code：`%USERPROFILE%\.vscode\mcp.json`。
5. **测试** — 运行 `organize_mcp_status`，然后运行 `organize_server_info`。`cliResolved` 必须为 true，`mcpLevel` 必须与应用一致。

## macOS 设置

使用 **python3** 和 `bash mcp/install-organize-files-mcp.sh`，步骤相同。如果 `python3 -V` 显示 3.9 或根本没有 Python，请先从 [python.org](https://www.python.org/downloads/macos/) 安装 Python。路径：`~/Library/Application Support/OrganizeFilesCrossPlatform/`、`~/.cursor/mcp.json`、Claude `~/Library/Application Support/Claude/claude_desktop_config.json`。

## Linux 设置

使用 **python3** 和 `bash mcp/install-organize-files-mcp.sh`，步骤相同。在 Debian 和 Ubuntu 上，请先运行 `sudo apt install python3-venv`。路径：`~/.local/share/OrganizeFilesCrossPlatform/`，或在设置了 `$XDG_DATA_HOME` 时使用该路径，`~/.cursor/mcp.json`、Claude `~/.config/Claude/claude_desktop_config.json`。

## 安全

- MCP 以操作系统的 **本地用户** 身份运行，权限与手动运行的命令行相同。
- 请像对待密码一样保密 **控制令牌** 和 **读取令牌**。开启控制后，请重新复制 JSON。
- **`organize_run_workspace`** 在命令行中运行，而不是通过应用的运行按钮。不要同时在同一个输出文件夹上运行两个任务。
- 示例：`mcp/examples/`。

## 会移动或删除的运行

对于每一次不是试运行的运行，无论是移动、删除还是归档，`--mcp-run-workspace` 都需要 `--confirm-destructive`。没有这个标志时，命令行会回答 `confirm_destructive_required`。除非调用设置了 `confirm_destructive=true`，否则连接器不会加上这个标志，而只有控制级别才能这样设置。因此，连接器默认会拒绝。

## 语言

设置答案来自与文档窗口和指南助手相同的已翻译指南。`organize_capabilities` 报告运行模式和目标，而不是应用中的主题名称。
