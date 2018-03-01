"""
Top level of BQ manager
"""
import logging
from flask import Flask, request, redirect
from app.projects import blueprint as projects_blueprint
from app.gcloud import blueprint as gcloud_blueprint
from app.utils.google import get_credentials, set_credentials
from app.utils.auth import get_credentials


logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)


def before_first_request_func():
    credential_data = get_credentials()
    if credential_data is not None:
        credential_data.pop("_id")
        set_credentials(credential_data)


def before_request_func():
    if get_credentials() is None:
        if "app.gcloud" not in request.endpoint:
            return redirect("/auth")


app = Flask(__name__)
app.before_first_request(before_first_request_func)
app.before_request(before_request_func)
app.register_blueprint(projects_blueprint)
app.register_blueprint(gcloud_blueprint)
