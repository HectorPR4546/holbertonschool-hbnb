import unittest
from app import create_app
import uuid

class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Create valid user and amenity
        self.user = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Smith",
            "email": "john@example.com"
        }).json

        self.amenity = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        }).json

    def test_create_place(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Nice Spot",
            "description": "Cozy location",
            "price": 120.0,
            "latitude": 18.0,
            "longitude": -66.0,
            "owner_id": self.user["id"],
            "amenities": [self.amenity["id"]]
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["title"], "Nice Spot")

    def test_create_place_invalid_price(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Bad Place",
            "price": -100,
            "latitude": 18.0,
            "longitude": -66.0,
            "owner_id": self.user["id"],
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)
