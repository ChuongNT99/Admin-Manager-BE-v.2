from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate

# # from config import config

app = Flask(__name__)
# app.config.from_object('config.Config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:001122@localhost/manager_book_room'
app.config['JWT_SECRET_KEY'] = '001122' 
db = SQLAlchemy(app)
migrate = Migrate(app, db)

jwt = JWTManager(app)
login_manager = LoginManager()
login_manager.init_app(app)

from main import controller, model