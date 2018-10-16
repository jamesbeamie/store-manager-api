
from flask import Flask, request, jsonify, make_response
from . import api
from .models import Products, Sales
product_class = Products()
sales_class = Sales()


class ProductsViews():
	@api.route('/products', methods=["GET"])
	def products():
	  """ Method to see all products."""
	  available_products = product_class.all_products()
	  return available_products

	@api.route('/products', methods=['POST'])
	def create():
		"""Add a product to inventory"""
		data = request.get_json()
		product_name = data['product_name']
		price = data['price']
		quantity = data['quantity']
		result = product_class.create_product(product_name, price, quantity)
		return result
	
	@api.route('/products/<int:product_id>', methods=['GET'])
	def specific(product_id, **kwargs):
		"""method to return a specific product"""
		result = product_class.specific_product(product_id)
		return result

class SalesViews():
	@api.route('/sales', methods=["GET"])
	def sales():
	  """ Method to see all products."""
	  sales_records = sales_class.all_sales()
	  return sales_records

	@api.route('/sales', methods=['POST'])
	def create_sales_record():
		"""Create a new sales record"""
		data = request.get_json()
		attendant = data['attendant']
		product = data['product']
		price = data['price']
		quantity = data['quantity']
		result = sales_class.create_record(attendant, product, price, quantity)
		return result