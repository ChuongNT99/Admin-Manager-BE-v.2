from main import app
from main.model import Room
from flask import Blueprint, jsonify, request
from datetime import datetime
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity


@app.route("/employees", methods=["GET"])
@jwt_required()
def get_employees():
    current_user = get_jwt_identity()
    if current_user == 1:
        employees = Employee.query.all()
        return jsonify({"employees": [employee.serialize() for employee in employees]})
    else:
        return jsonify({"error": "Permission denied"}), 403


@app.route("/bookings", methods=["POST"])
@jwt_required()
def book_room():
    current_user = get_jwt_identity()
    if current_user == 1:
        data = request.get_json()
        room_id = data.get('room_id')
        time_start = data.get('time_start_booking')
        time_end = data.get('time_end_booking')
        employee_id = data.get('employee_id')

        # Kiểm tra xem thời gian mới có nằm trong khoảng thời gian đã đặt trước đó không
        existing_booking = Booking.query.filter(
            Booking.room_id == room_id,
            Booking.time_end >= time_start,
            Booking.time_start <= time_end
        ).first()

        if existing_booking:
            return jsonify({'error': 'Room is already booked for this time'}), 400

        try:
            # Tiếp tục thêm thông tin đặt phòng
            new_booking = Booking(
                room_id=room_id, time_start=time_start, time_end=time_end)
            employee_booking = BookingEmployee(
                employee_id=employee_id, booking=new_booking)

            db.session.add(new_booking)
            db.session.add(employee_booking)
            db.session.commit()

            return jsonify({'message': 'Booking created successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify({'error': 'Permission denied'}), 403


@app.route("/bookings", methods=["GET"])
@jwt_required()
def get_bookings():
    current_user = get_jwt_identity()
    if current_user == 1:
        try:
            # Sử dụng SQLAlchemy để thực hiện truy vấn cơ sở dữ liệu
            bookings = Booking.query.join(Room).join(BookingEmployee).join(Employee).with_entities(
                Booking.booking_id,
                Booking.room_id,
                Booking.time_start,
                Booking.time_end,
                Room.room_name,
                Employee.employee_name
            ).all()

            return jsonify({'bookings': [booking._asdict() for booking in bookings]})
        except Exception as e:
            return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify({'error': 'Permission denied'}), 403


@app.route("/bookings/<int:booking_id>", methods=["DELETE"])
@jwt_required()
def delete_booking(booking_id):
    current_user = get_jwt_identity()
    if current_user.get == 1:
        try:
            booking = Booking.query.get(booking_id)

            if booking:
                booking.delete()  # Xóa đặt phòng

                return jsonify({'message': 'Booking deleted successfully'})
            else:
                return jsonify({'error': 'Booking not found'}), 404
        except IntegrityError as e:
            # Xử lý lỗi nếu có
            return jsonify({'error': 'Integrity Error'}), 500
    else:
        return jsonify({'error': 'Permission denied'}), 403
