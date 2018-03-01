"""
Utilities for managing google assets
"""
from google.cloud.bigquery import Client
from google.oauth2.credentials import Credentials


client_map = {}


CREDENTIALS = None


def set_credentials(credential_data):
    global CREDENTIALS
    CREDENTIALS = Credentials(**credential_data)


def get_credentials():
    return CREDENTIALS


def get_client(project=""):
    client = client_map.get(project)
    if client is None:
        client = Client(project=project, credentials=CREDENTIALS)
        client_map[project] = client
    return client
