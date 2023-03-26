from peewee import *
from .BaseModel import BaseModel
import uuid


class Track(BaseModel):
    id = UUIDField(column_name='id', primary_key=True, default=uuid.uuid4)
    track_name = CharField(column_name='track_name', max_length=255)
    time_signature = CharField(column_name='time_signature', max_length=255)
    tonalities = TextField(column_name='tonalities')
    events = TextField(column_name='events')

    class Meta:
        table_name = 'track'