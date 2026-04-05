from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from data_access.storage import get_user_by_id_data


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            current_user = get_user_by_id_data(current_user_id)

            if not current_user:
                return jsonify({"error": "User not found"}), 404

            return func(current_user, *args, **kwargs)
        except Exception as error:
            return jsonify({"error": str(error)}), 401

    return decorated
