from main import app,db
from main.model import Employee, Booking, Room, BookingEmployee
from flask import jsonify, request
from datetime import timedelta
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies,get_jwt_identity,get_jwt


@app.route('/form', methods=['OPTIONS'])  
def handle_preflight():
    response = app.make_default_options_response()
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@app.route('/form', methods=['POST'])
def handle_form():
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
    access_token = create_access_token(identity=employee.employee_id, additional_claims={"role": employee.role},expires_delta=timedelta(seconds=3600) )

    response = jsonify(message='Logged in successfully',access_token=access_token)
    set_access_cookies(response, access_token)
    return response, 200

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify(message='Logout successfully')
    unset_jwt_cookies(response)
    return response, 200
