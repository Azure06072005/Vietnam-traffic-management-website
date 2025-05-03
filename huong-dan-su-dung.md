# Hướng dẫn sử dụng - Phân tích Dữ liệu Giao thông Việt Nam

## Giới thiệu

Ứng dụng "Phân tích Dữ liệu Giao thông Việt Nam" là một công cụ trực quan hóa cho phép người dùng phân tích và hiển thị dữ liệu về vi phạm và tai nạn giao thông theo tỉnh/thành phố trên bản đồ Việt Nam.

## Cài đặt và Chạy

### Yêu cầu hệ thống

- Python 3.6 trở lên
- Các thư viện Python: dash, plotly, pandas, numpy

### Cài đặt

1. Cài đặt Python từ [python.org](https://www.python.org/downloads/)
2. Cài đặt các thư viện cần thiết:

```bash
pip install dash plotly pandas numpy
```

3. Chạy ứng dụng:

```bash
python main.py
```

4. Mở trình duyệt web và truy cập địa chỉ: `http://127.0.0.1:8050/`

## Sử dụng ứng dụng

### 1. Tải lên dữ liệu

Có hai cách để sử dụng dữ liệu trong ứng dụng:

#### A. Sử dụng dữ liệu mẫu

Cách đơn giản nhất để dùng thử ứng dụng là nhấn nút "Sử dụng dữ liệu mẫu". Ứng dụng sẽ tạo dữ liệu mẫu về vi phạm và tai nạn giao thông cho 63 tỉnh/thành phố của Việt Nam.

#### B. Tải lên dữ liệu của riêng bạn

Để sử dụng dữ liệu riêng:

1. **Tải lên file GeoJSON**: File GeoJSON chứa dữ liệu ranh giới địa lý của các tỉnh/thành phố. Nhấn vào khu vực tải lên hoặc nhấn "Chọn file GeoJSON" để chọn file. File GeoJSON cần có thuộc tính `ten_tinh` trong properties.

2. **Tải lên file CSV**: File CSV chứa dữ liệu về vi phạm và tai nạn giao thông. Nhấn vào khu vực tải lên hoặc nhấn "Chọn file CSV" để chọn file.

3. **Chọn cột dữ liệu**: Sau khi tải lên file CSV, chọn:

   - Cột chứa tên tỉnh/thành
   - Cột chứa dữ liệu vi phạm giao thông
   - Cột chứa dữ liệu tai nạn giao thông

4. **Xử lý dữ liệu**: Nhấn nút "Xử lý dữ liệu" để bắt đầu phân tích và hiển thị kết quả.

### 2. Xem kết quả phân tích

Sau khi xử lý dữ liệu, bạn sẽ thấy các phần kết quả phân tích:

#### Thống kê tổng quan

Hiển thị bốn chỉ số quan trọng:

- **Tổng số**: Tổng số vi phạm hoặc tai nạn trên toàn quốc
- **Trung bình mỗi tỉnh**: Số lượng trung bình trên mỗi tỉnh/thành
- **Cao nhất**: Tỉnh/thành có số lượng cao nhất và giá trị tương ứng
- **Thấp nhất**: Tỉnh/thành có số lượng thấp nhất và giá trị tương ứng

#### Bản đồ Choropleth

- Bản đồ màu thể hiện mức độ vi phạm hoặc tai nạn trên các tỉnh/thành
- Di chuột qua mỗi tỉnh/thành để xem chi tiết
- Màu sắc càng đậm thể hiện số lượng càng cao

#### Biểu đồ cột

Hiển thị top 10 tỉnh/thành có số lượng vi phạm hoặc tai nạn cao nhất.

#### Bảng dữ liệu

- Hiển thị chi tiết dữ liệu của tất cả tỉnh/thành, được sắp xếp theo thứ tự giảm dần
- Có thể sắp xếp và lọc dữ liệu bằng cách nhấn vào tiêu đề cột hoặc sử dụng ô tìm kiếm

### 3. Tùy chỉnh hiển thị

#### Chuyển đổi loại dữ liệu

Sử dụng tab ở phần đầu khu vực kết quả để chuyển đổi giữa:

- **Vi phạm giao thông**: Hiển thị dữ liệu về vi phạm giao thông
- **Tai nạn giao thông**: Hiển thị dữ liệu về tai nạn giao thông

#### Tùy chọn hiển thị

Bạn có thể chọn hiển thị hoặc ẩn các thành phần:

- Bản đồ
- Biểu đồ cột
- Bảng dữ liệu

#### Thay đổi bảng màu

Thay đổi bảng màu hiển thị trên bản đồ với các tùy chọn:

- Đỏ
- Xanh dương
- Xanh lá
- Vàng-Cam-Đỏ
- Tím
- Đỏ-Xanh
- Viridis
- Plasma

## Cấu trúc dữ liệu đầu vào

### Yêu cầu file GeoJSON

File GeoJSON cần có cấu trúc:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "ten_tinh": "Tên tỉnh/thành phố"
      },
      "geometry": {
        // Dữ liệu hình học của tỉnh/thành
      }
    }
    // Các tỉnh/thành khác
  ]
}
```

### Yêu cầu file CSV

File CSV cần có định dạng với ít nhất 3 cột:

```
ten_tinh,so_vi_pham,so_tai_nan
Tỉnh A,123,45
Tỉnh B,234,56
...
```

## Xử lý lỗi

Một số lỗi phổ biến và cách khắc phục:

1. **Lỗi file không đúng định dạng**: Đảm bảo bạn đang tải lên đúng loại file (GeoJSON và CSV).

2. **Lỗi không tìm thấy cột**: Kiểm tra xem bạn đã chọn đúng cột trong file CSV.

3. **Lỗi không hiển thị bản đồ**: Có thể do file GeoJSON có vấn đề về tọa độ. Ứng dụng sẽ cố gắng tự động sửa lỗi, nhưng trong một số trường hợp, bạn có thể cần sửa file GeoJSON trước khi tải lên.

4. **Không khớp dữ liệu**: Đảm bảo tên tỉnh/thành trong file CSV khớp chính xác với thuộc tính `ten_tinh` trong file GeoJSON.

## Liên hệ và hỗ trợ

Nếu bạn gặp vấn đề hoặc có câu hỏi, vui lòng liên hệ qua email: hotro@phantichdulieu.vn
