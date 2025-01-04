from flask import request
from flask_smorest import Blueprint, abort
from bs4 import BeautifulSoup
import requests
from config import Config

profile_blp = Blueprint("profile", __name__)

@profile_blp.route("/profile", methods=["GET"])
def show_profile():
    data = request.get_json()

    try:
        cookies = data['cookies']

        header = {
            "user-agent": "mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/131.0.0.0 safari/537.36",
        }

        response = requests.get(f"{Config.BASE_URL}/studentlogin/personal.php", headers=header, cookies=cookies)
        soup = BeautifulSoup(response.text, 'html.parser')

        profile = soup.find('table', attrs={"cellpadding": "0", "cellspacing": "0", "style": "padding-left:120px;"})

        """
        TODO: fix data stripping in this. (general data cleaning)
        """

        keys = [key.string.strip() for key in profile.find_all('td', class_="row9") if key and len(key.string.strip())]
        values = [value.string for value in profile.find_all('td', class_="row10")]

        prof_data = {
            "image": f"{Config.BASE_URL}/{soup.find("img", id="student").get("src")[5:]}"
        }

        for key, value in zip(keys, values):
            if value:
                prof_data[key] = value.strip().title()

        return {"profile": prof_data}, 200
    except KeyError:
        abort(404, message="cookies not found")

