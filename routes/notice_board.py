from flask import request
from flask_smorest import Blueprint, abort
from bs4 import BeautifulSoup
import requests
from config import Config

nb_blp = Blueprint("notice-board", __name__)

@nb_blp.route('/notice-board', methods=['GET'])
def notice_board():
    #TODO: add error handling
    cookies = request.get_json().get('cookies')

    if not cookies:
        abort(404, "cookies not found")

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    response = requests.get(f"{Config.BASE_URL}/studentlogin/notice_board.php", headers=header, cookies=cookies)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all("a")

    items = []

    for link in links:
        items.append(
            {
                "title": link.string.capitalize(),
                "link": link.get('href')
                # TODO: implement code to fill the link.
            }
        )

    if len(items) == 0:
        return {"notices": "N/A"}, 200

    return {"notices": items}, 200