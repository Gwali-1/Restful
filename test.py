import json
import requests
from api import generate_auth_token


#sample test for the api endpoints using the requests module to send http requests, checks for expected response code in situations of success and failure


def test_cats_info():
    '''Given that when /cats is visited 
        it checks that response is valid
    '''
    r = requests.get("http://127.0.0.1:5000/api/cats/")
    
    assert  r.status_code == 200
    assert "status","Ok" in r.text




def test_cat_info():
    ''' Given that when /cats/<str:cat_name> is visited 
        it checks that response is valid 
    '''
    r = requests.get("http://127.0.0.1:5000/api/cats/Abyssinian-Cats")
    print(r.status_code)
    assert r.status_code == 200
    assert "status","Ok" in r.text

def test_add_cat():
    '''Given that when /cats/add/ is visited
       it checks that response code and valid response text
     '''
    r = requests.post("http://127.0.0.1:5000/api/cats/add",json={
         "name":"testcat",
         "info":"validate"

     })
    assert r.status_code == 200
    assert "testcat" in r.text
    assert "status","Ok" in r.text



def test_register_user():
    '''Given that when /add_user/ is visited
       it checks that response code is correct
    '''
    r = requests.post("http://127.0.0.1:5000/api/add_user",json={
         "username":"testman",
         "password":"validationman"

     })
    assert r.status_code == 200
    assert "status","Ok" in r.text
    assert "token" in r.text


def test_token_verification():
    '''Given that when /verify_token/ is visited with correct
        details , response code is correct
    '''
    auth = generate_auth_token("manjouer","lemon street")
    r = requests.post("http://127.0.0.1:5000/api/verify_token",json={
         "id":auth["id"],
         "token":auth["token"]

     })

    assert r.status_code == 200
    assert "Active" in r.text
    assert "status","Ok" in r.text



def test_false_token_verification():
    '''Given that when /verify_token/ is visited with wrong auth
        details , response code is correct
    '''
    r = requests.post("http://127.0.0.1:5000/api/verify_token",json={
         "id":"4532D",
         "token":"kjdbsuw4844bdbewgwew7"

     })

    assert r.status_code == 200
    assert "Expired" in r.text
    assert "status","Bad" in r.text



def test_resource():
    '''Given that when /resource/ is visited
    with correct auth info ,response code is correct
    '''
    auth = generate_auth_token("manjouer","lemon street")
    r = requests.post("http://127.0.0.1:5000/api/resource",json={
         "id":auth["id"],
         "token":auth["token"]

     })

    assert r.status_code == 200
    assert "status","Ok" in r.text


def test_resource_false():
    '''Given that when /resource/ is visited
    with wrong auth info ,response code is correct
    '''
    r = requests.post("http://127.0.0.1:5000/api/resource",json={
         "id":"4532D",
         "token":"kjdbsuw4844bdbewgwew7"

     })
    assert r.status_code == 401
    assert "status","Bad" in r.text



