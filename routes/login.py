from datetime import timedelta
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token
from bs4 import BeautifulSoup
from extensions import rcli
import requests

from config import Config
from schemas import LoginSchema

login_bp = Blueprint("login", __name__)

@login_bp.route("/login")
class Login(MethodView):
    session = requests.session()

    @login_bp.arguments(LoginSchema)
    def post(self, login_data):
        payload = {
            "user_name": login_data["username"],
            "pass_word": login_data["password"],
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = self.session.post(
            f"{Config.BASE_URL}/studentlogin/login.php?action=process",
            data=payload,
            headers=headers
        )

        if response.ok:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find("title").string

            if 'login' not in title.lower():
                token = create_access_token(
                    identity=login_data['username'],
                    expires_delta=timedelta(days=7)
                )

                rcli.hset(
                    login_data['username'],
                    mapping=self.session.cookies.get_dict(),
                )

                return {'token': token}, 200
            else:
                abort(401, message="invalid username or password")
        
        abort(401, message="error occured during login")
