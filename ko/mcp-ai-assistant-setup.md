# AI 비서(MCP)

라이선스가 있는 팀은 **OrganizeFiles.Cli**를 Claude Desktop, **Cursor**, VS Code Copilot 또는 다른 Model Context Protocol 클라이언트에 연결합니다. 아래에서는 이 클라이언트를 MCP 클라이언트라고 부릅니다. 커넥터는 Python 패키지 **organize-files-mcp**입니다. github.com/GutRaz/organize-files-docs의 `mcp/` 폴더에서 무료로 내려받을 수 있습니다.

**데스크톱 앱에서:** 옵션 열의 **애플리케이션 및 데이터** 아래 또는 도구 메뉴에서 **MCP 설정…** 창을 엽니다. **MCP 액세스** 항목에서 **꺼짐**, **모니터**, **제어** 중 하나를 고릅니다. 그런 다음 JSON 조각을 복사합니다. 레벨을 바꿀 때마다 AI 앱에서 MCP를 다시 로드하세요. **제어**는 매번 새 토큰을 만들기 때문입니다.

**문서 도우미에게** "setup mcp" 또는 "cum setez mcp"라고 물으면 현재 시스템의 단계를 알려 줍니다.

## 앱에서 설정하는 MCP 액세스 레벨

레벨은 세 가지 작업에 대응합니다: **읽기 / 미리 보기 / 실행**.

| 레벨 | 작업 종류 | AI가 할 수 있는 일 |
|-------|--------|-------------------|
| **꺼짐** | — | `organize_mcp_status`만 가능합니다. 진단도 없고 작업 공간에도 접근하지 않습니다. |
| **모니터** | **읽기** | 꺼짐의 모든 기능에 더해 읽기 전용 진단, 실행 및 작업 기록, 잠금, 감사 확인, **`organize_capabilities`** 및 **`organize_workspace_snapshot`** 도구. `organize_capabilities`는 실행 모드와 그중의 **`ai`**, 이동 범위, 대상을 나열합니다. `organize_workspace_snapshot`은 기본 창에 저장된 작업 공간을 보여 줍니다. 미리 보기와 실행은 없습니다. |
| **제어** | **미리 보기** / **실행** | 모니터의 모든 기능에 더해 **`organize_create_job`**, **`organize_run_workspace`**, **`organize_remove_empty_organize_layout`** 도구. MCP 설정에 **제어 토큰** `ORGANIZE_FILES_MCP_CONTROL_TOKEN`이 필요합니다. **미리 보기**는 저장된 작업 공간에서 **드라이런**이 켜져 있을 때의 `organize_run_workspace`이므로 아무것도 쓰지 않습니다. **실행**은 드라이런이 꺼져 있을 때의 같은 도구이므로 파일이 이동됩니다. 호출이 `confirm_destructive=true`를 설정하지 않으면 커넥터는 `--confirm-destructive`를 붙이지 않으며, 이 플래그가 없으면 명령줄은 `confirm_destructive_required`로 거부합니다. |

제어 파일은 **`mcp-control.json`** 파일이며, 앱 프로필 폴더의 `automation-jobs.json` 옆에 있습니다. 커넥터가 기본 프로필 폴더에서 직접 찾기 때문에 복사한 조각에는 이 파일 이름이 없습니다. 파일이 다른 곳에 있을 때만 **`ORGANIZE_FILES_MCP_CONTROL_FILE`** 값을 설정합니다. **제어** 레벨에서는 조각이 **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`** 값도 설정합니다.

**옮기기와 삭제에는 사람이 하는 두 번째 단계가 필요합니다.** 비서는 확인을 스스로 설정하므로, 비서가 읽은 텍스트가 확인하도록 유도할 수 있습니다. 그래서 드라이런이 아닌 실행에는 **MCP 설정** 창에서 여는 시간 창도 필요하며, 이 시간 창은 15분 뒤 저절로 닫힙니다. 시간 창 밖에서도 비서는 실행을 준비하고 미리 볼 수 있지만, 실행 자체는 거부됩니다. 제어 파일과 시간 창은 모두 이 설치본이 가진 키로 서명됩니다. 손으로 고치거나 다른 컴퓨터에서 복사한 제어 파일은 꺼짐으로 처리됩니다.

## 레벨별 MCP 도구

**항상, 꺼짐에서도:** `organize_mcp_status`

**모니터 및 제어:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide`, 그리고 읽기 명령만 받는 `organize_run_raw_cli`.

**모니터 및 제어에도 있음:** AI 및 ML 파일용 실행 모드 **`ai`** 항목을 나열하는 `organize_capabilities`, 그리고 `organize_workspace_snapshot`.

**제어 전용:** 작업 공간 또는 작업 JSON에서 만드는 `organize_create_job`, 작업 공간의 드라이런 설정에 따라 미리 보기 또는 실제 실행을 하는 `organize_run_workspace`, 그리고 기존 출력 안의 빈 레이아웃 폴더를 지우고 출력 폴더 자체는 절대 만들지 않는 `organize_remove_empty_organize_layout`.

파일을 옮기거나 삭제하는 명령은 **제어** 레벨이 아니면 MCP를 통해 항상 차단됩니다. 다른 어떤 설정도 이 명령을 허용하지 않습니다.

## 커넥터가 쓰는 명령줄 플래그

| 플래그 | 레벨 | 용도 |
|------|-------|---------|
| `--mcp-control-status` | 모두 | 레벨, 제어 파일 경로, 모니터 및 제어 플래그가 담긴 JSON |
| `--mcp-capabilities` | 모니터 이상 | 실행 모드와 그중의 **`ai`**, 이동 범위, 대상을 담은 JSON 목록 |
| `--mcp-workspace-snapshot` | 모니터 이상 | 저장된 작업 공간과 그 공간이 작업으로 바뀌는 방식 |
| `--mcp-create-job` | 제어 | `--from-workspace` 또는 `--mcp-job-json`으로 작업 만들기 |
| `--mcp-run-workspace` | 제어 | 저장된 작업 공간을 `--allow-app-target` 및 `--mcp-control-token`과 함께 실행 |
| `--remove-empty-organize-layout` | 제어 | 기존 `--output` 안의 빈 레이아웃 폴더 삭제 |
| `--confirm-destructive` | 제어 | 옮기거나 삭제하는 실행에서 `--mcp-run-workspace`와 함께 필요합니다. 커넥터는 `confirm_destructive=true`일 때만 전달합니다 |

## MCP 클라이언트 JSON의 설정

| 설정 | 언제 |
|----------|------|
| `ORGANIZE_FILES_CLI` | OrganizeFiles.Cli 경로 |
| `ORGANIZE_FILES_JOBS_FILE` | `automation-jobs.json` 경로 |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | `mcp-control.json` 경로. 기본 프로필 폴더에 없을 때만 |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | **제어** 레벨 전용. 앱의 조각에서 가져옴 |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | **제어** 레벨. 저장된 작업 공간을 실행할 때 |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | 선택 사항. 호스트가 읽기 작업에 쓰는 것과 같은 토큰 |

## Windows 설정

1. **Python 3.10 이상** — PowerShell에서 `python -V`를 실행합니다. Python이 없거나 더 오래된 버전이면 [python.org](https://www.python.org/downloads/)에서 설치하고 **Add python.exe to PATH** 항목에 체크합니다.
2. **커넥터 내려받기 및 설치** — github.com/GutRaz/organize-files-docs를 ZIP으로 내려받아 압축을 풀고 `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1`를 실행합니다. 스크립트는 커넥터 전용 Python 환경을 만들고 AI 앱용 명령을 출력합니다.
3. **앱에서:** **MCP 설정…** 창에서 **모니터** 또는 **제어**를 고른 다음 JSON을 복사합니다.
4. **경로:** `%LocalAppData%\OrganizeFilesCrossPlatform\` 폴더에 작업과 `mcp-control.json`이 있습니다. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **테스트** — `organize_mcp_status`, 그다음 `organize_server_info`를 실행합니다. `cliResolved`는 true여야 하고 `mcpLevel`은 앱과 같아야 합니다.

## macOS 설정

**python3** 및 `bash mcp/install-organize-files-mcp.sh`로 같은 단계를 따릅니다. `python3 -V`가 3.9를 보여 주거나 Python이 전혀 없으면 먼저 [python.org](https://www.python.org/downloads/macos/)에서 Python을 설치합니다. 경로: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Linux 설정

**python3** 및 `bash mcp/install-organize-files-mcp.sh`로 같은 단계를 따릅니다. Debian과 Ubuntu에서는 먼저 `sudo apt install python3-venv`를 실행합니다. 경로: `~/.local/share/OrganizeFilesCrossPlatform/`, 또는 설정된 경우 `$XDG_DATA_HOME`, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## 보안

- MCP는 운영 체제의 **로컬 사용자**로 실행되며, 직접 실행한 명령줄과 같은 권한을 가집니다.
- **제어 토큰**과 **읽기 토큰**은 암호처럼 비밀로 지키세요. 제어를 켠 뒤에는 JSON을 다시 복사합니다.
- **`organize_run_workspace`** 도구는 앱의 실행 버튼이 아니라 명령줄에서 실행됩니다. 같은 출력 폴더에서 두 작업을 동시에 실행하지 마세요.
- 예: `mcp/examples/`.

## 옮기거나 삭제하는 실행

`--mcp-run-workspace`는 드라이런이 아닌 모든 실행에 `--confirm-destructive`가 필요합니다. 옮기기, 삭제, 보관 모두 마찬가지입니다. 이 플래그가 없으면 명령줄은 `confirm_destructive_required`로 답합니다. 호출이 `confirm_destructive=true`를 설정하지 않으면 커넥터는 이 플래그를 붙이지 않으며, 이 설정은 제어 레벨만 할 수 있습니다. 그래서 기본적으로 커넥터는 거부합니다.

## 언어

설정 답변은 문서 창과 가이드 도우미와 같은 번역된 가이드에서 나옵니다. `organize_capabilities`는 실행 모드와 대상을 알려 주며, 앱의 테마 이름은 알려 주지 않습니다.
