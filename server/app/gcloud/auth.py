"""
OAuth module for getting a token from google
"""
from flask import redirect, request
import requests as r
import logging
from app.utils.google import set_credentials
from app.utils.auth import save_credentials


AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/auth?redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fredirect&prompt=select_account&response_type=code&client_id=764086051850-6qr4p6gpi6hn506pt8ejuq83di341hur.apps.googleusercontent.com&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform&access_type=offline"
TOKEN_ENDPOINT = "https://accounts.google.com/o/oauth2/token"

CLIENT_ID = "764086051850-6qr4p6gpi6hn506pt8ejuq83di341hur.apps.googleusercontent.com"
CLIENT_SECRET = "d-FL95Q19q7MQmFpd7hHD0Ty"


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def add_routes(blueprint):
    blueprint.add_url_rule("/auth", "auth", view_func=do_auth)
    blueprint.add_url_rule("/redirect", "redirect", view_func=do_redirect)


def do_redirect():
    code = request.args['code']
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:5000/redirect"
    }
    resp = r.post(TOKEN_ENDPOINT, data=data)
    token_data = resp.json()
    credentials_data = {
        "token": token_data['access_token'],
        "refresh_token": token_data['refresh_token'],
        "id_token": token_data['id_token'],
        "token_uri": TOKEN_ENDPOINT,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    set_credentials(credentials_data)
    save_credentials(credentials_data)

    return redirect("/")


def do_auth():
    return redirect(AUTH_ENDPOINT)
