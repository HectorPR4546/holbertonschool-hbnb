from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'id': fields.String(readOnly=True, description='Amenity ID'),
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        """Get a list of all amenities"""
        return facade.get_all_amenities()

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        try:
            amenity_data = request.json
            return facade.create_amenity(amenity_data), 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'Amenity ID')
@api.response(404, 'Amenity not found')
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Get an amenity by ID"""
        try:
            return facade.get_amenity(amenity_id)
        except ValueError as e:
            api.abort(404, str(e))

    @api.expect(amenity_model)
    def put(self, amenity_id):
        """Update an amenity"""
        try:
            amenity_data = request.json
            return facade.update_amenity(amenity_id, amenity_data)
        except ValueError as e:
            api.abort(400, str(e))
