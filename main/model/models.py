from main.model import db
from flask_login import UserMixin
import bcrypt


class RevokedToken(db.Model):
    __tablename__ = "revoked_tokens"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36))
    
class Employee(db.Model,UserMixin):
    __tablename__ = "employees"
    employee_id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    booking_employees = db.relationship('BookingEmployee', backref='employees')

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def __init__(self, employee_name, email, phone_number, password, admin=False):
        self.employee_name = employee_name
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.admin = admin
    def serialize(self):
        return {
            'employee_id': self.employee_id,
            'employee_name': self.employee_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'role': self.admin
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


class BookingEmployee(db.Model):
    __tablename__ = "booking_employees"
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))


if __name__ == '__main__':
    db.create_all()
