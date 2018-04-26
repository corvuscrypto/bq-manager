"""
Get the credentials from the database
"""
from google.oauth2.credentials import Credentials
from app.config import Config
from structlog import get_logger


logger = get_logger(__name__)
CREDENTIALS = None


def get_credentials():
    global CREDENTIALS
    if CREDENTIALS is None:
        logger.debug("creating credentials object")
        CREDENTIALS = Credentials.from_authorized_user_file(
            Config.Google.credentials_file
        )
    return CREDENTIALS
