# third-party imports
import os
from flask import Flask

# local imports
from config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)

    from .v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    
    return app
