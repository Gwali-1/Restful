from asyncio import FastChildWatcher
from lib2to3.pgen2 import token
import time
import redis
import json

from redis import RedisError
from redis import AuthenticationError
from c import creatapp
from redis import StrictRedis
from flask_restful import Resource,Api,abort
import secrets

config = {"redis_host":"localhost","redis_port":6379}
redis_conn = StrictRedis(config["redis_host"],config["redis_port"],decode_responses=True)
app = creatapp()


def validate_user_password(username,password):
    users = redis_conn.hgetall("UsersD")
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



def  generate_auth_token():
    auth_token = secrets.token_urlsafe()
    auth_id = secrets.token_hex(2)
    try:
        redis_conn.set(auth_id,auth_token)
        redis_conn.expire(auth_id,3600)
        return True
    except (RedisError,AuthenticationError ,ConnectionError) as error:
        print(error)
        return False


def add_user(username,password):
    user_info = {username:password}
    try:
        redis_conn.hset("UsersD",mapping=user_info)
        return True
    except (RedisError,AuthenticationError ,ConnectionError) as error:
        print(error)
        return False
