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

````
├── assets/                         # Thư mục chứa CSS và tài nguyên tĩnh
│   |── ico                         # Thư mục chứa favicon
|   |
│   |── brandname.css
│   |── data-buttons.css
│   |── login.css
│   |── navigation.css
│   └── style.css                   # File CSS chính
├── ho_tro
│   |── dieu_khoan.html
│   |── huong_dan_su_dung.html
│   └── thong_bao.html
├── app.py                          # File chính của ứng dụng
├── callbacks.py                    # Xử lý tương tác người dùng
├── diaphantinh.geojson             # file geojson địa phận các tỉnh thành ở Việt Nam
├── index.html
├── layout.py                       # Định nghĩa giao diện người dùng
├── login.py                        # Xử lý đăng nhập
├── main.py                         # File để chạy ứng dụng
├── project-summary.md              # Tài liệu giới thiệu dự án
├── README.md                       # Tài liệu hướng dẫn
├── routes.py                       # Xử lý đường dẫn
└── vipham.csv                      # File csv dữ liệu vi phạm

YÊU CẦU TỐI THIỂU
| Yêu cầu             | Mô tả                                                            |
| ------------------- | ---------------------------------------------------------------- |
| Python 3.7+         | Môi trường chạy code Python                                      |
| Thư viện Python     | dash, dash-bootstrap-components, plotly, pandas, numpy, flask    |
| File GeoJSON hợp lệ | Dữ liệu địa lý tỉnh/thành (định dạng chuẩn)                      |
| File CSV dữ liệu    | Dữ liệu giao thông có cột tên tỉnh/thành và các trường cần thiết |
| Chạy file `main.py` | Khởi chạy app Dash và Flask server                               |
| Trình duyệt         | Truy cập localhost:8050 để dùng app                              |
└─────────────────────────────────────────────────────────────────────────────────────────

## Cài đặt

1. Yêu cầu môi trường (Dependencies)
   Cài đặt Python (phiên bản nên là 3.7 trở lên).

Cài đặt các thư viện Python cần thiết, đặc biệt:

dash

dash-bootstrap-components

dash-bootstrap-templates

plotly

pandas

numpy

flask (do Dash chạy trên Flask)

2. Clone repository này về máy

```bash
git https://github.com/Azure06072005/Vietnam-traffic-management-application.git
cd vietnam-traffic-analysis
````

3. Cài đặt các thư viện cần thiết

```bash
pip install dash dash-bootstrap-components dash-bootstrap-templates plotly pandas numpy flask
```

4. Chạy ứng dụng

```bash
python main.py
```

5. Mở trình duyệt và truy cập địa chỉ: `http://localhost:8050`

6. Sử dụng ứng dụng
   Trang đầu tiên sẽ là trang đăng nhập, dùng tài khoản mặc định:
   Username: admin
   Password: 123456

7. Đăng nhập thành công, bạn sẽ vào trang dashboard.
   - Upload file GeoJSON và CSV dữ liệu qua các khu vực upload.
   - Chọn cột dữ liệu, loại dữ liệu, tùy chỉnh hiển thị.
     ├── Cột tỉnh thành -> chọn Ten_Tinh_Thanh
     | ├── Cột loại dữ liệu -> các loại dữ liệu được chọn
     | ├── Vi phạm giao thông
     | ├── Tai nạn giao thông
     | ├── Tử vong
     | ├── Bị thương
     | └── Mức phạt
     | | └── Cột dữ liệu -> Chọn MAVP
   - Nhấn "Xử lý dữ liệu" để xem kết quả (bản đồ, biểu đồ, bảng dữ liệu).
   - Có thể chuyển đổi ngôn ngữ, truy cập các trang hỗ trợ qua menu.

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
