from . import creatapp
from redis import StrictRedis
from flask_restful import Resource,Api

config = {"redis_host":"localhost","redis_port":6379}
redis_conn = StrictRedis(config["redis_host"],config["redis_port"],decode_responses=True)

app = creatapp()