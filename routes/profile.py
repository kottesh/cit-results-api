from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from bs4 import BeautifulSoup
from extensions import rcli
import requests

from config import Config

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/profile", methods=["GET"])

class Profile(MethodView):
    @jwt_required()
    def get(self):
        username = get_jwt_identity() 

        if not rcli.exists(username):
            abort(401, message="you aren't logged in")
        
        cookies = rcli.hgetall(username)

        header = {
            "user-agent": "mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/131.0.0.0 safari/537.36",
        }

        response = requests.get(
            f"{Config.BASE_URL}/studentlogin/personal.php",
            headers=header,
            cookies=cookies
        )
        if not response.ok:
            abort(500, message="error occured while fetching profile")

        soup = BeautifulSoup(response.text, 'html.parser')

        tables = soup.find("td", attrs={"align": "center"}).parent.find_all("table")
        tables = list(map(
            lambda table: [
                tr.td.string.strip() if tr.td.string else None
                for tr in table.find_all("tr")
            ], 
            tables
        ))

        prof_data = {} 

        for label, value in zip(tables[0], tables[1]):
            if label and value:
                prof_data[label] = value

        return prof_data, 200 
