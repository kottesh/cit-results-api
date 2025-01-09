from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from bs4 import BeautifulSoup
import requests

from config import Config

profile = Blueprint("profile", __name__)

@profile.route("/profile", methods=["GET"])

class Profile(MethodView):
    def get(self):
        try:
            cookies = request.get_json()['cookie']
            header = {
                "user-agent": "mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/131.0.0.0 safari/537.36",
            }

            response = requests.get(f"{Config.BASE_URL}/studentlogin/personal.php", headers=header, cookies=cookies)
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

        except KeyError:
            abort(404, message="cookie not found in the body")
