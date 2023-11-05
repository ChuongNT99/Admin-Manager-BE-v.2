from main import app,db, login_manager
from main.model import Employee, Booking, Room, BookingEmployee
from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_login import login_required


# @login_manager.user_loader
# def load_user(employee_id):
#     return Employee.query.get(int(employee_id))

@app.route('/employees', methods=['POST'])
@jwt_required()
def create_employee():
    current_user = get_jwt_identity()
    print(current_user)
    if current_user== 1:
        data = request.get_json()
        employee_name = data.get('employee_name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        password = data.get('password')
        admin = data.get('admin', False)

        # Kiểm tra email và số điện thoại không trùng lặp
        existing_employee = Employee.query.filter_by(email=email).first()
        if existing_employee:
            return jsonify({'message': 'Email đã tồn tại'}), 400

        existing_phone = Employee.query.filter_by(phone_number=phone_number).first()
        if existing_phone:
            return jsonify({'message': 'Số điện thoại đã tồn tại'}), 400

        # Mã hóa mật khẩu
        new_employee = Employee(employee_name=employee_name, email=email, phone_number=phone_number, password=password , admin=admin)
        new_employee.set_password(password)
        db.session.add(new_employee)
        db.session.commit()
        return jsonify({'message': 'Created employee success'})
    return jsonify(message="this is user"), 403
# Đọc danh sách nhân viên
@app.route('/employees', methods=['GET'])
@jwt_required()
def get_employees():
    current_user = get_jwt_identity()
    print(current_user)
    if current_user== 1:
        employees = Employee.query.all()
        employee_list = [employee.serialize() for employee in employees]
        return jsonify({'employees': employee_list})
    return jsonify(message="this is user"), 403
    

# Đọc thông tin nhân viên theo ID
@app.route('/employees/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_employee(employee_id):
    current_user = get_jwt_identity()
    print(current_user)
    if current_user== 1:
        employee = Employee.query.get(employee_id)
        if employee is None:
            return jsonify({'message': 'Nhân viên không tồn tại'}), 404
        return jsonify(employee.serialize())
    return jsonify(message="this is user"), 403
   

# Cập nhật thông tin nhân viên theo ID
@app.route('/employees/<int:employee_id>', methods=['PUT'])
@jwt_required()
def update_employee(employee_id):
    current_user = get_jwt_identity()
    print(current_user)
    if current_user== 1:
        data = request.get_json()
        employee = Employee.query.get(employee_id)

        if not employee:
            return jsonify({'message': 'Nhân viên không tồn tại'}), 404

        if 'employee_name' in data:
            employee.employee_name = data['employee_name']
        if 'email' in data:
            # Kiểm tra email không trùng lặp
            existing_employee = Employee.query.filter(Employee.employee_id != employee_id, Employee.email == data['email']).first()
            if existing_employee:
                return jsonify({'message': 'Email đã tồn tại'}), 400
            employee.email = data['email']
        if 'phone_number' in data:
            # Kiểm tra số điện thoại không trùng lặp
            existing_employee = Employee.query.filter(Employee.employee_id != employee_id, Employee.phone_number == data['phone_number']).first()
            if existing_employee:
                return jsonify({'message': 'Số điện thoại đã tồn tại'}), 400
            employee.phone_number = data['phone_number']
        if 'password' in data:
            employee.set_password(data['password'])

        db.session.commit()
        return jsonify({'message': 'Thông tin nhân viên đã được cập nhật thành công'}), 200
    return jsonify(message="this is user"), 403

    

# Xóa nhân viên theo ID
@app.route('/employees/<int:employee_id>', methods=['DELETE'])
@jwt_required()
def delete_employee(employee_id):
    current_user = get_jwt_identity()
    print(current_user)
    if current_user== 1:
        employee = Employee.query.get(employee_id)

    if not employee:
        return jsonify({'message': 'Nhân viên không tồn tại'}), 404

    # Tìm và xóa tất cả các liên kết trong bảng booking_employees liên quan đến nhân viên
    booking_employees = BookingEmployee.query.filter_by(employee_id=employee_id).all()
    for booking_employee in booking_employees:
        db.session.delete(booking_employee)

    # Xóa nhân viên
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Nhân viên đã bị xóa thành công, cùng với các liên kết trong booking_employees'}), 200
    return jsonify(message="this is user"), 403