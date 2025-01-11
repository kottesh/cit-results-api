from flask_smorest import Blueprint, abort
from flask.views import MethodView
from bs4 import BeautifulSoup
from flask_jwt_extended import get_jwt_identity, jwt_required
from extensions import rcli
import requests

from config import Config

logout_bp = Blueprint("logout", __name__)

@logout_bp.route("/logout")
class Logout(MethodView):
    @jwt_required()
    @logout_bp.doc(security=[{"bearerAuth": []}])
    def get(self):
        username = get_jwt_identity()

        if not rcli.exists(username):
            abort(401, message="you aren't logged in to log out")
        
        cookies = rcli.hgetall(username)
        print(cookies)

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }

        response = requests.get(f"{Config.BASE_URL}/studentlogin/logout.php", headers=header, cookies=cookies)

        if not response.ok: 
            abort(500, message="error occured while logging out")

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find("title").string

        if title and 'logout' in title.lower():
            rcli.delete(username)
            return {"message": "you are now logged out!"}, 200
