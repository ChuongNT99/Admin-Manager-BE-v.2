from main import app,db, login_manager
from main.model import Employee, Booking, Room, BookingEmployee
from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_login import login_required


@login_manager.user_loader
def load_user(employee_id):
    return Employee.query.get(int(employee_id))

@app.route('/employees', methods=['POST'])
@jwt_required()
def create_employee():
    current_user = get_jwt_identity()
    claims = get_jwt()
    role = claims['role']
    if current_user:
        if role:
            data = request.get_json()
            employee_name = data.get('employee_name')
            email = data.get('email')
            phone_number = data.get('phone_number')
            password = data.get('password')
            role = data.get('role', False)

            # Kiểm tra email và số điện thoại không trùng lặp
            existing_employee = Employee.query.filter_by(email=email).first()
            if existing_employee:
                return jsonify({'error': 'Email existing'}), 400

            existing_phone = Employee.query.filter_by(phone_number=phone_number).first()
            if existing_phone:
                return jsonify({'error': 'Phone number existing'}), 400

            # Mã hóa mật khẩu
            new_employee = Employee(employee_name=employee_name, email=email, phone_number=phone_number, password=password , role=role)
            new_employee.set_password(password)
            db.session.add(new_employee)
            db.session.commit()
            return jsonify({'message': 'Created employee successfully'})
        return jsonify({"error": "Permission denied"}), 403
    return jsonify({"error": "You are not logged in"})
        
# Đọc danh sách nhân viên
@app.route('/employees', methods=['GET'])
@jwt_required()
def get_employees():
    current_user = get_jwt_identity()
    claims = get_jwt()
    role = claims['role']
    if current_user:
        if role:
            employees = Employee.query.filter_by(role=False).all()
            employee_list = [employee.serialize() for employee in employees]
            return jsonify({'employees': employee_list})
        return jsonify({"error": "Permission denied"}), 403
    return jsonify({"error": "You are not logged in"})

# Đọc thông tin nhân viên theo ID
@app.route('/employees/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_employee(employee_id):
    current_user = get_jwt_identity()
    claims = get_jwt()
    role = claims['role']
    if current_user:
        if role:
            employee = Employee.query.get(employee_id)
            if employee is None:
                return jsonify({'message': 'Employee is None'}), 404
            return jsonify(employee.serialize())
        return jsonify({"error": "Permission denied"}), 403
    return jsonify({"error": "You are not logged in"})

# Cập nhật thông tin nhân viên theo ID
@app.route('/employees/<int:employee_id>', methods=['PUT'])
@jwt_required()
def update_employee(employee_id):
    current_user = get_jwt_identity()
    claims = get_jwt()
    role = claims['role']
    if current_user:
        if role:
            data = request.get_json()
            employee = Employee.query.get(employee_id)

            if not employee:
                return jsonify({'message': 'Employee is None'}), 404

            if 'employee_name' in data:
                employee.employee_name = data['employee_name']
            if 'email' in data:
                # Kiểm tra email không trùng lặp
                existing_employee = Employee.query.filter(Employee.employee_id != employee_id, Employee.email == data['email']).first()
                if existing_employee:
                    return jsonify({'message': 'Email existing'}), 400
                employee.email = data['email']
            if 'phone_number' in data:
                # Kiểm tra số điện thoại không trùng lặp
                existing_employee = Employee.query.filter(Employee.employee_id != employee_id, Employee.phone_number == data['phone_number']).first()
                if existing_employee:
                    return jsonify({'message': 'Phone number existing'}), 400
                employee.phone_number = data['phone_number']
            if 'password' in data:
                employee.set_password(data['password'])

            db.session.commit()
            return jsonify({'message': 'Update employee successfully'}), 200
        return jsonify({"error": "Permission denied"}), 403
    return jsonify({"error": "You are not logged in"})

# Xóa nhân viên theo ID
@app.route('/employees/<int:employee_id>', methods=['DELETE'])
@jwt_required()
def delete_employee(employee_id):
    current_user = get_jwt_identity()
    claims = get_jwt()
    role = claims['role']
    if current_user:
        if role:
            employee = Employee.query.get(employee_id)

            if not employee:
                return jsonify({'message': 'Employee is None'}), 404

            # Tìm và xóa tất cả các liên kết trong bảng booking_employees liên quan đến nhân viên
            booking_employees = BookingEmployee.query.filter_by(employee_id=employee_id).all()
            for booking_employee in booking_employees:
                db.session.delete(booking_employee)

            # Xóa nhân viên
            db.session.delete(employee)
            db.session.commit()
            return jsonify({'message': 'Delete employee successfully'}), 200
        return jsonify({"error": "Permission denied"}), 403
    return jsonify({"error": "You are not logged in"})