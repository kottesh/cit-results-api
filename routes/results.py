from flask import jsonify, make_response 
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint, abort
from bs4 import BeautifulSoup
from extensions import rcli
import requests

from config import Config

result_bp = Blueprint("results", __name__)

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}

@result_bp.get("/result")
@jwt_required()
def results():
    username = get_jwt_identity() 

    if not rcli.exists(username):
        abort(401, message="you aren't logged in")
    
    cookies = rcli.hgetall(username)

    response = requests.get(
        f"{Config.BASE_URL}/studentlogin/exam/exam_result.php",
        headers=header, 
        cookies=cookies
    )
    if not response.ok:
        abort(500, message="error occured")

    soup = BeautifulSoup(response.content, 'html.parser')

    exam_codes = [option['value'].strip()[:-1] for option in soup.find_all("option")]

    return jsonify(exam_codes), 200

"""
TODO: Improve this route. Instead of scraping data from site
      which contains info about result such as course_code,
      course_name, grade, pass/fail. But It doesn't show the CGPA
      or GPA, I could get this data from the pdf.

      fixin: May scrap the data from the pdf I guess!.
"""
@result_bp.get("result/<string:exam_code>")
@jwt_required()
def getResultByExamCode(exam_code):
    username = get_jwt_identity() 

    if not rcli.exists(username):
        abort(401, message="you aren't logged in")
    
    cookies = rcli.hgetall(username)

    response = requests.get(
        f"{Config.BASE_URL}/studentlogin/exam/exam_result.php",
        headers=header,
        cookies=cookies
    )
    if not response.ok:
        abort(500, message="error occured")

    soup = BeautifulSoup(response.content, 'html.parser') 

    exam_codes = [option['value'].strip() for option in soup.find_all("option")]

    idx = -1
    for pos, code in enumerate(exam_codes):
        if code.startswith(exam_code):
            idx = pos
            break;
    if idx == -1:
        abort(404, message="invalid exam code")

    # if not any(code.startswith(exam_code) for code in exam_codes):
    #     abort(404, message="exam code not found")

    """
    This builds the string div_{table_no}. table_no is obtained from the exam_codes.
    Which will be in the format like NOV241 -> NOV(Session), 24(year), 1(order in the page)
    """
    table = soup.find('div', id=f"div_{exam_codes[idx][-1]}")

    rows = table.find_all("tr", class_="row1")
    data = [
        [
            td.get_text(strip=True).replace("$", "") 
            for td in row.find_all("td", class_="tablecol2")
        ]
        for row in rows
    ]
    result = {subject[1]: subject[2:] for subject in data}

    return jsonify(result), 200

@result_bp.get("p/result/<string:exam_code>")
@jwt_required()
def getPdfByExamCode(exam_code):
    username = get_jwt_identity() 

    if not rcli.exists(username):
        abort(401, message="you aren't logged in")
    
    cookies = rcli.hgetall(username)
    
    response = requests.get(
        f"{Config.BASE_URL}/studentlogin/exam/exam_result.php",
        headers = header,
        cookies = cookies
    )
    if not response.ok:
       abort(500, message="error occured")

    soup = BeautifulSoup(response.content, 'html.parser') 

    exam_codes = [option['value'].strip() for option in soup.find_all("option")]

    if not any(code.startswith(exam_code) for code in exam_codes):
        abort(404, message="invalid exam code")

    pdf_bin_data = requests.get(
        f"https://citstudentportal.org/studentlogin/exam/result.php?exam_cd={exam_code}",
        cookies=cookies,
        headers=header
    )
    if not pdf_bin_data.ok:
       abort(500, message="error occured while generating pdf")

    pdf = make_response(pdf_bin_data.content)
    pdf.headers['Content-Type'] = 'application/pdf'
    pdf.headers['Content-Disposition'] = f'attachment; filename="RESULT_{exam_code}_{username}.pdf"'

    return pdf, 200
