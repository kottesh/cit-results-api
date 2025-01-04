from flask import request
from flask_smorest import Blueprint, abort
from bs4 import BeautifulSoup
import requests
from config import Config

"""
This route just displays the exam codes for different

TODO: rewrite this route in human way
     "
        This shows the codes. But instead return semester like "Semester 1", "Semester 2", etc.,
     "
"""

result_blp = Blueprint("results", __name__)

@result_blp.route('/results', methods=['GET'])
def results():
    cookies = request.get_json().get('cookies')

    if not cookies:
        return {"message": "cookies not provided"}, 403

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    response = requests.get(f"{Config.BASE_URL}/studentlogin/exam/exam_result.php", headers = header, cookies = cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    exam_sessions = soup.find_all("option")

    exam_codes = []

    for exam in exam_sessions:
        exam_codes.append(exam.get('value')[:-1])

    return {"exam_codes": exam_codes}, 200

"""
TODO: implement pdf
"""
@result_blp.route('/results/<string:exam_code>', methods=['GET'])
def get_result_by_exam_code(exam_code):
    cookies = request.get_json().get('cookies')

    if not cookies:
        return {"message": "cookies not provided"}, 403

    header = {
        "user-agent": "mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/131.0.0.0 safari/537.36",
    }

    """
    TODO: enhance data processing, fetching
    """
    response = requests.get(f"{Config.BASE_URL}/studentlogin/exam/exam_result.php", headers = header, cookies = cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    exam_codes = [code.get('value') for code in soup.find_all("option")]

    results = {}

    for code in exam_codes:
        table = soup.find('div', id=f'div_{code[-1]}')
        data = [
            [td.string.strip().replace("$", "") for td in tr.find_all("td", class_="tablecol2")]
            for tr in table.find_all("tr", class_="row1")
        ]

        result = {
            "semester": data[0][0],
            "results": [],
        }

        for item in data:
            result["results"].append({
                "course_code": item[1],
                "course_name": item[2],
                "grade": item[3],
                "result": item[4]
            })

        results[code[:-1]] = result

    if exam_code in results:
        return { "results": results[exam_code]}, 200

    return {"message": f"no exam_code `{exam_code}` found"}, 404