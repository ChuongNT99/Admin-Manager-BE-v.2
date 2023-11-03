from main import app, login_manager,db
from main.model import Employee,RevokedToken, Booking, Room, BookingEmployee
from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,get_jwt
from flask_login import login_required,logout_user


@login_manager.user_loader
def load_user(employee_id):
    print(Employee.query.get(int(employee_id)))
    return Employee.query.get(int(employee_id))

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

@app.route('/logout')
@jwt_required()
def logout():
    logout_user()
    jti = get_jwt()['jti']
    revoked_token = RevokedToken(jti=jti)
    db.session.add(revoked_token)
    db.session.commit()
    return jsonify({"message": "Logout successful"})

@app.route('/check_login', methods=['GET'])
@jwt_required()
def check_login():
    return jsonify({"message": "Logged in"})

@app.route('/admin', methods=['GET'])
@jwt_required()
def admin_route():
    current_user = get_jwt_identity()
    print (current_user)
    if current_user== 1:
        return jsonify(message="This is an admin-only route")
    return jsonify(message="Permission denied"), 403
