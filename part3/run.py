import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
