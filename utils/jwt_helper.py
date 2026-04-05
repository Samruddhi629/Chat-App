from datetime import timedelta

from flask_jwt_extended import JWTManager, create_access_token


def configure_jwt(app):
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=15)
    JWTManager(app)


def generate_token(user_id: str) -> str:
    return create_access_token(identity=user_id)
