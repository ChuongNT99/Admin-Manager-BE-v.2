import unittest
from main import app, db
from main.model import Room, Booking
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_jwt_extended import jwt_required


class TestRoomController(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        self.create_sample_data()

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

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

        db.session.add(room1)
        db.session.add(room2)
        db.session.add(booking1)
        db.session.add(booking2)
        db.session.commit()

    def create_jwt_token(self, user_id, role):
        expires = timedelta(days=1)
        token_data = {
            "user_id": user_id,
            "role": role,
        }
        return create_access_token(identity=token_data, expires_delta=expires)

    def test_get_rooms_as_admin(self):
        admin_token = self.create_jwt_token(user_id=1, role=True)
        response = self.app.get(
            "/rooms", headers={"Authorization": f"Bearer {admin_token}"})

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("rooms", data)
        rooms = data["rooms"]
        self.assertEqual(len(rooms), 2)
        self.assertEqual(rooms[0]["room_name"], "CAU TIEN")
        self.assertEqual(rooms[1]["room_name"], "SANG TAO")


if __name__ == '__main__':
    unittest.main()
