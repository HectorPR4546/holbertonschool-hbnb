from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Review input/output model
review_model = api.model('Review', {
    'id': fields.String(readOnly=True, description='Review ID'),
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self):
        """Retrieve a list of all reviews"""
        return facade.get_all_reviews()

    @api.expect(review_model)
    @api.marshal_with(review_model, code=201)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        try:
            review_data = request.json
            return facade.create_review(review_data), 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<string:review_id>')
@api.param('review_id', 'Review ID')
@api.response(404, 'Review not found')
class ReviewResource(Resource):
    @api.marshal_with(review_model)
    def get(self, review_id):
        """Get review details by ID"""
        try:
            return facade.get_review(review_id)
        except ValueError as e:
            api.abort(404, str(e))

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        try:
            current_user = get_jwt_identity()
            is_admin = current_user.get('is_admin', False)

            review = facade.get_review(review_id)
            if not is_admin and review['user_id'] != current_user['id']:
                api.abort(403, "Unauthorized action: You can only update your own reviews")
            review_data = request.json
            return facade.update_review(review_id, review_data)
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'Review deleted successfully')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        try:
            current_user = get_jwt_identity()
            is_admin = current_user.get('is_admin', False)

            review = facade.get_review(review_id)
            if not is_admin and review['user_id'] != current_user['id']:
                api.abort(403, "Unauthorized action: You can only delete your own reviews")
            return facade.delete_review(review_id)
        except ValueError as e:
            api.abort(404, str(e))
