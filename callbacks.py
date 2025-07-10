# callbacks.py
import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json

def register_callbacks(app, parse_contents, parse_currency):
    """アプリケーションのすべてのコールバックを登録する"""
    
    # グローバル変数を使用
    global global_geojson, global_data, global_summary
    global_geojson = None
    global_data = None
    global_summary = None
    
    @app.callback(
    [Output('current-flag', 'src'),
     Output('current-language', 'children')],
    [Input('lang-vi', 'n_clicks'),
     Input('lang-en', 'n_clicks'),
     Input('lang-ja', 'n_clicks'),
     Input('lang-ru', 'n_clicks')],
    prevent_initial_call=True
    )
    def update_language(*args):
        # callback_contextを使用してどのボタンが押されたかを判断
        ctx = dash.callback_context
        
        # イベントがトリガーされていない場合は更新しない
        if not ctx.triggered:
            return dash.no_update, dash.no_update
        
        # イベントをトリガーしたコンポーネントのIDを取得
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # トリガーされたIDに基づいて言語を更新
        if triggered_id == 'lang-ja':
            return 'assets/japan.png', '日本語'
        elif triggered_id == 'lang-en':
            return 'assets/uk.png', 'English'
        elif triggered_id == 'lang-vi':
            return 'assets/vietnam.png', 'Tiếng Việt'
        elif triggered_id == 'lang-ru':
            return 'assets/russia.png', 'Русский'
        
        # デフォルトでは何も更新しない
        return dash.no_update, dash.no_update
    
    # GeoJSONアップロードステータス表示のコールバック
    @app.callback(
        Output('geojson-upload-status', 'children'),
        Output('geojson-upload-status', 'className'),
        Input('upload-geojson', 'contents'),
        State('upload-geojson', 'filename')
    )
    def update_geojson_upload_status(contents, filename):
        if contents is None:
            return "", "upload-status"
        
        global global_geojson
        
        data, error = parse_contents(contents, filename)
        if error:
            return error, "upload-status error-status"
        
        global_geojson = data
        return f"アップロード完了: {filename}", "upload-status success-status"

    # CSVアップロードステータス表示とドロップダウン更新のコールバック
    @app.callback(
        [Output('csv-upload-status', 'children'),
         Output('csv-upload-status', 'className'),
         Output('province-column', 'options'),
         Output('data-column', 'options')],
        [Input('upload-csv', 'contents'),
         Input('data-type', 'value')],
        [State('upload-csv', 'filename')]
    )
    def update_csv_upload_status(contents, data_type, filename):
        # ファイルの内容がない場合は空のステータスを返す
        if contents is None:
            return "", "upload-status", [], []
        
        # CSVファイルの内容を解析
        data, error = parse_contents(contents, filename)
        if error:
            return error, "upload-status error-status", [], []
        
        # 省/市選択ドロップダウンのオプションリストを作成
        province_options = [{'label': col, 'value': col} for col in data.columns]
        
        # データタイプに基づいてデータ列選択ドロップダウンのオプションリストを作成
        data_options = []
        
        # 選択されたデータタイプに合った列をフィルタリング
        for col in data.columns:
            col_lower = col.lower()
            if data_type == 'violations' and ('vi phạm' in col_lower or 'mavp' in col_lower):
                data_options.append({'label': col, 'value': col})
            elif data_type == 'accidents' and ('tai nạn' in col_lower or 'matn' in col_lower):
                data_options.append({'label': col, 'value': col})
            elif data_type == 'deaths' and ('tử vong' in col_lower or 'tuvong' in col_lower):
                data_options.append({'label': col, 'value': col})
            elif data_type == 'injuries' and ('bị thương' in col_lower or 'bithuong' in col_lower):
                data_options.append({'label': col, 'value': col})
            elif data_type == 'fines' and ('mức phạt' in col_lower or 'mucphat' in col_lower):
                data_options.append({'label': col, 'value': col})
        
        # 適切な列が見つからない場合、すべての数値列を追加
        if not data_options:
            for col in data.columns:
                if pd.api.types.is_numeric_dtype(data[col]):
                    data_options.append({'label': col, 'value': col})
        
        return f"アップロード完了: {filename}", "upload-status success-status", province_options, data_options

    # データタイプ変更時にdata-columnのオプションを更新するコールバック
    @app.callback(
        Output('data-column', 'options', allow_duplicate=True),
        Input('data-type', 'value'),
        State('upload-csv', 'contents'),
        State('upload-csv', 'filename'),
        prevent_initial_call=True
    )
    def update_data_column_options(data_type, contents, filename):
        # ファイルの内容がない場合は空のリストを返す
        if contents is None:
            return []
        
        # CSVファイルの内容を解析
        data, error = parse_contents(contents, filename)
        if error:
            return []
        
        # データタイプに基づいてデータ列選択ドロップダウンのオプションリストを作成
        data_options = []
        
        # 選択されたデータタイプに合った列をフィルタリング
        for col in data.columns:
            col_lower = col.lower()
            if data_type == 'violations' and ('vi phạm' in col_lower or 'mavp' in col_lower):
                data_options.append({'label': col, 'value': col})
            elif data_type == 'accidents' and ('tai nạn' in col_lower or 'matn' in col_lower):
                data_options.append({'label': col, 'value': col})
            elif data_type == 'deaths' and ('tử vong' in col_lower or 'tuvong' in col_lower):
                data_options.append({'label': col, 'value': col})
            elif data_type == 'injuries' and ('bị thương' in col_lower or 'bithuong' in col_lower):
                data_options.append({'label': col, 'value': col})
            elif data_type == 'fines' and ('mức phạt' in col_lower or 'mucphat' in col_lower):
                data_options.append({'label': col, 'value': col})
        
        # 適切な列が見つからない場合、すべての数値列を追加
        if not data_options:
            for col in data.columns:
                if pd.api.types.is_numeric_dtype(data[col]):
                    data_options.append({'label': col, 'value': col})
        
        return data_options
    
    # ボタンクリックでデータを処理するコールバック
    @app.callback(
        [Output('error-message-container', 'children'),
         Output('error-message-container', 'style'),
         Output('results-panel', 'className'),
         Output('results-title', 'children')],
        [Input('process-button', 'n_clicks')],
        [State('province-column', 'value'),
         State('data-column', 'value'),
         State('data-type', 'value'),
         State('upload-csv', 'contents'),
         State('upload-csv', 'filename'),
         State('upload-geojson', 'contents'),    
         State('upload-geojson', 'filename')],
        prevent_initial_call=True
    )
    def process_data(process_clicks, province_column, data_column, 
                    data_type, csv_contents, csv_filename, geojson_contents, geojson_filename):
        
        global global_geojson, global_data, global_summary
        
        # データタイプに応じたタイトルを取得
        title = get_title_from_data_type(data_type, data_column)
            
        # 十分なデータがアップロードされているか確認
        if csv_contents is None:
            return "データを処理する前にCSVファイルをアップロードしてください。", {'display': 'block'}, 'results-panel hidden', title
        
        if geojson_contents is None:
            return "データを処理する前にGeoJSONファイルをアップロードしてください。", {'display': 'block'}, 'results-panel hidden', title
        
        if not province_column:
            return "省/市名を含む列を選択してください。", {'display': 'block'}, 'results-panel hidden', title
        
        if not data_column:
            return "データ列を選択してください。", {'display': 'block'}, 'results-panel hidden', title
        
        try:
            # CSVデータを読み込み
            df, _ = parse_contents(csv_contents, csv_filename)
            
            # 選択された列がDataFrameに存在するか確認
            if province_column not in df.columns:
                return f"列 '{province_column}' はCSVファイルに存在しません。", {'display': 'block'}, 'results-panel hidden', title
            
            if data_column not in df.columns:
                return f"列 '{data_column}' はCSVファイルに存在しません。", {'display': 'block'}, 'results-panel hidden', title
            
            # データタイプに基づいてデータを処理
            if data_type == 'violations':
                # 省別の違反件数をカウント
                data_df = count_by_province(df, province_column, 'MAVP')
            elif data_type == 'accidents':
                # 省別の事故件数をカウント（各MATNは個別の事故）
                data_df = count_unique_by_province(df, province_column, 'MATN')
            elif data_type == 'deaths':
                # 省別の死亡者数を合計
                data_df = sum_by_province(df, province_column, 'TUVONG')
            elif data_type == 'injuries':
                # 省別の負傷者数を合計
                data_df = sum_by_province(df, province_column, 'BITHUONG')
            elif data_type == 'fines':
                # 省別の罰金額を合計（文字列を数値に変換）
                data_df = sum_currency_by_province(df, province_column, 'Tổng mức phạt', parse_currency)
            else:
                # 他のデータタイプの場合、選択された列で集計を試みる
                data_df = df[[province_column, data_column]].copy()
                
                # データ列が通貨形式か確認
                if isinstance(data_df[data_column].iloc[0], str) and ('₫' in data_df[data_column].iloc[0] or 'đ' in data_df[data_column].iloc[0]):
                    data_df[data_column] = data_df[data_column].apply(parse_currency)
                
                data_df = data_df.groupby(province_column, as_index=False).sum()
            
            # 後の処理を容易にするため、データ列の名前を'value'に変更
            if len(data_df.columns) > 1:
                data_df.rename(columns={data_df.columns[1]: 'value'}, inplace=True)
            
            global_data = data_df
            
            # 集計データを作成
            create_summary_data(df)
            
            return "", {'display': 'none'}, 'results-panel', title
                
        except Exception as e:
            return f"データ処理中にエラーが発生しました: {str(e)}", {'display': 'block'}, 'results-panel hidden', title
    
    # 省/市別の件数をカウントする関数
    def count_by_province(df, province_column, count_column):
        """省/市別の行数をカウントする"""
        count_df = df.groupby(province_column).size().reset_index(name='value')
        return count_df
    
    # 省/市別の一意な件数をカウントする関数
    def count_unique_by_province(df, province_column, unique_column):
        """省/市別のunique_columnの一意な値の数をカウントする"""
        count_df = df.groupby(province_column)[unique_column].nunique().reset_index(name='value')
        return count_df
    
    # 省/市別の合計を計算する関数
    def sum_by_province(df, province_column, sum_column):
        """省/市別のsum_columnの合計値を計算する"""
        df_copy = df.copy()
        df_copy[sum_column] = pd.to_numeric(df_copy[sum_column], errors='coerce')
        sum_df = df_copy.groupby(province_column)[sum_column].sum().reset_index(name='value')
        return sum_df
    
    # 省/市別の通貨の合計を計算する関数
    def sum_currency_by_province(df, province_column, currency_column, parse_func):
        """省/市別のcurrency_columnの通貨の合計値を計算する"""
        df_copy = df.copy()
        if df_copy[currency_column].dtype == 'object':
            df_copy[currency_column] = df_copy[currency_column].apply(parse_func)
        sum_df = df_copy.groupby(province_column)[currency_column].sum().reset_index(name='value')
        return sum_df
    
    # データタイプからタイトルを取得するヘルパー関数
    def get_title_from_data_type(data_type, data_column):
        if data_type == 'violations':
            return '省/市別の交通違反分析'
        elif data_type == 'accidents':
            return '省/市別の交通事故分析'
        elif data_type == 'deaths':
            return '省/市別の死亡者数分析'
        elif data_type == 'injuries':
            return '省/市別の負傷者数分析'
        elif data_type == 'fines':
            return '省/市別の罰金総額分析'
        else:
            return '省/市別の交通データ分析'
    
    # 集計データを作成する関数
    def create_summary_data(df):
        global global_summary
        summary = {}
        summary['violations'] = len(df)
        if 'MATN' in df.columns:
            summary['accidents'] = df['MATN'].nunique()
        else:
            summary['accidents'] = 'N/A'
        if 'TUVONG' in df.columns:
            df_copy = df.copy()
            df_copy['TUVONG'] = pd.to_numeric(df_copy['TUVONG'], errors='coerce')
            summary['deaths'] = df_copy['TUVONG'].sum()
        else:
            summary['deaths'] = 'N/A'
        if 'BITHUONG' in df.columns:
            df_copy = df.copy()
            df_copy['BITHUONG'] = pd.to_numeric(df_copy['BITHUONG'], errors='coerce')
            summary['injuries'] = df_copy['BITHUONG'].sum()
        else:
            summary['injuries'] = 'N/A'
        if 'Tổng mức phạt' in df.columns:
            df_copy = df.copy()
            if df_copy['Tổng mức phạt'].dtype == 'object':
                df_copy['Tổng mức phạt'] = df_copy['Tổng mức phạt'].apply(parse_currency)
            summary['fines'] = df_copy['Tổng mức phạt'].sum()
        else:
            summary['fines'] = 'N/A'
        global_summary = summary
    
    # 統計カードを更新するコールバック
    @app.callback(
        [Output('total-count', 'children'),
         Output('avg-count', 'children'),
         Output('max-count', 'children'),
         Output('max-province', 'children'),
         Output('min-count', 'children'),
         Output('min-province', 'children')],
        [Input('results-panel', 'className'),
         Input('data-type', 'value')]
    )
    def update_stats(results_panel_class, data_type):
        global global_data
        
        if results_panel_class == 'results-panel hidden' or global_data is None:
            return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"
        
        if data_type == 'fines':
            format_func = lambda x: f"{x:,.0f} ₫"
        else:
            format_func = lambda x: f"{x:,.0f}"
        
        total = global_data['value'].sum()
        avg = round(global_data['value'].mean(), 1)
        max_value = global_data['value'].max()
        max_province = global_data.loc[global_data['value'].idxmax(), global_data.columns[0]]
        min_value = global_data['value'].min()
        min_province = global_data.loc[global_data['value'].idxmin(), global_data.columns[0]]
        
        return format_func(total), format_func(avg), format_func(max_value), max_province, format_func(min_value), min_province
    
    # 集計統計を更新するコールバック
    @app.callback(
        [Output('total-violations', 'children'),
         Output('total-accidents', 'children'),
         Output('total-deaths', 'children'),
         Output('total-injuries', 'children'),
         Output('total-fines', 'children')],
        [Input('results-panel', 'className')]
    )
    def update_summary_stats(results_panel_class):
        global global_summary
        
        if results_panel_class == 'results-panel hidden' or global_summary is None:
            return "N/A", "N/A", "N/A", "N/A", "N/A"
        
        violations = global_summary.get('violations', 'N/A')
        accidents = global_summary.get('accidents', 'N/A')
        deaths = global_summary.get('deaths', 'N/A')
        injuries = global_summary.get('injuries', 'N/A')
        fines = global_summary.get('fines', 'N/A')
        
        if violations != 'N/A':
            violations = f"{violations:,}"
        if accidents != 'N/A':
            accidents = f"{accidents:,}"
        if deaths != 'N/A':
            deaths = f"{deaths:,}"
        if injuries != 'N/A':
            injuries = f"{injuries:,}"
        if fines != 'N/A':
            fines = f"{fines:,.0f} ₫"
        
        return violations, accidents, deaths, injuries, fines

    # コロプレス地図を更新するコールバック
    @app.callback(
        Output('map-container', 'children'),
        [Input('results-panel', 'className'),
         Input('color-scale', 'value'),
         Input('display-options', 'value'),
         Input('data-type', 'value')]
    )
    def update_map(results_panel_class, color_scale, display_options, data_type):
        global global_geojson, global_data
        
        if results_panel_class == 'results-panel hidden':
            return ""
        
        if 'show_map' not in display_options:
            return "地図は非表示です。「地図を表示」オプションを選択して地図を表示してください。"
        
        if global_data is None:
            return "地図を表示するためのデータがありません。"
        
        if global_geojson is None:
            return "地図を表示するためのGeoJSONデータがありません。"
        
        titles = {
            'violations': '省/市別の交通違反マップ',
            'accidents': '省/市別の交通事故マップ',
            'deaths': '省/市別の死亡者数マップ',
            'injuries': '省/市別の負傷者数マップ',
            'fines': '省/市別の罰金総額マップ'
        }
        hover_labels = {
            'violations': '違反件数',
            'accidents': '事故件数',
            'deaths': '死亡者数',
            'injuries': '負傷者数',
            'fines': '罰金総額'
        }
        
        title = titles.get(data_type, '省/市別の交通データマップ')
        hover_label = hover_labels.get(data_type, '値')
        hover_template = "<b>%{hovertext}</b><br>" + hover_label + ": %{customdata[0]:,.0f}" + (" ₫" if data_type == 'fines' else "") + "<extra></extra>"
        
        try:
            fig = px.choropleth_mapbox(
                global_data,
                geojson=global_geojson,
                locations=global_data.columns[0],
                featureidkey="id",
                color='value',
                color_continuous_scale=color_scale,
                mapbox_style="carto-positron",
                zoom=4.5,
                center={"lat": 16.0, "lon": 106.0},
                opacity=0.7,
                labels={'value': hover_label},
                hover_name=global_data.columns[0],
                hover_data={'value': True}
            )
            
            fig.update_traces(hovertemplate=hover_template)
            
            fig.update_layout(
                title=title,
                title_x=0.5,
                title_font_size=16,
                margin={"r": 0, "t": 40, "l": 0, "b": 0},
                height=600,
                mapbox=dict(bearing=0, pitch=0)
            )
            
            return dcc.Graph(figure=fig)
        
        except Exception as e:
            return f"地図作成中にエラーが発生しました: {str(e)}"

    # 棒グラフを更新するコールバック
    @app.callback(
        Output('chart-container', 'children'),
        [Input('results-panel', 'className'),
         Input('display-options', 'value'),
         Input('data-type', 'value')]
    )
    def update_chart(results_panel_class, display_options, data_type):
        global global_data
        
        if results_panel_class == 'results-panel hidden':
            return ""
        
        if 'show_bar' not in display_options:
            return "棒グラフは非表示です。「棒グラフを表示」オプションを選択してグラフを表示してください。"
        
        if global_data is None:
            return "グラフを表示するためのデータがありません。"
            
        titles = {
            'violations': '交通違反件数トップ10の省/市',
            'accidents': '交通事故件数トップ10の省/市',
            'deaths': '死亡者数トップ10の省/市',
            'injuries': '負傷者数トップ10の省/市',
            'fines': '罰金総額トップ10の省/市'
        }
        y_labels = {
            'violations': '違反件数',
            'accidents': '事故件数',
            'deaths': '死亡者数',
            'injuries': '負傷者数',
            'fines': '罰金総額 (₫)'
        }
        bar_colors = {
            'violations': '#b91c1c', 'accidents': '#1d4ed8', 'deaths': '#b91c1c',
            'injuries': '#ca8a04', 'fines': '#059669'
        }
        
        title = titles.get(data_type, '値が最も高いトップ10の省/市')
        y_label = y_labels.get(data_type, '値')
        bar_color = bar_colors.get(data_type, '#3b82f6')
        format_func = (lambda x: f"{x:,.0f} ₫") if data_type == 'fines' else (lambda x: f"{x:,.0f}")
        
        try:
            top10 = global_data.sort_values('value', ascending=False).head(10)
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=top10[top10.columns[0]],
                y=top10['value'],
                marker_color=bar_color,
                text=top10['value'].apply(format_func),
                textposition='auto',
                hovertemplate=f"<b>%{{x}}</b><br>{y_label}: %{{text}}<extra></extra>"
            ))
            
            fig.update_layout(
                title=title,
                title_x=0.5,
                title_font_size=16,
                xaxis_title="省/市",
                yaxis_title=y_label,
                xaxis_tickangle=-45,
                height=500,
                margin=dict(l=50, r=50, t=70, b=100)
            )
            
            return dcc.Graph(figure=fig)
        
        except Exception as e:
            return f"グラフ作成中にエラーが発生しました: {str(e)}"

    # データテーブルを更新するコールバック
    @app.callback(
        Output('table-container', 'children'),
        [Input('results-panel', 'className'),
        Input('display-options', 'value'),
        Input('data-type', 'value')]
    )
    def update_table(results_panel_class, display_options, data_type):
        global global_data
        
        if results_panel_class == 'results-panel hidden':
            return ""
        
        if 'show_table' not in display_options:
            return "データテーブルは非表示です。「データテーブルを表示」オプションを選択してテーブルを表示してください。"
        
        if global_data is None:
            return "テーブルを表示するためのデータがありません。"
        
        titles = {
            'violations': '詳細データ: 省/市別の交通違反',
            'accidents': '詳細データ: 省/市別の交通事故',
            'deaths': '詳細データ: 省/市別の死亡者数',
            'injuries': '詳細データ: 省/市別の負傷者数',
            'fines': '詳細データ: 省/市別の罰金総額'
        }
        value_columns = {
            'violations': '違反件数', 'accidents': '事故件数', 'deaths': '死亡者数',
            'injuries': '負傷者数', 'fines': '罰金総額 (₫)'
        }
        
        title = titles.get(data_type, '省/市別の詳細データ')
        value_column = value_columns.get(data_type, '値')
        formatter = (lambda x: f"{x:,.0f} ₫") if data_type == 'fines' else None
        
        try:
            sorted_data = global_data.sort_values('value', ascending=False).copy()
            
            if formatter:
                sorted_data['value'] = sorted_data['value'].apply(formatter)
            
            sorted_data.columns = [sorted_data.columns[0], value_column]
            
            sorted_data.insert(0, '番号', range(1, len(sorted_data) + 1))
            
            table = dash_table.DataTable(
                id='data-table',
                columns=[{"name": col, "id": col} for col in sorted_data.columns],
                data=sorted_data.to_dict('records'),
                sort_action="native",
                filter_action="native",
                page_size=15,
                style_table={'overflowX': 'auto'},
                style_header={
                    'backgroundColor': '#f1f5f9',
                    'fontWeight': 'bold',
                    'padding': '10px 15px',
                    'border': '1px solid #e2e8f0'
                },
                style_cell={
                    'padding': '10px 15px',
                    'border': '1px solid #e2e8f0',
                    'textAlign': 'left'
                },
                style_data_conditional=[
                    {'if': {'row_index': 'odd'}, 'backgroundColor': '#f8fafc'}
                ]
            )
            
            return html.Div([
                html.H3(title, style={'textAlign': 'center', 'marginBottom': '15px'}),
                table
            ])
        
        except Exception as e:
            return f"データテーブル作成中にエラーが発生しました: {str(e)}"