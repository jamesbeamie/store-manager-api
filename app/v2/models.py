
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
            return make_response(jsonify({"Message":"ADM exists"})), 200
        cur.execute("INSERT INTO my_users (username,password,confirmpass,addres,role) \
            VALUES (%(username)s,%(password)s,%(confirmpass)s,%(addres)s,%(role)s);",\
            {'username':username,'password':password, \
            'confirmpass':confirmpass,'addres':addres,'role':role})
        con.commit()
        return make_response(jsonify({"message":"admin created"}), 201)

