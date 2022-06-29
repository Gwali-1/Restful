from operator import imod
from flask import Flask



def creatapp(config):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "vjvvewm"

    return app
  
