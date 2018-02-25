"""
Model definition for tables in BQ
"""
from mongoengine import (
    Document, StringField, IntField,
    ObjectIdField, ListField, DateTimeField
)


class Table(Document):
    name = StringField()
    dataset = ObjectIdField()
    project = ObjectIdField()
    num_bytes = IntField()
    num_records = IntField()
    schema = ListField()
    created = DateTimeField()
    modified = DateTimeField()
    partitioning = StringField()
