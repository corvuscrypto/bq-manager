"""
Model definition for BQ projects
"""
from mongoengine import Document, StringField, IntField


class Project(Document):
    name = StringField()
    numeric_id = IntField()
