# Phân tích Dữ liệu Giao thông Việt Nam

Ứng dụng web được phát triển bằng Dash và Python để trực quan hóa dữ liệu vi phạm và tai nạn giao thông theo tỉnh/thành phố tại Việt Nam.

## Tính năng

- Tải lên và phân tích dữ liệu giao thông từ file CSV
- Tải lên file GeoJSON để hiển thị bản đồ Việt Nam theo tỉnh/thành
- Tạo bản đồ nhiệt (choropleth) hiển thị số liệu theo khu vực địa lý
- Biểu đồ cột thể hiện top 10 tỉnh/thành có số lượng vi phạm/tai nạn cao nhất
- Bảng dữ liệu chi tiết với chức năng sắp xếp và lọc
- Tùy chọn sử dụng dữ liệu mẫu để demo
- Đáp ứng tốt trên các thiết bị di động (responsive design)

## Cấu trúc thư mục

```
.
├── app.py                  # File chính của ứng dụng
├── layout.py               # Định nghĩa giao diện người dùng
├── callbacks.py            # Xử lý tương tác người dùng
├── assets/                 # Thư mục chứa CSS và tài nguyên tĩnh
│   └── style.css           # File CSS chính
├── main.py                 # File để chạy ứng dụng
└── README.md               # Tài liệu hướng dẫn
```

## Cài đặt

1. Clone repository này về máy

```bash
git clone https://github.com/username/vietnam-traffic-analysis.git
cd vietnam-traffic-analysis
```

2. Cài đặt các thư viện cần thiết

```bash
pip install dash dash-core-components dash-html-components dash-table plotly pandas numpy
```

3. Chạy ứng dụng

```bash
python main.py
```

4. Mở trình duyệt và truy cập địa chỉ: `http://127.0.0.1:8050/`

## Hướng dẫn sử dụng

### Tải lên dữ liệu

1. Tải lên file GeoJSON chứa dữ liệu ranh giới địa lý của các tỉnh/thành phố Việt Nam
2. Tải lên file CSV chứa dữ liệu về vi phạm và tai nạn giao thông
3. Chọn các cột tương ứng cho tên tỉnh/thành, dữ liệu vi phạm và dữ liệu tai nạn
4. Nhấn nút "Xử lý dữ liệu" để phân tích và hiển thị kết quả

Hoặc đơn giản nhấn nút "Sử dụng dữ liệu mẫu" để xem demo với dữ liệu mẫu được tạo sẵn.

### Tùy chỉnh hiển thị

- Chọn tab "Vi phạm giao thông" hoặc "Tai nạn giao thông" để xem dữ liệu tương ứng
- Tùy chỉnh hiển thị bằng cách chọn hoặc bỏ chọn các tùy chọn: bản đồ, biểu đồ cột, bảng dữ liệu
- Thay đổi bảng màu hiển thị trên bản đồ

## Yêu cầu về cấu trúc dữ liệu

### File GeoJSON

File GeoJSON cần có thuộc tính `ten_tinh` trong `properties` của mỗi feature. Đây là thuộc tính dùng để kết nối với dữ liệu CSV.

### File CSV

File CSV cần có ít nhất 3 cột:

- Cột chứa tên tỉnh/thành phố (phải khớp với thuộc tính `ten_tinh` trong GeoJSON)
- Cột chứa dữ liệu về vi phạm giao thông
- Cột chứa dữ liệu về tai nạn giao thông

## Phát triển

Ứng dụng có thể được mở rộng hoặc tùy chỉnh theo nhu cầu:

- Thêm các loại biểu đồ và phân tích thống kê phức tạp hơn
- Tích hợp phân tích theo thời gian (time series)
- Thêm tính năng so sánh giữa các khu vực hoặc thời điểm khác nhau
- Cải thiện giao diện người dùng và trải nghiệm người dùng

## Giấy phép

Dự án này được phân phối dưới giấy phép MIT.
