"""
Model definition for status updated and such
"""
from mongoengine import Document, StringField, DateTimeField


class InternalState(Document):
    status = StringField()
    last_refresh = DateTimeField()
