from main import app
from main.model import Employee, Booking, Room, BookingEmployee
from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_login import login_user, logout_user


# @login_manager.user_loader
# def load_user(employee_id):
#     return Employee.query.get(int(employee_id))

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
            return jsonify({"message": "Bad request, missing JSON data"}), 400
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email or not password:
        return jsonify({"message": "Bad request, missing email or password"}), 400

    employee = Employee.query.filter_by(email=email).first()
    
    if not employee or not employee.check_password(password):
        return jsonify({"message": "Email or password is incorrect"}), 401

    access_token = create_access_token(identity=employee.employee_id, additional_claims={"admin": employee.admin})
    return jsonify(access_token=access_token)

@app.route('/admin', methods=['GET'])
@jwt_required()
def admin_route():
    current_user = get_jwt_identity()
    print (current_user)
    if current_user== 1:
        return jsonify(message="This is an admin-only route")
    return jsonify(message="Permission denied"), 403
