# part2/app/api/v1/amenities.py

from flask_restx import Namespace, Resource, fields
from app.services import facade # Import the facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('AmenityInput', {
    'name': fields.String(required=True, description='Name of the amenity', max_length=50)
})

# Define a response model for consistent output and documentation
amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(description='The amenity unique identifier'),
    'name': fields.String(description='Name of the amenity'),
    'created_at': fields.DateTime(dt_format='iso8601', description='Timestamp of creation'),
    'updated_at': fields.DateTime(dt_format='iso8601', description='Timestamp of last update')
})

@api.route('/')
class AmenityList(Resource):
    @api.doc('create_amenity')
    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_response_model, code=201)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        try:
            # We don't have a specific uniqueness check for amenity names in the model/facade yet,
            # but if we wanted one, we'd add it here, similar to email for users.
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except ValueError as e:
            return {'message': str(e)}, 400
        except TypeError as e:
            return {'message': str(e)}, 400

    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_response_model)
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

@api.route('/<string:amenity_id>') # Use string converter for clarity in Swagger
@api.param('amenity_id', 'The amenity unique identifier')
class AmenityResource(Resource):
    @api.doc('get_amenity')
    @api.marshal_with(amenity_response_model)
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'message': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @api.doc('update_amenity')
    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_response_model) # Return the updated amenity details
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not updated_amenity:
                return {'message': 'Amenity not found'}, 404
            return updated_amenity.to_dict(), 200 # Return the full updated object
        except ValueError as e:
            return {'message': str(e)}, 400
        except TypeError as e:
            return {'message': str(e)}, 400
