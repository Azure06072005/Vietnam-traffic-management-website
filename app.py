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
from routes import register_routes
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

# Import các module khác
from routes import register_routes
from login import create_login_layout, register_login_callbacks, DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD

# Định nghĩa các biến toàn cục để lưu trữ dữ liệu
global_geojson = None
global_data = None
global_summary = None

# Tạo mẫu CSS tùy chỉnh
external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css',
    dbc.themes.BOOTSTRAP,
    '/assets/login.css'  # Thêm CSS cho login
]

# Khởi tạo ứng dụng Dash
app = dash.Dash(__name__, 
                title='VNTraffic Dashboard',
                suppress_callback_exceptions=True,
                external_stylesheets=external_stylesheets,
                meta_tags=[{'name': 'viewport', 
                           'content': 'width=device-width, initial-scale=1.0'}])

# Thiết lập favicon
app._favicon = 'favicon.ico'

# Import layout chủ từ file layout.py
from layout import create_layout

# Layout main app
def create_main_app_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='login-session', data={'authenticated': False}),
        html.Div(id='page-content')
    ])

# Set layout
app.layout = create_main_app_layout()

# Main callback để điều hướng trang
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    [State('login-session', 'data')]
)
def display_page(pathname, session_data):
    """Điều hướng trang dựa trên URL và trạng thái đăng nhập"""
    
    # Kiểm tra trạng thái đăng nhập
    if not session_data or not session_data.get('authenticated', False):
        # Chưa đăng nhập, hiển thị trang login
        return create_login_layout()
    
    # Đã đăng nhập, hiển thị dashboard
    if pathname in ['/', '/dashboard']:
        return create_layout()
    elif pathname == '/logout':
        # Xử lý đăng xuất
        return html.Div([
            dcc.Store(id='logout-trigger', data={'logout': True}),
            html.H2('Đang đăng xuất...', style={'text-align': 'center', 'margin-top': '50px'})
        ])
    else:
        # Trang không tìm thấy
        return html.Div([
            html.H2('404 - Trang không tồn tại', style={'text-align': 'center'}),
            html.P('Trang bạn tìm kiếm không tồn tại.', style={'text-align': 'center'}),
            html.A('Quay về trang chủ', href='/', style={'text-align': 'center', 'display': 'block'})
        ])

# Callback xử lý đăng nhập
@app.callback(
    [Output('login-session', 'data', allow_duplicate=True),
     Output('url', 'pathname', allow_duplicate=True)],
    [Input('login-button', 'n_clicks')],
    [State('username-input', 'value'),
     State('password-input', 'value'),
     State('remember-me', 'value')],
    prevent_initial_call=True
)
def handle_login(n_clicks, username, password, remember_me):
    """Xử lý logic đăng nhập"""
    if n_clicks == 0:
        return dash.no_update, dash.no_update
    
    # Xác thực thông tin đăng nhập
    if username == DEFAULT_ADMIN_USERNAME and password == DEFAULT_ADMIN_PASSWORD:
        # Đăng nhập thành công
        session_data = {
            'authenticated': True,
            'username': username,
            'remember': 'remember' in remember_me if remember_me else False
        }
        return session_data, '/dashboard'
    
    # Đăng nhập thất bại
    return {'authenticated': False}, '/login'

# Callback xử lý đăng xuất
@app.callback(
    [Output('login-session', 'data', allow_duplicate=True),
     Output('url', 'pathname', allow_duplicate=True)],
    [Input('logout-trigger', 'data')],
    prevent_initial_call=True
)
def handle_logout(logout_data):
    """Xử lý đăng xuất"""
    if logout_data and logout_data.get('logout', False):
        return {'authenticated': False}, '/'
    return dash.no_update, dash.no_update

# Callback hiển thị lỗi đăng nhập
@app.callback(
    [Output('login-error', 'children'),
     Output('login-error', 'className')],
    [Input('login-button', 'n_clicks')],
    [State('username-input', 'value'),
     State('password-input', 'value'),
     State('login-session', 'data')],
    prevent_initial_call=True
)
def show_login_error(n_clicks, username, password, session_data):
    """Hiển thị thông báo lỗi khi đăng nhập thất bại"""
    if n_clicks == 0:
        return "", "login-error"
    
    # Kiểm tra nếu đã đăng nhập thành công
    if session_data and session_data.get('authenticated', False):
        return "", "login-error"
    
    # Kiểm tra thông tin nhập vào
    if not username or not password:
        return "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu", "login-error show"
    
    # Thông báo lỗi sai thông tin
    if username != DEFAULT_ADMIN_USERNAME or password != DEFAULT_ADMIN_PASSWORD:
        return "Tên đăng nhập hoặc mật khẩu không chính xác", "login-error show"
    
    return "", "login-error"

# Import callbacks từ file callbacks.py
from callbacks import register_callbacks

# Function để sửa lỗi tọa độ trong GeoJSON (copy từ code cũ)
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

# Function xử lý giá trị tiền tệ
def parse_currency(value):
    """Chuyển đổi chuỗi tiền tệ (vd: '40000000 ₫') thành số"""
    if isinstance(value, str):
        # Loại bỏ ký tự tiền tệ và khoảng trắng
        return int(value.replace('₫', '').replace(' ', '').strip())
    return value

# Function để xử lý tải lên file
def parse_contents(contents, filename):
    """Phân tích nội dung file đã tải lên"""
    import base64
    import io
    import pandas as pd
    import json
    
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

# Đăng ký callbacks
register_callbacks(app, parse_contents, parse_currency)
register_routes(app)

# Chạy ứng dụng
if __name__ == '__main__':
    app.run(debug=True, host='localhost')