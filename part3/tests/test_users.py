import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user_success(self):
        payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        }
        response = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["first_name"], "Jane")

    def test_create_user_invalid_data(self):
        payload = {
            "first_name": "",
            "last_name": "",
            "email": "not-an-email"
        }
        response = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_get_user_not_found(self):
        response = self.client.get("/api/v1/users/unknown-id")
        self.assertEqual(response.status_code, 404)

    def test_get_all_users(self):
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

if __name__ == "__main__":
    unittest.main()
