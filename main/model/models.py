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
    bookings = db.relationship('BookingEmployee', backref='employees')
    def set_password(self, password):
            self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Room(db.Model):
    __tablename__ = "rooms"
    room_id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    bookings = db.relationship('Booking', backref='rooms', lazy=True)

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