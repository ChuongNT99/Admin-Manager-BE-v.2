from main import app, db
from main.model import Booking, Employee, Room, BookingEmployee
from flask import Blueprint, jsonify, request
from datetime import datetime
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_login import login_required
from sqlalchemy.exc import IntegrityError


@app.route("/bookings", methods=["GET"])
@jwt_required()
def get_bookings():
    current_user = get_jwt_identity()
    if current_user == 1:
        try:
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


@app.route("/bookings", methods=["POST"])
@jwt_required()
def book_room():
    current_user = get_jwt_identity()
    if current_user == 1:
        data = request.get_json()
        room_id = data.get('room_id')
        time_start = data.get('time_start')
        time_end = data.get('time_end')
        employee_ids = data.get('employee_id')

        if time_start == time_end:
            return jsonify({'error': 'Invalid time input'}), 400

        if time_start is not None and time_end is not None and time_start < time_end:
            existing_booking = Booking.query.filter(
                Booking.room_id == room_id,
                Booking.time_end >= time_start,
                Booking.time_start <= time_end
            ).first()

            if existing_booking:
                return jsonify({'error': 'Room is already booked for this time'}), 400

            try:
                new_booking = Booking(
                    room_id=room_id, time_start=time_start, time_end=time_end)
                db.session.add(new_booking)
                db.session.commit()

                for employee_id in employee_ids:
                    employee_booking = BookingEmployee(
                        employee_id=employee_id, booking_id=new_booking.booking_id)
                    db.session.add(employee_booking)

                db.session.commit()
                return jsonify({'message': 'Booking created successfully'})
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': 'Internal Server Error'}), 500
        else:
            return jsonify({'error': 'Invalid time input'}), 400
    else:
        return jsonify({'error': 'Permission denied'}), 403


@app.route("/bookings/<int:booking_id>", methods=["PUT"])
@jwt_required()
def update_booking(booking_id):
    current_user = get_jwt_identity()
    if current_user == 1:
        data = request.get_json()
        room_id = data.get('room_id')
        time_start = data.get('time_start')
        time_end = data.get('time_end')
        employee_ids = data.get('employee_id')

        if time_start is not None and time_end is not None and employee_ids is not None:
            if time_start <= time_end:
                return jsonify({'error': 'invalid time input '}), 400
            existing_booking = Booking.query.filter(
                Booking.room_id == room_id,
                Booking.time_end >= time_start,
                Booking.time_start <= time_end
            ).first()

            if existing_booking and existing_booking.booking_id != booking_id:
                return jsonify({'error': 'Room is already booked for this time'}), 400

            try:
                booking = Booking.query.get(booking_id)

                if booking is None:
                    return jsonify({'error': 'Booking not found'}), 404

                booking.room_id = room_id
                booking.time_start = time_start
                booking.time_end = time_end

                # Xóa tất cả các nhân viên từ cuộc họp
                for employee_booking in booking.booking_employees:
                    db.session.delete(employee_booking)

                # Thêm danh sách các nhân viên vào cuộc họp
                for employee_id in employee_ids:
                    employee_booking = BookingEmployee(
                        employee_id=employee_id, booking_id=booking.booking_id)
                    db.session.add(employee_booking)

                db.session.commit()
                return jsonify({'message': 'Booking updated successfully'})
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': 'Internal Server Error'}), 500
        else:
            return jsonify({'error': 'Invalid time input'}), 400
    else:
        return jsonify({'error': 'Permission denied'}), 403


@app.route("/bookings/<int:booking_id>", methods=["DELETE"])
@jwt_required()
def delete_booking(booking_id):
    current_user = get_jwt_identity()

    if current_user == 1:
        try:
            booking = Booking.query.get(booking_id)
            if booking:
                BookingEmployee.query.filter_by(
                    booking_id=booking.booking_id).delete()
                db.session.delete(booking)
                db.session.commit()
                return jsonify({'message': 'Booking deleted successfully'})
            else:
                return jsonify({'error': 'Booking not found'}), 404
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': 'IntegrityError: Cannot delete the booking, it might be in use'}), 500
    else:
        return jsonify({'error': 'Permission denied'}), 403
