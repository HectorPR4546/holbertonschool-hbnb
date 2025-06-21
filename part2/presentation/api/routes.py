"""API routes for HBnB."""

from flask import Blueprint, jsonify, request
from flask_restx import Api, Resource, fields
from business_logic.facade import HBNBFacade
from business_logic.services import HBNBService
from models.user import User

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, version='1.0', title='HBnB API',
          description='HBnB API endpoints')

facade = HBNBFacade()
service = HBNBService(facade)

# Namespace for User operations
user_ns = api.namespace('users', description='User operations')

# Model for User request/response
user_model = api.model('User', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})

@user_ns.route('/')
class UserList(Resource):
    @user_ns.doc('list_users')
    @user_ns.marshal_list_with(user_model, skip_none=True)
    def get(self):
        """List all users (excluding passwords)."""
        users = service.get_all_objects(User)
        # Remove password from response
        return [{
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat()
        } for user in users.values()]

    @user_ns.doc('create_user')
    @user_ns.expect(user_model)
    @user_ns.marshal_with(user_model, code=201, skip_none=True)
    def post(self):
        """Create a new user."""
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400
        
        # Basic validation
        if 'email' not in data or 'password' not in data:
            return {'message': 'Missing email or password'}, 400
        
        user = service.create_object(User, data)
        return {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat()
        }, 201

@user_ns.route('/<string:user_id>')
@user_ns.response(404, 'User not found')
@user_ns.param('user_id', 'The user identifier')
class UserResource(Resource):
    @user_ns.doc('get_user')
    @user_ns.marshal_with(user_model, skip_none=True)
    def get(self, user_id):
        """Fetch a user given its identifier."""
        user = service.get_object(User, user_id)
        if not user:
            return {'message': 'User not found'}, 404
        
        return {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat()
        }

    @user_ns.doc('update_user')
    @user_ns.expect(user_model)
    @user_ns.marshal_with(user_model, skip_none=True)
    def put(self, user_id):
        """Update a user given its identifier."""
        user = service.get_object(User, user_id)
        if not user:
            return {'message': 'User not found'}, 404
        
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400
        
        # Don't allow updating password via this endpoint
        if 'password' in data:
            del data['password']
        
        updated_user = service.update_object(User, user_id, data)
        return {
            'id': updated_user.id,
            'email': updated_user.email,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'created_at': updated_user.created_at.isoformat(),
            'updated_at': updated_user.updated_at.isoformat()
        }
