
from flask import Flask, request, jsonify, make_response
from . import api
from .models import Products, Sales
product_class = Products()
sales_class = Sales()

def validate_product(data):
    """Check to validate user input """
    try:
        #check if the product name is provided
        if " " in data['product_name']:
            return "Enter product name"
        # Check for a reasonable product name
        elif len(data['product_name']) < 2:
        	return "Invalid product name"
        # check if price for the product is valid
        elif " " in data['price']:
            return "Invalid product price"
        # check if quantity is enough for stoke
        elif data['quantity'] < 10:
            return "Quantity not enough for stoke"
        else:
            return "valid"
    except Exception as error:
        return "please provide all the fields, missing " + str(error)

def validate_record(data):
    """Check to validate user input """
    try:
        #check if the product name is provided
        if " " in data['product']:
            return "Enter product name"
        # Check for a reasonable product name
        elif len(data['product']) < 2:
        	return "Invalid product name"
        #check if the attendants name is provided
        elif " " in data['attendant'] or len(data['attendant']) < 3:
            return "Invalid attendant name"
        # check if price for the product is valid
        elif " " in data['price']:
            return "Invalid product price"
        # check if quantity is enough for stoke
        elif data['quantity'] < 1:
            return "Quantity can not be null or zero"
        else:
            return "valid"
    except Exception as error:
        return "please provide all the fields, missing " + str(error), 

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
		res = validate_product(data)
		product_name = data['product_name']
		price = data['price']
		quantity = data['quantity']
		if res == 'valid':
			result = product_class.create_product(product_name, price, quantity)
			return result
		return jsonify({"message":res}),400
	
	@api.route('/products/<int:product_id>', methods=['GET'])
	def specific(product_id, **kwargs):
		"""method to return a specific product"""
		result = product_class.specific_product(product_id)
		if result:
			return result
		return jsonify({"message":"The product ID doesn't exist"})

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
		res = validate_record(data)
		attendant = data['attendant']
		product = data['product']
		price = data['price']
		quantity = data['quantity']
		if res == 'valid':
			result = sales_class.create_record(attendant, product, price, quantity)
			return result
		return jsonify({"message":res}),400

	@api.route('/sales/<int:sales_id>', methods=['GET'])
	def specific_sales(sales_id, **kwargs):
		"""method to return a specific sales record"""
		result = sales_class.specific_record(sales_id)
		if result:
			return result
		return jsonify({"message":"The product ID doesn't exist"}) 