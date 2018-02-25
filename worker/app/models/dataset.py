"""
Model definition for datasets
"""
from mongoengine import Document, StringField, ObjectIdField, DateTimeField


class Dataset(Document):
    name = StringField()
    project = ObjectIdField()
    created = DateTimeField()
    modified = DateTimeField()
