from flask import request
from flask_smorest import Blueprint, abort
import requests
from config import Config

logout_blp = Blueprint("logout", __name__)

@logout_blp.route('/logout', methods=["GET"])
def logout():
    cookies = request.get_json()['cookies']

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    response = requests.get(f"{Config.BASE_URL}/studentlogin/logout.php", headers=header, cookies=cookies)

    if 'logged out' in response.text.lower():
        return {"message": "you are now logged out!"}, 200

    abort(500, message="error occured can't logout")