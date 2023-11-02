from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from db_config import db_config
import mysql.connector
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

app = Flask(__name__)

room_api = Blueprint("manage_room_api", __name__)


def create_db_connection():
    return mysql.connector.connect(**db_config)


@room_api.route("/rooms", methods=["GET"])
@jwt_required()
def get_rooms():
    current_user = get_jwt_identity()

    if current_user.get("admin") == 1:
        try:
            conn = create_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM room_meeting")
            rooms = cursor.fetchall()
            current_time = datetime.now()

            for room in rooms:
                room_id = room['room_id']

                # Check if there are any reservations for this room and if the current time is within that range
                cursor.execute(
                    "SELECT booking_id, time_start, time_end FROM booking WHERE room_id = %s AND %s BETWEEN time_start AND time_end",
                    (room_id, current_time)
                )
                booking_info = cursor.fetchone()

                if booking_info:
                    # The room's status is now 1 (busy)
                    cursor.execute(
                        "UPDATE room_meeting SET status = 1 WHERE room_id = %s", (room_id,))
                    conn.commit()
                else:
                    # Empty room
                    cursor.execute(
                        "UPDATE room_meeting SET status = 0 WHERE room_id = %s", (room_id,))
                    conn.commit()

            return jsonify({"rooms": rooms})
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Permission denied"}), 403


@room_api.route("/rooms", methods=["POST"])
@jwt_required()
def create_room():
    current_user = get_jwt_identity()

    if current_user.get("admin") == 1:
        data = request.get_json()
        room_name = data.get("room_name")
        status = data.get("status", 0)

        conn = create_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT room_name FROM room_meeting WHERE room_name = %s", (
                room_name,)
        )
        existing_room = cursor.fetchone()

        if existing_room:
            return jsonify({"error": "Room already exists"}), 400

        cursor.execute(
            "INSERT INTO room_meeting (room_name, status) VALUES (%s, %s)",
            (room_name, status),
        )
        conn.commit()
        return jsonify({"message": "Room created successfully"})
    else:
        return jsonify({"error": "Permission denied"}), 403


@room_api.route("/rooms/<int:room_id>", methods=["PUT"])
@jwt_required()
def update_room(room_id):
    current_user = get_jwt_identity()

    if current_user.get("admin") == 1:
        try:
            data = request.get_json()
            room_name = data.get("room_name")

            conn = create_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT room_name FROM room_meeting WHERE room_id != %s AND room_name = %s",
                (room_id, room_name),
            )
            existing_room = cursor.fetchone()

            if existing_room:
                return jsonify({"error": "Room name already exists"}), 400

            cursor.execute(
                "UPDATE room_meeting SET room_name=%s WHERE room_id=%s",
                (room_name, room_id),
            )
            conn.commit()
            return jsonify({"message": "Room updated successfully"})
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Permission denied"}), 403


@room_api.route("/rooms/<int:room_id>", methods=["DELETE"])
@jwt_required()
def delete_room(room_id):
    current_user = get_jwt_identity()

    if current_user.get("admin") == 1:
        try:
            conn = create_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM room_meeting WHERE room_id=%s", (room_id,))
            conn.commit()
            return jsonify({"message": "Room deleted successfully"})
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Permission denied"}), 403


@room_api.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found"}), 404


@room_api.route('/admin', methods=['GET'])
@jwt_required()
def admin_route():
    current_user = get_jwt_identity()
    if current_user.get("admin") == 1:
        return jsonify(message="This is an admin-only route")
    return jsonify(message="Permission denied"), 403
