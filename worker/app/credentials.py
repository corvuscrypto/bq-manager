"""
Get the credentials from the database
"""
from google.oauth2.credentials import Credentials
from structlog import get_logger

from bq_models.credentials import Authorization


logger = get_logger(__name__)
CREDENTIALS = None


def get_credentials():
    global CREDENTIALS
    if CREDENTIALS is None:
        logger.debug("requesting data from database")
        auth = Authorization.objects.first()
        if not auth:
            return None
        logger.debug("creating credentials object")
        CREDENTIALS = Credentials(
            token=auth.token,
            refresh_token=auth.refresh_token,
            id_token=auth.id_token,
            token_uri=auth.token_uri,
            client_id=auth.client_id,
            client_secret=auth.client_secret
        )
    return CREDENTIALS
