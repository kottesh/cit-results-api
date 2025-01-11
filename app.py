from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api, Blueprint
from config import Config
from routes import (
    login_bp,
    logout_bp,
    notice_board_bp,
    hallticket_bp,
    profile_bp,
    result_bp
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    api = Api(app)
    jwt = JWTManager(app)

    v1 = Blueprint("v1", __name__, url_prefix="/api/v1")

    v1.register_blueprint(login_bp)
    v1.register_blueprint(logout_bp)
    v1.register_blueprint(notice_board_bp)
    v1.register_blueprint(hallticket_bp)
    v1.register_blueprint(profile_bp)
    v1.register_blueprint(result_bp)

    api.register_blueprint(v1)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
else:
    app = create_app()
