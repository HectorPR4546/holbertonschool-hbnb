# part2/app/api/v1/places.py

from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.api.v1.reviews import review_list_item_model

api = Namespace('places', description='Place operations')

# Define the models for related entities to be used in output
owner_model_output = api.model('PlaceOwnerOutput', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

amenity_model_output = api.model('PlaceAmenityOutput', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

# Define the place model for input validation (POST/PUT)
place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place', max_length=100),
    'description': fields.String(required=False, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night', min=0.0),
    'latitude': fields.Float(required=True, description='Latitude of the place', min=-90.0, max=90.0),
    'longitude': fields.Float(required=True, description='Longitude of the place', min=-180.0, max=180.0),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=False, description="List of amenity IDs to associate")
})

# Define the full place response model for GET by ID and successful POST/PUT
place_response_model = api.model('PlaceResponse', {
    'id': fields.String(description='The place unique identifier'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner': fields.Nested(owner_model_output, description='Details of the place owner', allow_null=True),
    'amenities': fields.List(fields.Nested(amenity_model_output), description='List of amenities for the place'),
    'reviews': fields.List(fields.Nested(review_list_item_model), description='List of reviews for the place'), # UPDATED HERE
    'created_at': fields.DateTime(dt_format='iso8601', description='Timestamp of creation'),
    'updated_at': fields.DateTime(dt_format='iso8601', description='Timestamp of last update')
})

# Define a simpler place model for the list of all places (GET /places)
place_list_item_model = api.model('PlaceListItem', {
    'id': fields.String(description='The place unique identifier'),
    'title': fields.String(description='Title of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner_id': fields.String(description='ID of the owner', allow_null=True),
    'reviews': fields.List(fields.Nested(review_list_item_model), description='List of reviews for the place'), # ADDED HERE FOR CONSISTENCY
    'created_at': fields.DateTime(dt_format='iso8601', description='Timestamp of creation'),
    'updated_at': fields.DateTime(dt_format='iso8601', description='Timestamp of last update')
})


@api.route('/')
class PlaceList(Resource):
    @api.doc('create_place')
    @api.expect(place_input_model, validate=True)
    @api.marshal_with(place_response_model, code=201)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data or Owner not found or Invalid amenities')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(include_relationships=True), 201
        except (ValueError, TypeError) as e:
            return {'message': str(e)}, 400
        except Exception as e:
            api.abort(500, message=f"An unexpected error occurred: {str(e)}")


    @api.doc('list_places')
    @api.marshal_list_with(place_list_item_model)
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        # For list view, we include reviews by default now per list_item_model
        return [place.to_dict(include_relationships=True) for place in places], 200 # Must use True to get reviews

@api.route('/<string:place_id>')
@api.param('place_id', 'The place unique identifier')
class PlaceResource(Resource):
    @api.doc('get_place')
    @api.marshal_with(place_response_model)
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404
        return place.to_dict(include_relationships=True), 200

    @api.doc('update_place')
    @api.expect(place_input_model, validate=True)
    @api.marshal_with(place_response_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data or Owner not found')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        try:
            updated_place = facade.update_place(place_id, place_data)
            if not updated_place:
                return {'message': 'Place not found'}, 404
            return updated_place.to_dict(include_relationships=True), 200
        except (ValueError, TypeError) as e:
            return {'message': str(e)}, 400
        except Exception as e:
            api.abort(500, message=f"An unexpected error occurred: {str(e)}")
