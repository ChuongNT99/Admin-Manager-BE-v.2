from main import app
from main.model import Room, Booking
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_jwt_extended import jwt_required
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_testing import TestCase
import logging


class TestRoomController(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        self.app = app.test_client()
        self.engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()
        self.engine.dispose()

    def create_sample_data(self):
        room1 = Room(room_name="CAU TIEN", status=True)
        room2 = Room(room_name="SANG TAO", status=False)

        current_time = datetime.now()
        booking1 = Booking(
            room_id=room1.room_id,
            time_start=current_time,
            time_end=current_time + timedelta(hours=1)
        )
        booking2 = Booking(
            room_id=room2.room_id,
            time_start=current_time - timedelta(hours=1),
            time_end=current_time + timedelta(hours=2)
        )

        self.session.add(room1)
        self.session.add(room2)
        self.session.add(booking1)
        self.session.add(booking2)
        self.session.commit()

    def test_get_rooms_as_admin(self):
        self.create_sample_data()
        admin_token = self.create_jwt_token(employee_id=1, role=True)

        response = self.client.get(
            "/rooms", headers={"Authorization": f"Bearer {admin_token}"})

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("rooms", data)
        rooms = data["rooms"]
        self.assertEqual(len(rooms), 2)

        self.assertEqual(rooms[0]["room_name"], "CAU TIEN")
        self.assertTrue(rooms[0]["status"])
        self.assertEqual(rooms[1]["room_name"], "SANG TAO")
        self.assertFalse(rooms[1]["status"])


if __name__ == '__main__':
    import unittest
    unittest.main()
