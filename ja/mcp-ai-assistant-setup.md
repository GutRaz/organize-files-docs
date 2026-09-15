# AIアシスタント（MCP）

ライセンスを持つチームは、**OrganizeFiles.Cli** を Claude Desktop、**Cursor**、VS Code Copilot、またはほかの Model Context Protocol クライアントに接続します。以下ではこのクライアントを MCP クライアントと呼びます。コネクターは Python パッケージ **organize-files-mcp** です。github.com/GutRaz/organize-files-docs の `mcp/` フォルダーから無料でダウンロードできます。

**デスクトップ アプリでは:** オプション列の **アプリケーションとデータ** の下、またはツール メニューから **MCP セットアップ…** を開きます。**MCPアクセス** で **オフ**、**モニター**、**制御** のいずれかを選びます。次に JSON スニペットをコピーします。レベルを変えるたびに AI アプリで MCP を再読み込みしてください。**制御** は毎回新しいトークンを作るためです。

**ドキュメント アシスタントに**「setup mcp」または「cum setez mcp」と尋ねると、今のシステムでの手順がわかります。

## アプリで設定する MCP アクセス レベル

レベルは 3 種類の作業に対応します: **読み取り / プレビュー / 実行**。

| レベル | 作業の種類 | AI にできること |
|-------|--------|-------------------|
| **オフ** | — | `organize_mcp_status` のみ。診断はなく、ワークスペースにもアクセスしません。 |
| **モニター** | **読み取り** | オフのすべてに加えて、読み取り専用の診断、実行とジョブの履歴、ロック、監査チェック、**`organize_capabilities`**、**`organize_workspace_snapshot`**。`organize_capabilities` は実行モード、その中の **`ai`**、移動の範囲、ターゲットを一覧にします。`organize_workspace_snapshot` はメイン ウィンドウに保存されたワークスペースを示します。プレビューと実行はありません。 |
| **制御** | **プレビュー** / **実行** | モニターのすべてに加えて、**`organize_create_job`**、**`organize_run_workspace`**、**`organize_remove_empty_organize_layout`**。MCP の設定に **制御トークン** `ORGANIZE_FILES_MCP_CONTROL_TOKEN` が必要です。**プレビュー** は、保存されたワークスペースで **ドライラン** がオンのときの `organize_run_workspace` で、何も書き込まれません。**実行** はドライランがオフのときの同じツールで、ファイルが移動されます。呼び出しが `confirm_destructive=true` を設定しない限り、コネクターは `--confirm-destructive` を付けません。このフラグがないと、コマンド ラインは `confirm_destructive_required` で拒否します。 |

制御ファイルは **`mcp-control.json`** で、アプリのプロファイル フォルダーの `automation-jobs.json` の隣にあります。コネクターが既定のプロファイル フォルダーで見つけるため、コピーしたスニペットにはこのファイル名は入っていません。ファイルがほかの場所にあるときだけ **`ORGANIZE_FILES_MCP_CONTROL_FILE`** を設定します。**制御** では、スニペットは **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`** も設定します。

**移動と削除には、人による 2 つ目の手順が必要です。** アシスタントは自分で確認を設定するため、読んだテキストに促されて確認してしまうおそれがあります。そのため、ドライランではない実行には、**MCP セットアップ** で開く時間枠も必要です。この枠は 15 分後に自動で閉じます。枠の外でも、アシスタントは実行を準備してプレビューできますが、実行そのものは拒否されます。制御ファイルと時間枠はどちらもこのインストールが持つ鍵で署名されます。手で書き換えた制御ファイルや、ほかのコンピューターからコピーした制御ファイルはオフとして扱われます。

## レベル別の MCP ツール

**常に、オフでも:** `organize_mcp_status`

**モニターと制御:** `organize_server_info`、`organize_cli_help`、`organize_query_runs`、`organize_show_run`、`organize_list_running`、`organize_query_jobs`、`organize_due_pass_lock_status`、`organize_output_lock_status`、`organize_verify_audit`、`organize_exit_code_guide`、そして読み取りコマンドだけを受け付ける `organize_run_raw_cli`。

**同じくモニターと制御:** AI と ML のファイル向けの実行モード **`ai`** を一覧にする `organize_capabilities` と、`organize_workspace_snapshot`。

**制御のみ:** ワークスペースまたはジョブ JSON からの `organize_create_job`、ワークスペースのドライランの設定に従ってプレビューまたは本番の実行を行う `organize_run_workspace`、そして既存の出力の中にある空のレイアウト フォルダーを削除し、出力フォルダー自体は決して作らない `organize_remove_empty_organize_layout`。

ファイルを移動または削除するコマンドは、**制御** レベル以外では MCP を通じて常にブロックされます。ほかのどの設定でも許可されません。

## コネクターが使うコマンド ラインのフラグ

| フラグ | レベル | 目的 |
|------|-------|---------|
| `--mcp-control-status` | すべて | レベル、制御ファイルのパス、モニターと制御のフラグを含む JSON |
| `--mcp-capabilities` | モニター以上 | 実行モード、その中の **`ai`**、移動の範囲、ターゲットの JSON 一覧 |
| `--mcp-workspace-snapshot` | モニター以上 | 保存されたワークスペースと、そのワークスペースがジョブにどう対応するか |
| `--mcp-create-job` | 制御 | `--from-workspace` または `--mcp-job-json` でジョブを作成 |
| `--mcp-run-workspace` | 制御 | 保存されたワークスペースを `--allow-app-target` と `--mcp-control-token` で実行 |
| `--remove-empty-organize-layout` | 制御 | 既存の `--output` の中の空のレイアウト フォルダーを削除 |
| `--confirm-destructive` | 制御 | 移動または削除を行う実行で `--mcp-run-workspace` と一緒に必要です。コネクターは `confirm_destructive=true` のときだけ渡します |

## MCP クライアントの JSON の設定

| 設定 | いつ |
|----------|------|
| `ORGANIZE_FILES_CLI` | OrganizeFiles.Cli へのパス |
| `ORGANIZE_FILES_JOBS_FILE` | `automation-jobs.json` へのパス |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | `mcp-control.json` へのパス。既定のプロファイル フォルダーにないときだけ |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | **制御** レベルのみ。アプリのスニペットから |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | **制御** レベル。保存されたワークスペースの実行用 |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | 任意。ホストが読み取り操作に使うのと同じトークン |

## Windows のセットアップ

1. **Python 3.10 以降** — PowerShell で `python -V` を実行します。Python がないか古い場合は、[python.org](https://www.python.org/downloads/) からインストールし、**Add python.exe to PATH** にチェックを入れます。
2. **コネクターをダウンロードしてインストール** — github.com/GutRaz/organize-files-docs を ZIP でダウンロードして展開し、`powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1` を実行します。スクリプトはコネクター専用の Python 環境を作り、AI アプリ用のコマンドを表示します。
3. **アプリで:** **MCP セットアップ…** で **モニター** または **制御** を選び、JSON をコピーします。
4. **パス:** `%LocalAppData%\OrganizeFilesCrossPlatform\` にジョブと `mcp-control.json` があります。Cursor: `%USERPROFILE%\.cursor\mcp.json`。Claude: `%APPDATA%\Claude\claude_desktop_config.json`。VS Code: `%USERPROFILE%\.vscode\mcp.json`。
5. **テスト** — `organize_mcp_status`、次に `organize_server_info` を実行します。`cliResolved` が true で、`mcpLevel` がアプリと一致している必要があります。

## macOS のセットアップ

**python3** と `bash mcp/install-organize-files-mcp.sh` で同じ手順です。`python3 -V` が 3.9 を表示するか Python がまったくない場合は、先に [python.org](https://www.python.org/downloads/macos/) から Python をインストールします。パス: `~/Library/Application Support/OrganizeFilesCrossPlatform/`、`~/.cursor/mcp.json`、Claude `~/Library/Application Support/Claude/claude_desktop_config.json`。

## Linux のセットアップ

**python3** と `bash mcp/install-organize-files-mcp.sh` で同じ手順です。Debian と Ubuntu では、先に `sudo apt install python3-venv` を実行します。パス: `~/.local/share/OrganizeFilesCrossPlatform/`、設定されている場合は `$XDG_DATA_HOME`、`~/.cursor/mcp.json`、Claude `~/.config/Claude/claude_desktop_config.json`。

## セキュリティ

- MCP はオペレーティング システムの **ローカル ユーザー** として、手で実行するコマンド ラインと同じ権限で動きます。
- **制御トークン** と **読み取りトークン** は、パスワードと同じように秘密にしてください。制御をオンにしたあとは JSON をもう一度コピーします。
- **`organize_run_workspace`** はアプリの実行ボタンではなく、コマンド ラインで動きます。同じ出力フォルダーで 2 つのジョブを同時に実行しないでください。
- 例: `mcp/examples/`。

## 移動または削除を行う実行

`--mcp-run-workspace` は、ドライランではないすべての実行で `--confirm-destructive` を必要とします。移動、削除、アーカイブのどれでも同じです。このフラグがないと、コマンド ラインは `confirm_destructive_required` と答えます。呼び出しが `confirm_destructive=true` を設定しない限り、コネクターはこのフラグを付けません。それができるのは制御レベルだけです。そのため、既定ではコネクターは拒否します。

## 言語

セットアップの回答は、ドキュメント ウィンドウとガイドアシスタントと同じ翻訳済みガイドから来ます。`organize_capabilities` は実行モードとターゲットを報告し、アプリのテーマ名は報告しません。
