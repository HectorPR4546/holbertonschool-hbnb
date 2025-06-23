from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.String(readOnly=True, description='The unique identifier'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address')
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
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        try:
            user_data = request.json
            return facade.create_user(user_data), 201
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
    def put(self, user_id):
        """Update a user's info"""
        try:
            user_data = request.json
            return facade.update_user(user_id, user_data)
        except ValueError as e:
            api.abort(404, str(e))
