from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Models
place_model = api.model('PlaceInput', {
    'title': fields.String(required=True, example='Beautiful Apartment'),
    'description': fields.String(example='Lovely 2-bedroom in downtown'),
    'price': fields.Float(required=True, example=120.50),
    'latitude': fields.Float(required=True, example=40.7128),
    'longitude': fields.Float(required=True, example=-74.0060),
    'owner_id': fields.String(required=True, example='user-uuid-here')
})

place_response_model = api.model('PlaceResponse', {
    'id': fields.String,
    'title': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'latitude': fields.Float,
    'longitude': fields.Float,
    'owner_id': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
})

error_model = api.model('Error', {
    'message': fields.String,
    'field': fields.String(required=False)
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.marshal_with(place_response_model, code=201)
    @api.response(400, 'Validation Error', error_model)
    def post(self):
        """Create a new place"""
        result = facade.create_place(api.payload)
        if isinstance(result, dict) and result.get('error'):
            api.abort(400, result['message'], field=result.get('field'))
        return result, 201

    @api.marshal_list_with(place_response_model)
    def get(self):
        """List all places"""
        return facade.get_all_places(), 200

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.marshal_with(place_response_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')
        return place, 200
