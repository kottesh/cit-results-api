from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bs4 import BeautifulSoup
import requests

from config import Config

notice_board = Blueprint("notice-board", __name__)

@notice_board.route("notice-board")
class NoticeBoard(MethodView):
    def get(self):
        try:
            cookies = request.get_json()['cookie']

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
        except KeyError:
            abort(404, message="cookies not found")
