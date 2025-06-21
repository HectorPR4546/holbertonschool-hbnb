from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for Swagger documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'is_admin': fields.Boolean(description='Admin status')
})

user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email address'),
    'is_admin': fields.Boolean(description='Admin status')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_response_model, code=201)
    @api.response(400, 'Invalid input or email exists')
    def post(self):
        """Create a new user"""
        user_data = api.payload
        
        # Check if email already exists
        if facade.get_user_by_email(user_data['email']):
            api.abort(400, 'Email already registered')
        
        new_user = facade.create_user(user_data)
        return new_user, 201

    @api.marshal_list_with(user_response_model)
    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        return users, 200

@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.marshal_with(user_response_model)
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user, 200

    @api.expect(user_model)
    @api.marshal_with(user_response_model)
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input')
    def put(self, user_id):
        """Update user information"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        
        update_data = api.payload
        
        # Check if email is being changed to an existing one
        if 'email' in update_data:
            existing_user = facade.get_user_by_email(update_data['email'])
            if existing_user and existing_user.id != user_id:
                api.abort(400, 'Email already registered')
        
        updated_user = facade.update_user(user_id, update_data)
        return updated_user, 200
