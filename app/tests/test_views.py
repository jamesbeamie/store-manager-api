"""The module has test for the api"""
import unittest
from  flask_jwt_extended import create_access_token
import os
import json
#local imports
from app import create_app
"""the dictionaries are used for testing endpoints"""
#class for the unittests
user_token = None
admin_token = None
class TestApi(unittest.TestCase):
  """The class with individual tests for individual endpoints"""
  def setUp(self):
    """Set up test client"""
    self.app = create_app(config_name="testing")
    self.client = self.app.test_client

class TestUsers(TestApi):
  test_adm_exist={
      "username": "james",
      "password": "andela",
      "confirmpass": "andela",
      "addres": "kitale",
      "role":"admin"
      }
  test_reg_adm={
      "username": "james",
      "password": "andela",
      "confirmpass": "andela",
      "addres": "kitale",
      "role":"admin"
      }
  test_reg_user_role={
      "username": "masaa",
      "password": "andela",
      "confirmpass": "andela",
      "addres": "kitale",
      "role":"role"
      }
  test_reg_valid_user={
      "username": "m",
      "password": "andela",
      "confirmpass": "andela",
      "addres": "kitale",
      "role":"attendant"
      }
  test_reg_attendant={
      "username": "masaa",
      "password": "andela",
      "confirmpass": "andela",
      "addres": "kitale",
      "role":"attendant"
      }
  test_login_adm={
  "username":"james",
  "password":"andela"
  }
  test_login_user={
  "username":"masaa",
  "password":"andela"
  }

  def test_admin_exist(self):
    response = self.client().post('/api/v2/admin/signup', 
      data=json.dumps(self.test_reg_adm), 
      content_type='application/json')
    self.assertEqual( response.status_code, 201)

  def test_reg_admin(self):
    response = self.client().post('/api/v2/admin/signup', 
      data=json.dumps(self.test_reg_adm), 
      content_type='application/json')    
    res = json.loads(response.data)
    self.assertEqual(res["message"], "Username already taken")
    self.assertEqual( response.status_code, 400)

  def test_adm_login(self):
    with self.app.app_context():
      response = self.client().post('/api/v2/login', 
        data=json.dumps(self.test_login_adm), 
        content_type='application/json')   
      res = json.loads(response.data) 
      admin_token =  create_access_token(self.test_login_adm.get("username"))
      self.assertEqual(res["message"], "Username not recognized Please register")

      self.assertEqual( response.status_code, 200)
      self.assertNotEqual(response.json, admin_token)