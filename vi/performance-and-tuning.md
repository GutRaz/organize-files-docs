# Nâng cao / Chẩn đoán

## Sắp xếp điều chỉnh

Nâng cao / Chẩn đoán hiển thị các tùy chọn **OrganizeFilesEngine** mà không làm lộn xộn bảng điều khiển chính.

Các chế độ sắp xếp có thể điều chỉnh loại trừ trùng lặp, chỉ mục đích, quy tắc ngày duy nhất, luồng di chuyển và liệt kê, phần bổ sung BFS, tệp trạng thái tiếp tục chạy và các gốc duy nhất bổ sung.

Việc sửa chữa chỉ giữ lại thời gian thử lại toàn bộ mạng và ổ đĩa, các làn phần cứng đồ họa được phát hiện để kiểm tra video đầy đủ tùy chọn, bộ đệm đọc băm và nhịp tim JSON. Các trường khác hiển thị theo ngữ cảnh nhưng bị tắt.

Khi các nguồn hoặc đầu ra hoạt động trên các đường dẫn NAS hoặc UNC, độ song song thấp hơn, luôn bật thử lại mạng, bật phần bổ sung BFS cho các cây SMB lẻ và thử bộ đệm băm 8 MiB nếu quá trình băm chậm.

# Nâng cao / Chẩn đoán - mỗi tùy chọn

## Giới thiệu về chương này

Các điều khiển này là tùy chọn của bộ máy. Máy tính (Windows, macOS, Linux), Android, iOS và công cụ dòng lệnh đọc cùng các giá trị.

Chế độ **Sắp xếp** dùng mọi điều khiển bên dưới, trừ khi giao diện làm mờ chúng. **Sửa chữa** chỉ dùng thử lại mạng, thử lại khi đầy đĩa, các làn phần cứng đồ họa được phát hiện (có kiểm tra video đầy đủ), bộ đệm đọc băm, JSON nhịp tim, **Tệp trạng thái tiếp tục** và **Bắt đầu mới (cắt bớt tệp trạng thái tiếp tục)**. Các trường khác vẫn hiển thị nhưng bị bỏ qua trong quá trình sửa chữa.

## Nguồn mạng (NAS / UNC)

Khi Nguồn hoặc Đầu ra nằm trên các chia sẻ SMB/CIFS, khối NAS hoặc ổ đĩa được ánh xạ, hãy xem lại phần này một cách cẩn thận.

- **Tại sao điều chỉnh** — Số lượng luồng hoạt động trên ổ SSD cục bộ có thể làm chậm hoặc làm quá tải trình quay.
- **Cần thử gì** — Tiếp tục bật thử lại mạng. Hạ thấp các luồng di chuyển và tối đa song song enum khi hết thời gian chờ. Để phần bổ sung BFS bật trừ khi số lượng đầy đủ được xác minh mà không có nó. Hãy thử bộ đệm băm 8 MiB khi quá trình băm chậm qua mạng.
- **Vô hiệu hóa chờ mạng** — Lỗi nhanh do lỗi mạng tạm thời. Rủi ro trên Wi-Fi hoặc chia sẻ bận rộn.

## Chế

độ loại bỏ trùng lặp Cách công cụ xác định hai tệp là trùng lặp.

| Chế độ | Nó làm gì | Khi nào nên sử dụng | Đánh đổi |
| ---- | ------------ | ----------- | --------- |
| **Băm (SHA-256)** | Đọc và băm toàn bộ nội dung của mọi tệp nguồn được bao gồm, sau đó nhóm các byte giống hệt nhau. | Chế độ thực tế mạnh nhất. Hash (SHA-256) bắt buộc để xóa tại chỗ (bản sao và tệp có vấn đề). | Chậm nhất trên cây lớn hoặc NAS. Không có thuật toán nào nên được trình bày như một sự đảm bảo tuyệt đối. |
| **Kích thước + thời gian + tên** | Khóa = kích thước, dấu tích ghi lần cuối UTC, tên viết thường, sau đó xác minh SHA-256 đầy đủ. | Chế độ tương thích bảo thủ cho bố cục thư mục phương tiện cũ hơn. | Có thể bỏ lỡ các bản sao được đổi tên. Không bao giờ sử dụng với việc xóa bản sao hoặc tệp có vấn đề. |
| **Không có** | Không có sự trùng lặp giữa các tập tin. | Chỉ sắp xếp, không dọn dẹp trùng lặp. | Các bản sao vẫn ở trong nguồn. |

## Bỏ qua chỉ mục

- **Tắt (mặc định)** — Duyệt phần **Unique** đã có ở đích và lập chỉ mục trước khi băm. An toàn hơn khi dùng lại cùng một thư mục đích.
- **Bật** — Bỏ qua lượt duyệt đó.
- **Được gì** — Nhanh hơn trên những cây thư mục đích rất lớn.
- **Rủi ro** — Nhiều nội dung trùng lặp hơn có thể lọt vào trong **Unique**.

## Năm tối thiểu cho DuyNhat

Năm dương lịch tối thiểu cho các thư mục ngày trong **Duy nhất** trong bố cục phương tiện. **Tại sao** — Tránh phân tán các tệp rất cũ vào các thư mục năm lẻ khi siêu dữ liệu sai.

## Di chuyển chủ

đề Di chuyển tệp song song sau khi đích được đặt trước.

- **Cao hơn** — Nhanh hơn trên ổ SSD cục bộ.
- **Thấp hơn** — An toàn hơn trên các ổ đĩa được ánh xạ NAS, USB hoặc Wi-Fi.

## Luồng phân loại và băm

Các tiến trình song song khi quét nguồn và khử trùng lặp SHA-256.

- **Luồng phân loại** — Phát hiện và phân loại tệp. CLI: `--classify-threads <n>`.
- **Luồng băm** — Tiến trình băm nội dung. CLI: `--hash-threads <n>`.
- **Ghi đè** — Giá trị thủ công ghi đè mặc định của hồ sơ (`--profile`).

## Enum song song tối đa

Giới hạn số lượng thư mục được liệt kê song song trong quá trình quét.

- **0** = động cơ tự động.
- **Thấp hơn** — Ít áp lực hơn cho SMB khi nhiều thư mục được liệt kê cùng một lúc.

## Bổ sung thẻ thư mục

- **Bật (mặc định)** — Một lượt duyệt nông thêm, theo bề rộng trước.
- **Vì sao** — Một số đường dẫn NAS hoặc cây thư mục sâu trông như còn thiếu sau lượt duyệt đầu.
- **Tắt** — Chỉ sau khi đã xác nhận số tệp đầy đủ mà không cần lượt này.
- **CLI** — `--no-bfs` tắt lượt duyệt này.

## Tiếp tục tệp trạng thái

Đường dẫn UTF-8 tùy chọn. Các bước di chuyển thành công sẽ nối thêm các dòng `B64|` để lần chạy sắp xếp tiếp theo có thể bỏ qua các nguồn đã hoàn thành.

- **Tại sao** — Tiếp tục công việc lâu dài sau khi dừng hoặc gặp sự cố.
- **Đường dẫn mặc định** — Khi trường trống trong thời gian chạy, công cụ sẽ sử dụng `Output\_OrganizeMediaLogs\OrganizeFiles.resume.txt`. Không có Đầu ra, nó sử dụng `sessions\<id>\resume\OrganizeFiles.resume.txt` trong hồ sơ ứng dụng.
- **Giao diện người dùng máy tính để bàn** — Danh sách đường dẫn chỉ đọc để chọn và sao chép chuột. Khi tệp trạng thái tiếp tục chạy đã tồn tại ở vị trí mặc định, đường dẫn sẽ tự động xuất hiện. **Duyệt** chọn một thư mục nhật ký và thêm `OrganizeFiles.resume.txt`. **Xóa** xóa đường dẫn. Khi trống, gợi ý hiển thị đường dẫn được sử dụng trong thời gian chạy.

## Bắt đầu mới

Cắt bớt tệp trạng thái tiếp tục chạy khi quá trình chạy sắp xếp **thực** bắt đầu (chạy thử không cắt bớt). Với **Lưu tiến trình & không gian làm việc**, cũng xóa ảnh chụp nhanh giao diện người dùng đã lưu khi bắt đầu chạy. **Tại sao** — Buộc kể lại toàn bộ thay vì tiếp tục nhật ký tệp resume cũ.

## Các gốc quét độc

đáo bổ sung Một thư mục trên mỗi dòng: các cây **Duy nhất** bổ sung để lập chỉ mục (bố cục cũ, tập khác).

- **Tại sao** — Dedupe có thể xem các tệp đã được sắp xếp ở nơi khác mà không cần di chuyển chúng lại.
- **Giao diện người dùng máy tính để bàn** — Danh sách chỉ đọc cho bản sao trên mỗi dòng. **Thêm** nối thêm thư mục đã chọn. **Xóa** xóa dòng đã chọn (ví dụ: cây `Uniques` cũ trên NAS).

## Thử lại mạng (giây) / Tắt mạng chờ

Giây để thử lại I/O mạng tạm thời.

- **Tại sao** — Trình quay SMB bỏ phiên không hoạt động. Được sử dụng bởi sắp xếp và sửa chữa.
- **Tắt mạng chờ** — Thay vào đó, hãy dừng chờ và thất bại.

## Thử lại toàn bộ

đĩa (giây) / Tắt tính năng chờ

đầy đĩa Mẫu tương tự khi ổ đĩa đầu ra hết dung lượng. **Tại sao** — Thời gian để giải phóng đĩa trong thời gian dài.

## Làn của card đồ họa

Chỉ khi **kiểm tra video đầy đủ** dựng sẵn đang bật và **Dùng card đồ họa đã nhận ra** cũng đang bật. Giá trị lớn hơn **0** ấn định số làn rõ ràng cho việc kiểm tra song song trên các hãng đã nhận ra (NVIDIA, AMD, Intel, Apple, thiết bị di động). **0** nghĩa là số làn được tự tìm ra, chứ không có nghĩa là chỉ dùng bộ xử lý. Muốn lấy mẫu chỉ trên bộ xử lý, hãy chọn **Chỉ CPU** trong danh sách card đồ họa. Nhãn làn chỉ lên kế hoạch kiểm tra dòng bit trên bộ xử lý, không gọi đến bộ giải mã video phần cứng của hệ thống.

- **Thiết lập sẵn trên dòng lệnh** — Khi kiểm tra video đầy đủ đang chạy, `--hwaccel <value>` chọn một thiết lập sẵn cho làn kiểm tra (`cpu`, `auto`, `cuda`, `qsv`, `d3d11va`, `dxva2`, `vaapi`, `apple`, `mobile`).

## Bộ đệm đọc băm

Mỗi người lao động đọc bộ đệm trong khi băm (512 KiB, 1 MiB, 8 MiB). **Tại sao** — Bộ đệm lớn hơn giúp làm chậm NAS và chia sẻ có độ trễ cao.

## Ghi nhật ký hoàn tác

Nhật ký JSONL tùy chọn về các lần di chuyển dưới thư mục đầu ra của lần chạy.

- **Để làm gì** — Cho phép hoàn tác bằng CLI sau một lần chạy thật.
- **Lưu trữ** — Lưu trữ sau khi sắp xếp vẫn tắt khi nhật ký đang bật.
- **CLI** — `--record-undo-journal` (giống hộp kiểm ở cửa sổ chính).

## Viết nhịp tim chạy

Ghi tệp tùy chọn `Organize.Files.run.json` dưới `Output\_OrganizeMediaLogs`.

- **Vì sao** — Các công cụ bên ngoài có thể đọc bộ đếm đang chạy (đã duyệt, đã lên kế hoạch, đã xong) trong lúc sắp xếp hoặc sửa chữa.
- **Nhịp ghi** — Sau mỗi 10.000 tệp đã thấy, mỗi 5.000 lần khớp và khoảng mỗi 15 giây trong những lượt duyệt nguồn, sau mỗi 1.000 tệp và nhiều nhất 5 giây một lần trong lúc kiểm tra, băm và di chuyển, và ở mỗi giai đoạn lớn.
