from dash import dcc, html

def create_layout():
    """Tạo layout của ứng dụng Dash"""
    return html.Div([
        # Header
        html.Div([
            html.Div([
                # Logo và tên web
                html.Div([
                    html.Img(src='assets/logo.png', className='app-logo'),
                    html.Div('VNTraffic', className='brand-name')
                ], className='logo-container'),
                
                html.Div([
                    html.H1('Giao thông đường bộ Việt Nam', className='app-header-title'),
                    html.P('Trực quan hóa dữ liệu vi phạm và tai nạn giao thông', className='app-header-desc')
                ], className='header-text')
            ], className='header-container')
        ], className='app-header'),
        
        # Navigation Menu
        html.Div([
            html.Nav([
                html.Button([
                    html.I(className='fas fa-bars')
                ], className='mobile-menu-toggle', id='mobile-menu-toggle'),
                
                # Main navigation items
                html.Ul([
                    html.Li([
                        html.A('Trang chủ', href='/', className='nav-link')
                    ], className='nav-item active'),
                    
                    html.Li([
                        html.A('Tin tức', href='/tin-tuc', className='nav-link'),
                        html.Div([
                            html.A('Thông tin về cục cảnh sát giao thông', href='/tin-tuc/canh-sat-giao-thong', className='dropdown-item'),
                            html.A('Các số đường dây nóng', href='/tin-tuc/duong-day-nong', className='dropdown-item')
                        ], className='dropdown-menu')
                    ], className='nav-item nav-dropdown'),
                    
                    html.Li([
                        html.A('Tra cứu phương tiện', href='/tra-cuu', className='nav-link'),
                        html.Div([
                            html.A('Xe máy', href='/tra-cuu/xe-may', className='dropdown-item'),
                            html.A('Ô tô', href='/tra-cuu/o-to', className='dropdown-item')
                        ], className='dropdown-menu')
                    ], className='nav-item nav-dropdown'),
                    
                    html.Li([
                        html.A('Diễn đàn', href='/dien-dan', className='nav-link')
                    ], className='nav-item'),
                    
                    html.Li([
                        html.A('Đấu giá biển số', href='/dau-gia-bien-so', className='nav-link')
                    ], className='nav-item'),
                    
                    html.Li([
                        html.A('An toàn giao thông', href='/an-toan-giao-thong', className='nav-link'),
                        html.Div([
                            html.A('Quy tắc cơ bản khi tham gia giao thông', href='/an-toan-giao-thong/quy-tac', className='dropdown-item'),
                            html.A('Ngày hội an toàn giao thông Việt Nam', href='/an-toan-giao-thong/ngay-hoi', className='dropdown-item')
                        ], className='dropdown-menu')
                    ], className='nav-item nav-dropdown'),
                    
                    # Mục Hỗ trợ
                    html.Li([
                        html.A('Hỗ trợ', href='/ho-tro', className='nav-link'),
                        html.Div([
                            html.A('Điều khoản sử dụng', href='/ho_tro/dieu_khoan_su_dung.html', className='dropdown-item'),
                            html.A('Hướng dẫn sử dụng', href='/ho_tro/huong_dan_su_dung.html', className='dropdown-item'),
                            html.A('Thông báo', href='/ho_tro/thong_bao.html', className='dropdown-item')
                        ], className='dropdown-menu')
                    ], className='nav-item nav-dropdown')
                ], className='nav-list', id='nav-list'),
                
                # Right-side elements (language selector and user profile)
                html.Div([
                    # Language selector
                    html.Div([
                        html.A([
                            html.Img(src='assets/vietnam.png', className='language-icon', id='current-flag'),
                            html.Span('Tiếng Việt', id='current-language')
                        ], href='#', className='nav-link', id='language-selector'),
                        
                        html.Div([
                            html.A([
                                html.Img(src='assets/vietnam.png', className='language-icon'),
                                html.Span('Tiếng Việt', className='language-name')
                            ], href='#', className='dropdown-item language-item', id='lang-vi', **{'data-lang': 'vi'}),
                            
                            html.A([
                                html.Img(src='assets/uk.png', className='language-icon'),
                                html.Span('English', className='language-name')
                            ], href='#', className='dropdown-item language-item', id='lang-en', **{'data-lang': 'en'}),
                            
                            html.A([
                                html.Img(src='assets/japan.png', className='language-icon'),
                                html.Span('日本語', className='language-name')
                            ], href='#', className='dropdown-item language-item', id='lang-ja', **{'data-lang': 'ja'}),
                            
                            html.A([
                                html.Img(src='assets/russia.png', className='language-icon'),
                                html.Span('Русский', className='language-name')
                            ], href='#', className='dropdown-item language-item', id='lang-ru', **{'data-lang': 'ru'})
                            
                        ], className='dropdown-menu language-dropdown', id='language-dropdown')
                    ], className='language-selector nav-dropdown'),
                    
                    html.Div(className='nav-divider'),
                    
                    # User profile
                    html.Div([
                        html.A([
                            html.Span('Xin chào ', className='greeting'),
                            html.Span('Trần Anh Kiệt', className='user-name')
                        ], href='#', className='nav-link', id='user-profile'),
                        
                        html.Div([
                            html.A('Hồ sơ', href='/ho-so', className='dropdown-item'),
                            html.A('Báo cáo', href='/bao-cao', className='dropdown-item'),
                            html.A('Yêu cầu dữ liệu', href='/yeu-cau-du-lieu', className='dropdown-item'),
                            html.A('Cài đặt', href='/cai-dat', className='dropdown-item'),
                            html.Hr(style={'margin': '0.3rem 0', 'border-color': '#eaeaea'}),
                            html.A('Đăng xuất', href='/dang-xuat', className='dropdown-item')
                        ], className='dropdown-menu user-dropdown', id='user-dropdown')
                    ], className='user-profile nav-dropdown')
                ], className='nav-right', id='nav-right')
            ], className='nav-menu')
        ], className='nav-container'),
        
        # Container chính
        html.Div([
            # Data Management Section với 2 nút lớn
            html.Div([
                html.H2('Quản lý dữ liệu', className='section-title'),
                
                # Thêm hai nút lớn
                html.Div([
                    html.Button('Thêm dữ liệu', className='data-button add', id='add-data-btn'),
                    html.Button('Chỉnh sửa dữ liệu', className='data-button edit', id='edit-data-btn')
                ], className='data-buttons-container'),
                
                # GeoJSON upload
                html.Div([
                    html.Label('Tải lên file GeoJSON:', className='upload-label'),
                    dcc.Upload(
                        id='upload-geojson',
                        children=html.Div([
                            'Kéo thả hoặc ',
                            html.A('Chọn file GeoJSON', className='upload-link')
                        ]),
                        className='upload-area',
                        multiple=False
                    ),
                    html.Div(id='geojson-upload-status', className='upload-status')
                ], className='upload-container'),
                
                # CSV upload
                html.Div([
                    html.Label('Tải lên file CSV dữ liệu giao thông:', className='upload-label'),
                    dcc.Upload(
                        id='upload-csv',
                        children=html.Div([
                            'Kéo thả hoặc ',
                            html.A('Chọn file CSV', className='upload-link')
                        ]),
                        className='upload-area',
                        multiple=False
                    ),
                    html.Div(id='csv-upload-status', className='upload-status')
                ], className='upload-container'),
                
                # Nút xử lý
                html.Button('Xử lý dữ liệu', id='process-button', className='process-button', n_clicks=0)
                
            ], className='settings-section'),
            
            # Section cấu hình trực quan hóa  
            html.Div([
                html.H2('Cấu hình trực quan hóa', className='section-title'),
                
                # Chọn cột dữ liệu (dropdown)
                html.Div([
                    html.Div([
                        html.Label('Chọn cột tỉnh/thành:', className='control-label'),
                        dcc.Dropdown(
                            id='province-column',
                            options=[],
                            placeholder='Chọn cột chứa tên tỉnh/thành phố',
                            className='dropdown-control'
                        )
                    ], className='control-item'),
                    
                    html.Div([
                        html.Label('Chọn loại dữ liệu:', className='control-label'),
                        dcc.Dropdown(
                            id='data-type',
                            options=[
                                {'label': 'Vi phạm giao thông', 'value': 'violations'},
                                {'label': 'Tai nạn giao thông', 'value': 'accidents'},
                                {'label': 'Tử vong', 'value': 'deaths'},
                                {'label': 'Bị thương', 'value': 'injuries'},
                                {'label': 'Mức phạt', 'value': 'fines'}
                            ],
                            value='violations',
                            className='dropdown-control'
                        )
                    ], className='control-item'),
                    
                    html.Div([
                        html.Label('Chọn cột dữ liệu:', className='control-label'),
                        dcc.Dropdown(
                            id='data-column',
                            options=[],
                            placeholder='Chọn cột dữ liệu',
                            className='dropdown-control'
                        )
                    ], className='control-item')
                ], className='columns-container'),
                
                # Tùy chọn hiển thị
                html.Div([
                    html.Label('Tùy chọn hiển thị:', className='control-label'),
                    dcc.Checklist(
                        id='display-options',
                        options=[
                            {'label': ' Hiển thị bản đồ', 'value': 'show_map'},
                            {'label': ' Hiển thị biểu đồ cột', 'value': 'show_bar'},
                            {'label': ' Hiển thị bảng dữ liệu', 'value': 'show_table'}
                        ],
                        value=['show_map', 'show_bar', 'show_table'],
                        className='checklist-control'
                    )
                ], className='control-container'),
                
                # Bảng màu
                html.Div([
                    html.Label('Bảng màu bản đồ:', className='control-label'),
                    dcc.Dropdown(
                        id='color-scale',
                        options=[
                            {'label': 'Đỏ', 'value': 'Reds'},
                            {'label': 'Xanh dương', 'value': 'Blues'},
                            {'label': 'Xanh lá', 'value': 'Greens'},
                            {'label': 'Vàng-Cam-Đỏ', 'value': 'YlOrRd'},
                            {'label': 'Tím', 'value': 'Purples'},
                            {'label': 'Đỏ-Xanh', 'value': 'RdBu'},
                            {'label': 'Viridis', 'value': 'Viridis'},
                            {'label': 'Plasma', 'value': 'Plasma'}
                        ],
                        value='Reds',
                        className='dropdown-control'
                    )
                ], className='control-container')
            ], className='settings-section'),
            
            # Khu vực thông báo lỗi
            html.Div(id='error-message-container', className='error-container')
            
        ], className='settings-panel'),
        
        # Khu vực hiển thị kết quả
        html.Div([
            html.H2(id='results-title', className='results-title'),
            
            # Thẻ tổng quan - thống kê chính
            html.Div([
                html.Div([
                    html.H3('Tổng số', className='stat-title'),
                    html.Div(id='total-count', className='stat-value')
                ], className='stat-card'),
                
                html.Div([
                    html.H3('Trung bình mỗi tỉnh', className='stat-title'),
                    html.Div(id='avg-count', className='stat-value')
                ], className='stat-card'),
                
                html.Div([
                    html.H3('Cao nhất', className='stat-title'),
                    html.Div(id='max-count', className='stat-value'),
                    html.Div(id='max-province', className='stat-subtitle')
                ], className='stat-card'),
                
                html.Div([
                    html.H3('Thấp nhất', className='stat-title'),
                    html.Div(id='min-count', className='stat-value'),
                    html.Div(id='min-province', className='stat-subtitle')
                ], className='stat-card')
            ], className='stats-container'),
            
            # Thẻ tổng hợp - thống kê bổ sung
            html.Div([
                html.H3('Thống kê tổng hợp', className='section-subtitle'),
                html.Div([
                    html.Div([
                        html.H3('Tổng số vi phạm', className='stat-title'),
                        html.Div(id='total-violations', className='stat-value')
                    ], className='stat-card'),
                    
                    html.Div([
                        html.H3('Tổng số tai nạn', className='stat-title'),
                        html.Div(id='total-accidents', className='stat-value')
                    ], className='stat-card'),
                    
                    html.Div([
                        html.H3('Tổng số tử vong', className='stat-title'),
                        html.Div(id='total-deaths', className='stat-value')
                    ], className='stat-card'),
                    
                    html.Div([
                        html.H3('Tổng số bị thương', className='stat-title'),
                        html.Div(id='total-injuries', className='stat-value')
                    ], className='stat-card'),
                    
                    html.Div([
                        html.H3('Tổng mức phạt', className='stat-title'),
                        html.Div(id='total-fines', className='stat-value')
                    ], className='stat-card')
                ], className='stats-container')
            ], className='summary-section'),
            
            # Khu vực hiển thị bản đồ
            html.Div([
                html.Div(id='map-container', className='map-container')
            ], id='map-section', className='visualization-section'),
            
            # Khu vực hiển thị biểu đồ
            html.Div([
                html.Div(id='chart-container', className='chart-container')
            ], id='chart-section', className='visualization-section'),
            
            # Khu vực hiển thị bảng dữ liệu
            html.Div([
                html.Div(id='table-container', className='table-container')
            ], id='table-section', className='visualization-section')
            
        ], id='results-panel', className='results-panel hidden'),
        
        # Footer
        html.Footer([
            html.P('© 2025 - VNTraffic | Ứng dụng Phân tích Dữ liệu Giao thông Việt Nam', className='footer-text')
        ], className='app-footer'),
        
        # Load JavaScript cho navigation
        html.Script(src='assets/navigation.js')
        
    ], className='app-container')