from flask import Flask



def creatapp():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "vjvvewm"

    return app
  
