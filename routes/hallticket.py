from flask import request
from flask_smorest import Blueprint, abort
from bs4 import BeautifulSoup
import requests
from config import Config

"""
TODO: complete hallticket route
I have token convention in the new rewrite but still haven't implemented the
way to store the cookies in the server and provide only the auth token
"""

ht_blp = Blueprint("hallticket", __name__, description="hallticket route")

@ht_blp.route("/hallticket", methods=["GET"])
def get_hallticket():
    data = request.get_json()

    try:
        cookies = data['cookies']

        if 'roll_no' not in cookies: 
            abort(404, message="roll_no not found in cookie")

        header = {
            "user-agent": "mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/131.0.0.0 safari/537.36",
        }

        response = requests.get(f"{Config.BASE_URL}/studentlogin/exam/param_exam_hallticket.php", headers=header, cookies=cookies)
        soup = BeautifulSoup(response.text, 'html.parser')

        exam_code = soup.find("input", id="exam_cd").get('value').strip()

        pdf_data = requests.get(f"https://citstudentportal.org/studentlogin/exam/rpt_exam_hallticket.php?exam_cd={exam_code}&roll_no={cookies['roll_no']}", cookies=cookies, headers=header)
        with open("ht.pdf", "wb") as pdf:
            pdf.write(pdf_data.content)

        '''
        TODO: need to return the pdf link here. need to figure it out.
        '''
        return {}
    except KeyError:
        abort(404, message="cookies not provided")
