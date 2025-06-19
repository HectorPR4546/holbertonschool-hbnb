#!/usr/bin/python3
"""
Index view module
Defines basic API endpoints for status checks
"""
from flask_restx import Resource, Namespace

api = Namespace('index', description='Basic API status operations')

@api.route('/status')
class Status(Resource):
    """Status endpoint"""
    def get(self):
        """Returns API status"""
        return {"status": "OK"}, 200
