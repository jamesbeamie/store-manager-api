from flask import Flask, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api2
from .models import User
user_class = User()

def validate_user( data):
  """validate user details"""
  try:
      # check if the username is more than 3 characters
      if type(data['username']) != str:
          return "username can only be a string"
      elif len(data['username'].strip()) < 3:
          return "username must be more than 3 characters"
      # check if password has space
      elif " " in data["password"]:
          return "password should be one without spaces"
      elif len(data['password'].strip()) < 5:
          return "Password should have atleast 5 characters"
      # check if the passwords match
      elif data['password'] != data['confirmpass']:
          return "passwords do not match"
      else:
          return "valid"
  except Exception as error:
      return "please provide all the fields, missing " + str(error)


@api2.route('/admin/signup', methods=['POST'])
def reg_admin():
  """method to place an order"""
  data = request.get_json()
  res = validate_user(data)
  username = data['username']
  password = data['password']
  confirmpass = data['confirmpass']
  addres = data['addres']
  role = data['role']
  if res == 'valid':
    if role.lower() == 'admin':
      return user_class.create_admin(username, password, confirmpass, addres, role)
    return jsonify({"message":"Can only register role as admin"})
  return jsonify({"message":res}), 400

@api2.route('/login', methods=["POST"])
def login():
    """ Method to login user """
    data = request.get_json()
    username = data['username']
    password = data['password']
    result = user_class.login(username, password)
    return result
