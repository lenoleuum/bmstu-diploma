from peewee import *
from .BaseModel import BaseModel
import uuid
import datetime


class Stats(BaseModel):
    id = UUIDField(column_name='id', primary_key=True, default=uuid.uuid4)
    track_id = UUIDField(column_name='track_id')
    timestamp = DateTimeField(column_name='timestamp', default=datetime.datetime.now())

    class Meta:
        table_name = 'stats'