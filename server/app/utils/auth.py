"""
Utilities for getting google authorization
"""
import pymongo


COLLECTION = pymongo.MongoClient().bq_manager.authorization


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
