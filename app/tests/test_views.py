"""The module has test for the api"""
import unittest
import os
import json
#from flask_testing import TestCase
from app import create_app
"""the dictionaries are used for testing endpoints"""
#class for the unittests
class TestApi(unittest.TestCase):
  """The class with individual tests for individual endpoints"""
  def setUp(self):
    """Set up test client"""
    self.app = create_app(config_name="testing")
    self.client = self.app.test_client

class TestProducts(TestApi):
  """Class to test products end points"""
  def test_all_products(self):
      """Test if all products are returned"""
      response = self.client().get('/api/v1/products', 
        content_type='application/json')
      self.assertEqual( response.status_code, 200)
    
if __name__ == "__main__":
  unittest.main()
