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

 
 