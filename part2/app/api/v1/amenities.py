#!/usr/bin/python3
"""Amenity endpoints implementation."""
from flask_restx import Namespace, Resource, fields
from app.business.logic import BusinessLogic

# NEW: Created amenities namespace
api = Namespace('amenities', description='Amenity operations')
business = BusinessLogic()

# NEW: Amenity model for API documentation
amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True),
    'name': fields.String(required=True),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

@api.route('/')
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities."""
        amenities = business.all()
        return [amenity for amenity in amenities if isinstance(amenity, business.repo.models.Amenity)]

@api.route('/<string:amenity_id>')
class Amenity(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Get a single amenity by ID."""
        amenity = business.get(amenity_id)
        if not amenity or not isinstance(amenity, business.repo.models.Amenity):
            api.abort(404, "Amenity not found")
        return amenity

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update an amenity's information."""
        amenity = business.get(amenity_id)
        if not amenity or not isinstance(amenity, business.repo.models.Amenity):
            api.abort(404, "Amenity not found")

        # UPDATED: Only allow name to be modified
        if 'name' in api.payload:
            amenity.name = api.payload['name']
        
        business.repo.add(amenity)  # Save changes
        return amenity

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity."""
        data = api.payload
        if 'name' not in data:
            api.abort(400, "Name is required")
        
        amenity = business.repo.models.Amenity(**data)
        business.add(amenity)
        return amenity, 201
