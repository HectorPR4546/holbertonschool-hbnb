# part2/tests/test_user_endpoints.py
import unittest
import json
from app import create_app
from app.services.facade import HBnBFacade # To reset state if needed

class TestUserEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # This method is called once for the entire test class
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.app.config['TESTING'] = True # Enable testing mode

    def setUp(self):
        # This method is called before each test function
        # Ensure a clean state for InMemoryRepository by re-initializing Facade's repos
        # This is CRUCIAL for isolated unit tests
        HBnBFacade().user_repo.clear()
        HBnBFacade().place_repo.clear()
        HBnBFacade().review_repo.clear()
        HBnBFacade().amenity_repo.clear()

    def test_create_user_success(self):
        """Test successful user creation."""
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com"
        }
        response = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['email'], user_data['email'])
        self.assertEqual(data['first_name'], user_data['first_name'])
        self.assertEqual(data['last_name'], user_data['last_name'])

    def test_create_user_invalid_email_format(self):
        """Test user creation with invalid email format."""
        user_data = {
            "first_name": "Invalid",
            "last_name": "Email",
            "email": "invalid-email" # Missing @ or .
        }
        response = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Invalid email format.", data['message'])

    def test_create_user_empty_first_name(self):
        """Test user creation with empty first name."""
        user_data = {
            "first_name": "",
            "last_name": "User",
            "email": "empty_first@example.com"
        }
        response = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("First name cannot be empty.", data['message'])

    def test_create_user_empty_last_name(self):
        """Test user creation with empty last name."""
        user_data = {
            "first_name": "Test",
            "last_name": "",
            "email": "empty_last@example.com"
        }
        response = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Last name cannot be empty.", data['message'])

    def test_create_user_empty_email(self):
        """Test user creation with empty email."""
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": ""
        }
        response = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Email cannot be empty.", data['message'])

    def test_create_user_duplicate_email(self):
        """Test user creation with duplicate email."""
        user_data = {
            "first_name": "Duplicate",
            "last_name": "User",
            "email": "duplicate@example.com"
        }
        self.client.post('/api/v1/users/', json=user_data) # Create first user

        response = self.client.post('/api/v1/users/', json=user_data) # Try to create again
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertIn("User with email 'duplicate@example.com' already exists.", data['message'])

    def test_get_all_users_empty(self):
        """Test getting all users when none exist."""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [])

    def test_get_all_users_with_data(self):
        """Test getting all users when some exist."""
        self.client.post('/api/v1/users/', json={"first_name": "U1", "last_name": "L1", "email": "u1@e.com"})
        self.client.post('/api/v1/users/', json={"first_name": "U2", "last_name": "L2", "email": "u2@e.com"})
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['email'], 'u1@e.com')

    def test_get_user_by_id_success(self):
        """Test getting a user by ID successfully."""
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "Find", "last_name": "Me", "email": "findme@example.com"
        })
        user_id = json.loads(create_response.data)['id']

        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], user_id)
        self.assertEqual(data['email'], 'findme@example.com')

    def test_get_user_not_found(self):
        """Test getting a user with a non-existent ID."""
        response = self.client.get('/api/v1/users/non-existent-id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)['message'], 'User not found')

    def test_update_user_success(self):
        """Test successful user update."""
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "Old", "last_name": "Name", "email": "old@example.com"
        })
        user_id = json.loads(create_response.data)['id']

        update_data = {"first_name": "New", "last_name": "Updated"}
        response = self.client.put(f'/api/v1/users/{user_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], "New")
        self.assertEqual(data['last_name'], "Updated")
        self.assertEqual(data['email'], "old@example.com") # Email should remain unchanged if not in update_data

    def test_update_user_invalid_email(self):
        """Test updating user with invalid email."""
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "Valid", "last_name": "User", "email": "valid@example.com"
        })
        user_id = json.loads(create_response.data)['id']

        update_data = {"email": "bad_email"}
        response = self.client.put(f'/api/v1/users/{user_id}', json=update_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Invalid email format.", data['message'])

    def test_update_user_not_found(self):
        """Test updating a non-existent user."""
        response = self.client.put('/api/v1/users/non-existent-id', json={"first_name": "Test"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)['message'], 'User not found')

    def test_delete_user_success(self):
        """Test successful user deletion."""
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "Delete", "last_name": "Me", "email": "delete@example.com"
        })
        user_id = json.loads(create_response.data)['id']

        response = self.client.delete(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], 'User deleted successfully')

        # Verify deletion
        get_response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(get_response.status_code, 404)

    def test_delete_user_not_found(self):
        """Test deleting a non-existent user."""
        response = self.client.delete('/api/v1/users/non-existent-id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)['message'], 'User not found')
