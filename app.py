# app.py
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

# 他のモジュールをインポート
from routes import register_routes
from login import create_login_layout, register_login_callbacks, DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD

# データを保存するためのグローバル変数を定義
global_geojson = None
global_data = None
global_summary = None

# カスタムCSSテンプレートを作成
external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css',
    dbc.themes.BOOTSTRAP,
    '/assets/login.css'  # ログイン用CSSを追加
]

# Dashアプリケーションを初期化
app = dash.Dash(__name__, 
                title='VNTraffic Dashboard',
                suppress_callback_exceptions=True,
                external_stylesheets=external_stylesheets,
                meta_tags=[{'name': 'viewport', 
                           'content': 'width=device-width, initial-scale=1.0'}])

# ファビコンを設定
app._favicon = 'favicon.ico'

# layout.pyからメインレイアウトをインポート
from layout import create_layout

# Main app layout
def create_main_app_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='login-session', data={'authenticated': False}),
        html.Div(id='page-content')
    ])

# レイアウトを設定
app.layout = create_main_app_layout()

# ページナビゲーションのためのメインコールバック
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    [State('login-session', 'data')]
)
def display_page(pathname, session_data):
    """URLとログイン状態に基づいてページをナビゲートする"""
    
    # ログイン状態を確認
    if not session_data or not session_data.get('authenticated', False):
        # 未ログイン、ログインページを表示
        return create_login_layout()
    
    # ログイン済み、ダッシュボードを表示
    if pathname in ['/', '/dashboard']:
        return create_layout()
    elif pathname == '/logout':
        # ログアウト処理
        return html.Div([
            dcc.Store(id='logout-trigger', data={'logout': True}),
            html.H2('ログアウトしています...', style={'text-align': 'center', 'margin-top': '50px'})
        ])
    else:
        # ページが見つからない場合
        return html.Div([
            html.H2('404 - ページが見つかりません', style={'text-align': 'center'}),
            html.P('お探しのページは存在しません。', style={'text-align': 'center'}),
            html.A('ホームページに戻る', href='/', style={'text-align': 'center', 'display': 'block'})
        ])

# ログイン処理のコールバック
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
    """ログインロジックを処理する"""
    if n_clicks == 0:
        return dash.no_update, dash.no_update
    
    # ログイン情報を検証
    if username == DEFAULT_ADMIN_USERNAME and password == DEFAULT_ADMIN_PASSWORD:
        # ログイン成功
        session_data = {
            'authenticated': True,
            'username': username,
            'remember': 'remember' in remember_me if remember_me else False
        }
        return session_data, '/dashboard'
    
    # ログイン失敗
    return {'authenticated': False}, '/login'

# ログアウト処理のコールバック
@app.callback(
    [Output('login-session', 'data', allow_duplicate=True),
     Output('url', 'pathname', allow_duplicate=True)],
    [Input('logout-trigger', 'data')],
    prevent_initial_call=True
)
def handle_logout(logout_data):
    """ログアウトを処理する"""
    if logout_data and logout_data.get('logout', False):
        return {'authenticated': False}, '/'
    return dash.no_update, dash.no_update

# ログインエラー表示のコールバック
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
    """ログイン失敗時にエラーメッセージを表示する"""
    if n_clicks == 0:
        return "", "login-error"
    
    # ログインに成功しているか確認
    if session_data and session_data.get('authenticated', False):
        return "", "login-error"
    
    # 入力情報を確認
    if not username or not password:
        return "ユーザー名とパスワードをすべて入力してください", "login-error show"
    
    # 不正な情報のエラーメッセージ
    if username != DEFAULT_ADMIN_USERNAME or password != DEFAULT_ADMIN_PASSWORD:
        return "ユーザー名またはパスワードが正しくありません", "login-error show"
    
    return "", "login-error"

# callbacks.pyからコールバックをインポート
from callbacks import register_callbacks

# GeoJSONの座標エラーを修正する関数（旧コードからコピー）
def fix_geojson_coordinates(geojson_data):
    """GeoJSONの座標エラーを修正し、各フィーチャにIDを付与する"""
    
    # ベトナムの妥当な座標範囲
    VN_LON_MIN, VN_LON_MAX = 102.0, 110.0
    VN_LAT_MIN, VN_LAT_MAX = 8.0, 24.0
    
    coords_need_fixing = False
    
    # 最初の座標をチェックして反転が必要か判断
    if len(geojson_data['features']) > 0:
        feature = geojson_data['features'][0]
        if 'geometry' in feature and 'coordinates' in feature['geometry']:
            if feature['geometry']['type'] == 'Polygon':
                first_ring = feature['geometry']['coordinates'][0]
                if len(first_ring) > 0:
                    first_coord = first_ring[0]
                    
                    # 座標がベトナムの範囲内にあるか確認
                    if (first_coord[0] < VN_LON_MIN or first_coord[0] > VN_LON_MAX or
                        first_coord[1] < VN_LAT_MIN or first_coord[1] > VN_LAT_MAX):
                        coords_need_fixing = True
    
    # 必要なら座標を修正
    if coords_need_fixing:
        for feature in geojson_data['features']:
            if 'geometry' in feature and 'coordinates' in feature['geometry']:
                geometry_type = feature['geometry']['type']
                
                if geometry_type == 'Polygon':
                    for ring_idx in range(len(feature['geometry']['coordinates'])):
                        for point_idx in range(len(feature['geometry']['coordinates'][ring_idx])):
                            # [x, y]を[y, x]に反転
                            feature['geometry']['coordinates'][ring_idx][point_idx] = [
                                feature['geometry']['coordinates'][ring_idx][point_idx][1],
                                feature['geometry']['coordinates'][ring_idx][point_idx][0]
                            ]
                
                elif geometry_type == 'MultiPolygon':
                    for poly_idx in range(len(feature['geometry']['coordinates'])):
                        for ring_idx in range(len(feature['geometry']['coordinates'][poly_idx])):
                            for point_idx in range(len(feature['geometry']['coordinates'][poly_idx][ring_idx])):
                                # [x, y]を[y, x]に反転
                                feature['geometry']['coordinates'][poly_idx][ring_idx][point_idx] = [
                                    feature['geometry']['coordinates'][poly_idx][ring_idx][point_idx][1],
                                    feature['geometry']['coordinates'][poly_idx][ring_idx][point_idx][0]
                                ]
    
    # 各フィーチャにIDを追加
    for feature in geojson_data['features']:
        if 'properties' in feature and 'ten_tinh' in feature['properties']:
            feature['id'] = feature['properties']['ten_tinh']
    
    return geojson_data

# 通貨の値を処理する関数
def parse_currency(value):
    """通貨文字列（例: '40000000 ₫'）を数値に変換する"""
    if isinstance(value, str):
        # 通貨記号と空白を削除
        return int(value.replace('₫', '').replace(' ', '').strip())
    return value

# ファイルアップロードを処理する関数
def parse_contents(contents, filename):
    """アップロードされたファイルの内容を解析する"""
    import base64
    import io
    import pandas as pd
    import json
    
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        if 'csv' in filename.lower():
            # CSVファイルを読み込む
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            return df, None
        elif 'json' in filename.lower() or 'geojson' in filename.lower():
            # GeoJSONファイルを読み込む
            geojson_data = json.loads(decoded.decode('utf-8'))
            # GeoJSONの座標エラーを修正
            fixed_geojson = fix_geojson_coordinates(geojson_data)
            return fixed_geojson, None
        else:
            return None, f"ファイル形式 {filename} はサポートされていません。"
    except Exception as e:
        return None, f"ファイル {filename} の処理中にエラーが発生しました: {str(e)}"

# コールバックを登録
register_callbacks(app, parse_contents, parse_currency)
register_routes(app)

# アプリケーションを実行
if __name__ == '__main__':
    app.run(debug=True, host='localhost')