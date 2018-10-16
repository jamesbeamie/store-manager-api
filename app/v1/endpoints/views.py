
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