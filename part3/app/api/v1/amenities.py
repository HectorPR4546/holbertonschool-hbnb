from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
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
    @jwt_required()
    def post(self):
        """Create a new amenity"""
        try:
            current_user = get_jwt_identity()
            if not current_user.get('is_admin'):
                api.abort(403, "Admin privileges required")
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
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity"""
        try:
            current_user = get_jwt_identity()
            if not current_user.get('is_admin'):
                api.abort(403, "Admin privileges required")
            amenity_data = request.json
            return facade.update_amenity(amenity_id, amenity_data)
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_amenity')
    @api.response(204, 'Amenity successfully deleted')
    @jwt_required()
    def delete(self, amenity_id):
        """Delete an amenity"""
        try:
            current_user = get_jwt_identity()
            if not current_user.get('is_admin'):
                api.abort(403, "Admin privileges required")
            facade.delete_amenity(amenity_id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))
