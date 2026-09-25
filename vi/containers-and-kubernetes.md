# Vùng chứa — thiết lập

## Những gì được yêu cầu

Chỉ có chương trình `docker` hoặc `kubectl` mới có thể truy cập được trên máy chạy công việc. Không có gì khác là cần thiết. Docker Desktop không phải là một yêu cầu. Docker Engine trên Linux, Rancher Desktop, colima và Podman với lệnh tương thích với docker đều hoạt động theo cách tương tự, vì ứng dụng chỉ chạy lệnh mà nó tìm thấy trên đường dẫn hệ thống.

Kubernetes hoạt động tương tự. Mọi cụm có thể truy cập thông qua `kubectl` đều được hỗ trợ, bao gồm k3s, kind, minikube và các cụm được quản lý như EKS, GKE hoặc AKS.

## Sử dụng một daemon hoặc cụm khác

Để gửi công việc đến một trình nền Docker khác, hãy đặt `DOCKER_HOST` hoặc chuyển đổi bằng `docker context use`. Để sử dụng một cụm Kubernetes khác, hãy chuyển ngữ cảnh hiện tại bằng `kubectl config use-context`. Ứng dụng tuân theo bất kỳ dòng lệnh nào đã sử dụng, do đó không cần cài đặt bổ sung bên trong ứng dụng.

## Nơi tập tin được gắn kết

Đối với Kubernetes, thư mục được đính kèm theo một trong hai cách. Bối cảnh phát triển cục bộ có được sự gắn kết thư mục máy chủ trực tiếp. Điều đó bao gồm bối cảnh có tên `desktop`, `colima` hoặc `orbstack`, bối cảnh có tên kết thúc bằng `@desktop`, bối cảnh có tên bắt đầu bằng `kind-`, `minikube` hoặc `k3d-`, và bối cảnh có tên chứa `docker-desktop`, `docker-for-desktop` hoặc `rancher-desktop`. Mọi bối cảnh khác đều được coi là một cụm thực và thay vào đó nhận được yêu cầu volume lưu trữ bền vững vì nút cụm thực không thể nhìn thấy các thư mục trên máy tính để bàn. Đặt `ORGANIZE_FILES_K8S_VOLUME_MODE` thành `pvc` hoặc `hostpath` sẽ ghi đè lựa chọn đó cho mọi bối cảnh.

## Thư mục mạng trên Windows

Docker Desktop trên Windows không thể đính kèm đường dẫn mạng như `\\server\share` vào vùng chứa Linux. Windows nhìn thấy thư mục nhưng vùng chứa thì không. Có hai cách để tránh điều này. Hãy dùng một thư mục trên đĩa cục bộ, hoặc chạy công việc với mục tiêu Ứng dụng, công việc này thực hiện trong chính ứng dụng. Ký tự ổ đĩa ánh xạ tới thư mục chia sẻ không giúp được, vì ứng dụng lần theo nó về đường dẫn mạng và từ chối theo cùng cách.

## Tệp được tạo sẵn

Các bộ công cụ dòng lệnh cho Linux có sẵn tệp trong thư mục `containers`: một Dockerfile tạo image từ chính bộ công cụ, một ví dụ Compose, các ví dụ Job của Kubernetes và `containers/README.md`, bên cạnh là README cho từng ngôn ngữ.

# Worker container và CLI

## Công việc đã lên lịch — Mục tiêu của Docker và Kubernetes

Mở **Việc làm** từ thanh bên của cửa sổ chính. Nhấp vào **Công việc mới** hoặc **Chỉnh sửa** trên thẻ hiện có. Trong trình đơn thả xuống **Mục tiêu**, hãy chọn **Lệnh Docker** hoặc **Công việc Kubernetes**.

1. Đặt **Nguồn** (đường dẫn máy chủ) và **Đầu ra** (đường dẫn máy chủ — phải tồn tại trước khi công việc chạy).
2. Chọn **Chế độ** và **Tùy chọn chạy** như đối với bất kỳ công việc nào khác.
3. Bảng **Xem trước lệnh** hiển thị chính xác lệnh `docker run` hoặc Kubernetes Job YAML sẽ được áp dụng.
4. **Lưu** công việc và đặt **Lịch biểu** hoặc nhấp vào **Chạy ngay** trên thẻ để bắt đầu ngay.

Ứng dụng tự động tạo cờ gắn kết và đường dẫn âm lượng từ ảnh chụp nhanh đã lưu. Docker daemon hoặc `kubectl` phải có thể truy cập được trên máy chủ. **Preflight** kiểm tra kết nối và báo cáo mọi lỗi trong nhật ký công việc trước khi quá trình chạy bắt đầu. Để biết quy trình phê duyệt, truy xuất nhật ký và lập lịch không giao diện, hãy xem **Công việc đã lên lịch**.

## Cửa sổ dòng lệnh của máy chủ (PowerShell / bash / cmd)

Có — trên máy chủ, hãy chạy **OrganizeFiles.Cli** từ PowerShell, bash hoặc cmd. Đó là lối đi qua dòng lệnh được hỗ trợ. Cửa sổ Avalonia trên máy tính là một giao diện đồ họa riêng. Hãy xuất bản hoặc cài bộ CLI cạnh ứng dụng (hoặc trên PATH), rồi truyền **--source** (lặp được), **--output** và **--mode**. Nên chạy thử trước. Chỉ thêm **--execute** khi đã sẵn sàng.

## Giao diện máy tính và vùng chứa

Bộ chứa và tự động hóa: GUI máy tính để bàn Avalonia không có nghĩa là chạy bên trong bộ chứa Linux headless thông thường. Đối với một hoặc nhiều công việc riêng biệt, bao gồm một số công việc song song, hãy sử dụng đồng hành OrganizeFiles.Cli: trong mỗi thư mục nguồn gắn vùng chứa chỉ đọc cho các công việc xem trước chạy thử. Các bước di chuyển thực sự với **--execute** yêu cầu gắn nguồn có thể ghi vì công cụ di chuyển các tệp ra khỏi cây nguồn. Sử dụng ổ đĩa đầu ra đọc/ghi chuyên dụng, đảm bảo quyền hợp lệ của cửa hàng hoặc nhà xuất bản cho tất cả các lần chạy sắp xếp/sửa chữa (chạy thử và thực thi), truyền **--source** (có thể lặp lại), **--output** và **--mode**. Mỗi công nhân đồng thời cần có gốc đầu ra riêng. Thư mục **Output** phải tồn tại trên máy chủ trước khi công việc Docker hoặc Kubernetes chạy (preflight từ chối đích đến bị thiếu và không tạo đích đến đó). Đường dẫn ví dụ: containers/README.md và containers/docker-compose.sample.yml. Jobs/JobAgent đã tạo `docker run` gắn các nguồn tại `/in1`, `/in2`, … và xuất ra tại `/out`. Các ví dụ nguồn đơn thủ công có thể sử dụng `/in` (xem containers/README.md).
