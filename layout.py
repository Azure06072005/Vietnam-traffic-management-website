from dash import dcc, html

def create_layout():
    """Tạo layout của ứng dụng Dash"""
    return html.Div([
        # Header
        html.Div([
            html.H1('Phân tích Dữ liệu Giao thông Việt Nam', className='app-header-title'),
            html.P('Trực quan hóa dữ liệu vi phạm và tai nạn giao thông theo tỉnh/thành phố', className='app-header-desc')
        ], className='app-header'),
        
        # Container chính
        html.Div([
            # Section tải lên dữ liệu
            html.Div([
                html.H2('Tải lên dữ liệu', className='section-title'),
                
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
                html.Button('Xử lý dữ liệu', id='process-button', className='process-button', n_clicks=0),
                
                # Hoặc sử dụng dữ liệu mẫu
                html.Div([
                    html.P('hoặc', className='option-divider'),
                    html.Button('Sử dụng dữ liệu mẫu', id='use-sample-data', className='sample-data-button', n_clicks=0)
                ], className='option-container')
                
            ], className='settings-section'),
            
            # Section cấu hình trực quan hóa  
            html.Div([
                html.H2('Cấu hình trực quan hóa', className='section-title'),
                
                # Chọn kiểu dữ liệu hiển thị
                html.Div([
                    html.Label('Loại dữ liệu:', className='control-label'),
                    dcc.Tabs(id='data-type-tabs', value='violations', children=[
                        dcc.Tab(label='Vi phạm giao thông', value='violations', className='custom-tab', selected_className='custom-tab-selected'),
                        dcc.Tab(label='Tai nạn giao thông', value='accidents', className='custom-tab', selected_className='custom-tab-selected')
                    ], className='tabs-container')
                ], className='control-container'),
                
                # Chọn cột dữ liệu
                html.Div([
                    html.Div([
                        html.Label('Cột tên tỉnh/thành:', className='control-label'),
                        dcc.Dropdown(id='province-column', className='dropdown-control', disabled=True)
                    ], className='control-item'),
                    
                    html.Div([
                        html.Label('Cột dữ liệu vi phạm:', className='control-label'),
                        dcc.Dropdown(id='violations-column', className='dropdown-control', disabled=True)
                    ], className='control-item'),
                    
                    html.Div([
                        html.Label('Cột dữ liệu tai nạn:', className='control-label'),
                        dcc.Dropdown(id='accidents-column', className='dropdown-control', disabled=True)
                    ], className='control-item')
                ], className='columns-container'),
                
                # Tùy chọn hiển thị
                html.Div([
                    html.Label('Tùy chọn hiển thị:', className='control-label'),
                    dcc.Checklist(
                        id='display-options',
                        options=[
                            {'label': 'Hiển thị bản đồ', 'value': 'show_map'},
                            {'label': 'Hiển thị biểu đồ cột', 'value': 'show_bar'},
                            {'label': 'Hiển thị bảng dữ liệu', 'value': 'show_table'}
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
            
            # Thẻ tổng quan
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
            html.P('© 2025 - Ứng dụng Phân tích Dữ liệu Giao thông Việt Nam', className='footer-text')
        ], className='app-footer')
        
    ], className='app-container')