from dash import dcc, html, Input, Output, State, callback_context
import dash

# Định nghĩa thông tin đăng nhập mặc định
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "123456"

def create_login_layout():
    """Tạo layout cho trang đăng nhập"""
    return html.Div([
        html.Div([
            html.Div([
                # Logo và tiêu đề
                html.Div([
                    html.Img(src='/assets/logo.png', className='login-logo'),
                    html.H1('Giao thông đường bộ Việt Nam', className='login-title'),
                    html.H2('Đăng nhập hệ thống', className='login-subtitle')
                ], className='login-header'),
                
                # Form đăng nhập
                html.Div([
                    html.Div([
                        html.Label('Tên đăng nhập', className='login-label'),
                        dcc.Input(
                            id='username-input',
                            type='text',
                            placeholder='Nhập tên đăng nhập của bạn',
                            className='login-input',
                            value=''
                        )
                    ], className='login-field'),
                    
                    html.Div([
                        html.Label('Mật khẩu', className='login-label'),
                        dcc.Input(
                            id='password-input',
                            type='password',
                            placeholder='Nhập mật khẩu của bạn',
                            className='login-input',
                            value=''
                        )
                    ], className='login-field'),
                    
                    # Checkbox "Ghi nhớ đăng nhập"
                    html.Div([
                        dcc.Checklist(
                            id='remember-me',
                            options=[{'label': ' Ghi nhớ đăng nhập', 'value': 'remember'}],
                            value=[],
                            className='remember-checkbox'
                        )
                    ], className='login-field'),
                    
                    # Nút đăng nhập
                    html.Button('Đăng nhập', id='login-button', className='login-button', n_clicks=0),
                    
                    # Hiển thị lỗi
                    html.Div(id='login-error', className='login-error'),
                    
                    # Các liên kết phụ
                    html.Div([
                        html.A('Quên mật khẩu?', href='#', className='login-link forgot-password'),
                        html.A('Chưa có tài khoản? Đăng ký ngay', href='#', className='login-link register')
                    ], className='login-options'),
                    
                    # Thông tin tài khoản mặc định
                    html.Div([
                        html.P('Tài khoản demo:', className='login-demo-title'),
                        html.P(f'Username: {DEFAULT_ADMIN_USERNAME}', className='login-demo-info'),
                        html.P(f'Password: {DEFAULT_ADMIN_PASSWORD}', className='login-demo-info')
                    ], className='login-demo-section')
                ], className='login-form-container')
            ], className='login-card')
        ], className='login-wrapper'),
        
        # Store để lưu trạng thái đăng nhập
        dcc.Store(id='login-state', data={'authenticated': False}),
        dcc.Location(id='login-url', refresh=True)
    ], className='login-page')


def register_login_callbacks(app):
    """Đăng ký các callback cho hệ thống đăng nhập"""
    
    @app.callback(
        [Output('login-error', 'children'),
         Output('login-error', 'className'),
         Output('login-state', 'data'),
         Output('login-url', 'pathname')],
        [Input('login-button', 'n_clicks')],
        [State('username-input', 'value'),
         State('password-input', 'value'),
         State('remember-me', 'value')],
        prevent_initial_call=True
    )
    def authenticate_user(n_clicks, username, password, remember_me):
        """Xử lý đăng nhập"""
        if n_clicks == 0:
            return "", "login-error", {'authenticated': False}, "/"
        
        # Reset thông báo lỗi
        error_message = ""
        error_class = "login-error"
        
        # Kiểm tra thông tin đăng nhập
        if not username or not password:
            error_message = "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu"
            error_class = "login-error show"
            return error_message, error_class, {'authenticated': False}, "/"
        
        # Xác thực người dùng
        if username == DEFAULT_ADMIN_USERNAME and password == DEFAULT_ADMIN_PASSWORD:
            # Đăng nhập thành công
            login_data = {
                'authenticated': True,
                'username': username,
                'remember': 'remember' in remember_me if remember_me else False
            }
            return "", "login-error", login_data, "/dashboard"
        else:
            # Đăng nhập thất bại
            error_message = "Tên đăng nhập hoặc mật khẩu không chính xác"
            error_class = "login-error show"
            return error_message, error_class, {'authenticated': False}, "/"
    
    @app.callback(
        [Output('username-input', 'value', allow_duplicate=True),
         Output('password-input', 'value', allow_duplicate=True)],
        [Input('login-url', 'pathname')],
        prevent_initial_call=True
    )
    def clear_inputs_on_load(pathname):
        """Xóa input khi tải trang"""
        if pathname in ['/', '/login']:
            return '', ''
        return dash.no_update, dash.no_update


def check_authentication():
    """Kiểm tra trạng thái xác thực"""
    # Hàm này có thể được mở rộng để kiểm tra session, token, v.v.
    pass