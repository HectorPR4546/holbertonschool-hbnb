import unittest
from app import create_app

class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Create valid user and place
        self.user = self.client.post('/api/v1/users/', json={
            "first_name": "Ana",
            "last_name": "Ramos",
            "email": "ana@example.com"
        }).json

        self.place = self.client.post('/api/v1/places/', json={
            "title": "Seaside View",
            "description": "Ocean breeze",
            "price": 150.0,
            "latitude": 18.3,
            "longitude": -66.5,
            "owner_id": self.user["id"],
            "amenities": []
        }).json

    def test_create_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Amazing stay!",
            "rating": 5,
            "user_id": self.user["id"],
            "place_id": self.place["id"]
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["rating"], 5)

    def test_create_review_invalid(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 7,
            "user_id": self.user["id"],
            "place_id": self.place["id"]
        })
        self.assertEqual(response.status_code, 400)
