from main import app, db
from main.model import Booking, Employee, Room, BookingEmployee
from flask import Blueprint, jsonify, request
from datetime import datetime
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_login import login_required


@app.route("/rooms", methods=["GET"])
@jwt_required()
def get_rooms():
    current_user = get_jwt_identity()
    if current_user == 1:
        rooms = Room.query.all()
        return jsonify({"rooms": [room.serialize() for room in rooms]})
    else:
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/update_room_status", methods=["GET"])
def update_room_status():
    current_time = datetime.now()
    rooms = Room.query.all()

    for room in rooms:
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
def create_room():
    current_user = get_jwt_identity()

    if current_user == 1:
        data = request.get_json()
        room_name = data.get("room_name")
        status = data.get("status", 0)

        # Thực hiện kiểm tra xem room_name đã tồn tại trong CSDL chưa
        existing_room = Room.query.filter_by(room_name=room_name).first()
        if existing_room:
            return jsonify({"error": "Room already exists"}), 400

        # Tạo phòng mới và lưu vào CSDL
        new_room = Room(room_name=room_name, status=status)
        db.session.add(new_room)
        db.session.commit()

        return jsonify({"message": "Room created successfully"})
    else:
        return jsonify({"error": "Permission denied"}), 403


@app.route("/rooms/<int:room_id>", methods=["PUT"])
@jwt_required()
def update_room(room_id):
    current_user = get_jwt_identity()

    if current_user == 1:
        data = request.get_json()
        room_name = data.get("room_name")

        # Kiểm tra xem room_name đã tồn tại trong CSDL cho một phòng khác
        existing_room = Room.query.filter(
            Room.room_id != room_id, Room.room_name == room_name).first()
        if existing_room:
            return jsonify({"error": "Room name already exists"}), 400

        # Tìm phòng cần cập nhật theo room_id
        room_to_update = Room.query.get(room_id)

        if room_to_update:
            # Cập nhật thông tin phòng và lưu vào CSDL
            room_to_update.room_name = room_name
            db.session.commit()
            return jsonify({"message": "Room updated successfully"})
        else:
            return jsonify({"error": "Room not found"}), 404
    else:
        return jsonify({"error": "Permission denied"}), 403


@app.route("/rooms/<int:room_id>", methods=["DELETE"])
@jwt_required()
def delete_room(room_id):
    current_user = get_jwt_identity()

    if current_user == 1:
        # Tìm phòng cần xóa theo room_id
        room_to_delete = Room.query.get(room_id)

        if room_to_delete:
            # Xóa phòng khỏi CSDL và lưu thay đổi
            db.session.delete(room_to_delete)
            db.session.commit()
            return jsonify({"message": "Room deleted successfully"})
        else:
            return jsonify({"error": "Room not found"}), 404
    else:
        return jsonify({"error": "Permission denied"}), 403
