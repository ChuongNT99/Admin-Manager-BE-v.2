from flask import Flask, Blueprint,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)

# Cấu hình SQLAlchemy kết nối đến MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:001122@localhost/manager_book_room'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from model.models import *

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)