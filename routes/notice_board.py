from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint, abort
from bs4 import BeautifulSoup
from extensions import rcli
import requests

from config import Config

notice_board_bp = Blueprint("notice-board", __name__)

@notice_board_bp.route("notice-board")
class NoticeBoard(MethodView):
    @jwt_required()
    def get(self):
        username = get_jwt_identity() 

        if not rcli.exists(username):
            abort(401, message="you aren't logged in")

        cookies = rcli.hgetall(username)

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }
        response = requests.get(f"{Config.BASE_URL}/studentlogin/notice_board.php", headers=header, cookies=cookies)
        soup = BeautifulSoup(response.content, 'html.parser')

        """
        TODO: attach links for each of the announcements
        """
        announcements = soup.find_all('a')
        response_data = list(map(lambda x : x.string.strip(), announcements))

        return {"notice-board": response_data}, 200
