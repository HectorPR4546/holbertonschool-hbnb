from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.String(readOnly=True, description='The unique identifier'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password', write_only=True)
})


@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        return facade.get_all_users()

    @api.doc('create_user')
    @api.expect(user_model)
    def post(self):
        """Create a new user"""
        try:
            user_data = request.json
            user = facade.create_user(user_data)
            return {'id': user.id, 'message': 'User created successfully'}, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Fetch a user by ID"""
        try:
            return facade.get_user(user_id)
        except ValueError as e:
            api.abort(404, str(e))

    @api.doc('update_user')
    @api.expect(user_model)
    @jwt_required()
    def put(self, user_id):
        """Update a user's info"""
        try:
            current_user = get_jwt_identity()
            if user_id != current_user['id']:
                api.abort(403, "Unauthorized action: You can only update your own user details")
            user_data = request.json
            if 'email' in user_data or 'password' in user_data:
                api.abort(400, "You cannot modify email or password.")
            return facade.update_user(user_id, user_data)
        except ValueError as e:
            api.abort(404, str(e))


