from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Place operations')

# Models for related entities (used in output only)
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Model for client input (POST/PUT)
place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

# Model for output (GET)
place_output_model = api.model('Place', {
    'id': fields.Integer(readOnly=True, description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner_id': fields.String(description='ID of the owner'),
    'owner': fields.Nested(user_model),
    'amenities': fields.List(fields.Nested(amenity_model)),
    'reviews': fields.List(fields.Nested(review_model))
})


@api.route('/')
class PlaceList(Resource):
    @api.marshal_list_with(place_output_model)
    def get(self):
        """Retrieve a list of all places"""
        return facade.get_all_places()

    @api.expect(place_input_model)
    @api.marshal_with(place_output_model, code=201)
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        try:
            current_user = get_jwt_identity()
            is_admin = current_user.get('is_admin', False)

            place_data = request.json
            if not is_admin and place_data.get('owner_id') != current_user['id']:
                api.abort(403, "Unauthorized action: owner_id must match authenticated user")
            return facade.create_place(place_data), 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<int:place_id>')
@api.param('place_id', 'Place ID')
@api.response(404, 'Place not found')
class PlaceResource(Resource):
    @api.marshal_with(place_output_model)
    def get(self, place_id):
        """Get place details by ID"""
        try:
            return facade.get_place(place_id)
        except ValueError as e:
            api.abort(404, str(e))

    @api.expect(place_input_model)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        try:
            current_user = get_jwt_identity()
            is_admin = current_user.get('is_admin', False)

            place = facade.get_place(place_id)
            if not is_admin and place['owner_id'] != current_user['id']:
                api.abort(403, "Unauthorized action: You can only update your own places")
            place_data = request.json
            return facade.update_place(place_id, place_data)
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_place')
    @api.response(204, 'Place successfully deleted')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        try:
            current_user = get_jwt_identity()
            is_admin = current_user.get('is_admin', False)

            place = facade.get_place(place_id)
            if not is_admin and place['owner_id'] != current_user['id']:
                api.abort(403, "Unauthorized action: You can only delete your own places")

            facade.delete_place(place_id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))

@api.route('/<int:place_id>/reviews')
@api.param('place_id', 'Place ID')
@api.response(404, 'Place not found')
class PlaceReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            return facade.get_reviews_by_place(place_id)
        except ValueError as e:
            api.abort(404, str(e))

