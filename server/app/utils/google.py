"""
Utilities for managing google assets
"""
from google.cloud.bigquery import Client


client_map = {}


def get_client(project=None):
    client = client_map.get(project)
    if client is None:
        client = Client(project=project)
        client_map[project] = client
    return client
