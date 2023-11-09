from main import controller, model
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from config import load_config

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
mode = 'PRODUCTION'

config = load_config(mode)

app.config.from_object(config)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

db = SQLAlchemy(app)
migrate = Migrate(app, db)

jwt = JWTManager(app)
