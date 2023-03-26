import redis
import json

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

conn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def redis_set(key:str, value:dict):
    json_images = json.dumps(value)
    conn.set(key, json_images)

def redis_get(key:str):
    return json.loads(conn.get(key).decode('utf-8'))