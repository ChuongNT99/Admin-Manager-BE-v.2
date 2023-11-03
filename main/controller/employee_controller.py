from main import app, login_manager
from main.model import Employee, Booking, Room, BookingEmployee
from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_login import login_required


# @login_manager.user_loader
# def load_user(employee_id):
#     return Employee.query.get(int(employee_id))

@app.route('/employee', methods=['GET'])
@jwt_required()
@login_required
def employee():
    current_user = get_jwt_identity()
    print (current_user)
    if current_user== 1:
        employees = Employee.query.all()
        employee_list = []
        for employee in employees:
            employee_data = {
                'employee_id': employee.employee_id,
                'employee_name': employee.employee_name,
                'email': employee.email,
                'phone_number': employee.phone_number,
                'admin': employee.admin
            }
            employee_list.append(employee_data)
        return jsonify(employees=employee_list)
    return jsonify(message="Permission denied"), 403
