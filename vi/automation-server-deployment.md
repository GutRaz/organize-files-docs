# CLI, Docker và Kubernetes (bố cục tham khảo)

## Tự động hóa CLI

Chương này tuân theo phong cách Microsoft/HashiCorp: dòng sử dụng, bảng cờ (mã thông báo tiếng Anh), sau đó sao chép-dán ví dụ.

CLI (OrganizeFiles.Cli)
  SỬ DỤNG: OrganizeFiles.Cli --output <dir> (--source <dir>)+ [options]
  SỬ DỤNG: OrganizeFiles.Cli --output <dir> --mode repair [options]

  Cờ (dài) | Ý nghĩa
  -------------------------|---------------------------------------
  --execute | Di chuyển thực sự (mặc định chỉ chạy thử).
  --move-scope <token> | all | unique-only | issues-only | duplicates-only | duplicates-issues | unique-issues | unique-duplicates
  --mode / -m <name> | all | media | documents | archives | disk | emails | code | cad | databases | security | ai | repair
  --resume <file> | Tệp tệp resume UTF-8 với B64| dòng.
  --delete-duplicates | Xóa các ứng viên trùng lặp (cần --confirm-delete với --execute).
  --delete-issues | Xóa các ứng cử viên trong nhóm vấn đề (cần --confirm-delete với --execute). Không có trên các mục tiêu tự động hóa từ xa.
  --archive-after-organize | Sau khi sắp xếp: mỗi file ZIP anh chị em sau đó xóa bản gốc (cần --confirm-delete với --execute). Bỏ qua các tiện ích mở rộng đã lưu trữ.

  **Lưu ý:** CLI `--mode models` chọn **mô hình CAD / 3D**, không phải tạo phẩm AI. Sử dụng `--mode ai` hoặc `--mode models-ai` cho AI / ML.

  Ví dụ (chạy thử, tất cả các thùng): OrganizeFiles.Cli -s D:\In -o D:\Out -m media
  Ví dụ (chỉ các bước di chuyển duy nhất, thực hiện): OrganizeFiles.Cli -s D:\In -o D:\Out -m media --move-scope unique-only --execute

Docker
  Bản dựng: docker build -f containers/Dockerfile -t organize-files-cli:latest .
  Chạy thử: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope unique-issues
  Đối với --execute, hãy xóa :ro khỏi giá treo nguồn. Xem containers/README.md để biết quy tắc nhiều worker (một gốc đầu ra cho mỗi worker).

Kubernetes (công việc tham khảo)
  PVC nguồn chỉ đọc có giá trị cho các công việc chạy thử. Các bước di chuyển thực sự với --execute cần có PVC nguồn có thể ghi. Cung cấp quyền hợp lệ của cửa hàng hoặc nhà xuất bản cho tất cả các hoạt động sắp xếp/sửa chữa (chạy thử và thực thi). Một Pod cho mỗi cây đầu ra. Mẫu tối thiểu được ghi lại trong containers/README.md cùng với tệp kê khai mẫu.

Tiến trình công việc
  Cửa sổ Công việc hiển thị tiến trình cho các lần chạy App, CLI, Docker và Kubernetes. Các giai đoạn có tổng số đã biết hiển thị phần trăm. Các lần quét không có tổng số vẫn ở trạng thái không xác định.
  Tự động hóa khởi chạy tiến trình CLI với ORGANIZE_FILES_EMIT_PROGRESS_MARKERS=1 và loại bỏ những dòng dấu hiệu đó khỏi nhật ký hiển thị. Một lần chạy CLI khởi động bằng tay không phát dấu hiệu trừ khi biến đó được đặt.
  Tiến trình Docker và Kubernetes nhận cùng biến đó, nên những lần chạy ấy cũng báo phần trăm. Con số được đọc từ nhật ký của tiến trình, nên nó xuất hiện ngay khi container hoặc pod bắt đầu ghi.
  --list-running và --show-run mang các trường tiến trình cho công việc đang hoạt động khi lần chạy đã báo điều gì đó.

# Ví dụ về lần chạy

## Giao diện người dùng đồ họa

Thêm **Nguồn** và thư mục đầu ra, chọn chế độ chạy, bật **Chạy thử** để xem trước, rồi nhấn **Chạy**. Để **Chạy thử** tắt khi muốn di chuyển thật. Các tùy chọn xóa sẽ hỏi xác nhận trước khi thực thi.

## Ví dụ CLI

CLI Chạy thử: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --move-scope unique-issues

CLI execute: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --move-scope all --execute

CLI delete flow: OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

Docker: docker run --rm -v /data/in:/in:ro -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --move-scope duplicates-only

## Reference snippets

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode all --include-ext .jpg,.png --execute

OrganizeFiles.Cli --source C:\Data --output D:\Organized --mode media --delete-duplicates --confirm-delete --execute

docker run --rm -v /data/in:/in -v /data/out:/out organize-files-cli:latest --source /in --output /out --mode all --include-ext .foo --execute
