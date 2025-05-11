from dash import dcc, html
import dash 
import flask import send_from_directory
import os

def register_routes(app): 
    @app.server.route('/ho-tro/dieu_khoan.html')
    @app.server.route('/ho-tro/huong_dan_su_dung.html')
    @app.server.route('ho-tro/thong_bao.html')
    def serve_support_files(dieu_khoan.html):
        return send_from_directory('ho-tro', dieu_khoan.html)
    def serve_support_files(huong_dan_su_dung.html):
        return send_from_directory('ho-tro', huong_dan_su_dung.html)
    def serve_support_files(thong_bao.html):
        return send_from_directory('ho-tro', thong_bao.html)