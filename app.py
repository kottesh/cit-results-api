from flask import Flask
from flask_smorest import Api, Blueprint
from config import Config
from routes import (
    login,
    logout,
    notice_board,
    hallticket,
    profile,
    result
)

def create_app():
    server = Flask(__name__)
    server.config.from_object(Config)

    api = Api(server)

    v1 = Blueprint("v1", __name__, url_prefix="/api/v1")

    v1.register_blueprint(login)
    v1.register_blueprint(logout)
    v1.register_blueprint(notice_board)
    v1.register_blueprint(hallticket)
    v1.register_blueprint(profile)
    v1.register_blueprint(result)

    api.register_blueprint(v1)

    return server
