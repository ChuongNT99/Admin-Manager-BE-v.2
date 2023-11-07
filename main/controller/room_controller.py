from main import app, db
from main.model import Booking, Employee, Room, BookingEmployee
from flask import jsonify, request
from datetime import datetime
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt


@app.route("/rooms", methods=["GET"])
@jwt_required()
def get_rooms():
    current_user = get_jwt_identity()
    claims = get_jwt()
    role = claims['role']
    if current_user:
        if role:
            rooms = Room.query.all()

            for room in rooms:
                current_time = datetime.now()
                current_bookings = Booking.query.filter(
                    Booking.room_id == room.room_id,
                    Booking.time_start <= current_time,
                    Booking.time_end >= current_time
                ).all()

                if current_bookings:
                    room.status = True
                else:
                    room.status = False

            db.session.commit()
            return jsonify({"rooms": [room.serialize() for room in rooms]})
        else:
            return jsonify({"error": "Internal Server Error"}), 500
    return jsonify({"error": "You are not logged in"})


@app.route("/rooms", methods=["POST"])
@jwt_required()
def create_room():
    current_user = get_jwt_identity()
    claims = get_jwt()
    role = claims['role']
    if current_user:
        if role:
            data = request.get_json()
            room_name = data.get("room_name")
            status = data.get("status", 0)

            existing_room = Room.query.filter_by(room_name=room_name).first()
            if existing_room:
                return jsonify({"error": "Room already exists"}), 400

            new_room = Room(room_name=room_name, status=status)
            db.session.add(new_room)
            db.session.commit()

            return jsonify({"message": "Room created successfully"})
        else:
            return jsonify({"error": "Permission denied"}), 403
    return jsonify({"error": "You are not logged in"})


@app.route("/rooms/<int:room_id>", methods=["PUT"])
@jwt_required()
def update_room(room_id):
    current_user = get_jwt_identity()
    claims = get_jwt()
    role = claims['role']
    if current_user:
        if role:
            data = request.get_json()
            room_name = data.get("room_name")

            existing_room = Room.query.filter(
                Room.room_id != room_id, Room.room_name == room_name).first()
            if existing_room:
                return jsonify({"error": "Room name already exists"}), 400

            room_to_update = Room.query.get(room_id)

            if room_to_update:
                room_to_update.room_name = room_name
                db.session.commit()
                return jsonify({"message": "Room updated successfully"})
            else:
                return jsonify({"error": "Room not found"}), 404
        else:
            return jsonify({"error": "Permission denied"}), 403
    return jsonify({"error": "You are not logged in"})


@app.route("/rooms/<int:room_id>", methods=["DELETE"])
@jwt_required()
def delete_room(room_id):
    current_user = get_jwt_identity()
    claims = get_jwt()
    role = claims['role']
    if current_user:
        if role:
            room_to_delete = Room.query.get(room_id)

            if room_to_delete:
                db.session.delete(room_to_delete)
                db.session.commit()
                return jsonify({"message": "Room deleted successfully"})
            else:
                return jsonify({"error": "Room not found"}), 404
        else:
            return jsonify({"error": "Permission denied"}), 403
    return jsonify({"error": "You are not logged in"})
