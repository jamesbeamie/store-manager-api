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
  test_product={
        "product_id": 1,
        "product_name": "Denim",
        "price": "1600",
        "quantity": 100,
  }
  test_invalid={
        "product_id": 1,
        "product_name": " ",
        "price": " ",
        "quantity": 100,
  }
  def test_all_products(self):
      """Test if all products are returned"""
      response = self.client().get('/api/v1/products', 
        content_type='application/json')
      self.assertEqual( response.status_code, 200)      

  def test_create_product(self):
    """Test if new product is created and returns,201"""
    response = self.client().post('/api/v1/products', 
      data=json.dumps(self.test_product), 
      content_type='application/json')
    data = json.loads(response.data.decode())
    self.assertEqual( response.status_code, 201)
    self.assertEqual(data['message'], 'New product added.')

  def test_invalid_product(self):
    """Test if new product is created and returns,201"""
    response = self.client().post('/api/v1/products', 
      data=json.dumps(self.test_invalid), 
      content_type='application/json')
    data = json.loads(response.data.decode())
    self.assertEqual( response.status_code, 400)
    self.assertEqual(data['message'], 'Enter product name')

  def test_specific_product(self):
    """Test if specified product is returned and returns success code,200"""
    response = self.client().get('/api/v1/products/1',
      data=json.dumps(self.test_product), 
      content_type='application/json')
    self.assertEqual( response.status_code, 200)

  def test_mising_id(self):
    """Test if specified product is missing id"""
    response = self.client().get('/api/v1/products/', 
      content_type='application/json')
    self.assertEqual( response.status_code, 404)


class TestSales(TestApi):
  """Class to test products end points"""
  test_record={
        "sales_id": 1,
        "attendant": "James",
        "product": "Denim",
        "price": "1600",
        "quantity": 100
  }
  test_invalid_record={
        "sales_id": 1,
        "attendant": " ",
        "product": " ",
        "price": " ",
        "quantity": 100
  }
  def test_all_sales(self):
      """Test if all sales records are returned"""
      response = self.client().get('/api/v1/sales', 
        content_type='application/json')
      self.assertEqual( response.status_code, 200)

  def test_create_sales_record(self):
    """Test if new record is placed and returns success code,201"""
    response = self.client().post('/api/v1/sales', 
      data=json.dumps(self.test_record), 
      content_type='application/json')
    data = json.loads(response.data.decode())
    self.assertEqual( response.status_code, 201)
    self.assertEqual(data['message'], 'New record added.')

  def test_invalid_sales_record(self):
    """Test if new record is placed and returns success code,201"""
    response = self.client().post('/api/v1/sales', 
      data=json.dumps(self.test_invalid_record), 
      content_type='application/json')
    data = json.loads(response.data.decode())
    self.assertEqual( response.status_code, 400)
    self.assertEqual(data['message'], 'Enter product name')
    
  def test_specific_record(self):
    """Test if specified sales record is returned and returns success code,200"""
    response = self.client().get('/api/v1/sales/1',
      data=json.dumps(self.test_record), 
      content_type='application/json')
    self.assertEqual( response.status_code, 200)

  def test_records_id(self):
    """Test if specific sales record to fetch is missing id"""
    response = self.client().get('/api/v1/sales/', 
      content_type='application/json')
    self.assertEqual( response.status_code, 404)
    
if __name__ == "__main__":
  unittest.main()
