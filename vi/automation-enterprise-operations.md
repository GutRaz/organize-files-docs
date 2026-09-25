# Giám sát bằng Prometheus và Grafana

## Các bộ đếm bao gồm những gì

Công việc theo lịch trình giữ một tập nhỏ các bộ đếm và thước đo Prometheus. Mọi tên đều bắt đầu bằng `organize_files_automation_`, và cả tập được công bố dưới dạng văn bản Prometheus. Cả ba máy chủ chạy công việc đều công bố cùng một tập: ứng dụng máy tính để bàn, dịch vụ `OrganizeFiles.JobAgent` và máy chủ dòng lệnh dùng bên trong container.

Các bộ đếm mô tả bộ lập lịch, không mô tả tệp. Những thứ được đếm là lượt quét, kết quả công việc, phê duyệt, việc gửi webhook và việc dọn dẹp lịch sử. Không có gì được đếm về những tệp mà một công việc di chuyển.

## Xuất ra tệp, không mở cổng nào

`automation-metrics.prom` được ghi vào thư mục dữ liệu tự động hóa, cạnh `automation-jobs.json`, và được làm mới sau mỗi lượt quét đến hạn và ở mỗi lần đọc. Bố cục đúng theo thứ mà bộ thu thập textfile của `node_exporter` đọc, nên một máy đã chạy `node_exporter` được bao phủ mà không cần cổng lắng nghe, không cần mã thông báo và không cần luật tường lửa. Tệp được thay thế trọn vẹn một lần, và một liên kết tượng trưng để lại ở chỗ của nó sẽ chặn việc ghi thay vì được đi theo.

## Điểm đọc số liệu

Điểm đọc chỉ tồn tại khi `ORGANIZE_FILES_METRICS_HTTP_PORT` giữ một cổng trong khoảng 1 đến 65535. Thiếu biến đó thì không có gì lắng nghe.

| Biến | Tác dụng |
| -------- | ------ |
| `ORGANIZE_FILES_METRICS_HTTP_PORT` | Cổng để lắng nghe. Thiếu hoặc nằm ngoài khoảng thì hoàn toàn không có điểm đọc. |
| `ORGANIZE_FILES_METRICS_HTTP_BIND` | Địa chỉ lắng nghe. Mặc định là `127.0.0.1`. Các giá trị `0.0.0.0`, `+` và `*` đều có nghĩa là mọi địa chỉ, còn giá trị khác quay về `127.0.0.1`. |
| `ORGANIZE_FILES_METRICS_BEARER_TOKEN` | Mã bearer bắt buộc trên `/metrics` và trên `/ready`. |
| `ORGANIZE_FILES_METRICS_READY_PUBLIC` | `1` cho phép `/ready` trả lời mà không cần mã đó, dành cho phép dò của cụm. Đường dẫn của máy chủ khi ấy bị bỏ khỏi câu trả lời. |
| `ORGANIZE_FILES_READY_FAIL_ON_DUE_PASS_EXIT_CODES` | Các mã thoát ngăn cách bằng dấu phẩy khiến `/ready` báo chưa sẵn sàng. Thay cho danh sách dựng sẵn. |
| `ORGANIZE_FILES_READY_IGNORE_LAST_DUE_EXIT` | `1` bỏ qua mã thoát của lượt quét gần nhất, và cả trạng thái trước khi lượt quét đầu tiên kết thúc. |
| `ORGANIZE_FILES_READY_JSON` | `1` buộc phần thân JSON trên `/ready`, kể cả với bên gọi đã xin văn bản thuần. |

Một địa chỉ ngoài vòng nội bộ bị từ chối trước khi bộ lắng nghe mở ra, nếu chưa đặt mã bearer. Việc từ chối được ghi ra luồng lỗi và gửi đi như một sự kiện webhook, vì tổ hợp đó sẽ trao các bộ đếm cho cả mạng.

## Các đường dẫn được phục vụ

- `/metrics` — các bộ đếm dưới dạng văn bản Prometheus. Một yêu cầu tới `/` trả về cùng nội dung.
- `/ready` — mức sẵn sàng cho bộ điều phối. Câu trả lời là `200` ngay khi thư mục tự động hóa nhận một lần ghi thử, tệp công việc mở được, thư mục lịch sử phân giải bên trong gốc dữ liệu, và lượt quét đến hạn gần nhất kết thúc với mã thoát không chặn. Ngược lại câu trả lời là `503` kèm một lý do ngắn như `due_pass_not_completed` hoặc `last_due_pass_license_failed`.
- `/health` — chỉ là dấu hiệu còn sống. Đường dẫn đó vẫn vô danh ngay cả khi đã đặt mã, vì nó trả lời `ok` và không gì khác.

Các mã thoát `3` cho lỗi giấy phép, `8` cho cây đầu ra bị khóa, `10` cho một lần xóa chưa từng được xác nhận và `11` cho xung đột quyền giữ chặn mức sẵn sàng theo mặc định. Phần thân của `/ready` là JSON trừ khi bên gọi gửi `Accept: text/plain` hoặc thêm `?format=text`.

## Các bộ đếm

| Tên | Nội dung |
| ---- | ------------- |
| `organize_files_automation_due_passes_total` | Số lượt quét đến hạn mà bộ lập lịch đã bắt đầu. |
| `organize_files_automation_jobs_started_total` | Số lần chạy công việc đã đạt trạng thái đang chạy. |
| `organize_files_automation_jobs_skipped_total` | Công việc bị bỏ qua: môi trường Docker hoặc Kubernetes chưa sẵn sàng, công việc nhắm vào ứng dụng trên máy chủ không có màn hình, gốc đầu ra đang bận, hoặc công việc bị bộ điều phối từ chối. |
| `organize_files_automation_jobs_failed_total` | Số lần chạy công việc kết thúc bằng thất bại. |
| `organize_files_automation_jobs_awaiting_approval_total` | Số lần chạy thật bị giữ lại chờ phê duyệt. |
| `organize_files_automation_execute_approvals_total` | Số phê duyệt đã cấp cho một lần chạy thật. |
| `organize_files_automation_execute_approvals_expired_total` | Số phê duyệt hết hạn trước khi dùng. |
| `organize_files_automation_claim_conflicts_total` | Số lần một máy chủ khác đã giữ quyền trên gốc đầu ra. |
| `organize_files_automation_runs_orphaned_total` | Số lần chạy được thu hồi như mồ côi, do một máy chủ đã dừng để lại. |
| `organize_files_automation_job_events_total` | Một bộ đếm cho mỗi sự kiện, với các nhãn `event`, `job_id`, `target` và `jobs_file`. |
| `organize_files_automation_webhook_posts_succeeded_total` | Số lần gửi webhook được chấp nhận. |
| `organize_files_automation_webhook_posts_failed_total` | Số lần gửi webhook bị từ chối hoặc không tới được. |
| `organize_files_automation_webhook_dead_letter_depth` | Số dòng đang chờ ngay lúc này trong tệp webhook chưa gửi được. |
| `organize_files_automation_log_retention_pruned_total` | Số nhật ký chạy bị chính sách lưu giữ xóa đi. |
| `organize_files_automation_runs_index_compacted_total` | Số dòng bị loại khỏi chỉ mục lần chạy khi nén gọn. |
| `organize_files_automation_last_due_pass_exit_code` | Mã thoát của lượt quét kết thúc gần nhất. `0` là một lượt quét sạch. |
| `organize_files_automation_last_due_pass_completed_utc` | Thời gian Unix tính bằng giây của lượt quét kết thúc gần nhất, và `0` trước lượt đầu tiên. |

## Bảng điều khiển và luật cảnh báo

Một bảng điều khiển Grafana dựng sẵn được công bố cùng các tệp triển khai với tên `grafana-organize-files-automation.json`, dưới tiêu đề **OrganizeFiles Automation**. Mười khung của nó hiển thị các lượt quét đến hạn, công việc đã bắt đầu và thất bại, xung đột quyền giữ, lưu lượng công việc trong một giờ, mã thoát gần nhất, độ sâu của thông điệp chưa gửi được, lỗi webhook trong một ngày, công việc chờ phê duyệt, và sự kiện công việc theo trạng thái. Mỗi khung gọi tên nguồn dữ liệu của nó qua chỗ giữ `${DS_PROMETHEUS}`.

Các luật cảnh báo tương ứng nằm trong `alerts-organize-files-automation.yaml`, còn `prometheus-rule-automation.yaml` là lớp vỏ Kubernetes cho `kube-prometheus-stack`. Mã thoát gần nhất khác không sẽ cảnh báo sau năm phút, lỗi giấy phép là nghiêm trọng sau một phút, và những luật còn lại bao quát công việc thất bại, xung đột quyền giữ, lỗi webhook, một đống thông điệp chưa gửi được và các phê duyệt bị bỏ chờ một ngày. Cả hai tệp đều được kiểm tra ở mỗi lần dựng, nên những cái tên ở trên luôn theo kịp các bộ đếm.

# Đầu ra của lần chạy và số liệu

## Hàng trạng thái

Vùng **Đầu ra của lần chạy** hiển thị:

- Trạng thái hiện tại của ứng dụng và tiến độ của công cụ.
- **CPU** và hai giá trị **bộ nhớ** chỉ dành cho quá trình này.
- Các dòng **GPU**, trên Windows: phần tiến trình này dùng trên từng card đồ họa, không phải toàn bộ card.

Thanh tài nguyên nhỏ gọn tương tự được tái sử dụng trong các cửa sổ công cụ phụ như khám phá tệp, công việc đã lên lịch và sửa chữa tệp.

## Nhãn bộ nhớ

- **Byte riêng tư / cam kết** — bộ nhớ ảo riêng được quy trình dành riêng.
- **Bộ làm việc / bộ nhớ** — RAM thường trú hiện đang được quy trình này nắm giữ. Nó có thể khác với một màn hình hệ điều hành khác vì mỗi hệ điều hành và môi trường máy tính để bàn có nhãn xử lý bộ nhớ khác nhau.

## Chạy JSON nhịp tim (tùy chọn)

Bật **Ghi JSON nhịp tim chạy** trong **Nâng cao / Chẩn đoán**. Công cụ ghi `Organize.Files.run.json` trong `Output\_OrganizeMediaLogs` (cùng thư mục với tệp trạng thái tiếp tục chạy sắp xếp mặc định).

- **Đường dẫn** — được cập nhật nguyên tử trong quá trình sắp xếp và sửa chữa.
- **Nhịp ghi** — trong lúc duyệt các nguồn, tệp được ghi lại sau mỗi 10.000 tệp đã thấy, mỗi 5.000 lần khớp và khoảng mỗi 15 giây khi việc duyệt vẫn đang chạy, nên một cây thư mục mạng lớn liệt kê chậm vẫn cho thấy lượt chạy còn sống. Trong lúc kiểm tra, băm và di chuyển, tệp được ghi lại sau mỗi 1.000 tệp, nhiều nhất 5 giây một lần. Các lần ghi lúc bắt đầu và lúc kết thúc vẫn diễn ra khi một lượt chạy mở đầu và hoàn tất.
- **Tiến độ** — chừng nào số tệp còn tăng, thanh tiến độ chính hiển thị số tệp đã thấy cho tới lúc đó thay vì 100%, cho đến khi một giai đoạn biết được tổng số của mình.
- **Trường** — `schema`, `mode`, `phase` (e.g. `enumerate`, `enumerate-done`, `classify`, `validate`, `move`, `done`), `runState` (`active` / `completed` / `failed` / `cancelled`), `utc` (ISO-8601), `dryRun`, `outputRoot`, `validateMedia`, `deepVideoValidate`, `gpuDeviceCount`, `hwaccel`, tùy chọn `correlationId`, các bộ đếm `progress` lồng nhau.
- **Nhật ký** — bảng đầu ra chạy in đường dẫn đầy đủ khi bắt đầu và khi tệp được lưu ở cuối. Sử dụng **Mở thư mục nhật ký nhịp tim** / **Hiển thị tệp JSON nhịp tim** trong phần Nâng cao / Chẩn đoán.
- **CLI** — `--heartbeat-json` trên OrganizeFiles.Cli. Hủy và các lỗi shell nghiêm trọng ghi `cancelled` / `failed` `runState` khi được bật.
