
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


