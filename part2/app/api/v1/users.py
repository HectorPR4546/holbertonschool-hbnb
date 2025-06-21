#!/usr/bin/python3
"""User endpoints implementation."""
from flask_restx import Namespace, Resource, fields
from app.business.logic import BusinessLogic

# NEW: Created users namespace
api = Namespace('users', description='User operations')
business = BusinessLogic()

# NEW: User model for API documentation
user_model = api.model('User', {
    'id': fields.String(readonly=True),
    'email': fields.String(required=True),
    'first_name': fields.String,
    'last_name': fields.String,
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        """List all users (password excluded automatically)."""
        users = business.all()
        return [user for user in users if isinstance(user, business.repo.models.User)]

@api.route('/<string:user_id>')
class User(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Get a single user by ID."""
        user = business.get(user_id)
        if not user or not isinstance(user, business.repo.models.User):
            api.abort(404, "User not found")
        return user

    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Update a user's information."""
        user = business.get(user_id)
        if not user or not isinstance(user, business.repo.models.User):
            api.abort(404, "User not found")

        # UPDATED: Only allow certain fields to be modified
        allowed_fields = ['email', 'first_name', 'last_name']
        data = {k: v for k, v in api.payload.items() if k in allowed_fields}
        
        for field, value in data.items():
            setattr(user, field, value)
        
        business.repo.add(user)  # Save changes
        return user

    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user."""
        data = api.payload
        if 'email' not in data:
            api.abort(400, "Email is required")
        
        user = business.repo.models.User(**data)
        business.add(user)
        return user, 201
