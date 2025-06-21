import unittest
from app import create_app
from app.services import facade

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.valid_user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com"
        }

    def test_create_valid_user(self):
        response = self.client.post('/api/v1/users/', json=self.valid_user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_create_user_missing_fields(self):
        invalid_data = self.valid_user_data.copy()
        del invalid_data['first_name']
        response = self.client.post('/api/v1/users/', json=invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_email(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data['email'] = "not-an-email"
        response = self.client.post('/api/v1/users/', json=invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_get_user(self):
        # First create a user
        create_response = self.client.post('/api/v1/users/', json=self.valid_user_data)
        user_id = create_response.json['id']
        
        # Then try to retrieve it
        get_response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json['email'], self.valid_user_data['email'])

    def tearDown(self):
        # Clean up the repository after each test
        facade.user_repo._storage = {}
