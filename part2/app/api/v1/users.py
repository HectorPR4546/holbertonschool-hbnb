from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, example='John'),
    'last_name': fields.String(required=True, example='Doe'),
    'email': fields.String(required=True, example='john@example.com'),
    'is_admin': fields.Boolean(default=False)
})

user_response_model = api.model('UserResponse', {
    'id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'is_admin': fields.Boolean,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
})

error_model = api.model('Error', {
    'message': fields.String,
    'field': fields.String(required=False)
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model)
    @api.marshal_with(user_response_model, code=201)
    @api.response(400, 'Validation Error', error_model)
    def post(self):
        """Create a new user"""
        user_data = api.payload
        
        result = facade.create_user(user_data)
        if isinstance(result, dict) and result.get('error'):
            api.abort(400, result['message'], field=result.get('field'))
        
        return result, 201

    @api.marshal_list_with(user_response_model)
    def get(self):
        """List all users"""
        return facade.get_all_users(), 200

@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.marshal_with(user_response_model)
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user, 200

    @api.expect(user_model)
    @api.marshal_with(user_response_model)
    @api.response(400, 'Validation Error', error_model)
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        
        result = facade.update_user(user_id, api.payload)
        if isinstance(result, dict) and result.get('error'):
            api.abort(400, result['message'])
        
        return result, 200
