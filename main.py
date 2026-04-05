from flask import Flask, jsonify

from handler.api_handler import api_bp
from utils.jwt_helper import configure_jwt


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "super-secret-key-change-me"

    configure_jwt(app)
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    @app.route("/")
    def health_check():
        return jsonify({"message": "Flask chat backend is running"})

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Route not found"}), 404

    @app.errorhandler(500)
    def internal_error(_error):
        return jsonify({"error": "Internal server error"}), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
