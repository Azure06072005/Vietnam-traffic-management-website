import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json

def register_callbacks(app, parse_contents, parse_currency):
    """Đăng ký tất cả các callbacks của ứng dụng Dash"""
    
    # Sử dụng các biến toàn cục
    global global_geojson, global_data, global_summary
    global_geojson = None
    global_data = None
    global_summary = None
    
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

    # Callback hiển thị trạng thái tải lên CSV và cập nhật dropdown
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
        # Nếu không có nội dung file, trả về trạng thái trống
        if contents is None:
            return "", "upload-status", [], []
        
        # Phân tích nội dung file CSV
        data, error = parse_contents(contents, filename)
        if error:
            return error, "upload-status error-status", [], []
        
        # Tạo danh sách options cho dropdown chọn cột tỉnh/thành
        province_options = [{'label': col, 'value': col} for col in data.columns]
        
        # Tạo danh sách options cho dropdown chọn cột dữ liệu dựa vào loại dữ liệu
        data_options = []
        
        # Lọc các cột phù hợp với loại dữ liệu được chọn
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
        
        # Nếu không tìm thấy cột phù hợp, bổ sung tất cả các cột số
        if not data_options:
            for col in data.columns:
                if pd.api.types.is_numeric_dtype(data[col]):
                    data_options.append({'label': col, 'value': col})
        
        return f"Đã tải lên: {filename}", "upload-status success-status", province_options, data_options

    # Callback cập nhật options cho data-column khi thay đổi data-type
    @app.callback(
        Output('data-column', 'options', allow_duplicate=True),
        Input('data-type', 'value'),
        State('upload-csv', 'contents'),
        State('upload-csv', 'filename'),
        prevent_initial_call=True
    )
    def update_data_column_options(data_type, contents, filename):
        # Nếu không có nội dung file, trả về danh sách rỗng
        if contents is None:
            return []
        
        # Phân tích nội dung file CSV
        data, error = parse_contents(contents, filename)
        if error:
            return []
        
        # Tạo danh sách options cho dropdown chọn cột dữ liệu dựa vào loại dữ liệu
        data_options = []
        
        # Lọc các cột phù hợp với loại dữ liệu được chọn
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
        
        # Nếu không tìm thấy cột phù hợp, bổ sung tất cả các cột số
        if not data_options:
            for col in data.columns:
                if pd.api.types.is_numeric_dtype(data[col]):
                    data_options.append({'label': col, 'value': col})
        
        return data_options
    
    # Callback xử lý dữ liệu khi nhấn nút
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
        
        # Lấy tiêu đề phù hợp với loại dữ liệu
        title = get_title_from_data_type(data_type, data_column)
            
        # Kiểm tra xem đã tải lên đủ dữ liệu chưa
        if csv_contents is None:
            return "Vui lòng tải lên file CSV trước khi xử lý dữ liệu.", {'display': 'block'}, 'results-panel hidden', title
        
        if geojson_contents is None:
            return "Vui lòng tải lên file GeoJSON trước khi xử lý dữ liệu.", {'display': 'block'}, 'results-panel hidden', title
        
        if not province_column:
            return "Vui lòng chọn cột chứa tên tỉnh/thành phố.", {'display': 'block'}, 'results-panel hidden', title
        
        if not data_column:
            return "Vui lòng chọn cột dữ liệu.", {'display': 'block'}, 'results-panel hidden', title
        
        try:
            # Đọc dữ liệu CSV
            df, _ = parse_contents(csv_contents, csv_filename)
            
            # Kiểm tra xem các cột đã chọn có tồn tại trong DataFrame không
            if province_column not in df.columns:
                return f"Cột '{province_column}' không tồn tại trong file CSV.", {'display': 'block'}, 'results-panel hidden', title
            
            if data_column not in df.columns:
                return f"Cột '{data_column}' không tồn tại trong file CSV.", {'display': 'block'}, 'results-panel hidden', title
            
            # Xử lý dữ liệu dựa vào loại dữ liệu
            if data_type == 'violations':
                # Đếm số lượng vi phạm theo tỉnh
                data_df = count_by_province(df, province_column, 'MAVP')
            elif data_type == 'accidents':
                # Đếm số lượng tai nạn theo tỉnh (mỗi mã MATN là một tai nạn riêng biệt)
                data_df = count_unique_by_province(df, province_column, 'MATN')
            elif data_type == 'deaths':
                # Tính tổng số người tử vong theo tỉnh
                data_df = sum_by_province(df, province_column, 'TUVONG')
            elif data_type == 'injuries':
                # Tính tổng số người bị thương theo tỉnh
                data_df = sum_by_province(df, province_column, 'BITHUONG')
            elif data_type == 'fines':
                # Tính tổng mức phạt theo tỉnh (đảm bảo chuyển đổi chuỗi sang số)
                data_df = sum_currency_by_province(df, province_column, 'Tổng mức phạt', parse_currency)
            else:
                # Nếu là loại dữ liệu khác, cố gắng tổng hợp theo cột đã chọn
                data_df = df[[province_column, data_column]].copy()
                
                # Kiểm tra xem cột dữ liệu có phải là dạng tiền tệ không
                if isinstance(data_df[data_column].iloc[0], str) and ('₫' in data_df[data_column].iloc[0] or 'đ' in data_df[data_column].iloc[0]):
                    data_df[data_column] = data_df[data_column].apply(parse_currency)
                
                data_df = data_df.groupby(province_column, as_index=False).sum()
            
            # Đổi tên cột dữ liệu thành 'value' để dễ dàng xử lý sau này
            if len(data_df.columns) > 1:
                data_df.rename(columns={data_df.columns[1]: 'value'}, inplace=True)
            
            global_data = data_df
            
            # Tạo dữ liệu tổng hợp
            create_summary_data(df)
            
            return "", {'display': 'none'}, 'results-panel', title
                
        except Exception as e:
            return f"Lỗi khi xử lý dữ liệu: {str(e)}", {'display': 'block'}, 'results-panel hidden', title
    
    # Hàm đếm số lượng theo tỉnh/thành
    def count_by_province(df, province_column, count_column):
        """Đếm số lượng hàng theo tỉnh/thành"""
        # Tạo DataFrame mới với cột province_column và cột đếm
        count_df = df.groupby(province_column).size().reset_index(name='value')
        return count_df
    
    # Hàm đếm số lượng độc nhất theo tỉnh/thành
    def count_unique_by_province(df, province_column, unique_column):
        """Đếm số lượng giá trị độc nhất của unique_column theo tỉnh/thành"""
        # Tạo DataFrame mới với cột province_column và cột đếm giá trị độc nhất
        count_df = df.groupby(province_column)[unique_column].nunique().reset_index(name='value')
        return count_df
    
    # Hàm tính tổng số lượng theo tỉnh/thành
    def sum_by_province(df, province_column, sum_column):
        """Tính tổng giá trị của sum_column theo tỉnh/thành"""
        # Chuyển đổi sang kiểu số trước khi tính tổng
        df_copy = df.copy()
        df_copy[sum_column] = pd.to_numeric(df_copy[sum_column], errors='coerce')
        
        # Tạo DataFrame mới với cột province_column và cột tổng
        sum_df = df_copy.groupby(province_column)[sum_column].sum().reset_index(name='value')
        return sum_df
    
    # Hàm tính tổng tiền tệ theo tỉnh/thành
    def sum_currency_by_province(df, province_column, currency_column, parse_func):
        """Tính tổng giá trị tiền tệ của currency_column theo tỉnh/thành"""
        # Tạo bản sao DataFrame để không ảnh hưởng đến dữ liệu gốc
        df_copy = df.copy()
        
        # Kiểm tra xem cột tiền tệ có phải là chuỗi không
        if df_copy[currency_column].dtype == 'object':
            # Chuyển đổi chuỗi tiền tệ sang số
            df_copy[currency_column] = df_copy[currency_column].apply(parse_func)
        
        # Tính tổng theo tỉnh/thành
        sum_df = df_copy.groupby(province_column)[currency_column].sum().reset_index(name='value')
        return sum_df
    
    # Hàm hỗ trợ để lấy tiêu đề dựa vào loại dữ liệu
    def get_title_from_data_type(data_type, data_column):
        if data_type == 'violations':
            if data_column and 'MAVP' in data_column:
                return 'Phân tích Vi phạm Giao thông Theo Tỉnh/Thành'
            return 'Phân tích Vi phạm Giao thông Theo Tỉnh/Thành'
        elif data_type == 'accidents':
            return 'Phân tích Tai nạn Giao thông Theo Tỉnh/Thành'
        elif data_type == 'deaths':
            return 'Phân tích Số Người Tử Vong Theo Tỉnh/Thành'
        elif data_type == 'injuries':
            return 'Phân tích Số Người Bị Thương Theo Tỉnh/Thành'
        elif data_type == 'fines':
            return 'Phân tích Tổng Mức Phạt Theo Tỉnh/Thành'
        else:
            return 'Phân tích Dữ liệu Giao thông Theo Tỉnh/Thành'
    
    # Hàm tạo dữ liệu tổng hợp
    def create_summary_data(df):
        global global_summary
        
        # Tạo dictionary để lưu các thống kê tổng hợp
        summary = {}
        
        # Tính tổng số vi phạm (mỗi hàng là một vi phạm)
        summary['violations'] = len(df)
        
        # Tính tổng số tai nạn (mỗi MATN là một tai nạn độc nhất)
        if 'MATN' in df.columns:
            summary['accidents'] = df['MATN'].nunique()
        else:
            summary['accidents'] = 'N/A'
        
        # Tính tổng số người tử vong
        if 'TUVONG' in df.columns:
            df_copy = df.copy()
            df_copy['TUVONG'] = pd.to_numeric(df_copy['TUVONG'], errors='coerce')
            summary['deaths'] = df_copy['TUVONG'].sum()
        else:
            summary['deaths'] = 'N/A'
        
        # Tính tổng số người bị thương
        if 'BITHUONG' in df.columns:
            df_copy = df.copy()
            df_copy['BITHUONG'] = pd.to_numeric(df_copy['BITHUONG'], errors='coerce')
            summary['injuries'] = df_copy['BITHUONG'].sum()
        else:
            summary['injuries'] = 'N/A'
        
        # Tính tổng mức phạt
        if 'Tổng mức phạt' in df.columns:
            df_copy = df.copy()
            if df_copy['Tổng mức phạt'].dtype == 'object':
                # Nếu là chuỗi, chuyển đổi sang số
                df_copy['Tổng mức phạt'] = df_copy['Tổng mức phạt'].apply(parse_currency)
            summary['fines'] = df_copy['Tổng mức phạt'].sum()
        else:
            summary['fines'] = 'N/A'
        
        global_summary = summary
    
    # Callback cập nhật thẻ tổng quan
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
        
        # Xác định hàm định dạng dựa vào loại dữ liệu
        if data_type == 'fines':
            format_func = lambda x: f"{x:,} ₫"
        else:
            format_func = lambda x: f"{x:,}"
        
        # Tính toán các thống kê
        total = global_data['value'].sum()
        avg = round(global_data['value'].mean(), 1)
        max_value = global_data['value'].max()
        max_province = global_data.loc[global_data['value'].idxmax(), global_data.columns[0]]
        min_value = global_data['value'].min()
        min_province = global_data.loc[global_data['value'].idxmin(), global_data.columns[0]]
        
        return format_func(total), format_func(avg), format_func(max_value), max_province, format_func(min_value), min_province
    
    # Callback cập nhật thống kê tổng hợp
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
        
        # Lấy thống kê từ global_summary
        violations = global_summary.get('violations', 'N/A')
        accidents = global_summary.get('accidents', 'N/A')
        deaths = global_summary.get('deaths', 'N/A')
        injuries = global_summary.get('injuries', 'N/A')
        fines = global_summary.get('fines', 'N/A')
        
        # Định dạng các giá trị
        if violations != 'N/A':
            violations = f"{violations:,}"
        
        if accidents != 'N/A':
            accidents = f"{accidents:,}"
        
        if deaths != 'N/A':
            deaths = f"{deaths:,}"
        
        if injuries != 'N/A':
            injuries = f"{injuries:,}"
        
        if fines != 'N/A':
            fines = f"{fines:,} ₫"
        
        return violations, accidents, deaths, injuries, fines

    # Callback cập nhật bản đồ choropleth
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
            return "Bản đồ đã bị ẩn. Hãy chọn 'Hiển thị bản đồ' trong tùy chọn hiển thị để xem bản đồ."
        
        if global_data is None:
            return "Không có dữ liệu để hiển thị bản đồ."
        
        if global_geojson is None:
            return "Không có dữ liệu GeoJSON để hiển thị bản đồ."
        
        # Xác định tiêu đề và nhãn hover dựa vào loại dữ liệu
        if data_type == 'violations':
            title = 'Bản đồ Vi phạm Giao thông Theo Tỉnh/Thành'
            hover_label = 'Số vi phạm'
            hover_template = "<b>%{hovertext}</b><br>" + hover_label + ": %{customdata[0]:,.0f}<extra></extra>"
        elif data_type == 'accidents':
            title = 'Bản đồ Tai nạn Giao thông Theo Tỉnh/Thành'
            hover_label = 'Số tai nạn'
            hover_template = "<b>%{hovertext}</b><br>" + hover_label + ": %{customdata[0]:,.0f}<extra></extra>"
        elif data_type == 'deaths':
            title = 'Bản đồ Số Người Tử Vong Theo Tỉnh/Thành'
            hover_label = 'Số người tử vong'
            hover_template = "<b>%{hovertext}</b><br>" + hover_label + ": %{customdata[0]:,.0f}<extra></extra>"
        elif data_type == 'injuries':
            title = 'Bản đồ Số Người Bị Thương Theo Tỉnh/Thành'
            hover_label = 'Số người bị thương'
            hover_template = "<b>%{hovertext}</b><br>" + hover_label + ": %{customdata[0]:,.0f}<extra></extra>"
        elif data_type == 'fines':
            title = 'Bản đồ Tổng Mức Phạt Theo Tỉnh/Thành'
            hover_label = 'Tổng mức phạt'
            hover_template = "<b>%{hovertext}</b><br>" + hover_label + ": %{customdata[0]:,.0f} ₫<extra></extra>"
        else:
            title = 'Bản đồ Dữ liệu Giao thông Theo Tỉnh/Thành'
            hover_label = 'Giá trị'
            hover_template = "<b>%{hovertext}</b><br>" + hover_label + ": %{customdata[0]:,.0f}<extra></extra>"
        
        try:
            # Tạo choropleth mapbox
            fig = px.choropleth_mapbox(
                global_data,
                geojson=global_geojson,
                locations=global_data.columns[0],
                featureidkey="id",
                color='value',
                color_continuous_scale=color_scale,
                mapbox_style="carto-positron",
                zoom=4.5,  # Điều chỉnh mức zoom
                center={"lat": 16.0, "lon": 106.0},  # Điều chỉnh vị trí trung tâm
                opacity=0.7,
                labels={'value': hover_label},
                hover_name=global_data.columns[0],
                hover_data={'value': True}
            )
            
            # Tùy chỉnh hiển thị hover
            fig.update_traces(hovertemplate=hover_template)
            
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
        [Input('results-panel', 'className'),
         Input('display-options', 'value'),
         Input('data-type', 'value')]
    )
    def update_chart(results_panel_class, display_options, data_type):
        global global_data
        
        if results_panel_class == 'results-panel hidden':
            return ""
        
        if 'show_bar' not in display_options:
            return "Biểu đồ cột đã bị ẩn. Hãy chọn 'Hiển thị biểu đồ cột' trong tùy chọn hiển thị để xem biểu đồ."
        
        if global_data is None:
            return "Không có dữ liệu để hiển thị biểu đồ."
        
        # Xác định tiêu đề, nhãn Y và màu dựa vào loại dữ liệu
        if data_type == 'violations':
            title = 'Top 10 Tỉnh/Thành Có Số Vi phạm Giao thông Cao Nhất'
            y_label = 'Số vi phạm'
            bar_color = '#b91c1c'
            format_func = lambda x: f"{x:,.0f}"
        elif data_type == 'accidents':
            title = 'Top 10 Tỉnh/Thành Có Số Tai nạn Giao thông Cao Nhất'
            y_label = 'Số tai nạn'
            bar_color = '#1d4ed8'
            format_func = lambda x: f"{x:,.0f}"
        elif data_type == 'deaths':
            title = 'Top 10 Tỉnh/Thành Có Số Người Tử Vong Cao Nhất'
            y_label = 'Số người tử vong'
            bar_color = '#b91c1c'
            format_func = lambda x: f"{x:,.0f}"
        elif data_type == 'injuries':
            title = 'Top 10 Tỉnh/Thành Có Số Người Bị Thương Cao Nhất'
            y_label = 'Số người bị thương'
            bar_color = '#ca8a04'
            format_func = lambda x: f"{x:,.0f}"
        elif data_type == 'fines':
            title = 'Top 10 Tỉnh/Thành Có Tổng Mức Phạt Cao Nhất'
            y_label = 'Tổng mức phạt (₫)'
            bar_color = '#059669'
            format_func = lambda x: f"{x:,.0f} ₫"
        else:
            title = 'Top 10 Tỉnh/Thành Có Giá Trị Cao Nhất'
            y_label = 'Giá trị'
            bar_color = '#3b82f6'
            format_func = lambda x: f"{x:,.0f}"
        
        try:
            # Lấy top 10 tỉnh/thành có giá trị cao nhất
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
        [Input('results-panel', 'className'),
         Input('display-options', 'value'),
         Input('data-type', 'value')]
    )
    def update_table(results_panel_class, display_options, data_type):
        global global_data
        
        if results_panel_class == 'results-panel hidden':
            return ""
        
        if 'show_table' not in display_options:
            return "Bảng dữ liệu đã bị ẩn. Hãy chọn 'Hiển thị bảng dữ liệu' trong tùy chọn hiển thị để xem bảng."
        
        if global_data is None:
            return "Không có dữ liệu để hiển thị bảng."
        
        # Xác định tiêu đề và tên cột value dựa vào loại dữ liệu
        if data_type == 'violations':
            title = 'Dữ liệu chi tiết: Vi phạm giao thông theo tỉnh/thành'
            value_column = 'Số vi phạm'
            formatter = None
        elif data_type == 'accidents':
            title = 'Dữ liệu chi tiết: Tai nạn giao thông theo tỉnh/thành'
            value_column = 'Số tai nạn'
            formatter = None
        elif data_type == 'deaths':
            title = 'Dữ liệu chi tiết: Số người tử vong theo tỉnh/thành'
            value_column = 'Số người tử vong'
            formatter = None
        elif data_type == 'injuries':
            title = 'Dữ liệu chi tiết: Số người bị thương theo tỉnh/thành'
            value_column = 'Số người bị thương'
            formatter = None
        elif data_type == 'fines':
            title = 'Dữ liệu chi tiết: Tổng mức phạt theo tỉnh/thành'
            value_column = 'Tổng mức phạt (₫)'
            formatter = lambda x: f"{x:,.0f} ₫"
        else:
            title = 'Dữ liệu chi tiết theo tỉnh/thành'
            value_column = 'Giá trị'
            formatter = None
        
        try:
            # Sắp xếp dữ liệu theo giá trị giảm dần
            sorted_data = global_data.sort_values('value', ascending=False).copy()
            
            # Định dạng giá trị tiền tệ nếu cần
            if formatter:
                sorted_data['value'] = sorted_data['value'].apply(formatter)
            
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