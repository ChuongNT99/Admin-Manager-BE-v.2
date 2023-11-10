from main.model import db
from flask_login import UserMixin
import bcrypt

class Employee(db.Model, UserMixin):
    __tablename__ = "employees"
    employee_id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(11), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Boolean, nullable=False, default=False)
    booking_employees = db.relationship('BookingEmployee', backref='employees')

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def serialize(self):
        return {
            'employee_id': self.employee_id,
            'employee_name': self.employee_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'role': self.role
        }


class Room(db.Model):
    __tablename__ = "rooms"
    room_id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    bookings = db.relationship('Booking', backref='rooms', lazy=True)

    def serialize(self):
        return {
            'room_id': self.room_id,
            'room_name': self.room_name,
            'status': self.status,
        }


class Booking(db.Model):
    __tablename__ = "bookings"
    booking_id = db.Column(db.Integer, primary_key=True)
    time_start = db.Column(db.TIMESTAMP, nullable=False)
    time_end = db.Column(db.TIMESTAMP, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.room_id'))
    booking_employees = db.relationship('BookingEmployee', backref='bookings')

    def serialize(self):
        return {
            'booking_id': self.booking_id,
            'time_start': self.time_start.strftime('%Y-%m-%d %H:%M:%S'),
            'time_end': self.time_end.strftime('%Y-%m-%d %H:%M:%S'),
            'room_id': self.room_id,
            'booking_employees': [be.serialize() for be in self.booking_employees]
        }


class BookingEmployee(db.Model):
    __tablename__ = "booking_employees"
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))

    def serialize(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'employee_id': self.employee_id
        }


if __name__ == '__main__':
    db.create_all()
