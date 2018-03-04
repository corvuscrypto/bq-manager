"""
Get the credentials from the database
"""
import pymongo
from app.config import Config
from google.oauth2.credentials import Credentials
from structlog import get_logger


logger = get_logger(__name__)
CREDENTIALS = None
CLIENT = pymongo.MongoClient(host=Config.Mongo.host, port=Config.Mongo.port)


def get_credentials():
    global CREDENTIALS
    if CREDENTIALS is None:
        logger.debug("requesting data from database")
        credential_data = CLIENT.bq_manager.authorization.find_one()
        if not credential_data:
            return None
        credential_data.pop("_id")
        logger.debug("creating credentials object")
        CREDENTIALS = Credentials(**credential_data)
    return CREDENTIALS
