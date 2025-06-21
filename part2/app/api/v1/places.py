from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Models for documentation
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String,
    'name': fields.String
})

user_model = api.model('PlaceUser', {
    'id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String
})

# Add the review model for place responses
review_model = api.model('PlaceReview', {
    'id': fields.String,
    'text': fields.String,
    'rating': fields.Integer(min=1, max=5),
    'user_id': fields.String,
    'created_at': fields.DateTime
})

place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True),
    'amenity_ids': fields.List(fields.String)
})

place_response_model = api.model('PlaceResponse', {
    'id': fields.String,
    'title': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'latitude': fields.Float,
    'longitude': fields.Float,
    'owner': fields.Nested(user_model),
    'amenities': fields.List(fields.Nested(amenity_model)),
    'reviews': fields.List(fields.Nested(review_model))  # Added reviews field
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_input_model)
    @api.marshal_with(place_response_model, code=201)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place"""
        try:
            new_place = facade.create_place(api.payload)
            return new_place, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.marshal_list_with(place_response_model)
    def get(self):
        """Get all places"""
        places = facade.get_all_places()
        return places, 200

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.marshal_with(place_response_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')
        
        # Get reviews for this place
        place.reviews = facade.get_reviews_by_place(place_id)
        return place, 200

    @api.expect(place_input_model)
    @api.marshal_with(place_response_model)
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update place information"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')
        
        try:
            updated_place = facade.update_place(place_id, api.payload)
            return updated_place, 200
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:place_id>/amenities/<string:amenity_id>')
class PlaceAmenityResource(Resource):
    @api.response(200, 'Amenity added to place')
    @api.response(404, 'Place or Amenity not found')
    def post(self, place_id, amenity_id):
        """Add amenity to a place"""
        if not facade.add_amenity_to_place(place_id, amenity_id):
            api.abort(404, 'Place or Amenity not found')
        return {'message': 'Amenity added to place'}, 200
