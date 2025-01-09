from flask import request, jsonify
from flask_smorest import Blueprint, abort
from bs4 import BeautifulSoup
import requests

from config import Config

result = Blueprint("results", __name__)

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}

@result.get("/result")
def results():
    try:
        cookie = request.get_json()['cookie']

        response = requests.get(f"{Config.BASE_URL}/studentlogin/exam/exam_result.php", headers=header, cookies=cookie)
        soup = BeautifulSoup(response.content, 'html.parser')

        exam_codes = [option['value'].strip()[:-1] for option in soup.find_all("option")]

        return exam_codes, 200
    except KeyError:
        abort(404, message="cookie not found")

"""
TODO: Improve this route. Instead of scraping data from site
      which contains info about result such as course_code,
      course_name, grade, pass/fail. But It doesn't show the CGPA
      or GPA, I could get this data from the pdf.

      fixin: May scrap the data from the pdf I guess!.
"""
@result.get("result/<string:exam_code>")
def getResultByExamCode(exam_code):
    try:
        cookie = request.get_json()['cookie']
        response = requests.get(f"{Config.BASE_URL}/studentlogin/exam/exam_result.php", headers = header, cookies = cookie)
        soup = BeautifulSoup(response.content, 'html.parser') 

        exam_codes = [option['value'].strip() for option in soup.find_all("option")]

        if not any(code.startswith(exam_code) for code in exam_codes):
            abort(404, message="exam code not found")
        
        table = soup.find('div', id=f"div_{exam_code}")
        rows = table.find_all("tr", class_="row1")
        data = [
            td.get_text(strip=True).replace("$", "") 
            for td in row.find_all("td", class_="tablecol2")
            for row in rows
        ]

        result = {subject[0]: subject[1:] for subject in data}

        return jsonify(result), 200
    except KeyError:
        abort(404, message="cookie not found")

"""
TODO: Implement this route, send pdf data as json.
"""
@result.get("result/<string:exam_code>/pdf")
def getPdfByExamCode(exam_code):
    try:
        cookie = request.get_json()['cookie']
        return {}
    except:
        abort(404, message="cookie not found")