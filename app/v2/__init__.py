from flask import Blueprint

api2 = Blueprint('api2', __name__)

from . import views
