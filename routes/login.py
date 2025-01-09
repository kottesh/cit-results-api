from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bs4 import BeautifulSoup
import requests

from config import Config
from schemas import LoginSchema

login = Blueprint("login", __name__)

@login.route("/login")
class Login(MethodView):
    session = requests.session()

    @login.arguments(LoginSchema)
    def post(self, login_data):
        payload = {
            "user_name": login_data["username"],
            "pass_word": login_data["password"],
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = self.session.post(f"{Config.BASE_URL}/studentlogin/login.php?action=process", data=payload, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find("title").string

        if response.ok:
            if 'login' not in title.lower():
                return {"cookie": self.session.cookies.get_dict()}
            else:
                abort(401, message="Invalid username or password")
        
        abort(401, message="Error occured during login")
