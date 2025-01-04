from flask import Flask
from flask_smorest import Api
from config import Config

server = Flask(__name__)
server.config.from_object(Config)
api = Api(server)

from routes import login, logout, hallticket, notice_board, profile, results

api.register_blueprint(hallticket.ht_blp)
api.register_blueprint(login.login_blp)
api.register_blueprint(logout.logout_blp)
api.register_blueprint(notice_board.nb_blp)
api.register_blueprint(profile.profile_blp)
api.register_blueprint(results.result_blp)

if __name__ == "__main__":
    server.run(debug = True)
