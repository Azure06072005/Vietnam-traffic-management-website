from dash import dcc, html
import dash
from flask import send_from_directory
import os

def register_routes(app):
    """Register routes for static HTML files in the ho_tro directory"""
    
    @app.server.route('/ho_tro/dieu_khoan.html')
    def serve_terms():
        return send_from_directory('ho_tro', 'dieu_khoan.html')
    
    @app.server.route('/ho_tro/huong_dan_su_dung.html')
    def serve_guide():
        return send_from_directory('ho_tro', 'huong_dan_su_dung.html')
    
    @app.server.route('/ho_tro/thong_bao.html')
    def serve_notifications():
        return send_from_directory('ho_tro', 'thong_bao.html')
    
    # A more generic route for any file in the ho_tro directory
    @app.server.route('/ho_tro/<path:filename>')
    def serve_support_file(filename):
        return send_from_directory('ho_tro', filename)