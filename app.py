from main import app
from waitress import serve

if __name__ == "__main":
    serve(app, host='0.0.0.0', port=5000, threads=4)
