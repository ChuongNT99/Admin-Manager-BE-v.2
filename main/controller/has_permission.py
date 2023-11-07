from functools import wraps
from flask import request, jsonify
from main.model import Employee 
from flask_jwt_extended import JWTManager,get_jwt_identity

# Hàm để lấy vai trò của người dùng dựa trên employee_id
def get_user_role(employee_id):
    # Thực hiện xác thực người dùng và lấy vai trò dựa trên employee_id
    # Thay thế dòng này bằng cách lấy vai trò từ cơ sở dữ liệu hoặc thông tin xác thực khác
    employee = Employee.query.get(employee_id)
    if employee:
        return 'admin' if employee.role else 'user'

# Hàm kiểm tra quyền truy cập
def has_permission(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Lấy employee_id từ thông tin xác thực (có thể lấy từ token JWT hoặc gửi qua yêu cầu)
            employee_id = get_jwt_identity()

            if not employee_id:
                return jsonify({"message": "Employee ID is required"}), 401

            # Lấy vai trò của người dùng
            user_role = get_user_role(employee_id)

            if user_role == required_role:
                return func(*args, **kwargs)
            else:
                return jsonify({"message": "Access denied"}), 403
        return wrapper
    return decorator
