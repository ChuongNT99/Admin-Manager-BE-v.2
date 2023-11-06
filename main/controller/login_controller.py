from main import app, login_manager,db
from main.model import Employee, Booking, Room, BookingEmployee
from flask import Blueprint, jsonify, request
from datetime import timedelta
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies,get_jwt_identity,get_jwt
from flask_login import login_required,logout_user


@login_manager.user_loader
def load_user(employee_id):
    print(Employee.query.get(int(employee_id)))
    return Employee.query.get(int(employee_id))

@app.route('/form', methods=['OPTIONS'])  # Xử lý preflight request
def handle_preflight():
    response = app.make_default_options_response()
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@app.route('/form', methods=['POST'])
def handle_form():
    # Kiểm tra credentials
    if request.authorization:
        username = request.authorization.username
        password = request.authorization.password
    else:
        return 'Unauthorized', 401
    return 'Success'

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
    access_token = create_access_token(identity=employee.employe_ide , additional_claims={"role": employee.role},expires_delta=timedelta(seconds=3600) )

    response = jsonify(message='Logged in successfully',access_token=access_token)
    set_access_cookies(response, access_token)
    return response, 200

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify(message='Logout successfully')
    unset_jwt_cookies(response)
    return response, 200

# @app.route('/admin', methods=['GET'])
# @jwt_required()
# def admin_route():
#     current_user = get_jwt_identity()
#     claims = get_jwt()
#     role = claims['role']
#     if current_user:
#         if role:
#             return"

#         return jsonify({"error": "Permission denied"}), 403
#     return jsonify({"error": "You are not logged in"})
    