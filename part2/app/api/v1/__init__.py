#!/usr/bin/python3
"""Initialize API v1 package."""
from flask_restx import Api

api = Api(version='1.0', title='HBnB API',
          description='A simple HBnB REST API')

# UPDATED: Added places to imports
from app.api.v1 import users, amenities, places
