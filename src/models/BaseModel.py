from peewee import *
import psycopg2


DB_NAME = "vkr_midi"
DB_USER = "postgres"
DB_PASS = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"

conn = PostgresqlDatabase(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)

class BaseModel(Model):
    class Meta:
        database = conn
