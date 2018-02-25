"""
Module for project manipulation and such
"""
import logging
from bq_manager.utils.google import get_client
from bq_manager.utils.decorators import render
from flask import Blueprint
from bq_manager.projects.dashboard import add_routes


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


blueprint = Blueprint(__name__, "projects")
add_routes(blueprint)


def get_projects():
    """
    Return a list of available projects
    """
    return list(get_client().list_projects())


@blueprint.route("/")
@render("main/index.j2")
def index():
    """
    Index of the manager web interface
    which shows the available projects
    """
    logger.error("getting projects")
    return {
        "projects": get_projects()
    }

