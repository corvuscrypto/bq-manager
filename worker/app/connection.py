"""
Initialization of the MongoEngine connection
"""
from mongoengine import connect
from app.config import Config


def initialize():
    connect("bq_manager", host=Config.Mongo.host, port=Config.Mongo.port)
