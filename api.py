from asyncio import FastChildWatcher
import time
import redis
import json
from c import creatapp
from redis import StrictRedis
from flask_restful import Resource,Api,abort

config = {"redis_host":"localhost","redis_port":6379}
redis_conn = StrictRedis(config["redis_host"],config["redis_port"],decode_responses=True)
app = creatapp()


def validate_user_password(username,password):
    users = redis_conn.hgetall("userConfig")
    if username in users.keys():
        if users[username] == password:
            return True
    return False





def validate_user_token(user_token,id):
    token = redis_conn.get(id)
    if token:
        if user_token == token:
            print("success")
            return True
    print("authentication failled")
    return False
