# Import tất cả từ app.py
from app import app

# Chạy ứng dụng nếu file này được thực thi trực tiếp
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)