import unittest
from app import create_app
from app.services import facade
from app.models.user import User

class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Create owner directly
        self.owner = User(
            first_name="Test",
            last_name="Owner",
            email="owner@example.com"
        )
        facade.user_repo.add(self.owner)
        
        self.valid_data = {
            "title": "Test Place",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.owner.id
        }
        
        # Clear existing data
        facade.place_repo._storage = {}

    def test_create_valid_place(self):
        response = self.client.post('/api/v1/places/', json=self.valid_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
        self.assertEqual(response.json['title'], self.valid_data['title'])

    def test_create_place_invalid_coordinates(self):
        test_cases = [
            ({"latitude": 100}, "Latitude must be between -90 and 90"),
            ({"longitude": -190}, "Longitude must be between -180 and 180"),
            ({"price": -50}, "Price must be a positive number"),
            ({"title": ""}, "Missing required fields")
        ]
        
        for data, expected_error in test_cases:
            with self.subTest(data=data):
                invalid_data = {**self.valid_data, **data}
                response = self.client.post('/api/v1/places/', json=invalid_data)
                self.assertEqual(response.status_code, 400)
                self.assertIn(expected_error, response.json['message'])

    def tearDown(self):
        # Clean up after tests
        facade.place_repo._storage = {}
        facade.user_repo._storage = {}
