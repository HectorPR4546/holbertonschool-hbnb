#!/usr/bin/python3
"""Place endpoints implementation."""
from flask_restx import Namespace, Resource, fields
from app.business.logic import BusinessLogic

# NEW: Created places namespace
api = Namespace('places', description='Place operations')
business = BusinessLogic()

# NEW: Place model with relationships
place_model = api.model('Place', {
    'id': fields.String(readonly=True),
    'name': fields.String(required=True),
    'city_id': fields.String(required=True),
    'user_id': fields.String(required=True, description='Owner ID'),
    'description': fields.String,
    'number_rooms': fields.Integer(min=0),
    'number_bathrooms': fields.Integer(min=0),
    'max_guest': fields.Integer(min=0),
    'price_by_night': fields.Integer(min=0),
    'latitude': fields.Float,
    'longitude': fields.Float,
    'amenity_ids': fields.List(fields.String),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

@api.route('/')
class PlaceList(Resource):
    @api.marshal_list_with(place_model)
    def get(self):
        """List all places."""
        places = business.all()
        return [place for place in places if isinstance(place, business.repo.models.Place)]

@api.route('/<string:place_id>')
class Place(Resource):
    @api.marshal_with(place_model)
    def get(self, place_id):
        """Get a single place by ID."""
        place = business.get(place_id)
        if not place or not isinstance(place, business.repo.models.Place):
            api.abort(404, "Place not found")
        return place

    @api.expect(place_model)
    @api.marshal_with(place_model)
    def put(self, place_id):
        """Update place information."""
        place = business.get(place_id)
        if not place or not isinstance(place, business.repo.models.Place):
            api.abort(404, "Place not found")

        # UPDATED: Validation for numeric fields
        numeric_fields = {
            'price_by_night': (0, None),
            'latitude': (-90, 90),
            'longitude': (-180, 180)
        }
        
        for field, (min_val, max_val) in numeric_fields.items():
            if field in api.payload:
                try:
                    value = float(api.payload[field])
                    if min_val is not None and value < min_val:
                        raise ValueError
                    if max_val is not None and value > max_val:
                        raise ValueError
                    setattr(place, field, value)
                except (ValueError, TypeError):
                    api.abort(400, f"Invalid {field} value")

        # Update other fields
        for field in ['name', 'description', 'city_id', 'amenity_ids']:
            if field in api.payload:
                setattr(place, field, api.payload[field])

        business.repo.add(place)
        return place

    @api.expect(place_model)
    @api.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place."""
        required_fields = ['name', 'city_id', 'user_id']
        if not all(field in api.payload for field in required_fields):
            api.abort(400, "Missing required fields")

        # NEW: Verify owner exists
        owner = business.get(api.payload['user_id'])
        if not owner or not isinstance(owner, business.repo.models.User):
            api.abort(400, "Invalid owner ID")

        place = business.repo.models.Place(**api.payload)
        business.add(place)
        return place, 201
