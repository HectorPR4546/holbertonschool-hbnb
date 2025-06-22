import unittest
from app import create_app
from app.services import facade
from app.models.user import User

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.valid_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "valid@example.com"
        }
        facade.user_repo._storage = {}

    def test_create_valid_user(self):
        response = self.client.post('/api/v1/users/', json=self.valid_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_create_user_invalid_email(self):
        test_cases = [
            ("invalid-email", "Invalid email format"),
            ("", "Email must be a string"),
            (None, "Email must be a string"),
            ("a"*121 + "@test.com", "Email too long")
        ]
        
        for email, expected_error in test_cases:
            with self.subTest(email=email):
                invalid_data = self.valid_data.copy()
                invalid_data['email'] = email
                response = self.client.post('/api/v1/users/', json=invalid_data)
                self.assertEqual(response.status_code, 400)
                self.assertIn(expected_error, response.json['message'])

    def test_get_user(self):
        # Create directly to avoid API dependency
        user = User(**self.valid_data)
        facade.user_repo.add(user)
        
        response = self.client.get(f'/api/v1/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], self.valid_data['email'])

    def tearDown(self):
        facade.user_repo._storage = {}
