"""
Module for getting authentication tokens.
Most logic is in the auth submodule
"""
from flask import Blueprint
from app.gcloud.auth import add_routes


blueprint = Blueprint(__name__, "gcloud")

add_routes(blueprint)
