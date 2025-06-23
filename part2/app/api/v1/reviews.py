# part2/app/api/v1/reviews.py

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the models for input and output

# Full Review model for POST, GET by ID, and PUT response
review_full_model = api.model('ReviewFull', {
    'id': fields.String(readOnly=True, description='The review unique identifier'),
    'text': fields.String(required=True, description='Text of the review', min_length=1),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)', min=1, max=5),
    'user_id': fields.String(required=True, description='ID of the user who made the review'),
    'place_id': fields.String(required=True, description='ID of the place being reviewed'),
    'created_at': fields.DateTime(dt_format='iso8601', description='Timestamp of creation', readOnly=True),
    'updated_at': fields.DateTime(dt_format='iso8601', description='Timestamp of last update', readOnly=True)
})

# Input model for POST (user_id and place_id are required here)
review_input_post_model = api.model('ReviewInputPost', {
    'text': fields.String(required=True, description='Text of the review', min_length=1),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)', min=1, max=5),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Input model for PUT (user_id and place_id are not updated via PUT, only text/rating)
review_input_put_model = api.model('ReviewInputPut', {
    'text': fields.String(required=False, description='Text of the review', min_length=1),
    'rating': fields.Integer(required=False, description='Rating of the place (1-5)', min=1, max=5)
})

# Simplified Review model for list views or nested displays (e.g., within a Place object)
review_list_item_model = api.model('ReviewListItem', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)')
})

@api.route('/')
class ReviewList(Resource):
    @api.doc('create_review')
    @api.expect(review_input_post_model, validate=True)
    @api.marshal_with(review_full_model, code=201)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data or User/Place not found')
    def post(self):
        """Register a new review"""
        review_data = api.payload
        try:
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except (ValueError, TypeError) as e:
            return {'message': str(e)}, 400
        except Exception as e:
            api.abort(500, message=f"An unexpected error occurred: {str(e)}")


    @api.doc('list_all_reviews')
    @api.marshal_list_with(review_list_item_model) # Use simplified model for list
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        # Marshal using to_nested_dict as it matches the fields in review_list_item_model
        return [review.to_nested_dict() for review in reviews], 200

@api.route('/<string:review_id>')
@api.param('review_id', 'The review unique identifier')
class ReviewResource(Resource):
    @api.doc('get_review')
    @api.marshal_with(review_full_model)
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.doc('update_review')
    @api.expect(review_input_put_model, validate=True) # Use PUT specific input model
    @api.marshal_with(review_full_model) # Return full updated object
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        try:
            updated_review = facade.update_review(review_id, review_data)
            if not updated_review:
                return {'message': 'Review not found'}, 404
            return updated_review.to_dict(), 200 # Return the updated review object
        except (ValueError, TypeError) as e:
            return {'message': str(e)}, 400
        except Exception as e:
            api.abort(500, message=f"An unexpected error occurred: {str(e)}")

    @api.doc('delete_review')
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        deleted = facade.delete_review(review_id)
        if not deleted:
            return {'message': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<string:place_id>/reviews')
@api.param('place_id', 'The place unique identifier')
class PlaceReviewList(Resource):
    @api.doc('get_reviews_by_place')
    @api.marshal_list_with(review_list_item_model) # Use simplified model for list
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None: # Facade returns None if place not found
            return {'message': 'Place not found'}, 404
        # Place.reviews returns Review objects, convert to simplified dict for list
        return [review.to_nested_dict() for review in reviews], 200
