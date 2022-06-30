from redis import RedisError
from redis import AuthenticationError
from c import creatapp
from redis import StrictRedis
from flask_restful import Resource,Api,abort,reqparse
import secrets


config = {"redis_host":"localhost","redis_port":6379}
redis_conn = StrictRedis(config["redis_host"],config["redis_port"],decode_responses=True)
app = creatapp()
api = Api(app)



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
            return True
    return False



def  generate_auth_token(username,password):
    auth_token = secrets.token_urlsafe()
    auth_id = secrets.token_hex(2)
   
    if validate_user_password(username,password):
        try:
            redis_conn.set(auth_id,auth_token)
            redis_conn.expire(auth_id,2000)
            return {"id":auth_id,"token":auth_token}
        except (RedisError,AuthenticationError ,ConnectionError) as error:
            print(error)
            return False
    return False


def add_user(username,password):
    user_info = {username:password}
    if username in redis_conn.hgetall("UsersD").keys():
        return 5
    try:
        redis_conn.hset("UsersD",mapping=user_info)
        return True
    except (RedisError,AuthenticationError ,ConnectionError) as error:
        print(error)
        return False



Cats = {
    "Devon-Rex-Cats":"""
    The Devon Rex is a relatively newer breed of cats, discovered by accident in the region of Devonshire, England, in 1960 and has been called many things: a pixie cat,
    an alien cat, a cat that looks like an elf — or a bat. It is also known to behave more like a dog than like a cat.
    """,
    "Abyssinian-Cats":"""
    Abys, as they are lovingly called, are elegant and regal-looking, easy to care for and make ideal pets for cat lovers.
    Lively and expressive, with slightly wedge-shaped heads, half-cupped ears, medium length bodies and well-developed muscles,
    Abyssinians have long, slender legs and their coats are short and close-lying to their bodies
    """
}



#reqparse configuration for user auth
username_password_parser = reqparse.RequestParser()
username_password_parser.add_argument("username",help ="Username is not a string",required=True)
username_password_parser.add_argument("password",help="password arguement provided not a string",required=True)


#reqparse configuration for add_cat class 
cat_info_parser = reqparse.RequestParser(bundle_errors=True)
cat_info_parser.add_argument("name",required=True)
cat_info_parser.add_argument("info",required=True)


#reqparse config for token and id auth
token_auth_parser = reqparse.RequestParser()
token_auth_parser.add_argument("id",help = "provide verification id",required=True)
token_auth_parser.add_argument("token",help= "provide verification token",required=True)




#endpoints for Cat resource
class cats_info(Resource):
    def get(self):
        if Cats:
            return {"status":"Ok","Cats":Cats},200

        return {"status":"Bad","Description":"Something Went wrong"},501
            
class cat_info(Resource):
    def get(self,cat_name):
        if cat_name in Cats.keys():
            return {"status":"Ok","name":cat_name,"info":Cats[cat_name].strip()},200
        return {"status":"Bad","Description":"No resource match"},401

class add_cat(Resource):
    def post(self):
        args = cat_info_parser.parse_args(strict=True)
        if args["name"] in Cats.keys():
            Cats[args["name"]] = args["info"]
            return {"status":"Ok","Description":f"Entry for {args['name']} already existed hence was updated","Cats":Cats},200

        Cats[args["name"]] = args["info"]
        return  {"status":"Ok","Description":"Added Succesfuly","Cats":Cats},200




class register_user(Resource):
    def post(self):
        args = username_password_parser.parse_args()
        username = args["username"]
        password = args["password"]
        user = add_user(username,password)
        if user == 5:
            #username already exist
            return  {"status":"Bad","Description":"Username taken.Could not add user"},401
        if user:
            #passes
            auth_token = generate_auth_token(username,password)
            redis_conn.set(auth_token["token"],username)
            redis_conn.expire(auth_token["token"],2000)
            return {"status":"Ok","Description":"User added successfully","auth":auth_token,"token expiration":10},200

        return  {"status":"Bad","Description":"Could not add user.Try again later!"},401
    

class token_verifaction(Resource):
    def post(self):
        args = token_auth_parser.parse_args()
        id = args["id"]
        token = args["token"]
        validation = validate_user_token(token,id)
        if validation:
            return {"status":"Ok","User":redis_conn.get(token),"Token":"Active"},200

        return {"status":"Bad","User":redis_conn.get(token),"Token":"Expired"},200
        


class resource(Resource):
    def post(self):
        args = token_auth_parser.parse_args()
        validation = validate_user_token(args["token"],args["id"])
        if validation:
            return {"status":"Ok","data":"Good endpoint"},200
        return {"status":"Bad","Desccription":"Could not verify token and id. Check to see if token is still active or input is correct"},401







#cat resource routes
api.add_resource(cats_info,"/cats/")
api.add_resource(cat_info,"/cats/<string:cat_name>")
api.add_resource(add_cat,"/cats/add")

#adding user
api.add_resource(register_user,"/add_user/")


#user account  verification
api.add_resource(token_verifaction,"/verify_token/")

#resource endpoint with verification
api.add_resource(resource,"/resource/")
if (__name__) == "__main__":
    app.run(debug=True)