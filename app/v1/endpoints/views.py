
from flask import Flask, request, jsonify, make_response
from . import api
from .models import Products
product_class = Products()


class ProductsViews():
	@api.route('/products', methods=["GET"])
	def products():
	  """ Method to see all products."""
	  available_products = product_class.all_products()
	  return available_products

	@api.route('/products', methods=['POST'])
	def create():
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