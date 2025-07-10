from dash import dcc, html, Input, Output, State, callback_context
import dash

# デフォルトのログイン情報
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "123456"

def create_login_layout():
    """ログインページのレイアウトを作成する"""
    return html.Div([
        html.Div([
            html.Div([
                # ロゴとタイトル
                html.Div([
                    html.Img(src='/assets/logo.png', className='login-logo'),
                    html.H1('ベトナムの道路交通システム', className='login-title'),
                    html.H2('ログイン画面', className='login-subtitle')
                ], className='login-header'),
                
                # ログインフォーム
                html.Div([
                    html.Div([
                        html.Label('ユーザー名', className='login-label'),
                        dcc.Input(
                            id='username-input',
                            type='text',
                            placeholder='ユーザー名を入力してください',
                            className='login-input',
                            value=''
                        )
                    ], className='login-field'),
                    
                    html.Div([
                        html.Label('パスワード', className='login-label'),
                        dcc.Input(
                            id='password-input',
                            type='password',
                            placeholder='パスワードを入力してください',
                            className='login-input',
                            value=''
                        )
                    ], className='login-field'),
                    
                    # 「ログイン状態を記憶」チェックボックス
                    html.Div([
                        dcc.Checklist(
                            id='remember-me',
                            options=[{'label': ' ログイン状態を記憶する', 'value': 'remember'}],
                            value=[],
                            className='remember-checkbox'
                        )
                    ], className='login-field'),
                    
                    # ログインボタン
                    html.Button('ログイン', id='login-button', className='login-button', n_clicks=0),
                    
                    # エラーメッセージの表示
                    html.Div(id='login-error', className='login-error'),
                    
                    # サブリンク
                    html.Div([
                        html.A('パスワードを忘れた場合', href='#', className='login-link forgot-password'),
                        html.A('アカウントが未登録ですか？今すぐ登録', href='#', className='login-link register')
                    ], className='login-options'),
                    
                    # デモ用ログイン情報
                    html.Div([
                        html.P('デモアカウント：', className='login-demo-title'),
                        html.P(f'ユーザー名: {DEFAULT_ADMIN_USERNAME}', className='login-demo-info'),
                        html.P(f'パスワード: {DEFAULT_ADMIN_PASSWORD}', className='login-demo-info')
                    ], className='login-demo-section')
                ], className='login-form-container')
            ], className='login-card')
        ], className='login-wrapper'),
        
        # ログイン状態を保存するStore
        dcc.Store(id='login-state', data={'authenticated': False}),
        dcc.Location(id='login-url', refresh=True)
    ], className='login-page')


def register_login_callbacks(app):
    """ログインシステムのコールバックを登録する"""
    
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
        """ユーザー認証処理"""
        if n_clicks == 0:
            return "", "login-error", {'authenticated': False}, "/"
        
        # エラーメッセージ初期化
        error_message = ""
        error_class = "login-error"
        
        # 入力確認
        if not username or not password:
            error_message = "ユーザー名とパスワードを入力してください。"
            error_class = "login-error show"
            return error_message, error_class, {'authenticated': False}, "/"
        
        # 認証処理
        if username == DEFAULT_ADMIN_USERNAME and password == DEFAULT_ADMIN_PASSWORD:
            # 認証成功
            login_data = {
                'authenticated': True,
                'username': username,
                'remember': 'remember' in remember_me if remember_me else False
            }
            return "", "login-error", login_data, "/dashboard"
        else:
            # 認証失敗
            error_message = "ユーザー名またはパスワードが正しくありません。"
            error_class = "login-error show"
            return error_message, error_class, {'authenticated': False}, "/"
    
    @app.callback(
        [Output('username-input', 'value', allow_duplicate=True),
         Output('password-input', 'value', allow_duplicate=True)],
        [Input('login-url', 'pathname')],
        prevent_initial_call=True
    )
    def clear_inputs_on_load(pathname):
        """ページ読み込み時に入力をクリア"""
        if pathname in ['/', '/login']:
            return '', ''
        return dash.no_update, dash.no_update


def check_authentication():
    """認証状態をチェックする関数（今後拡張予定）"""
    pass
