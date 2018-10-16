
from flask import jsonify, request, make_response

class Products(object):
    def __init__(self):
        """ Initialize empty products list"""  
        self.products_list = []        

    def all_products(self):
        """ fetch all products """
        if len(self.products_list) > 0:
            return make_response(jsonify({"Products": self.products_list}))
        return make_response(jsonify({"message":"No products."}), 200)

    def create_product(self, product_name, price, quantity):
        """Create order"""
        self.product = {}
        self.product_id = len(self.products_list)

        self.product['product_id'] = self.product_id + 1
        self.product['product_name'] = product_name
        self.product['price'] = price
        self.product['quantity'] = quantity
        res = self.products_list.append(self.product)
        return jsonify({"message": "New product added."}), 201

    
    def specific_product(self, product_id):
        """The function returns a specific order, specified by id"""
        for product in self.products_list:
            if product['product_id'] == product_id:
                return jsonify({"Product":product}), 200
                
class Sales(object):
    def __init__(self):
        """ Initialize empty sales list"""  
        self.sales_list = []        

    def all_sales(self):
        """ fetch all products """
        if len(self.sales_list) > 0:
            return make_response(jsonify({"Sales": self.sales_list}))
        return make_response(jsonify({"message":"No sales made."}), 200)




