# Import everything from app.py
from app import app

# Run the application if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)