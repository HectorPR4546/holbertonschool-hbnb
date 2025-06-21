import unittest
from app import create_app
from app.services import facade

class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Create a user to be the owner
        self.owner = facade.create_user({
            "first_name": "Place",
            "last_name": "Owner",
            "email": "owner@example.com"
        })
        
        self.valid_place_data = {
            "title": "Test Place",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.owner.id
        }

    def test_create_valid_place(self):
        response = self.client.post('/api/v1/places/', json=self.valid_place_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_create_place_invalid_coordinates(self):
        invalid_data = self.valid_place_data.copy()
        invalid_data['latitude'] = 100  # Invalid latitude
        response = self.client.post('/api/v1/places/', json=invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_get_place_with_reviews(self):
        # Create a place
        place = facade.create_place(self.valid_place_data)
        
        # Add a review
        facade.create_review({
            "text": "Great place!",
            "rating": 5,
            "user_id": self.owner.id,
            "place_id": place.id
        })
        
        # Get the place
        response = self.client.get(f'/api/v1/places/{place.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['reviews']), 1)

    def tearDown(self):
        facade.place_repo._storage = {}
        facade.user_repo._storage = {}
        facade.review_repo._storage = {}
