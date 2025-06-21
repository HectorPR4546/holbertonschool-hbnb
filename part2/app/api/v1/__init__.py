#!/usr/bin/python3
"""Initialize API v1 package."""
from flask_restx import Api

# NEW: Added API version and description metadata
api = Api(version='1.0', title='HBnB API',
          description='A simple HBnB REST API')

from app.api.v1 import users
