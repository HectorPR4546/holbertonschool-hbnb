#!/usr/bin/python3
"""Initialize the API package."""
from flask_restx import Api

api = Api(
    title='HBnB API',
    version='1.0',
    description='A simple HBnB API'
)

# Import namespaces here later
