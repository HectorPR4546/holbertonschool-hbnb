from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='User ID'),
    'place_id': fields.String(required=True, description='Place ID')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review created')
    @api.response(400, 'Bad input')
    def post(self):
        """Create new review"""
        data = api.payload
        try:
            review = facade.create_review(data)
            return review, 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of reviews')
    def get(self):
        """Get all reviews"""
        return facade.get_all_reviews(), 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review found')
    @api.response(404, 'Not found')
    def get(self, review_id):
        """Get review by ID"""
        review = facade.get_review(review_id)
        if review:
            return review, 200
        return {"error": "Not found"}, 404

    @api.expect(review_model)
    @api.response(200, 'Updated')
    @api.response(404, 'Not found')
    def put(self, review_id):
        """Update review"""
        data = api.payload
        try:
            updated = facade.update_review(review_id, data)
            return {"message": "Review updated"}, 200
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'Deleted')
    @api.response(404, 'Not found')
    def delete(self, review_id):
        """Delete review"""
        deleted = facade.delete_review(review_id)
        if deleted:
            return {"message": "Review deleted"}, 200
        return {"error": "Not found"}, 404

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'Reviews for place')
    def get(self, place_id):
        """Get all reviews for a place"""
        return facade.get_reviews_by_place(place_id), 200
