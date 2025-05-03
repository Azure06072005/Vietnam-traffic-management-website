import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def register_callbacks(app, parse_contents, create_sample_data):
    """Đăng ký tất cả các callbacks của ứng dụng Dash"""
    
    # Biến toàn cục
    global global_geojson, global_violations_data, global_accidents_data
    global_geojson = None
    global_violations_data = None
    global_accidents_data = None
    
    # Callback hiển thị trạng thái tải lên GeoJSON
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
        return f"Đã tải lên: {filename}", "upload-status success-status"

    # Callback hiển thị trạng thái tải lên CSV
    @app.callback(
        Output('csv-upload-status', 'children'),
        Output('csv-upload-status', 'className'),
        Output('province-column', 'options'),
        Output('province-column', 'disabled'),
        Output('violations-column', 'options'),
        Output('violations-column', 'disabled'),
        Output('accidents-column', 'options'),
        Output('accidents-column', 'disabled'),
        Input('upload-csv', 'contents'),
        State('upload-csv', 'filename')
    )
    def update_csv_upload_status(contents, filename):
        if contents is None:
            return "", "upload-status", [], True, [], True, [], True
        
        data, error = parse_contents(contents, filename)
        if error:
            return error, "upload-status error-status", [], True, [], True, [], True
        
        # Tạo danh sách tùy chọn cho các dropdown từ các cột trong CSV
        column_options = [{'label': col, 'value': col} for col in data.columns]
        
        return f"Đã tải lên: {filename}", "upload-status success-status", column_options, False, column_options, False, column_options, False

    # Callback xử lý dữ liệu khi nhấn nút
    @app.callback(
        Output('error-message-container', 'children'),
        Output('error-message-container', 'style'),
        Output('results-panel', 'className'),
        Input('process-button', 'n_clicks'),
        Input('use-sample-data', 'n_clicks'),
        State('province-column', 'value'),
        State('violations-column', 'value'),
        State('accidents-column', 'value'),
        State('upload-csv', 'contents'),
        State('upload-csv', 'filename'),
        State('upload-geojson', 'contents'),    
        State('upload-geojson', 'filename'),
        prevent_initial_call=True
    )
    def process_data(process_clicks, sample_clicks, province_column, violations_column, accidents_column, 
                    csv_contents, csv_filename, geojson_contents, geojson_filename):
        # Xác định context để biết nút nào được nhấn
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        global global_geojson, global_violations_data, global_accidents_data
        
        # Trường hợp sử dụng dữ liệu mẫu
        if trigger_id == 'use-sample-data':
            geojson_data, df = create_sample_data()
            global_geojson = geojson_data
            
            province_column = 'Ten_Tinh_Thanh'
            violations_column = 'Count of MAVP'
            accidents_column = 'Count of MATN'
            
            # Tạo dữ liệu vi phạm và tai nạn
            violations_df = df[[province_column, violations_column]].copy()
            violations_df = violations_df.groupby(province_column, as_index=False).sum()
            violations_df.rename(columns={violations_column: 'value'}, inplace=True)
            
            accidents_df = df[[province_column, accidents_column]].copy()
            accidents_df = accidents_df.groupby(province_column, as_index=False).sum()
            accidents_df.rename(columns={accidents_column: 'value'}, inplace=True)
            
            global_violations_data = violations_df
            global_accidents_data = accidents_df
            
            return "", {'display': 'none'}, 'results-panel'
        
        # Trường hợp xử lý dữ liệu đã tải lên
        elif trigger_id == 'process-button':
            # Kiểm tra xem đã tải lên đủ dữ liệu chưa
            if csv_contents is None:
                return "Vui lòng tải lên file CSV trước khi xử lý dữ liệu.", {'display': 'block'}, 'results-panel hidden'
            
            if geojson_contents is None:
                return "Vui lòng tải lên file GeoJSON trước khi xử lý dữ liệu.", {'display': 'block'}, 'results-panel hidden'
            
            if not province_column:
                return "Vui lòng chọn cột chứa tên tỉnh/thành phố.", {'display': 'block'}, 'results-panel hidden'
            
            if not violations_column:
                return "Vui lòng chọn cột chứa dữ liệu vi phạm giao thông.", {'display': 'block'}, 'results-panel hidden'
            
            if not accidents_column:
                return "Vui lòng chọn cột chứa dữ liệu tai nạn giao thông.", {'display': 'block'}, 'results-panel hidden'
            
            try:
                # Đọc dữ liệu CSV
                df, _ = parse_contents(csv_contents, csv_filename)
                
                # Kiểm tra xem các cột đã chọn có tồn tại trong DataFrame không
                required_columns = [province_column, violations_column, accidents_column]
                for col in required_columns:
                    if col not in df.columns:
                        return f"Cột '{col}' không tồn tại trong file CSV.", {'display': 'block'}, 'results-panel hidden'
                
                # Tạo dữ liệu vi phạm và tai nạn
                violations_df = df[[province_column, violations_column]].copy()
                violations_df = violations_df.groupby(province_column, as_index=False).sum()
                violations_df.rename(columns={violations_column: 'value'}, inplace=True)
                
                accidents_df = df[[province_column, accidents_column]].copy()
                accidents_df = accidents_df.groupby(province_column, as_index=False).sum()
                accidents_df.rename(columns={accidents_column: 'value'}, inplace=True)
                
                global_violations_data = violations_df
                global_accidents_data = accidents_df
                
                return "", {'display': 'none'}, 'results-panel'
                
            except Exception as e:
                return f"Lỗi khi xử lý dữ liệu: {str(e)}", {'display': 'block'}, 'results-panel hidden'

    # Callback cập nhật title kết quả
    @app.callback(
        Output('results-title', 'children'),
        Input('data-type-tabs', 'value')
    )
    def update_results_title(data_type):
        if data_type == 'violations':
            return 'Phân tích Vi phạm Giao thông Theo Tỉnh/Thành'
        else:
            return 'Phân tích Tai nạn Giao thông Theo Tỉnh/Thành'

    # Callback cập nhật thẻ tổng quan
    @app.callback(
        [Output('total-count', 'children'),
         Output('avg-count', 'children'),
         Output('max-count', 'children'),
         Output('max-province', 'children'),
         Output('min-count', 'children'),
         Output('min-province', 'children')],
        [Input('data-type-tabs', 'value')]
    )
    def update_stats(data_type):
        global global_violations_data, global_accidents_data
        
        if data_type == 'violations' and global_violations_data is not None:
            data = global_violations_data
        elif data_type == 'accidents' and global_accidents_data is not None:
            data = global_accidents_data
        else:
            return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"
        
        total = data['value'].sum()
        avg = round(data['value'].mean(), 1)
        max_value = data['value'].max()
        max_province = data.loc[data['value'].idxmax(), data.columns[0]]
        min_value = data['value'].min()
        min_province = data.loc[data['value'].idxmin(), data.columns[0]]
        
        return f"{total:,}", f"{avg:,}", f"{max_value:,}", max_province, f"{min_value:,}", min_province

    # Callback cập nhật bản đồ choropleth
    @app.callback(
        Output('map-container', 'children'),
        [Input('data-type-tabs', 'value'),
         Input('color-scale', 'value'),
         Input('display-options', 'value')]
    )
    def update_map(data_type, color_scale, display_options):
        global global_geojson, global_violations_data, global_accidents_data
        
        if 'show_map' not in display_options:
            return "Bản đồ đã bị ẩn. Hãy chọn 'Hiển thị bản đồ' trong tùy chọn hiển thị để xem bản đồ."
        
        if data_type == 'violations' and global_violations_data is not None:
            data = global_violations_data
            title = 'Bản đồ Vi phạm Giao thông Theo Tỉnh/Thành'
            hover_label = 'Số vi phạm'
        elif data_type == 'accidents' and global_accidents_data is not None:
            data = global_accidents_data
            title = 'Bản đồ Tai nạn Giao thông Theo Tỉnh/Thành'
            hover_label = 'Số tai nạn'
        else:
            return "Không có dữ liệu để hiển thị bản đồ."
        
        if global_geojson is None:
            return "Không có dữ liệu GeoJSON để hiển thị bản đồ."
        
        try:
            fig = px.choropleth_mapbox(
                data,
                geojson=global_geojson,
                locations=data.columns[0],
                featureidkey="id",
                color='value',
                color_continuous_scale=color_scale,
                mapbox_style="carto-positron",
                zoom=4.5,  # Điều chỉnh mức zoom
                center={"lat": 16.0, "lon": 106.0},  # Điều chỉnh vị trí trung tâm
                opacity=0.7,
                labels={'value': hover_label},
                hover_name=data.columns[0],
                hover_data={'value': True}
            )

            fig.update_layout(
                title=title,
                title_x=0.5,
                title_font_size=16,
                margin={"r": 0, "t": 40, "l": 0, "b": 0},
                height=600,
                mapbox=dict(
                    bearing=0,  # Hướng của bản đồ
                    pitch=0     # Góc nhìn
                )
            )
            
            return dcc.Graph(figure=fig)
        
        except Exception as e:
            return f"Lỗi khi tạo bản đồ: {str(e)}"

    # Callback cập nhật biểu đồ cột
    @app.callback(
        Output('chart-container', 'children'),
        [Input('data-type-tabs', 'value'),
         Input('display-options', 'value')]
    )
    def update_chart(data_type, display_options):
        global global_violations_data, global_accidents_data
        
        if 'show_bar' not in display_options:
            return "Biểu đồ cột đã bị ẩn. Hãy chọn 'Hiển thị biểu đồ cột' trong tùy chọn hiển thị để xem biểu đồ."
        
        if data_type == 'violations' and global_violations_data is not None:
            data = global_violations_data
            title = 'Top 10 Tỉnh/Thành Có Số Vi phạm Giao thông Cao Nhất'
            y_label = 'Số vi phạm'
            bar_color = '#b91c1c'
        elif data_type == 'accidents' and global_accidents_data is not None:
            data = global_accidents_data
            title = 'Top 10 Tỉnh/Thành Có Số Tai nạn Giao thông Cao Nhất'
            y_label = 'Số tai nạn'
            bar_color = '#1d4ed8'
        else:
            return "Không có dữ liệu để hiển thị biểu đồ."
        
        try:
            # Lấy top 10 tỉnh/thành có giá trị cao nhất
            top10 = data.sort_values('value', ascending=False).head(10)
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=top10[top10.columns[0]],
                y=top10['value'],
                marker_color=bar_color,
                hovertemplate=f"<b>%{{x}}</b><br>{y_label}: %{{y:,}}<extra></extra>"
            ))
            
            fig.update_layout(
                title=title,
                title_x=0.5,
                title_font_size=16,
                xaxis_title="Tỉnh/Thành phố",
                yaxis_title=y_label,
                xaxis_tickangle=-45,
                height=500,
                margin=dict(l=50, r=50, t=70, b=100)
            )
            
            return dcc.Graph(figure=fig)
        
        except Exception as e:
            return f"Lỗi khi tạo biểu đồ: {str(e)}"

    # Callback cập nhật bảng dữ liệu
    @app.callback(
        Output('table-container', 'children'),
        [Input('data-type-tabs', 'value'),
         Input('display-options', 'value')]
    )
    def update_table(data_type, display_options):
        global global_violations_data, global_accidents_data
        
        if 'show_table' not in display_options:
            return "Bảng dữ liệu đã bị ẩn. Hãy chọn 'Hiển thị bảng dữ liệu' trong tùy chọn hiển thị để xem bảng."
        
        if data_type == 'violations' and global_violations_data is not None:
            data = global_violations_data
            title = 'Dữ liệu chi tiết: Vi phạm giao thông theo tỉnh/thành'
            value_column = 'Số vi phạm'
        elif data_type == 'accidents' and global_accidents_data is not None:
            data = global_accidents_data
            title = 'Dữ liệu chi tiết: Tai nạn giao thông theo tỉnh/thành'
            value_column = 'Số tai nạn'
        else:
            return "Không có dữ liệu để hiển thị bảng."
        
        try:
            # Sắp xếp dữ liệu theo giá trị giảm dần
            sorted_data = data.sort_values('value', ascending=False).copy()
            
            # Đổi tên cột để hiển thị
            sorted_data.columns = [sorted_data.columns[0], value_column]
            
            # Thêm cột STT
            sorted_data.insert(0, 'STT', range(1, len(sorted_data) + 1))
            
            # Tạo bảng dữ liệu
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
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#f8fafc'
                    }
                ]
            )
            
            return html.Div([
                html.H3(title, style={'textAlign': 'center', 'marginBottom': '15px'}),
                table
            ])
        
        except Exception as e:
            return f"Lỗi khi tạo bảng dữ liệu: {str(e)}"