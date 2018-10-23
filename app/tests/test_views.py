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
      "username": "James",
      "password": "andela",
      "confirmpass": "andela",
      "addres": "kitale",
      "role":"admin"
      }
  test_reg_adm={
      "username": "jake",
      "password": "andela",
      "confirmpass": "andela",
      "addres": "kitale",
      "role":"admin"
      }

  def test_admin_exist(self):
    response = self.client().post('/api/v2/admin/signup', 
      data=json.dumps(self.test_adm_exist), 
      content_type='application/json')
    self.assertEqual( response.status_code, 201)

  def test_reg_admin(self):
    response = self.client().post('/api/v2/admin/signup', 
      data=json.dumps(self.test_reg_adm), 
      content_type='application/json')
    self.assertEqual( response.status_code, 200)


    
if __name__ == "__main__":
  unittest.main()
