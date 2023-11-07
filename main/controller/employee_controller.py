from main import app, db
from main.model import Employee, Booking, Room, BookingEmployee
from flask import jsonify, request
from flask_jwt_extended import JWTManager, jwt_required
from main.controller.has_permission import has_permission


@app.route('/employees', methods=['POST'])
@jwt_required()
@has_permission("admin")
def create_employee():
    data = request.get_json()
    employee_name = data.get('employee_name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')
    role = data.get('role', False)

    existing_employee = Employee.query.filter_by(email=email).first()
    if existing_employee:
        return jsonify({'error': 'Email existing'}), 400

    existing_phone = Employee.query.filter_by(
        phone_number=phone_number).first()
    if existing_phone:
        return jsonify({'error': 'Phone number existing'}), 400

    new_employee = Employee(employee_name=employee_name, email=email,
                            phone_number=phone_number, password=password, role=role)
    new_employee.set_password(password)
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Created employee successfully'})


@app.route('/employees', methods=['GET'])
@jwt_required()
@has_permission("admin")
def get_employees():
    employees = Employee.query.filter_by(role=False).all()
    employee_list = [employee.serialize() for employee in employees]
    return jsonify({'employees': employee_list})


@app.route('/employees/<int:employee_id>', methods=['GET'])
@jwt_required()
@has_permission("admin")
def get_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if employee is None:
        return jsonify({'message': 'Employee is None'}), 404
    return jsonify(employee.serialize())


@app.route('/employees/<int:employee_id>', methods=['PUT'])
@jwt_required()
@has_permission("admin")
def update_employee(employee_id):
    data = request.get_json()
    employee = Employee.query.get(employee_id)

    if not employee:
        return jsonify({'message': 'Employee is None'}), 404

    if 'employee_name' in data:
        employee.employee_name = data['employee_name']
    if 'email' in data:
        existing_employee = Employee.query.filter(
            Employee.employee_id != employee_id, Employee.email == data['email']).first()
        if existing_employee:
            return jsonify({'message': 'Email existing'}), 400
        employee.email = data['email']
    if 'phone_number' in data:
        existing_employee = Employee.query.filter(
            Employee.employee_id != employee_id, Employee.phone_number == data['phone_number']).first()
        if existing_employee:
            return jsonify({'message': 'Phone number existing'}), 400
        employee.phone_number = data['phone_number']
    if 'password' in data:
        employee.set_password(data['password'])

    db.session.commit()
    return jsonify({'message': 'Update employee successfully'}), 200


@app.route('/employees/<int:employee_id>', methods=['DELETE'])
@jwt_required()
@has_permission("admin")
def delete_employee(employee_id):
    employee = Employee.query.get(employee_id)

    if not employee:
        return jsonify({'message': 'Employee is None'}), 404

    booking_employees = BookingEmployee.query.filter_by(
        employee_id=employee_id).all()
    for booking_employee in booking_employees:
        db.session.delete(booking_employee)

    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Delete employee successfully'}), 200

