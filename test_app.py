import pytest
from app import app
from flask.testing import FlaskClient
import json
 
 
 
def test_index_route(api):
   response =api.get('/')
   assert response.status == "200 OK"
