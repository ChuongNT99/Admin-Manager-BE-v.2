from functools import wraps
from flask import request, jsonify
from main.model import Employee
from flask_jwt_extended import JWTManager, get_jwt_identity
from main import db


def get_user_role(employee_id):
    employee = db.session.get(Employee, employee_id)
    if employee:
        return 'admin' if employee.role else 'user'


def has_permission(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            employee_id = get_jwt_identity()

            if not employee_id:
                return jsonify({"message": "Employee ID is required"}), 401

            user_role = get_user_role(employee_id)

            if user_role == required_role:
                return func(*args, **kwargs)
            else:
                return jsonify({"message": "Access denied"}), 403
        return wrapper
    return decorator
