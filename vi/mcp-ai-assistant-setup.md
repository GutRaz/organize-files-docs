# Trợ lý AI (MCP)

Các nhóm có giấy phép kết nối **OrganizeFiles.Cli** với Claude Desktop, **Cursor**, VS Code Copilot hoặc một máy khách Model Context Protocol khác, bên dưới gọi là máy khách MCP. Trình kết nối là gói Python **organize-files-mcp**. Gói này được tải miễn phí từ github.com/GutRaz/organize-files-docs, trong thư mục `mcp/`.

**Trong ứng dụng máy tính:** mở **Thiết lập MCP…** trong **Ứng dụng & dữ liệu** ở cột tùy chọn, hoặc từ menu công cụ. Chọn **quyền truy cập MCP**: **Tắt**, **Giám sát** hoặc **Kiểm soát**. Sau đó sao chép đoạn JSON. Tải lại MCP trong ứng dụng AI sau mỗi lần đổi mức, vì **Kiểm soát** tạo mã thông báo mới mỗi lần.

**Hỏi trợ lý tài liệu** “setup mcp” hoặc “cum setez mcp” để xem các bước cho hệ thống hiện tại.

## Các mức truy cập MCP, đặt trong ứng dụng

Các mức ứng với ba loại công việc: **đọc / xem trước / thực thi**.

| Mức | Loại công việc | AI có thể làm gì |
|-------|--------|-------------------|
| **Tắt** | — | Chỉ `organize_mcp_status`. Không có chẩn đoán và không truy cập không gian làm việc. |
| **Giám sát** | **Đọc** | Mọi thứ của Tắt, cùng với chẩn đoán chỉ đọc, lịch sử lần chạy và tác vụ, khóa, kiểm tra kiểm toán, **`organize_capabilities`** và **`organize_workspace_snapshot`**. `organize_capabilities` liệt kê các chế độ chạy, trong đó có **`ai`**, các phạm vi di chuyển và các đích. `organize_workspace_snapshot` cho thấy không gian làm việc đã lưu trong cửa sổ chính. Không xem trước và không thực thi. |
| **Kiểm soát** | **Xem trước** / **Thực thi** | Mọi thứ của Giám sát, cùng với **`organize_create_job`**, **`organize_run_workspace`** và **`organize_remove_empty_organize_layout`**. Cần một **mã thông báo kiểm soát** trong cài đặt MCP, `ORGANIZE_FILES_MCP_CONTROL_TOKEN`. **Xem trước** là `organize_run_workspace` khi không gian làm việc đã lưu bật **Chạy thử**, nên không có gì được ghi. **Thực thi** là cùng công cụ đó khi tắt Chạy thử, nên các tệp được di chuyển. Trình kết nối bỏ `--confirm-destructive` trừ khi lệnh gọi đặt `confirm_destructive=true`, và khi thiếu cờ này dòng lệnh từ chối với `confirm_destructive_required`. |

Tệp kiểm soát là **`mcp-control.json`**, nằm cạnh `automation-jobs.json` trong thư mục hồ sơ của ứng dụng. Đoạn đã sao chép không nêu tên tệp này, vì trình kết nối tự tìm thấy tệp trong thư mục hồ sơ mặc định. Chỉ đặt **`ORGANIZE_FILES_MCP_CONTROL_FILE`** khi tệp nằm ở nơi khác. Ở mức **Kiểm soát**, đoạn này cũng đặt **`ORGANIZE_FILES_ALLOW_APP_TARGET=1`**.

**Di chuyển và xóa cần bước thứ hai do con người thực hiện.** Trợ lý tự đặt xác nhận của mình, nên văn bản mà trợ lý đọc có thể thuyết phục trợ lý xác nhận. Vì vậy, một lần chạy không phải chạy thử còn cần một khoảng thời gian được mở trong **Thiết lập MCP**, và khoảng đó tự đóng sau 15 phút. Ngoài khoảng đó, trợ lý vẫn có thể chuẩn bị và xem trước một lần chạy, nhưng bản thân lần chạy bị từ chối. Cả tệp kiểm soát lẫn khoảng thời gian đều được ký bằng khóa mà bản cài đặt này giữ. Tệp kiểm soát bị sửa bằng tay hoặc sao chép từ máy tính khác được tính là Tắt.

## Công cụ MCP theo mức

**Luôn có, kể cả ở Tắt:** `organize_mcp_status`

**Giám sát và Kiểm soát:** `organize_server_info`, `organize_cli_help`, `organize_query_runs`, `organize_show_run`, `organize_list_running`, `organize_query_jobs`, `organize_due_pass_lock_status`, `organize_output_lock_status`, `organize_verify_audit`, `organize_exit_code_guide` và `organize_run_raw_cli`, công cụ chỉ nhận lệnh đọc.

**Cũng có ở Giám sát và Kiểm soát:** `organize_capabilities`, công cụ liệt kê chế độ chạy **`ai`** cho tệp AI và ML, và `organize_workspace_snapshot`.

**Chỉ Kiểm soát:** `organize_create_job` từ không gian làm việc hoặc từ JSON của tác vụ, `organize_run_workspace` để xem trước hoặc chạy thật theo cài đặt Chạy thử của không gian làm việc, và `organize_remove_empty_organize_layout`, công cụ xóa các thư mục bố cục trống bên trong một đầu ra có sẵn và không bao giờ tạo chính thư mục đầu ra.

Các lệnh di chuyển hoặc xóa tệp luôn bị chặn qua MCP ngoài mức **Kiểm soát**. Không có cài đặt nào khác cho phép các lệnh này.

## Các cờ dòng lệnh mà trình kết nối dùng

| Cờ | Mức | Mục đích |
|------|-------|---------|
| `--mcp-control-status` | mọi mức | JSON với mức, đường dẫn tệp kiểm soát và các cờ Giám sát và Kiểm soát |
| `--mcp-capabilities` | Giám sát trở lên | Danh sách JSON các chế độ chạy, trong đó có **`ai`**, các phạm vi di chuyển và các đích |
| `--mcp-workspace-snapshot` | Giám sát trở lên | Không gian làm việc đã lưu và cách không gian đó trở thành một tác vụ |
| `--mcp-create-job` | Kiểm soát | Tạo tác vụ với `--from-workspace` hoặc `--mcp-job-json` |
| `--mcp-run-workspace` | Kiểm soát | Chạy không gian làm việc đã lưu, với `--allow-app-target` và `--mcp-control-token` |
| `--remove-empty-organize-layout` | Kiểm soát | Xóa các thư mục bố cục trống bên trong một `--output` có sẵn |
| `--confirm-destructive` | Kiểm soát | Cần cùng `--mcp-run-workspace` cho lần chạy có di chuyển hoặc xóa. Trình kết nối chỉ truyền cờ này khi `confirm_destructive=true` |

## Cài đặt trong JSON của máy khách MCP

| Cài đặt | Khi nào |
|----------|------|
| `ORGANIZE_FILES_CLI` | Đường dẫn tới OrganizeFiles.Cli |
| `ORGANIZE_FILES_JOBS_FILE` | Đường dẫn tới `automation-jobs.json` |
| `ORGANIZE_FILES_MCP_CONTROL_FILE` | Đường dẫn tới `mcp-control.json`, chỉ khi tệp không ở thư mục hồ sơ mặc định |
| `ORGANIZE_FILES_MCP_CONTROL_TOKEN` | Chỉ mức **Kiểm soát**, lấy từ đoạn của ứng dụng |
| `ORGANIZE_FILES_ALLOW_APP_TARGET` | Mức **Kiểm soát**, cho các lần chạy không gian làm việc đã lưu |
| `ORGANIZE_FILES_MCP_READ_TOKEN` | Tùy chọn. Cùng mã thông báo mà máy chủ dùng cho thao tác đọc |

## Thiết lập trên Windows

1. **Python 3.10 hoặc mới hơn** — chạy `python -V` trong PowerShell. Nếu thiếu Python hoặc bản cũ hơn, hãy cài từ [python.org](https://www.python.org/downloads/) và đánh dấu **Add python.exe to PATH**.
2. **Tải và cài trình kết nối** — tải github.com/GutRaz/organize-files-docs dưới dạng ZIP, giải nén và chạy `powershell -ExecutionPolicy Bypass -File mcp\Install-OrganizeFilesMcp.ps1`. Tập lệnh tạo một môi trường Python riêng cho trình kết nối và in lệnh cho ứng dụng AI.
3. **Trong ứng dụng:** **Thiết lập MCP…**, chọn **Giám sát** hoặc **Kiểm soát**, rồi sao chép JSON.
4. **Đường dẫn:** `%LocalAppData%\OrganizeFilesCrossPlatform\` chứa các tác vụ và `mcp-control.json`. Cursor: `%USERPROFILE%\.cursor\mcp.json`. Claude: `%APPDATA%\Claude\claude_desktop_config.json`. VS Code: `%USERPROFILE%\.vscode\mcp.json`.
5. **Kiểm tra** — chạy `organize_mcp_status`, rồi `organize_server_info`. `cliResolved` phải là true và `mcpLevel` phải khớp với ứng dụng.

## Thiết lập trên macOS

Các bước giống vậy với **python3** và `bash mcp/install-organize-files-mcp.sh`. Nếu `python3 -V` hiện 3.9 hoặc không có Python, trước tiên hãy cài Python từ [python.org](https://www.python.org/downloads/macos/). Đường dẫn: `~/Library/Application Support/OrganizeFilesCrossPlatform/`, `~/.cursor/mcp.json`, Claude `~/Library/Application Support/Claude/claude_desktop_config.json`.

## Thiết lập trên Linux

Các bước giống vậy với **python3** và `bash mcp/install-organize-files-mcp.sh`. Trên Debian và Ubuntu, trước tiên hãy chạy `sudo apt install python3-venv`. Đường dẫn: `~/.local/share/OrganizeFilesCrossPlatform/`, hoặc `$XDG_DATA_HOME` khi biến này được đặt, `~/.cursor/mcp.json`, Claude `~/.config/Claude/claude_desktop_config.json`.

## Bảo mật

- MCP chạy dưới **người dùng cục bộ** của hệ điều hành, với cùng quyền như dòng lệnh chạy bằng tay.
- Giữ bí mật **mã thông báo kiểm soát** và **mã thông báo đọc**, như mật khẩu. Sao chép lại JSON sau khi bật Kiểm soát.
- **`organize_run_workspace`** chạy trong dòng lệnh, không qua nút Chạy của ứng dụng. Không chạy hai tác vụ trên cùng một thư mục đầu ra cùng lúc.
- Ví dụ: `mcp/examples/`.

## Các lần chạy có di chuyển hoặc xóa

`--mcp-run-workspace` cần `--confirm-destructive` cho mọi lần chạy không phải chạy thử, dù lần chạy di chuyển, xóa hay lưu trữ. Khi thiếu cờ này, dòng lệnh trả lời `confirm_destructive_required`. Trình kết nối bỏ cờ này trừ khi lệnh gọi đặt `confirm_destructive=true`, và chỉ mức Kiểm soát làm được điều đó. Vì vậy, theo mặc định trình kết nối từ chối.

## Ngôn ngữ

Các câu trả lời về thiết lập lấy từ cùng hướng dẫn đã dịch như cửa sổ Tài liệu và Trợ lý hướng dẫn. `organize_capabilities` báo các chế độ chạy và các đích, không báo tên chủ đề trong ứng dụng.
