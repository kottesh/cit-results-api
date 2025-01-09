from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from bs4 import BeautifulSoup
import requests

from config import Config

logout = Blueprint("logout", __name__)

@logout.route("/logout")
class Logout(MethodView):
    def get(self):
        try:
            cookie = request.get_json()['cookie']
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            }

            response = requests.get(f"{Config.BASE_URL}/studentlogin/logout.php", headers=header, cookies=cookie)

            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find("title").string

            if title and 'logout' in title.lower():
                return {"message": "you are now logged out!"}, 200

            abort(500, message="Error occured logout failed.")
        except KeyError:
            abort(404, message="cookie not found")
