
from flask import jsonify, request, make_response
import psycopg2
import jwt
import datetime
from functools import wraps
from  flask_jwt_extended import create_access_token
import os
from ..dbconect import dbcon


class User(object):
    def __init__(self):
        """ Initialize connection to database"""
        #self.con = dbcon()

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
        #if admin already exists
        cur.execute("SELECT * FROM my_users WHERE role=%(role)s",\
            {"role":role})
        row = cur.rowcount
        available = cur.fetchall()
        if available:
            return make_response(jsonify({"Message":"ADM exists"})), 400
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

    def login(self, username, password):
        if self.invalid_user(username):
            con = dbcon()
            cur = con.cursor()
            cur.execute("SELECT * FROM my_users WHERE username=%(username)s \
                and password=%(password)s",{'username':username, 'password':password})
            user = cur.fetchone()
            if user:
                return jsonify({"User token":create_access_token(username)}), 200
            return jsonify({"message":"You entered a wrong password"})
        return jsonify({"message":"Username not recognized Please register"})

class Product(object):

    def create_product(self, product_name,price,quantity):
        """Create new product"""
        con = dbcon()
        cur = con.cursor()
        #if product already exists
        cur.execute("SELECT * FROM products WHERE product_name=%(product_name)s",\
            {"product_name":product_name})
        available = cur.fetchall()
        if available:
            return make_response(jsonify({"Message":"Product already in stoke."})), 200
        cur.execute("INSERT INTO products (product_name,price,quantity)\
         VALUES (%(product_name)s,%(price)s,%(quantity)s);",\
         {'product_name':product_name,'price':price,'quantity':quantity})
        con.commit()
        return make_response(jsonify({"message":"Product added in catalog"}),201)

    def modify_product(self, product_id,product_name,price,quantity):
        """This function edits the order placed, takes user inputs in json form"""
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



