# ... (previous imports remain the same)
from models.amenity import Amenity

# ... (previous code remains the same until namespace creation)

# Namespace for Amenity operations
amenity_ns = api.namespace('amenities', description='Amenity operations')

# Model for Amenity request/response
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Amenity name')
})

@amenity_ns.route('/')
class AmenityList(Resource):
    @amenity_ns.doc('list_amenities')
    @amenity_ns.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities."""
        amenities = service.get_all_objects(Amenity)
        return [{
            'id': amenity.id,
            'name': amenity.name,
            'created_at': amenity.created_at.isoformat(),
            'updated_at': amenity.updated_at.isoformat()
        } for amenity in amenities.values()]

    @amenity_ns.doc('create_amenity')
    @amenity_ns.expect(amenity_model)
    @amenity_ns.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity."""
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400
        
        if 'name' not in data:
            return {'message': 'Missing amenity name'}, 400
        
        amenity = service.create_object(Amenity, data)
        return {
            'id': amenity.id,
            'name': amenity.name,
            'created_at': amenity.created_at.isoformat(),
            'updated_at': amenity.updated_at.isoformat()
        }, 201

@amenity_ns.route('/<string:amenity_id>')
@amenity_ns.response(404, 'Amenity not found')
@amenity_ns.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @amenity_ns.doc('get_amenity')
    @amenity_ns.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Fetch an amenity given its identifier."""
        amenity = service.get_object(Amenity, amenity_id)
        if not amenity:
            return {'message': 'Amenity not found'}, 404
        
        return {
            'id': amenity.id,
            'name': amenity.name,
            'created_at': amenity.created_at.isoformat(),
            'updated_at': amenity.updated_at.isoformat()
        }

    @amenity_ns.doc('update_amenity')
    @amenity_ns.expect(amenity_model)
    @amenity_ns.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update an amenity given its identifier."""
        amenity = service.get_object(Amenity, amenity_id)
        if not amenity:
            return {'message': 'Amenity not found'}, 404
        
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400
        
        updated_amenity = service.update_object(Amenity, amenity_id, data)
        return {
            'id': updated_amenity.id,
            'name': updated_amenity.name,
            'created_at': updated_amenity.created_at.isoformat(),
            'updated_at': updated_amenity.updated_at.isoformat()
        }
