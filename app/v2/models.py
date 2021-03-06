
from flask import jsonify, request, make_response
import psycopg2
import jwt
import datetime
from  flask_jwt_extended import create_access_token
import os
from ..dbconect import dbcon


class User(object):
    """
    This is a class for functionality related to the users
    """
    def __init__(self):
        """ Initialize connection to database"""

    def invalid_user(self, username):
        """Checks if user exists"""
        con = dbcon()
        cur = con.cursor()
        cur.execute("SELECT * FROM my_users WHERE username=%(username)s",\
         {'username':username})
        rows = cur.rowcount
        if rows > 0:
            return True
        return False

    def is_admin(self, username):
        """checks if the user is admin user"""
        con = dbcon()
        cur = con.cursor()
        cur.execute("SELECT * FROM my_users WHERE username=%(username)s",\
            {"username":username})
        res = cur.fetchone()
        if res[5].lower() == 'admin':
            return True
        return False

    def create_admin(self, username, password, confirmpass, addres, role):
        """Create admin"""
        if self.invalid_user(username):
            return jsonify({"message":"Username already taken"}),400
        con = dbcon()
        cur = con.cursor()
        #checks if admin already exists
        cur.execute("SELECT * FROM my_users WHERE role=%(role)s",\
            {"role":role})
        row = cur.rowcount
        available = cur.fetchall()
        if available:
            return make_response(jsonify({"message":"Admin exists"})), 400
        cur.execute("INSERT INTO my_users (username,password,confirmpass,addres,role) \
            VALUES (%(username)s,%(password)s,%(confirmpass)s,%(addres)s,%(role)s);",\
            {'username':username,'password':password, \
            'confirmpass':confirmpass,'addres':addres,'role':role})
        con.commit()
        return make_response(jsonify({"message":"admin created"}), 201)
    
    def reg_attendant(self, username, password, confirmpass, addres, role):
        """Create users"""
        if self.invalid_user(username):
            return jsonify({"message":"Username already taken"}),400
        else:
            con = dbcon()
            cur = con.cursor()
            cur.execute("INSERT INTO my_users (username, password, confirmpass, \
                addres, role) VALUES (%(username)s,%(password)s,\
                %(confirmpass)s,%(addres)s,%(role)s);",\
                {'username':username,'password':password,'confirmpass':confirmpass,\
                'addres':addres,'role':role})
            con.commit()
            return make_response(jsonify({"message":"user created successfully"}), 201)

    def view_users(self):
        """fetches all the registered users"""
        con = dbcon()
        cur = con.cursor()
        cur.execute("SELECT * FROM my_users")
        res = cur.fetchall()
        user_list=[]
        for user in res:
            user_det = {
            'user_id':user[0],
            'username':user[1],
            'password':user[2],
            'confirmpass':user[3],
            'addres':user[4],
            'role':user[5]
            }
            user_list.append(user_det)
        return jsonify({'Users': user_list}), 200

    def login(self, username, password):
        """This is to check for a user and sign them in"""
        if self.invalid_user(username):
            con = dbcon()
            cur = con.cursor()
            cur.execute("SELECT * FROM my_users WHERE username=%(username)s \
                and password=%(password)s",{'username':username, 'password':password})
            user = cur.fetchone()
            if user:
                return jsonify({"Usertoken":create_access_token(username), \
                    "message":"Logged in successfully", \
                    "identity":user[1]}), 200
            return jsonify({"message":"You entered a wrong password"})
        return jsonify({"message":"Username not recognized Please register"})

class Product(object):
    """
    This is a class for manipulating products
    """
    def in_stoke(self, product_name):
        #check if product is in stoke
        con = dbcon()
        cur = con.cursor()
        cur.execute("SELECT * FROM products WHERE product_name=%(product_name)s",\
            {"product_name":product_name})
        res = cur.fetchone()
        if res:
            if res[3] > 10:
                return True
            return False
        return jsonify({"message":"Could not find product in catalog"})

    def create_product(self, product_name,price,quantity):
        """Create new product"""
        con = dbcon()
        cur = con.cursor()
        #checks if product already exists
        cur.execute("SELECT * FROM products WHERE product_name=%(product_name)s",\
            {"product_name":product_name})
        available = cur.fetchall()
        if available:
            return make_response(jsonify({"message":"Product already in stoke."})), 200
        cur.execute("INSERT INTO products (product_name,price,quantity)\
         VALUES (%(product_name)s,%(price)s,%(quantity)s);",\
         {'product_name':product_name,'price':price,'quantity':quantity})
        con.commit()
        return make_response(jsonify({"message":"Product added in catalog"}),201)

    def modify_product(self, product_id,product_name,price,quantity):
        """This function edits the product, takes user inputs in json form"""
        con = dbcon()
        cur = con.cursor()
        cur.execute("SELECT * FROM products WHERE product_id=%(product_id)s",\
            {"product_id":product_id})
        found_id = cur.fetchall()
        if found_id:
            cur.execute("UPDATE  products SET product_name=%s, price=%s, \
            quantity= %s WHERE product_id=%s",\
            (product_name, price, quantity, product_id))
            con.commit()
            return make_response(jsonify({'message': 'Product modified'}), 200)
        return jsonify({"message":"Couldn't find product ID"})

    def delete_product(self, product_id):
        """This function deletes a product"""
        con = dbcon()
        cur = con.cursor()
        cur.execute("SELECT * FROM products WHERE product_id=%(product_id)s",\
            {"product_id":product_id})
        found_id = cur.fetchall()
        if found_id:
            cur.execute("DELETE FROM products WHERE product_id=%(product_id)s",\
                {'product_id':product_id})
            con.commit()
            return jsonify({'message': 'Product deleted successfully'})
        return jsonify({"message":"Couldn't find product ID"}) 

    def get_products(self):
        """A unction to fetch all products"""
        con = dbcon()
        cur = con.cursor()
        cur.execute("SELECT * FROM products;")
        res = cur.fetchall()
        if res:
            prdcts=[]
            for prodct_item in res:
                picked_prdct = {
                'product_id':prodct_item[0],
                'product_name':prodct_item[1],
                'price':prodct_item[2],
                'quantity':prodct_item[3]
                }
                prdcts.append(picked_prdct)
            return jsonify({"Products": prdcts}), 200
        return jsonify({"message":"No products in store"})

    def specific_product(self, product_id):
        """The function gets a specific product"""
        con = dbcon()
        cur = con.cursor()
        cur.execute("SELECT * FROM products WHERE product_id=%(product_id)s",\
            {'product_id':product_id})
        res = cur.fetchall()
        #check if the product exists
        if res:
            my_product=[]
            for a_product in res:
                product = {
                'product_id':a_product[0],
                'product_name':a_product[1],
                'price':a_product[2],
                'quantity':a_product[3]
                }
                my_product.append(product)
            return make_response(jsonify({"Products":my_product}), 200)
        return jsonify({"message":"could not find product with that id"}), 400


class Sales(object):
    """
    This is a class to manipulate sales
    """
    def create_record(self, attendant,product_name,price,quantity):
        """Create sales"""
        con = dbcon()
        cur = con.cursor()
        cur.execute("SELECT quantity FROM products WHERE product_name=%(product_name)s",\
            {'product_name':product_name})
        #qty_left  checks if the product is in catalog by getting its qty
        qty_left = cur.fetchone()
        if qty_left:
            cur.execute("INSERT INTO sales (attendant,product_name,price,quantity)\
             VALUES (%(attendant)s,%(product_name)s,%(price)s,%(quantity)s);",\
             {'attendant':attendant,'product_name':product_name,'price':price,\
             'quantity':quantity})
            con.commit()
            new_qty = qty_left[0] - int(quantity)
            cur.execute("UPDATE products SET quantity=%s WHERE product_name=%s",\
                (new_qty,product_name))
            con.commit()
            return make_response(jsonify({"message":"New record created"}),201)
        return jsonify({"message":"The product is not in catalog"}), 200

    def specific_record(self, attendant):
        """The function gets a record specified by the id"""
        con = dbcon()
        cur = con.cursor()
        cur.execute("SELECT * FROM sales WHERE attendant=%(attendant)s",\
            {'attendant':attendant})
        res = cur.fetchall()
        if res:
            sales_rec=[]
            for a_record in res:
                user_record = {
                'sales_id':a_record[0],
                'attendant':a_record[1],
                'product_name':a_record[2],
                'price':a_record[3],
                'quantity':a_record[4]
                }
                sales_rec.append(user_record)
            return make_response(jsonify({"Record":sales_rec}), 200)
        return jsonify({"message":"could not find record with that id"}), 400

    def all_sales(self, username):
        """ fetch all sales records"""
        con = dbcon()
        cur = con.cursor()
        cur.execute("SELECT * FROM sales;")
        res = cur.fetchall()
        sales_records=[]
        for a_sale in res:
            record = {
            'sales_id':a_sale[0],
            'attendant':a_sale[1],
            'product_name':a_sale[2],
            'price':a_sale[3],
            'quantity':a_sale[4]
            }
            sales_records.append(record)
        return jsonify({"Records": sales_records}), 200

