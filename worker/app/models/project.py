"""
Model definition for BQ projects
"""
from mongoengine import Document, StringField


class Project(Document):
    name = StringField()
