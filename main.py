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

@server.route('/logout', methods=["POST"])
def logout():
    cookies = request.get_json()['cookies']

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    response = requests.get(f"{BASE_URL}/logout.php", headers=header, cookies=cookies)

    if 'logged out' in response.text.lower():
        return jsonify({"message": "you are now logged out!"}), 200

    return jsonify({"message": "error occured can't logout"}), 500

if __name__ == "__main__":
    server.run(debug = True)
