# part2/tests/test_review_endpoints.py
import unittest
import json
from app import create_app
from app.services.facade import HBnBFacade

class TestReviewEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.app.config['TESTING'] = True

    def setUp(self):
        # Clear repositories for each test to ensure isolation
        HBnBFacade().user_repo.clear()
        HBnBFacade().place_repo.clear()
        HBnBFacade().review_repo.clear()
        HBnBFacade().amenity_repo.clear()

        # Create a user and a place for review creation tests
        self.user_data = {"first_name": "Reviewer", "last_name": "User", "email": "reviewer@example.com"}
        user_response = self.client.post('/api/v1/users/', json=self.user_data)
        self.user_id = json.loads(user_response.data)['id']

        self.place_data = {
            "title": "Reviewable Place", "description": "Great for reviews", "price": 100,
            "latitude": 10, "longitude": 10, "owner_id": self.user_id
        }
        place_response = self.client.post('/api/v1/places/', json=self.place_data)
        self.place_id = json.loads(place_response.data)['id']

    def test_create_review_success(self):
        """Test successful review creation."""
        review_data = {
            "text": "This is a great review!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        response = self.client.post('/api/v1/reviews/', json=review_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['text'], review_data['text'])
        self.assertEqual(data['rating'], review_data['rating'])
        self.assertEqual(data['user_id'], self.user_id)
        self.assertEqual(data['place_id'], self.place_id)

    def test_create_review_empty_text(self):
        """Test review creation with empty text."""
        review_data = {
            "text": "",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        response = self.client.post('/api/v1/reviews/', json=review_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Review text cannot be empty.", data['message'])

    def test_create_review_invalid_rating_low(self):
        """Test review creation with rating below 1."""
        review_data = {
            "text": "Rating too low",
            "rating": 0,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        response = self.client.post('/api/v1/reviews/', json=review_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Rating must be between 1 and 5.", data['message'])

    def test_create_review_invalid_rating_high(self):
        """Test review creation with rating above 5."""
        review_data = {
            "text": "Rating too high",
            "rating": 6,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        response = self.client.post('/api/v1/reviews/', json=review_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Rating must be between 1 and 5.", data['message'])

    def test_create_review_non_existent_user(self):
        """Test review creation with non-existent user ID."""
        review_data = {
            "text": "Missing user",
            "rating": 4,
            "user_id": "non-existent-user-id",
            "place_id": self.place_id
        }
        response = self.client.post('/api/v1/reviews/', json=review_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("User with ID 'non-existent-user-id' not found for review.", data['message'])

    def test_create_review_non_existent_place(self):
        """Test review creation with non-existent place ID."""
        review_data = {
            "text": "Missing place",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": "non-existent-place-id"
        }
        response = self.client.post('/api/v1/reviews/', json=review_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Place with ID 'non-existent-place-id' not found for review.", data['message'])

    def test_get_all_reviews_empty(self):
        """Test getting all reviews when none exist."""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [])

    def test_get_review_by_id_success(self):
        """Test getting a review by ID successfully."""
        review_data = {
            "text": "Get This Review", "rating": 5,
            "user_id": self.user_id, "place_id": self.place_id
        }
        create_response = self.client.post('/api/v1/reviews/', json=review_data)
        review_id = json.loads(create_response.data)['id']

        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], review_id)
        self.assertEqual(data['text'], "Get This Review")

    def test_get_review_not_found(self):
        """Test getting a non-existent review."""
        response = self.client.get('/api/v1/reviews/non-existent-id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)['message'], 'Review not found')

    def test_update_review_success(self):
        """Test successful review update."""
        review_data = {
            "text": "Original Review", "rating": 3,
            "user_id": self.user_id, "place_id": self.place_id
        }
        create_response = self.client.post('/api/v1/reviews/', json=review_data)
        review_id = json.loads(create_response.data)['id']

        update_data = {"text": "Updated Review Text", "rating": 4}
        response = self.client.put(f'/api/v1/reviews/{review_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['text'], "Updated Review Text")
        self.assertEqual(data['rating'], 4)

    def test_update_review_invalid_rating(self):
        """Test updating review with invalid rating."""
        review_data = {
            "text": "Original Review", "rating": 3,
            "user_id": self.user_id, "place_id": self.place_id
        }
        create_response = self.client.post('/api/v1/reviews/', json=review_data)
        review_id = json.loads(create_response.data)['id']

        update_data = {"rating": 0}
        response = self.client.put(f'/api/v1/reviews/{review_id}', json=update_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Rating must be between 1 and 5.", data['message'])

    def test_update_review_not_found(self):
        """Test updating a non-existent review."""
        response = self.client.put('/api/v1/reviews/non-existent-id', json={"text": "Test"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)['message'], 'Review not found')

    def test_delete_review_success(self):
        """Test successful review deletion."""
        review_data = {
            "text": "Delete Me", "rating": 2,
            "user_id": self.user_id, "place_id": self.place_id
        }
        create_response = self.client.post('/api/v1/reviews/', json=review_data)
        review_id = json.loads(create_response.data)['id']

        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], 'Review deleted successfully')

        # Verify deletion
        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)

    def test_delete_review_not_found(self):
        """Test deleting a non-existent review."""
        response = self.client.delete('/api/v1/reviews/non-existent-id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)['message'], 'Review not found')

    def test_get_reviews_for_place_success(self):
        """Test getting all reviews for a specific place."""
        # Create a second place and review for it
        place_data_2 = {
            "title": "Another Place", "description": "Another great place", "price": 50,
            "latitude": 20, "longitude": 20, "owner_id": self.user_id
        }
        place_response_2 = self.client.post('/api/v1/places/', json=place_data_2)
        place_id_2 = json.loads(place_response_2.data)['id']

        # Reviews for first place
        self.client.post('/api/v1/reviews/', json={
            "text": "Review 1 for Place 1", "rating": 5, "user_id": self.user_id, "place_id": self.place_id
        })
        self.client.post('/api/v1/reviews/', json={
            "text": "Review 2 for Place 1", "rating": 4, "user_id": self.user_id, "place_id": self.place_id
        })
        # Review for second place
        self.client.post('/api/v1/reviews/', json={
            "text": "Review 1 for Place 2", "rating": 3, "user_id": self.user_id, "place_id": place_id_2
        })

        response = self.client.get(f'/api/v1/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['text'], "Review 1 for Place 1")
        self.assertEqual(data[1]['text'], "Review 2 for Place 1")

    def test_get_reviews_for_place_not_found(self):
        """Test getting reviews for a non-existent place."""
        response = self.client.get('/api/v1/places/non-existent-place-id/reviews')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)['message'], 'Place not found')

    def test_place_has_nested_reviews_on_get_single_place(self):
        """Test that getting a single place includes its nested reviews."""
        self.client.post('/api/v1/reviews/', json={
            "text": "Nested Review Test", "rating": 4, "user_id": self.user_id, "place_id": self.place_id
        })

        response = self.client.get(f'/api/v1/places/{self.place_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('reviews', data)
        self.assertEqual(len(data['reviews']), 1)
        self.assertEqual(data['reviews'][0]['text'], "Nested Review Test")
        self.assertEqual(data['reviews'][0]['rating'], 4)
