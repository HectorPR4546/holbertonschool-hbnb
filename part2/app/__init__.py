#!/usr/bin/python3
"""
HBnB API initialization module
Creates a Flask application instance and registers blueprints
"""
from flask import Flask
from flask_restx import Api

app = Flask(__name__)
api = Api(app, version='1.0', title='HBnB API',
          description='A Holberton School Airbnb Clone API')

# Import API views
from app.api.v1.views.index import api as index_ns
api.add_namespace(index_ns)

def create_app():
    """Application factory pattern"""
    return app
