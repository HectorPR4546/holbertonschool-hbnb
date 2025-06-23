# part2/tests/test_amenity_endpoints.py
import unittest
import json
from app import create_app
from app.services.facade import HBnBFacade

class TestAmenityEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.app.config['TESTING'] = True

    def setUp(self):
        HBnBFacade().user_repo.clear()
        HBnBFacade().place_repo.clear()
        HBnBFacade().review_repo.clear()
        HBnBFacade().amenity_repo.clear()

    def test_create_amenity_success(self):
        """Test successful amenity creation."""
        amenity_data = {"name": "Wi-Fi"}
        response = self.client.post('/api/v1/amenities/', json=amenity_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], amenity_data['name'])

    def test_create_amenity_empty_name(self):
        """Test amenity creation with empty name."""
        amenity_data = {"name": ""}
        response = self.client.post('/api/v1/amenities/', json=amenity_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Amenity name cannot be empty.", data['message'])

    def test_create_amenity_duplicate_name(self):
        """Test amenity creation with duplicate name."""
        amenity_data = {"name": "Parking"}
        self.client.post('/api/v1/amenities/', json=amenity_data)

        response = self.client.post('/api/v1/amenities/', json=amenity_data)
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertIn("Amenity with name 'Parking' already exists.", data['message'])

    def test_get_all_amenities_empty(self):
        """Test getting all amenities when none exist."""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [])

    def test_get_amenity_by_id_success(self):
        """Test getting an amenity by ID successfully."""
        create_response = self.client.post('/api/v1/amenities/', json={"name": "Pool"})
        amenity_id = json.loads(create_response.data)['id']

        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], amenity_id)
        self.assertEqual(data['name'], "Pool")

    def test_get_amenity_not_found(self):
        """Test getting a non-existent amenity."""
        response = self.client.get('/api/v1/amenities/non-existent-id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)['message'], 'Amenity not found')

    def test_update_amenity_success(self):
        """Test successful amenity update."""
        create_response = self.client.post('/api/v1/amenities/', json={"name": "OldName"})
        amenity_id = json.loads(create_response.data)['id']

        update_data = {"name": "NewName"}
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "NewName")

    def test_update_amenity_empty_name(self):
        """Test updating amenity with empty name."""
        create_response = self.client.post('/api/v1/amenities/', json={"name": "Test"})
        amenity_id = json.loads(create_response.data)['id']

        update_data = {"name": ""}
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json=update_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Amenity name cannot be empty.", data['message'])

    def test_update_amenity_not_found(self):
        """Test updating a non-existent amenity."""
        response = self.client.put('/api/v1/amenities/non-existent-id', json={"name": "Test"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)['message'], 'Amenity not found')

    def test_delete_amenity_success(self):
        """Test successful amenity deletion."""
        create_response = self.client.post('/api/v1/amenities/', json={"name": "DeleteMe"})
        amenity_id = json.loads(create_response.data)['id']

        response = self.client.delete(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], 'Amenity deleted successfully')

        # Verify deletion
        get_response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(get_response.status_code, 404)

    def test_delete_amenity_not_found(self):
        """Test deleting a non-existent amenity."""
        response = self.client.delete('/api/v1/amenities/non-existent-id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)['message'], 'Amenity not found')
