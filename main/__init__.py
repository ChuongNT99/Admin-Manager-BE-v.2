import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)

env =  os.environ['FLASK_ENV']
print (env)
if env == 'production':
    app.config.from_object('config.ProductionConfig')
    print("Ứng dụng đang chạy trong môi trường production")
elif env == 'development':
    app.config.from_object('config.DevelopmentConfig')
    print("Ứng dụng đang chạy trong môi trường development")
else:
    app.config.from_object('config.Config')
    print("Ứng dụng đang chạy trong môi trường khác")

print(f"DEBUG: {app.config['DEBUG']}")
print(f"SECRET_KEY: {app.config['SECRET_KEY']}")

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

db = SQLAlchemy(app)
migrate = Migrate(app, db)

jwt = JWTManager(app)


from main import controller, model