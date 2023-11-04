from main import app
from main.model import Room
from flask import Blueprint, jsonify, request
from datetime import datetime
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity


@app.route("/rooms", methods=["GET"])
@jwt_required()
def get_rooms():
    current_user = get_jwt_identity()
    print(current_user, "--------------------------------------------------")
    if current_user == 1:
        #     rooms = Room.query.all()
        #     room_list = []
        #     for room in rooms:
        #         room_data = {
        #             'room_id': room.room_id,
        #             'room_name': room.room_name,
        #             'status': room.status
        #         }
        #         room_list.append(room_data)
        #     return jsonify(rooms=room_list)
        # return jsonify(message="Permission denied"), 403
        rooms = Room.query.all()
        return jsonify({"rooms": [room.serialize() for room in rooms]})
    else:
        return jsonify({"error": "Internal Server Error"}), 500


# @app.route("/rooms", methods=["POST"])
# @jwt_required()
# def create_room():
#     current_user = get_jwt_identity()

#     if current_user.get("admin") == 1:
#         data = request.get_json()
#         room_name = data.get("room_name")
#         status = data.get("status", 0)

#         conn = create_db_connection()
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT room_name FROM room_meeting WHERE room_name = %s", (
#                 room_name,)
#         )
#         existing_room = cursor.fetchone()

#         if existing_room:
#             return jsonify({"error": "Room already exists"}), 400

#         cursor.execute(
#             "INSERT INTO room_meeting (room_name, status) VALUES (%s, %s)",
#             (room_name, status),
#         )
#         conn.commit()
#         return jsonify({"message": "Room created successfully"})
#     else:
#         return jsonify({"error": "Permission denied"}), 403


# @app.route("/rooms/<int:room_id>", methods=["PUT"])
# @jwt_required()
# def update_room(room_id):
#     current_user = get_jwt_identity()

#     if current_user.get("admin") == 1:
#         try:
#             data = request.get_json()
#             room_name = data.get("room_name")

#             conn = create_db_connection()
#             cursor = conn.cursor()
#             cursor.execute(
#                 "SELECT room_name FROM room_meeting WHERE room_id != %s AND room_name = %s",
#                 (room_id, room_name),
#             )
#             existing_room = cursor.fetchone()

#             if existing_room:
#                 return jsonify({"error": "Room name already exists"}), 400

#             cursor.execute(
#                 "UPDATE room_meeting SET room_name=%s WHERE room_id=%s",
#                 (room_name, room_id),
#             )
#             conn.commit()
#             return jsonify({"message": "Room updated successfully"})
#         except Exception as e:
#             return jsonify({"error": "Internal Server Error"}), 500
#         finally:
#             cursor.close()
#             conn.close()
#     else:
#         return jsonify({"error": "Permission denied"}), 403


# @app.route("/rooms/<int:room_id>", methods=["DELETE"])
# @jwt_required()
# def delete_room(room_id):
#     current_user = get_jwt_identity()

#     if current_user.get("admin") == 1:
#         try:
#             conn = create_db_connection()
#             cursor = conn.cursor()
#             cursor.execute(
#                 "DELETE FROM room_meeting WHERE room_id=%s", (room_id,))
#             conn.commit()
#             return jsonify({"message": "Room deleted successfully"})
#         except Exception as e:
#             return jsonify({"error": "Internal Server Error"}), 500
#         finally:
#             cursor.close()
#             conn.close()
#     else:
#         return jsonify({"error": "Permission denied"}), 403
