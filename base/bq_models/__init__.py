"""
Models for use in the manager worker

Uses MongoEngine
"""
from mongoengine import connect


def initialize(host, port):
    """
    initialize the connection here

    *karate sounds*
    """
    connect("bq_manager", host=host, port=port)
