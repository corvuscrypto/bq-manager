"""
Model definition for credentials.

Probably just gonna be one model for now but eh.
"""
from mongoengine import Document, StringField


class Authorization(Document):
    token = StringField()
    refresh_token = StringField()
    id_token = StringField()
    token_uri = StringField()
    client_id = StringField()
    client_secret = StringField()
