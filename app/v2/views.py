from flask import Flask, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api2
from .models import User, Product, Sales
user_class = User()
product_class = Product()
sales_class = Sales()

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

def validate_sale(data):
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
        elif data['quantity'] < 1:
            return "Quantity should be atleast 1 item"
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

@api2.route('/users', methods=["GET"])
def all_users():
  """ Route to get all the registered users."""
  return user_class.view_users()

@api2.route('/login', methods=["POST"])
def login():
    """ Method to login user """
    data = request.get_json()
    username = data['username']
    password = data['password']
    result = user_class.login(username, password)
    return result

"""
Products
"""

@api2.route('/products', methods=['POST'])
@jwt_required
def add_product():
  """method to create product"""
  logedin = get_jwt_identity()
  adm=user_class.is_admin(logedin)
  if adm == True:
    data = request.get_json()
    res = validate_product(data)
    product_name = data['product_name']
    price = data['price']
    quantity = data['quantity']
    if res == 'valid':
      return product_class.create_product(product_name,price,quantity)
    return jsonify({"message":res})
  return jsonify({"message":"Restricted to admin only"})

@api2.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required
def update_product(product_id, **kwargs):
  """method for the admin to update order status"""
  logedin = get_jwt_identity()
  adm=user_class.is_admin(logedin)
  if adm == True:
    product_details = request.get_json()
    res = validate_product(product_details)
    product_name = product_details['product_name']
    price = product_details['price']
    quantity = product_details['quantity']
    if res == 'valid':
      return product_class.modify_product(product_id,product_name,price,quantity)
    return jsonify({"message":res})
  return jsonify({"message":"Restricted to admin only"}) 
  

@api2.route('products/<int:product_id>', methods=["DELETE"])
@jwt_required
def delete_item(product_id, **kwargs):
  """Route to delete a user from the db using the user name"""
  logedin = get_jwt_identity()
  adm=user_class.is_admin(logedin)
  if adm == True:
    res = product_class.delete_product(product_id)
    return res, 200
  return jsonify({"message":"Restricted to admin only"})

@api2.route('/products', methods=["GET"])
def all_products():
  """Get all products"""
  return product_class.get_products()

@api2.route('products/<int:product_id>', methods=['GET'])
@jwt_required
def single_product(product_id, **kwargs):
  """method to return a specific product"""
  result = product_class.specific_product(product_id)
  return result


"""
Sales
"""

@api2.route('/sales', methods=['POST'])
@jwt_required
def add_record():
  """method to create a sales record"""
  logedin = get_jwt_identity()
  adm=user_class.is_admin(logedin)
  if adm == False:
    data = request.get_json()
    res = validate_sale(data)
    attendant = data['attendant']
    product_name = data['product_name']
    price = data['price']
    quantity = data['quantity']
    if res == 'valid':
        found = product_class.in_stoke(product_name)
        #checks if the product is in stoke
        if found == True:
            return sales_class.create_record(attendant,product_name,price,quantity)
        return jsonify({"message":"Product is out of stoke"})
    return jsonify({"message":res}), 400
  return jsonify({"message":"Only attendant can create record"}), 400

@api2.route('/sales/<int:sales_id>', methods=['GET'])
@jwt_required
def specific(sales_id, **kwargs):
  """method to return a specific sales record"""
  result = sales_class.specific_record(sales_id)
  if not result:
    return jsonify({"message":"could not find the specified record id"}), 400
  return result

@api2.route('/sales', methods=["GET"])
@jwt_required
def sales_records():
  """Get all sales records"""
  logedin = get_jwt_identity()
  adm=user_class.is_admin(logedin)
  if adm == True:
    return sales_class.all_sales(logedin)
  return jsonify({"message":"Only admin can view all records"})






