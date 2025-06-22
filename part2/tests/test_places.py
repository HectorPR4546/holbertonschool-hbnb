import unittest
from app import create_app
from app.services import facade
from app.models.user import User
from app.models.place import Place

class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Create user directly
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
        facade.place_repo._storage = {}

    def test_create_valid_place(self):
        response = self.client.post('/api/v1/places/', json=self.valid_data)
        self.assertEqual(response.status_code, 201)

    def test_create_place_invalid_coordinates(self):
        invalid_data = self.valid_data.copy()
        invalid_data['latitude'] = 100  # Invalid
        response = self.client.post('/api/v1/places/', json=invalid_data)
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        facade.place_repo._storage = {}
        facade.user_repo._storage = {}
