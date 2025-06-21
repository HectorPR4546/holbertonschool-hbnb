from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('ReviewInput', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True, min=1, max=5),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True)
})

review_response_model = api.model('ReviewResponse', {
    'id': fields.String,
    'text': fields.String,
    'rating': fields.Integer,
    'user_id': fields.String,
    'place_id': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.marshal_with(review_response_model, code=201)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new review"""
        try:
            new_review = facade.create_review(api.payload)
            return new_review, 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.marshal_list_with(review_response_model)
    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return reviews, 200

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.marshal_with(review_response_model)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')
        return review, 200

    @api.expect(review_model)
    @api.marshal_with(review_response_model)
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update review"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')
        
        try:
            updated_review = facade.update_review(review_id, api.payload)
            return updated_review, 200
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'Review deleted')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete review"""
        if not facade.delete_review(review_id):
            api.abort(404, 'Review not found')
        return {'message': 'Review deleted'}, 200

@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @api.marshal_list_with(review_response_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get reviews for a place"""
        reviews = facade.get_reviews_by_place(place_id)
        if not reviews and not facade.place_repo.get(place_id):
            api.abort(404, 'Place not found')
        return reviews, 200
