from flask_restx import Namespace, Resource, fields
from app.services import facade
# We also need to import the User model if we want to return a more structured response later
# from app.models.user import User

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
# This model will be used for POST and PUT requests
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user', max_length=50),
    'last_name': fields.String(required=True, description='Last name of the user', max_length=50),
    'email': fields.String(required=True, description='Email of the user', pattern=r"[^@]+@[^@]+\.[^@]+") # Add pattern for email
})

# Define a response model to ensure consistent output, especially for lists
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='The user unique identifier'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'is_admin': fields.Boolean(description='Is user an administrator'),
    'created_at': fields.DateTime(dt_format='iso8601', description='Timestamp of creation'),
    'updated_at': fields.DateTime(dt_format='iso8601', description='Timestamp of last update')
})


@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_response_model) # Use marshal_list_with for lists
    @api.response(200, 'Success')
    def get(self):
        """Get a list of all users"""
        users = facade.get_all_users()
        # The to_dict method from our User model is perfect for this!
        return [user.to_dict() for user in users], 200

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_response_model, code=201) # Use marshal_with for single objects, specify code
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Handle validation errors from the model's setters
        try:
            # The Facade's create_user method will now instantiate User and apply its internal validation
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                # Add validation for unique email here before creating
                return {'message': 'Email already registered'}, 400

            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            return {'message': str(e)}, 400
        except TypeError as e:
            return {'message': str(e)}, 400


@api.route('/<string:user_id>') # Ensure user_id is typed as string for Swagger UI
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_response_model)
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.to_dict(), 200 # Use to_dict() for consistent output

    @api.doc('update_user')
    @api.expect(user_model, validate=True) # Expect the same user_model for updates
    @api.marshal_with(user_response_model)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data or Email already registered')
    def put(self, user_id):
        """Update an existing user's information"""
        user_data = api.payload

        # Optional: Check if email is being changed to an already existing email (for another user)
        if 'email' in user_data:
            existing_user_with_new_email = facade.get_user_by_email(user_data['email'])
            if existing_user_with_new_email and existing_user_with_new_email.id != user_id:
                return {'message': 'Email already registered by another user'}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'message': 'User not found'}, 404
            return updated_user.to_dict(), 200
        except ValueError as e:
            return {'message': str(e)}, 400
        except TypeError as e:
            return {'message': str(e)}, 400
