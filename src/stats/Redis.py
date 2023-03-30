import redis
import json
import pickle

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

conn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def redis_set(key:str, value:dict, flg_serialize=True):
    if flg_serialize:
        json_images = json.dumps(value)
    else:
        json_images = pickle.dumps(value)
        
    conn.set(key, json_images)

def redis_get(key:str):
    return json.loads(conn.get(key).decode('utf-8'))

def redis_get_parsed(key:str):
    return pickle.loads(conn.get(key))