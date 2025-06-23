# part2/app/__init__.py

from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns # <-- ADD THIS LINE

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    # Register the amenities namespace <-- ADD THIS LINE
    api.add_namespace(amenities_ns, path='/api/v1/amenities') # <-- ADD THIS LINE

    return app
