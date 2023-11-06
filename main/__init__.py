from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
# # from config import config

app = Flask(__name__)

# @app.after_request
# def after_request(response):
#     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
#     response.headers['Access-Control-Allow-Credentials'] = 'True'  # hỗ trợ thông tin xác thực (credentials)
#     return response

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:001122@localhost/manager_book_room'
app.config['JWT_SECRET_KEY'] = '001122' 
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
jwt = JWTManager(app)
login_manager = LoginManager()
login_manager.init_app(app)
CORS(app,origins="http://localhost:3000")

from main import controller, model