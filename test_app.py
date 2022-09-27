import pytest
from app import app
from flask.testing import FlaskClient
import json
 
 
 
def test_index_route(api):
   response =api.get('/')
   assert response.status == "200 OK"
 
def test_home(api):
   resp = api.get('/')
   assert b"Hello!" in resp.data


 
 
@pytest.fixture(scope='module')
def flask_app():
   with app.app_context():
       yield app
 
 
@pytest.fixture(scope='module')
def client(flask_app):
   app = flask_app
   ctx = app.test_request_context()
   ctx.push()
   app.test_client_class = FlaskClient
   return app.test_client()
 
 
def test_index_page__logged_in(client):
   with client:
       client.post('/login', data=dict(username='user', password='test'))
       res = client.get('/')
       assert res.status_code == 200

 
def test_home_bad_http_method(api):
   resp = api.post('/logout')
   assert resp.status_code == 500


import json
def test_add_user(api):
    """Ensure a new user can be added to the database."""
    with api as client:
        response = client.post(
            '/register',
            data=json.dumps(dict(
                username='chess',
                email='naka@real.com'
            )),
            content_type='application/json',
        )
        data = json.loads(response.data.decode())
        assert response.status_code == 200
     
        assert b"something went wrong!" in response.data
      
 
def test_reg_user(api):
   """Ensure a new user can be added to the database."""
   with api as client:
       response = client.post(
           '/register',
           data=json.dumps(dict(
               username='dhar',
               email="dh89@gnail.co",
               password='learny3'
           )),
           content_type='application/json',
       )
       data = json.loads(response.data.decode())
       assert response.status_code == 200
       assert b"user created" in response.data
