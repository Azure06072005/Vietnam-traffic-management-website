# layout.py
from dash import dcc, html

def create_layout():
    """アプリケーションのレイアウトを作成する"""
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
                    html.H1('ベトナムの道路交通', className='app-header-title'),
                    html.P('交通違反と交通事故データの可視化', className='app-header-desc')
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
                        html.A('ホーム', href='/', className='nav-link')
                    ], className='nav-item active'),
                    
                    html.Li([
                        html.A('ニュース', href='/tin-tuc', className='nav-link'),
                        html.Div([
                            html.A('交通警察局に関する情報', href='/tin-tuc/canh-sat-giao-thong', className='dropdown-item'),
                            html.A('ホットライン番号', href='/tin-tuc/duong-day-nong', className='dropdown-item')
                        ], className='dropdown-menu')
                    ], className='nav-item nav-dropdown'),
                    
                    html.Li([
                        html.A('車両照会', href='/tra-cuu', className='nav-link'),
                        html.Div([
                            html.A('バイク', href='/tra-cuu/xe-may', className='dropdown-item'),
                            html.A('自動車', href='/tra-cuu/o-to', className='dropdown-item')
                        ], className='dropdown-menu')
                    ], className='nav-item nav-dropdown'),
                    
                    html.Li([
                        html.A('フォーラム', href='/dien-dan', className='nav-link')
                    ], className='nav-item'),
                    
                    html.Li([
                        html.A('ナンバープレートオークション', href='/dau-gia-bien-so', className='nav-link')
                    ], className='nav-item'),
                    
                    html.Li([
                        html.A('交通安全', href='/an-toan-giao-thong', className='nav-link'),
                        html.Div([
                            html.A('交通参加時の基本ルール', href='/an-toan-giao-thong/quy-tac', className='dropdown-item'),
                            html.A('ベトナム交通安全デー', href='/an-toan-giao-thong/ngay-hoi', className='dropdown-item')
                        ], className='dropdown-menu')
                    ], className='nav-item nav-dropdown'),
                    
                    # Mục Hỗ trợ
                    html.Li([
                        html.A('サポート', href='/ho-tro', className='nav-link'),
                        html.Div([
                            html.A('利用規約', href='/ho_tro/dieu_khoan.html', className='dropdown-item'),
                            html.A('利用ガイド', href='/ho_tro/huong_dan_su_dung.html', className='dropdown-item'),
                            html.A('お知らせ', href='/ho_tro/thong_bao.html', className='dropdown-item')
                        ], className='dropdown-menu')
                    ], className='nav-item nav-dropdown')
                ], className='nav-list', id='nav-list'),
                
                # Right-side elements (language selector and user profile)
                html.Div([
                    # Language selector
                    html.Div([
                        html.A([
                            html.Img(src='assets/japan.png', className='language-icon', id='current-flag'),
                            html.Span('日本語', id='current-language')
                        ], href='#', className='nav-link', id='language-selector'),
                        
                        html.Div([
                            html.A([
                                html.Img(src='assets/japan.png', className='language-icon'),
                                html.Span('日本語', className='language-name')
                            ], href='#', className='dropdown-item language-item', id='lang-jp', **{'data-lang': 'vi'}),
                            
                            html.A([
                                html.Img(src='assets/uk.png', className='language-icon'),
                                html.Span('English', className='language-name')
                            ], href='#', className='dropdown-item language-item', id='lang-en', **{'data-lang': 'en'}),
                            
                            html.A([
                                html.Img(src='assets/vietnam.png', className='language-icon'),
                                html.Span('ベトナム語', className='language-name')
                            ], href='#', className='dropdown-item language-item', id='lang-vn', **{'data-lang': 'ja'}),
                            
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
                            html.Span('こんにちは、', className='greeting'),
                            html.Span('Trần Anh Kiệt', className='user-name')
                        ], href='#', className='nav-link', id='user-profile'),
                        
                        html.Div([
                            html.A('プロフィール', href='/ho-so', className='dropdown-item'),
                            html.A('レポート', href='/bao-cao', className='dropdown-item'),
                            html.A('データリクエスト', href='/yeu-cau-du-lieu', className='dropdown-item'),
                            html.A('設定', href='/cai-dat', className='dropdown-item'),
                            html.Hr(style={'margin': '0.3rem 0', 'border-color': '#eaeaea'}),
                            html.A('ログアウト', href='/dang-xuat', className='dropdown-item')
                        ], className='dropdown-menu user-dropdown', id='user-dropdown')
                    ], className='user-profile nav-dropdown')
                ], className='nav-right', id='nav-right')
            ], className='nav-menu')
        ], className='nav-container'),
        
        # Container chính
        html.Div([
            # Data Management Section với 2 nút lớn
            html.Div([
                html.H2('データ管理', className='section-title'),
                
                # Thêm hai nút lớn
                html.Div([
                    html.Button('データを追加', className='data-button add', id='add-data-btn'),
                    html.Button('データを編集', className='data-button edit', id='edit-data-btn')
                ], className='data-buttons-container'),
                
                # GeoJSON upload
                html.Div([
                    html.Label('GeoJSONファイルをアップロード:', className='upload-label'),
                    dcc.Upload(
                        id='upload-geojson',
                        children=html.Div([
                            'ドラッグ＆ドロップまたは ',
                            html.A('GeoJSONファイルを選択', className='upload-link')
                        ]),
                        className='upload-area',
                        multiple=False
                    ),
                    html.Div(id='geojson-upload-status', className='upload-status')
                ], className='upload-container'),
                
                # CSV upload
                html.Div([
                    html.Label('交通データCSVファイルをアップロード:', className='upload-label'),
                    dcc.Upload(
                        id='upload-csv',
                        children=html.Div([
                            'ドラッグ＆ドロップまたは ',
                            html.A('CSVファイルを選択', className='upload-link')
                        ]),
                        className='upload-area',
                        multiple=False
                    ),
                    html.Div(id='csv-upload-status', className='upload-status')
                ], className='upload-container'),
                
                # Nút xử lý
                html.Button('データ処理', id='process-button', className='process-button', n_clicks=0)
                
            ], className='settings-section'),
            
            # Section cấu hình trực quan hóa  
            html.Div([
                html.H2('可視化設定', className='section-title'),
                
                # Chọn cột dữ liệu (dropdown)
                html.Div([
                    html.Div([
                        html.Label('省/市列を選択:', className='control-label'),
                        dcc.Dropdown(
                            id='province-column',
                            options=[],
                            placeholder='省/市の名前を含む列を選択してください',
                            className='dropdown-control'
                        )
                    ], className='control-item'),
                    
                    html.Div([
                        html.Label('データタイプを選択:', className='control-label'),
                        dcc.Dropdown(
                            id='data-type',
                            options=[
                                {'label': '交通違反', 'value': 'violations'},
                                {'label': '交通事故', 'value': 'accidents'},
                                {'label': '死亡者数', 'value': 'deaths'},
                                {'label': '負傷者数', 'value': 'injuries'},
                                {'label': '罰金額', 'value': 'fines'}
                            ],
                            value='violations',
                            className='dropdown-control'
                        )
                    ], className='control-item'),
                    
                    html.Div([
                        html.Label('データ列を選択:', className='control-label'),
                        dcc.Dropdown(
                            id='data-column',
                            options=[],
                            placeholder='データ列を選択してください',
                            className='dropdown-control'
                        )
                    ], className='control-item')
                ], className='columns-container'),
                
                # Tùy chọn hiển thị
                html.Div([
                    html.Label('表示オプション:', className='control-label'),
                    dcc.Checklist(
                        id='display-options',
                        options=[
                            {'label': ' 地図を表示', 'value': 'show_map'},
                            {'label': ' 棒グラフを表示', 'value': 'show_bar'},
                            {'label': ' データテーブルを表示', 'value': 'show_table'}
                        ],
                        value=['show_map', 'show_bar', 'show_table'],
                        className='checklist-control'
                    )
                ], className='control-container'),
                
                # Bảng màu
                html.Div([
                    html.Label('地図のカラースケール:', className='control-label'),
                    dcc.Dropdown(
                        id='color-scale',
                        options=[
                            {'label': '赤', 'value': 'Reds'},
                            {'label': '青', 'value': 'Blues'},
                            {'label': '緑', 'value': 'Greens'},
                            {'label': '黄-橙-赤', 'value': 'YlOrRd'},
                            {'label': '紫', 'value': 'Purples'},
                            {'label': '赤-青', 'value': 'RdBu'},
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
                    html.H3('合計', className='stat-title'),
                    html.Div(id='total-count', className='stat-value')
                ], className='stat-card'),
                
                html.Div([
                    html.H3('各省の平均', className='stat-title'),
                    html.Div(id='avg-count', className='stat-value')
                ], className='stat-card'),
                
                html.Div([
                    html.H3('最大', className='stat-title'),
                    html.Div(id='max-count', className='stat-value'),
                    html.Div(id='max-province', className='stat-subtitle')
                ], className='stat-card'),
                
                html.Div([
                    html.H3('最小', className='stat-title'),
                    html.Div(id='min-count', className='stat-value'),
                    html.Div(id='min-province', className='stat-subtitle')
                ], className='stat-card')
            ], className='stats-container'),
            
            # Thẻ tổng hợp - thống kê bổ sung
            html.Div([
                html.H3('集計統計', className='section-subtitle'),
                html.Div([
                    html.Div([
                        html.H3('総違反件数', className='stat-title'),
                        html.Div(id='total-violations', className='stat-value')
                    ], className='stat-card'),
                    
                    html.Div([
                        html.H3('総事故件数', className='stat-title'),
                        html.Div(id='total-accidents', className='stat-value')
                    ], className='stat-card'),
                    
                    html.Div([
                        html.H3('総死亡者数', className='stat-title'),
                        html.Div(id='total-deaths', className='stat-value')
                    ], className='stat-card'),
                    
                    html.Div([
                        html.H3('総負傷者数', className='stat-title'),
                        html.Div(id='total-injuries', className='stat-value')
                    ], className='stat-card'),
                    
                    html.Div([
                        html.H3('罰金総額', className='stat-title'),
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
            html.P('© 2025 - VNTraffic | ベトナム交通データ分析アプリケーション', className='footer-text')
        ], className='app-footer'),
        
        # Load JavaScript cho navigation
        html.Script(src='assets/navigation.js')
        
    ], className='app-container')
