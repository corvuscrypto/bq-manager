"""
Initialization of the MongoEngine connection
"""
from mongoengine import connect


def initialize():
    connect("bq_manager")
