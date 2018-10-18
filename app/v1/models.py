
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
        """Create record"""
        self.product = {}
        self.product_id = len(self.products_list)

        self.product['product_id'] = self.product_id + 1
        self.product['product_name'] = product_name
        self.product['price'] = price
        self.product['quantity'] = quantity
        #check for duplicate products
        for product in self.products_list:
            if self.product['product_name'] in product['product_name']:
                return jsonify({"message":"Product already exists"}), 400
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

    def create_record(self, attendant, product, price, quantity):
        """Create record"""
        self.record = {}
        self.sales_id = len(self.sales_list)

        self.record['sales_id'] = self.sales_id + 1
        self.record['attendant'] = attendant
        self.record['product'] = product
        self.record['price'] = price
        self.record['quantity'] = quantity
        res = self.sales_list.append(self.record)
        return jsonify({"message": "New record added."}), 201

    def specific_record(self, sales_id):
        """The function returns a specific sales record, specified by id"""
        for record in self.sales_list:
            if record['sales_id'] == sales_id:
                return jsonify({"Sales record":record}), 200
