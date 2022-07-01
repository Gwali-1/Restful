
# RESTFUL
_This  is an implementation of rest api using flask and flask restful.This implementation makes use of redis which is an in memory data store._
_Here it is used as a database to hold user auth details._
_I used redis mainly because the data im working with is light weigth and a traditional relational database would be an overkill in my opinion._
_With redis i store user information such as username and password(which is hashed) in a `redit hash` , which is a data type in redis where values are stored as key value pairs like a python dictionary._
_Also user tokens generated are stored under a key which is an id with a expiration time. Tokens generated for users are under expiration time. Tokens are returned to users with the time they expire as well as the id which together with token is used for authentication to access endpoints which have a security layer._


Attached to the repo is a couple of unit test written to test the various endpoints for this api.`test.py`.
All test passed succesfully at the time this was written.
several imorovements could be added to this api implementaion, for example adding a time restriction to how many tokens could be requested by a particular account.

* To run the tests
```
 pytest test.py
```




## Installation
After cloning the repo

* set up a virtual environment
* install requirements.txt 

```
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt

```

if you are on windows

```
$ virtualenv venv
$ venv\Scripts\activate
(venv) $ pip install -r requirements.txt

```


## Running The Server

* to run the server
make sure you are in the project directory
```
python api.py
```
* from a different terminal window , you can then send request to the server running locally




## Documentation For Api


* GET /api/cats

Returns a json object containing fields of cat names and information about them.
On success the status code 200 is returned. This endpoint doesnt require any authentication.
On failure status code 501 is returned indicating the resource could not be returned. This will most definitley be a server 
error as no auth is required for this endpoint.




* GET /api/cats/<string:cat_name>

Returns a json object with information for the the requested cat.
On success the status code is 200, a json object with fields  `status` equal to "Ok", `name` equal to cat name  and `info` which is a description of the cat is returned.
On failure, in a situation where there is no match for requested cat, status code 401 is returned. Also a json object is returned with fild `status` equal to "Bad"
and `Description` with and error message.


* POST /api/cats/add

Adds a new cat with a description and returns the updated cat database.
The request body must be a json object that defines fields `name` and `info` . Fields are required!
* The request body posted must be of form json or server won't process the request.
On success status code 200 is returned  together with a json object containing message that entry has been added. If name of cat already already exist it is updated and a message telling user so is sent back.
On failure, if  for some reason entry could not be added or an error while adding the entry, status code 501 is returned with a json object containing description of situation.





* POST api/add_user

Adds a new user and returns an generated id and token to be used as auth verification for endpoints that require authentication.
The request body must be a json object that defines fields `username` and `password`. Fields are required!
* The request body posted must be of form json or server won't perform process
* The username and password are stored and account created for user
The password is hashed first.
On success status code 200 is returned together with a json object containing generated id and token and expiration time for token in seconds.
On failure, in situations where username is already taken, a status code 401 is returned with a json object with a description of the situation.
On failure, when user account could not be created and user not added, status code 501 is returned with with a json object with a description of the situation.


* POST api/verify_token
Returns a json object with status of a token, whether active or expired
* The request body posted must be of form json or server won't acknowledge request.
The request body must be a json object that defines fields `id` and `token`. Fields are required!
On success status code 200 is returned  together with a json object containing field `status` equal to `OK` , username of account and token status `Active`.
On failure , in situations where token is expired, a status code 200 is still returned with a json object with token status `Expired`.



* POST api/resource

Returns a json object with a `data` field on success.
This endpoint requires authentication hence request body posted must be of form json that defines fields `id` and `token` equal to auth details returned to user on creation of account(token and id).
Fields are required!
On success status code 200 is returned  together with a json object containing field `Data` and `status`(equal to `Ok`).
On failure, in situations where auth details provided are wrong or token is expired, a status code 401 is returned with a json object with a description of the situation.


## Examples
* The following requests are sent using curl


* GET /api/cats

```
curl -i -X  GET  http://127.0.0.1:5000/api/cats/

HTTP/1.1 200 OK
Server: Werkzeug/2.1.2 Python/3.10.4
Date: Thu, 30 Jun 2022 20:13:01 GMT
Content-Type: application/json
Content-Length: 764
Connection: close

{
    "status": "Ok",
    "Cats": {
        "Devon-Rex-Cats": "\n    The Devon Rex is a relatively newer breed of cats, discovered by accident in the region of Devonshire, England, in 1960 and has been called many things: a pixie cat,\n    an alien cat, a cat that looks like an elf \u2014 or a bat. It is also known to behave more like a dog than like a cat.\n    ",
        "Abyssinian-Cats": "\n    Abys, as they are lovingly called, are elegant and regal-looking, easy to care for and make ideal pets for cat lovers.\n    Lively and expressive, with slightly wedge-shaped heads, half-cupped ears, medium length bodies and well-developed muscles,\n    Abyssinians have long, slender legs and their coats are short and close-lying to their bodies\n    "
    }
}


```

* GET /api/cats/<string:cat_name>
```
curl -i -X  GET  http://127.0.0.1:5000/api/cats/Devon-Rex-Cats

HTTP/1.1 200 OK
Server: Werkzeug/2.1.2 Python/3.10.4
Date: Thu, 30 Jun 2022 20:15:51 GMT
Content-Type: application/json
Content-Length: 359
Connection: close

{
    "status": "Ok",
    "name": "Devon-Rex-Cats",
    "info": "The Devon Rex is a relatively newer breed of cats, discovered by accident in the region of Devonshire, England, in 1960 and has been called many things: a pixie cat,\n    an alien cat, a cat that looks like an elf \u2014 or a bat. It is also known to behave more like a dog than like a cat."
}

```

* POST /api/cats/add

```
curl -i -X POST -H "Content-Type: application/json" -d '{"name":"testcat","info":"the best type of cats"}' http://127.0.0.1:5000/api/cats/add

HTTP/1.1 200 OK
Server: Werkzeug/2.1.2 Python/3.10.4
Date: Thu, 30 Jun 2022 21:18:01 GMT
Content-Type: application/json
Content-Length: 847
Connection: close

{
    "status": "Ok",
    "Description": "Added Succesfuly",
    "Cats": {
        "Devon-Rex-Cats": "\n    The Devon Rex is a relatively newer breed of cats, discovered by accident in the region of Devonshire, England, in 1960 and has been called many things: a pixie cat,\n    an alien cat, a cat that looks like an elf \u2014 or a bat. It is also known to behave more like a dog than like a cat.\n    ",
        "Abyssinian-Cats": "\n    Abys, as they are lovingly called, are elegant and regal-looking, easy to care for and make ideal pets for cat lovers.\n    Lively and expressive, with slightly wedge-shaped heads, half-cupped ears, medium length bodies and well-developed muscles,\n    Abyssinians have long, slender legs and their coats are short and close-lying to their bodies\n    ",
        "testcat": "the best type of cats"
    }
}
```

* POST api/add_user

```
curl -i -X POST -H "Content-Type: application/json" -d '{"username":"TestUserr","password":"lemon street"}' http://127.0.0.1:5000/api/add_user/

HTTP/1.1 200 OK
Server: Werkzeug/2.1.2 Python/3.10.4
Date: Thu, 30 Jun 2022 21:28:45 GMT
Content-Type: application/json
Content-Length: 205
Connection: close

{
    "status": "Ok",
    "Description": "User added successfully",
    "auth": {
        "id": "002d",
        "token": "JJ6lG9A9oZsAgmu17am817X_wSrJkqNnm6w8ZHaLZhg"
    },
    "token expiration time": 3600
}

```

* For when username is taken

```
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/2.1.2 Python/3.10.4
Date: Thu, 30 Jun 2022 21:22:59 GMT
Content-Type: application/json
Content-Length: 80
Connection: close

{
    "status": "Bad",
    "Description": "Username taken.Could not add user"
}
```

* POST api/verify_token


```
curl -i -X POST -H "Content-Type: application/json" -d '{"id":"002d","token":"JJ6lG9A9oZsAgmu17am817X_wSrJkqNnm6w8ZHaLZhg"}' http://127.0.0.1:5000/api/verify_token/ 

HTTP/1.1 200 OK
Server: Werkzeug/2.1.2 Python/3.10.4
Date: Thu, 30 Jun 2022 21:30:02 GMT
Content-Type: application/json
Content-Length: 71
Connection: close

{
    "status": "Ok",
    "User": "TestUserr",
    "Token": "Active"
}
```
* For when token is expires

```
HTTP/1.1 200 OK
Server: Werkzeug/2.1.2 Python/3.10.4
Date: Thu, 30 Jun 2022 21:24:43 GMT
Content-Type: application/json
Content-Length: 64
Connection: close

{
    "status": "Ok",
    "User": TestUserr,
    "Token": "Expired"
}

```


* POST api/resource

```
curl -i -X POST -H "Content-Type: application/json" -d '{"id":"002d","token":"JJ6lG9A9oZsAgmu17am817X_wSrJkqNnm6w8ZHaLZhg"}' http://127.0.0.1:5000/api/resource/

HTTP/1.1 200 OK
Server: Werkzeug/2.1.2 Python/3.10.4
Date: Thu, 30 Jun 2022 21:31:59 GMT
Content-Type: application/json
Content-Length: 52
Connection: close

{
    "status": "Ok",
    "data": "Good endpoint"
}
```
* For when auth details are wrong

```
HTTP/1.1 401 UNAUTHORIZED
Server: Werkzeug/2.1.2 Python/3.10.4
Date: Thu, 30 Jun 2022 21:32:51 GMT
Content-Type: application/json
Content-Length: 136
Connection: close

{
    "status": "Bad",
    "Desccription": "Could not verify token and id. Check to see if token is still active or input is correct"
}
```
