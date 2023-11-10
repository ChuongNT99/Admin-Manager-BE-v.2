from main import app
from main.model import Room, Booking, Employee
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_jwt_extended import jwt_required
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_testing import TestCase
import logging
import json


class TestLoginAPI(TestCase):
    def create_app(self):

        return app

    def setUp(self):
        self.app = app.test_client()
        self.engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        with app.app_context():
            self.session.begin()

    def tearDown(self):
        with app.app_context():
            self.session.rollback()
            self.session.close()
            self.engine.dispose()

    def test_login_valid_credentials(self):
        valid_credentials = {
            "email": "admin@gmail.com",
            "password": "admin"
        }

        response = self.app.post(
            '/login', data=json.dumps(valid_credentials), content_type='application/json')

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Logged in successfully')

        self.assertIn('access_token', data)

    def test_login_missing_credentials(self):
        missing_credentials = {
            "email": "admin@gmail.com",
            "password": ""
        }

        response = self.app.post(
            '/login', data=json.dumps(missing_credentials), content_type='application/json')

        self.assertEqual(response.status_code, 400)

        data = json.loads(response.data)
        self.assertEqual(
            data['message'], 'Bad request, missing email or password')

    def test_login_invalid_credentials(self):
        invalid_credentials = {
            "email": "admin@gmail.com",
            "password": "12346"
        }

        response = self.app.post(
            '/login', data=json.dumps(invalid_credentials), content_type='application/json')

        self.assertEqual(response.status_code, 401)

        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Email or password is incorrect')
