import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import json
import os
import base64
import io

# Khởi tạo ứng dụng Dash
app = dash.Dash(__name__, 
                title='Phân tích Giao thông Việt Nam',
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport', 
                           'content': 'width=device-width, initial-scale=1.0'}])

# Định nghĩa các biến toàn cục để lưu trữ dữ liệu
global_geojson = None
global_violations_data = None
global_accidents_data = None

# Tạo mẫu CSS tùy chỉnh
external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Import layout từ file layout.py
from layout import create_layout
app.layout = create_layout()

# Hàm để sửa lỗi tọa độ trong GeoJSON
def fix_geojson_coordinates(geojson_data):
    """Sửa lỗi trong các tọa độ GeoJSON và đảm bảo mỗi feature có ID"""
    
    # Phạm vi tọa độ hợp lý cho Việt Nam
    VN_LON_MIN, VN_LON_MAX = 102.0, 110.0
    VN_LAT_MIN, VN_LAT_MAX = 8.0, 24.0
    
    coords_need_fixing = False
    
    # Kiểm tra tọa độ đầu tiên để xem có cần đảo ngược không
    if len(geojson_data['features']) > 0:
        feature = geojson_data['features'][0]
        if 'geometry' in feature and 'coordinates' in feature['geometry']:
            if feature['geometry']['type'] == 'Polygon':
                first_ring = feature['geometry']['coordinates'][0]
                if len(first_ring) > 0:
                    first_coord = first_ring[0]
                    
                    # Kiểm tra xem tọa độ có nằm trong phạm vi Việt Nam không
                    if (first_coord[0] < VN_LON_MIN or first_coord[0] > VN_LON_MAX or
                        first_coord[1] < VN_LAT_MIN or first_coord[1] > VN_LAT_MAX):
                        coords_need_fixing = True
    
    # Sửa tọa độ nếu cần
    if coords_need_fixing:
        for feature in geojson_data['features']:
            if 'geometry' in feature and 'coordinates' in feature['geometry']:
                geometry_type = feature['geometry']['type']
                
                if geometry_type == 'Polygon':
                    for ring_idx in range(len(feature['geometry']['coordinates'])):
                        for point_idx in range(len(feature['geometry']['coordinates'][ring_idx])):
                            # Đảo ngược [x, y] thành [y, x]
                            feature['geometry']['coordinates'][ring_idx][point_idx] = [
                                feature['geometry']['coordinates'][ring_idx][point_idx][1],
                                feature['geometry']['coordinates'][ring_idx][point_idx][0]
                            ]
                
                elif geometry_type == 'MultiPolygon':
                    for poly_idx in range(len(feature['geometry']['coordinates'])):
                        for ring_idx in range(len(feature['geometry']['coordinates'][poly_idx])):
                            for point_idx in range(len(feature['geometry']['coordinates'][poly_idx][ring_idx])):
                                # Đảo ngược [x, y] thành [y, x]
                                feature['geometry']['coordinates'][poly_idx][ring_idx][point_idx] = [
                                    feature['geometry']['coordinates'][poly_idx][ring_idx][point_idx][1],
                                    feature['geometry']['coordinates'][poly_idx][ring_idx][point_idx][0]
                                ]
    
    # Thêm ID cho mỗi feature
    for feature in geojson_data['features']:
        if 'properties' in feature and 'ten_tinh' in feature['properties']:
            feature['id'] = feature['properties']['ten_tinh']
    
    return geojson_data

# Hàm để xử lý tải lên file
def parse_contents(contents, filename):
    """Phân tích nội dung file đã tải lên"""
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        if 'csv' in filename.lower():
            # Đọc file CSV
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            return df, None
        elif 'json' in filename.lower() or 'geojson' in filename.lower():
            # Đọc file GeoJSON
            geojson_data = json.loads(decoded.decode('utf-8'))
            # Sửa lỗi tọa độ trong GeoJSON
            fixed_geojson = fix_geojson_coordinates(geojson_data)
            return fixed_geojson, None
        else:
            return None, f"Định dạng file {filename} không được hỗ trợ."
    except Exception as e:
        return None, f"Đã xảy ra lỗi khi xử lý file {filename}: {str(e)}"

# Hàm tạo dữ liệu mẫu
def create_sample_data():
    """Tạo dữ liệu mẫu để demo"""
    # Tạo GeoJSON mẫu
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }
    
    # Danh sách các tỉnh thành
    provinces = [
        "An Giang", "Bà Rịa - Vũng Tàu", "Bắc Giang", "Bắc Kạn", "Bạc Liêu", 
        "Bắc Ninh", "Bến Tre", "Bình Định", "Bình Dương", "Bình Phước", 
        "Bình Thuận", "Cà Mau", "TP.Cần Thơ", "Cao Bằng", "TP.Đà Nẵng", 
        "Đắk Lắk", "Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp", 
        "Gia Lai", "Hà Giang", "Hà Nam", "TP.Hà Nội", "Hà Tĩnh", 
        "Hải Dương", "TP.Hải Phòng", "Hậu Giang", "Hòa Bình", "Hưng Yên", 
        "Khánh Hòa", "Kiên Giang", "Kon Tum", "Lai Châu", "Lâm Đồng", 
        "Lạng Sơn", "Lào Cai", "Long An", "Nam Định", "Nghệ An", 
        "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Phú Yên", "Quảng Bình", 
        "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng", 
        "Sơn La", "Tây Ninh", "Thái Bình", "Thái Nguyên", "Thanh Hóa", 
        "TP.Huế", "Tiền Giang", "TP.Hồ Chí Minh", "Trà Vinh", "Tuyên Quang", 
        "Vĩnh Long", "Vĩnh Phúc", "Yên Bái"
    ]
    
    # Tạo features cho GeoJSON
    for i, province in enumerate(provinces):
        # Đặt tọa độ trong phạm vi của Việt Nam
        center_lon = 105.0 + (i % 8) * 0.5  # Phân bố trong khoảng 105-109 độ
        center_lat = 10.0 + (i // 8) * 1.0  # Phân bố trong khoảng 10-20 độ
        
        # Tạo một hình vuông nhỏ cho mỗi tỉnh
        feature = {
            "type": "Feature",
            "properties": {
                "gid": i + 1,
                "ten_tinh": province
            },
            "id": province,
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[center_lon - 0.2, center_lat - 0.2], 
                                 [center_lon + 0.2, center_lat - 0.2], 
                                 [center_lon + 0.2, center_lat + 0.2], 
                                 [center_lon - 0.2, center_lat + 0.2], 
                                 [center_lon - 0.2, center_lat - 0.2]]]
            }
        }
        geojson_data["features"].append(feature)
    
    # Tạo DataFrame mẫu
    np.random.seed(42)
    
    # Dữ liệu vi phạm theo quy tắc: Hà Nội và TP.HCM cao nhất
    violations = []
    for province in provinces:
        if province == "TP.Hà Nội":
            violations.append(np.random.randint(2500, 3000))
        elif province == "TP.Hồ Chí Minh":
            violations.append(np.random.randint(1800, 2200))
        elif province in ["TP.Đà Nẵng", "TP.Hải Phòng", "TP.Cần Thơ"]:
            violations.append(np.random.randint(300, 500))
        else:
            violations.append(np.random.randint(20, 300))
    
    # Dữ liệu tai nạn theo quy tắc tương tự nhưng thấp hơn
    accidents = []
    for province in provinces:
        if province == "TP.Hà Nội":
            accidents.append(np.random.randint(1400, 1700))
        elif province == "TP.Hồ Chí Minh":
            accidents.append(np.random.randint(1000, 1300))
        elif province in ["TP.Đà Nẵng", "TP.Hải Phòng", "TP.Cần Thơ"]:
            accidents.append(np.random.randint(150, 250))
        else:
            accidents.append(np.random.randint(10, 150))
    
    # Tạo DataFrame
    df = pd.DataFrame({
        'Ten_Tinh_Thanh': provinces,
        'Count of MAVP': violations,
        'Count of MATN': accidents
    })
    
    return geojson_data, df

# Import callbacks từ file callbacks.py
from callbacks import register_callbacks
register_callbacks(app, parse_contents, create_sample_data)

# Chạy ứng dụng
if __name__ == '__main__':
    app.run(debug=True)