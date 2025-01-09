from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bs4 import BeautifulSoup
import requests

from config import Config

hallticket = Blueprint("Hallticket", __name__)

@hallticket.route("/hallticket")
class Hallticket(MethodView):
    def get(self):
        try:
            cookies = request.get_json()['cookies']
            header = {
                "user-agent": "mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/131.0.0.0 safari/537.36",
            }

            response = requests.get(f"{Config.BASE_URL}/studentlogin/exam/param_exam_hallticket.php", headers=header, cookies=cookies)
            soup = BeautifulSoup(response.text, 'html.parser')
            halltickets = soup.find_all("a", attrs={"onclick": "exam_hallticket()"})

            res_data = list(map(lambda ticket : {
                "name": ticket.parent.a.string.strip().capitalize(),
                "code": ticket.parent.input.get('value'),
                "pdf_link": f"https://citstudentportal.org/studentlogin/exam/rpt_exam_hallticket.php?exam_cd={ticket.parent.input.get('value')}&roll_no={cookies['roll_no']}"
                }
                ,halltickets
            ))

            return {"halltickets": res_data}, 200
        except KeyError:
            abort(404, message="cookies not found")
