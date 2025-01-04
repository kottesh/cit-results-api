from flask import request
from flask_smorest import Blueprint, abort
from bs4 import BeautifulSoup
from schemas import LoginSchema
import requests
from config import Config

login_blp = Blueprint("login", __name__)

@login_blp.route("/login", methods=["POST"])
@login_blp.arguments(LoginSchema)
def login(data):
    username = data['username']
    password = data['password']

    session = requests.Session()

    payload = {
        "user_name": username,
        "pass_word": password,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = session.post(f"{Config.BASE_URL}/studentlogin/login.php?action=process", data=payload, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('title').text.strip().lower()

    if title and 'login' in title:
        abort(401, message="Invalid username or password")

    cookies = session.cookies.get_dict()

    return ({"message": "login successfull", "cookies": cookies}), 200