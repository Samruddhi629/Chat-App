import random
import re
import time

from data_access.storage import (
    get_all_users_data,
    get_next_user_id,
    get_otp_record,
    get_rate_limit_record,
    get_user_by_email,
    get_user_by_id_data,
    save_otp_record,
    save_rate_limit_record,
    save_user,
    update_user_name,
    delete_otp_record,
)
from utils.jwt_helper import generate_token

EMAIL_REGEX = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
OTP_VALIDITY_SECONDS = 300
RATE_LIMIT_SECONDS = 60


def send_otp(data: dict):
    email = (data.get("email") or "").strip().lower()

    if not email:
        return {"error": "Email is required"}, 400

    if not re.match(EMAIL_REGEX, email):
        return {"error": "Please enter a valid email"}, 400

    rate_limit_record = get_rate_limit_record(email)
    current_time = time.time()

    if rate_limit_record and current_time - rate_limit_record["timestamp"] < RATE_LIMIT_SECONDS:
        return {"error": "Please wait 1 minute before requesting OTP again"}, 429

    otp = str(random.randint(100000, 999999))
    save_otp_record(
        email,
        {
            "otp": otp,
            "created_at": current_time,
            "expires_at": current_time + OTP_VALIDITY_SECONDS,
        },
    )
    save_rate_limit_record(email, {"timestamp": current_time})

    return {
        "message": "OTP sent",
        "otp": otp,
    }, 200


def verify_otp(data: dict):
    email = (data.get("email") or "").strip().lower()
    otp = str(data.get("otp") or "").strip()

    if not email or not otp:
        return {"error": "Email and OTP are required"}, 400

    otp_record = get_otp_record(email)
    current_time = time.time()

    if not otp_record:
        return {"error": "OTP not found. Please request a new OTP"}, 400

    if current_time > otp_record["expires_at"]:
        delete_otp_record(email)
        return {"error": "OTP expired. Please request a new OTP"}, 400

    if otp_record["otp"] != otp:
        return {"error": "Invalid OTP"}, 400

    delete_otp_record(email)

    user = get_user_by_email(email)
    if not user:
        user_id = get_next_user_id()
        default_name = email.split("@")[0][:12] or f"user{user_id}"
        user = {
            "id": user_id,
            "name": default_name,
            "email": email,
            "isOnline": False,
        }
        save_user(user)

    token = generate_token(user["id"])

    return {
        "message": "Login successful",
        "user": user,
        "token": token,
    }, 200


def get_all_users():
    return {"users": get_all_users_data()}, 200


def get_user_by_id(user_id: str):
    user = get_user_by_id_data(user_id)

    if not user:
        return {"error": "User not found"}, 404

    return {"user": user}, 200


def update_current_user(current_user: dict, data: dict):
    new_name = (data.get("name") or "").strip()

    if not new_name:
        return {"error": "Name is required"}, 400

    updated_user = update_user_name(current_user["id"], new_name)
    return {
        "message": "User updated successfully",
        "user": updated_user,
    }, 200
