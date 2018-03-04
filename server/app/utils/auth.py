"""
Utilities for getting google authorization
"""
import pymongo
from app.config import Config


COLLECTION = pymongo.MongoClient(
    host=Config.Mongo.host,
    port=Config.Mongo.port
).bq_manager.authorization


def get_credentials():
    """
    Get credentials yo
    """
    return COLLECTION.find_one()


def save_credentials(credential_data):
    """
    Save credentials yo
    """
    COLLECTION.insert(credential_data)
