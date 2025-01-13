from flask import make_response
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from flask_smorest import Blueprint, abort
from bs4 import BeautifulSoup
from extensions import rcli
import requests

from config import Config

hallticket_bp = Blueprint("Hallticket", __name__)
header = {
    "user-agent": "mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/131.0.0.0 safari/537.36",
}

@hallticket_bp.route("/hallticket")
@jwt_required()
def getHalltickets():
    username = get_jwt_identity()
    
    if not rcli.exists(username):
        abort(401, message="you aren't logged in")

    cookies = rcli.hgetall(username)
    response = requests.get(
        f"{Config.BASE_URL}/studentlogin/exam/param_exam_hallticket.php",
        headers=header, 
        cookies=cookies
    )

    if not response.ok:
        abort(500, message="error occured while retrieving halltickets")

    soup = BeautifulSoup(response.text, 'html.parser')
    halltickets = soup.find_all("a", attrs={"onclick": "exam_hallticket()"})

    res_data = list(map(lambda ticket : {
        "exam": ticket.parent.a.string.strip().capitalize(),
        "code": ticket.parent.input.get('value'),
        }
        ,halltickets
    ))

    return {"halltickets": res_data}, 200


@hallticket_bp.get('/p/hallticket/<string:exam_code>')
@jwt_required()
def getHallTicketPdf(exam_code):
    username = get_jwt_identity()

    if not rcli.exists(username):
        abort(401, message="you aren't logged in")
    
    cookies = rcli.hgetall(username)

    response = requests.get(
        f"{Config.BASE_URL}/studentlogin/exam/param_exam_hallticket.php",
        headers=header,
        cookies=cookies
    )
    if not response.ok:
        abort(500, message="error occured while generating pdf.")

    soup = BeautifulSoup(response.content, 'html.parser')
    codes = [a.parent.input['value'] for a in soup.find_all("a", attrs={"onclick": "exam_hallticket()"})]

    if exam_code not in codes:
        abort(404, message='exam code not found')

    hallticket_bin_data = requests.get(
        f"https://citstudentportal.org/studentlogin/exam/rpt_exam_hallticket.php?exam_cd={exam_code}&roll_no={username}",
        headers=header,
        cookies=cookies
    )

    hallticket = make_response(hallticket_bin_data.content)
    hallticket.headers['Content-Type'] = 'application/pdf'
    hallticket.headers['Content-Disposition'] = f'attachment; filename="HT_{exam_code}_{username}.pdf"'

    return hallticket, 200
