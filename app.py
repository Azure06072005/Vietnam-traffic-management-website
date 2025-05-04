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

# Định nghĩa các biến toàn cục để lưu trữ dữ liệu
global_geojson = None
global_data = None
global_summary = None

# Tạo mẫu CSS tùy chỉnh
external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css']

# Khởi tạo ứng dụng Dash (chỉ khởi tạo một lần)
app = dash.Dash(__name__, 
                title='Dashboard',
                suppress_callback_exceptions=True,
                external_stylesheets=external_stylesheets,
                meta_tags=[{'name': 'viewport', 
                           'content': 'width=device-width, initial-scale=1.0'}])

# Thiết lập favicon
app._favicon = 'favicon.ico'

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

# Hàm xử lý giá trị tiền tệ
def parse_currency(value):
    """Chuyển đổi chuỗi tiền tệ (vd: '40000000 ₫') thành số"""
    if isinstance(value, str):
        # Loại bỏ ký tự tiền tệ và khoảng trắng
        return int(value.replace('₫', '').replace(' ', '').strip())
    return value

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

# Import layout từ file layout.py
from layout import create_layout
app.layout = create_layout()

# Import callbacks từ file callbacks.py
from callbacks import register_callbacks
register_callbacks(app, parse_contents, parse_currency)

# Chạy ứng dụng
if __name__ == '__main__':
    app.run(debug=True)