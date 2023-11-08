from main import app, db
from main.model import Booking, Employee, Room, BookingEmployee
from flask import jsonify, request
from datetime import datetime
from flask_jwt_extended import JWTManager, jwt_required
from main.controller.has_permission import has_permission


@app.route("/rooms", methods=["GET"])
@jwt_required()
@has_permission("admin")
def get_rooms():
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


@app.route("/rooms", methods=["POST"])
@jwt_required()
@has_permission("admin")
def create_room():
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


@app.route("/rooms/<int:room_id>", methods=["PUT"])
@jwt_required()
@has_permission("admin")
def update_room(room_id):
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


@app.route("/rooms/<int:room_id>", methods=["DELETE"])
@jwt_required()
@has_permission("admin")
def delete_room(room_id):
    room_to_delete = Room.query.get(room_id)

    if room_to_delete:
        if room_to_delete.status == 1:
            return jsonify({"error": "Cannot delete a busy room"}), 400

        bookings_to_delete = Booking.query.filter_by(room_id=room_id).all()

        for booking in bookings_to_delete:
            db.session.delete(booking)

        db.session.delete(room_to_delete)
        db.session.commit()

        return jsonify({"message": "Room and associated bookings deleted successfully"})
    else:
        return jsonify({"error": "Room not found"}), 404
