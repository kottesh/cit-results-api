from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

server = Flask(__name__)

BASE_URL = "https://citstudentportal.org/studentlogin"

@server.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if not username or not password:
        return {"message": "username and password is required"}, 401

    session = requests.Session()

    payload = {
        "user_name": username,
        "pass_word": password,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = session.post(f"{BASE_URL}/login.php?action=process", data=payload, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('title').text.strip().lower()

    if title and 'login' in title:
        return jsonify({"message": "invalid username or password"}), 401

    cookies = session.cookies.get_dict()

    return jsonify({"message": "login successfull", "cookies": cookies}), 200

@server.route('/logout', methods=["GET"])
def logout():
    cookies = request.get_json()['cookies']

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    response = requests.get(f"{BASE_URL}/logout.php", headers=header, cookies=cookies)

    if 'logged out' in response.text.lower():
        return jsonify({"message": "you are now logged out!"}), 200

    return jsonify({"message": "error occured can't logout"}), 500

@server.route('/notice-board', methods=['GET'])
def notice_board():
    #TODO: add error handling
    cookies = request.get_json().get('cookies')

    if not cookies:
        return {"message": "cookies not provided"}, 403

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    response = requests.get(f"{BASE_URL}/notice_board.php", headers=header, cookies=cookies)
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
        return jsonify({"notices": "N/A"}), 200

    return jsonify({"notices": items}), 200

# TODO: complete displaying result
@server.route('/results', methods=['GET'])
def results():
    cookies = request.get_json().get('cookies')

    if not cookies:
        return {"message": "cookies not provided"}, 403

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    response = requests.get(f"{BASE_URL}/exam/exam_result.php", headers = header, cookies = cookies)
    print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    exam_sessions = soup.find_all("option")

    exam_codes = []

    for exam in exam_sessions:
        exam_codes.append(exam.get('value')[:-1])

    return {"exam_codes": exam_codes}, 200

if __name__ == "__main__":
    server.run(debug = True)
