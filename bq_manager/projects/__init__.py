"""
Module for project manipulation and such
"""
from bq_manager import bq_client


def get_projects():
    """
    Return a list of available projects
    """
    return list(bq_client.list_projects())
