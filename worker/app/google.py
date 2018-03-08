"""
Google utils
"""
import time

from google.cloud.bigquery import Client
from structlog import get_logger

from app.credentials import get_credentials


logger = get_logger(__name__)
CLIENT = None


def get_client():
    global CLIENT
    if CLIENT is None:
        logger.info("Obtaining credentials")
        credentials = get_credentials()
        while credentials is None:
            logger.debug("Credentials not found, retrying in 10s")
            time.sleep(10)
            credentials = get_credentials()
        logger.info("Instantiating Google client")
        CLIENT = Client(project="", credentials=credentials)
    return CLIENT
