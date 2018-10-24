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


def validate_product(data):
    """Check to validate user input """
    try:
        #check if the product name is provided
        if " " in data['product_name']:
            return "Enter product name"
        # Check for a reasonable product name
        elif len(data['product_name']) < 2:
            return "Invalid product name"
        elif '@'  in data['product_name'] or '#'  in data['product_name']:
          return "Product cant be special character"
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


@api2.route('/attendant/signup', methods=["POST"])
@jwt_required
def reg():
  """ Method to create user account."""
  logedin = get_jwt_identity()
  adm=user_class.is_admin(logedin)
  if adm == True:
    data = request.get_json()
    res = validate_user(data)
    username = data['username']
    password = data['password']
    confirmpass = data['confirmpass']
    addres = data['addres']
    role = data['role']
    if res == "valid":
      if role.lower() == 'attendant' or role.lower() == 'admin':
        response = user_class.reg_attendant(username, password, confirmpass, addres, role) 
        return response
      return jsonify({"message":"can only register role as attendant or admin"}), 400
    return jsonify({"message":res}), 400
  return jsonify({"message":"Restricted to admin only"})

@api2.route('/login', methods=["POST"])
def login():
    """ Method to login user """
    data = request.get_json()
    username = data['username']
    password = data['password']
    result = user_class.login(username, password)
    return result
