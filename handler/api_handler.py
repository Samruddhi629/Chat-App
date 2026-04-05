from flask import Blueprint, jsonify, request

from service import chat_service, message_service, user_service
from utils.auth_middleware import token_required

api_bp = Blueprint("api", __name__)


# API 1: POST /api/v1/login
# Generate a 6-digit OTP for the given email and store it temporarily.
@api_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    result, status_code = user_service.send_otp(data)
    return jsonify(result), status_code


# API 2: POST /api/v1/verify
# Verify OTP, create the user if needed, and return JWT token with user details.
@api_bp.route("/verify", methods=["POST"])
def verify():
    data = request.get_json(silent=True) or {}
    result, status_code = user_service.verify_otp(data)
    return jsonify(result), status_code


# API 3: GET /api/v1/me
# Return the profile of the currently logged-in user using JWT.
@api_bp.route("/me", methods=["GET"])
@token_required
def me(current_user):
    return jsonify(current_user), 200


# API 4: GET /api/v1/user/all
# Return all registered users from in-memory storage.
@api_bp.route("/user/all", methods=["GET"])
def get_all_users():
    result, status_code = user_service.get_all_users()
    return jsonify(result), status_code


# API 5: GET /api/v1/user/<user_id>
# Return one specific user by user ID.
@api_bp.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    result, status_code = user_service.get_user_by_id(user_id)
    return jsonify(result), status_code


# API 6: POST /api/v1/update/user
# Update the name of the currently logged-in user.
@api_bp.route("/update/user", methods=["POST"])
@token_required
def update_user(current_user):
    data = request.get_json(silent=True) or {}
    result, status_code = user_service.update_current_user(current_user, data)
    return jsonify(result), status_code


# API 7: POST /api/v1/chat/new
# Create a one-to-one chat between the logged-in user and another user.
@api_bp.route("/chat/new", methods=["POST"])
@token_required
def create_chat(current_user):
    data = request.get_json(silent=True) or {}
    result, status_code = chat_service.create_chat(current_user, data)
    return jsonify(result), status_code


# API 8: GET /api/v1/chat/all
# Return all chats for the logged-in user with unseen message counts.
@api_bp.route("/chat/all", methods=["GET"])
@token_required
def get_chats(current_user):
    result, status_code = chat_service.get_all_chats(current_user)
    return jsonify(result), status_code


# API 9: POST /api/v1/message
# Store a text message or image message for a chat using multipart/form-data.
@api_bp.route("/message", methods=["POST"])
@token_required
def send_message(current_user):
    text = request.form.get("text", "")
    chat_id = request.form.get("chatId", "")
    image = request.files.get("image")

    payload = {
        "chatId": chat_id,
        "text": text,
        "image": image,
    }

    result, status_code = message_service.send_message(current_user, payload)
    return jsonify(result), status_code


# API 10: GET /api/v1/message/<chat_id>
# Return all messages for a chat and mark unseen incoming messages as seen.
@api_bp.route("/message/<chat_id>", methods=["GET"])
@token_required
def get_messages(current_user, chat_id):
    result, status_code = message_service.get_messages(current_user, chat_id)
    return jsonify(result), status_code
