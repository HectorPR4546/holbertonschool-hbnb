# part2/tests/test_place_endpoints.py
import unittest
import json
from app import create_app
from app.services.facade import HBnBFacade

class TestPlaceEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.app.config['TESTING'] = True

    def setUp(self):
        # Clear repositories for each test to ensure isolation
        HBnBFacade().user_repo.clear()
        HBnBFacade().place_repo.clear()
        HBnBFacade().review_repo.clear()
        HBnBFacade().amenity_repo.clear()

        # Create a default user and amenity for place creation tests
        self.user_data = {"first_name": "Place", "last_name": "Owner", "email": "place.owner@example.com"}
        user_response = self.client.post('/api/v1/users/', json=self.user_data)
        self.user_id = json.loads(user_response.data)['id']

        self.amenity_data = {"name": "Parking"}
        amenity_response = self.client.post('/api/v1/amenities/', json=self.amenity_data)
        self.amenity_id = json.loads(amenity_response.data)['id']

    def test_create_place_success(self):
        """Test successful place creation."""
        place_data = {
            "title": "Cozy Apartment",
            "description": "Lovely place downtown.",
            "price": 150.0,
            "latitude": 34.05,
            "longitude": -118.25,
            "owner_id": self.user_id,
            "amenities": [self.amenity_id]
        }
        response = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['title'], place_data['title'])
        self.assertEqual(data['owner_id'], self.user_id)
        self.assertIn(self.amenity_id, [a['id'] for a in data['amenities']]) # Check nested amenities

    def test_create_place_empty_title(self):
        """Test place creation with empty title."""
        place_data = {
            "title": "",
            "description": "...", "price": 100, "latitude": 0, "longitude": 0, "owner_id": self.user_id
        }
        response = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Title cannot be empty.", data['message'])

    def test_create_place_negative_price(self):
        """Test place creation with negative price."""
        place_data = {
            "title": "Bad Price Place",
            "description": "...", "price": -10.0, "latitude": 0, "longitude": 0, "owner_id": self.user_id
        }
        response = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Price must be a non-negative number.", data['message'])

    def test_create_place_invalid_latitude(self):
        """Test place creation with out-of-range latitude."""
        place_data = {
            "title": "Bad Lat Place",
            "description": "...", "price": 100, "latitude": 91.0, "longitude": 0, "owner_id": self.user_id
        }
        response = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Latitude must be between -90 and 90.", data['message'])

    def test_create_place_invalid_longitude(self):
        """Test place creation with out-of-range longitude."""
        place_data = {
            "title": "Bad Lon Place",
            "description": "...", "price": 100, "latitude": 0, "longitude": -181.0, "owner_id": self.user_id
        }
        response = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Longitude must be between -180 and 180.", data['message'])

    def test_create_place_non_existent_owner(self):
        """Test place creation with non-existent owner ID."""
        place_data = {
            "title": "No Owner Place",
            "description": "...", "price": 100, "latitude": 0, "longitude": 0, "owner_id": "non-existent-user-id"
        }
        response = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Owner with ID 'non-existent-user-id' not found.", data['message'])

    def test_get_all_places_empty(self):
        """Test getting all places when none exist."""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [])

    def test_get_place_by_id_success(self):
        """Test getting a place by ID successfully."""
        place_data = {
            "title": "Test Place", "description": "Desc", "price": 100,
            "latitude": 10, "longitude": 10, "owner_id": self.user_id
        }
        create_response = self.client.post('/api/v1/places/', json=place_data)
        place_id = json.loads(create_response.data)['id']

        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], place_id)
        self.assertEqual(data['title'], "Test Place")

    def test_get_place_not_found(self):
        """Test getting a non-existent place."""
        response = self.client.get('/api/v1/places/non-existent-id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)['message'], 'Place not found')

    def test_update_place_success(self):
        """Test successful place update."""
        place_data = {
            "title": "Original Place", "description": "Desc", "price": 100,
            "latitude": 10, "longitude": 10, "owner_id": self.user_id
        }
        create_response = self.client.post('/api/v1/places/', json=place_data)
        place_id = json.loads(create_response.data)['id']

        update_data = {"title": "Updated Place", "price": 200.0, "description": "New Desc"}
        response = self.client.put(f'/api/v1/places/{place_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], "Updated Place")
        self.assertEqual(data['price'], 200.0)
        self.assertEqual(data['description'], "New Desc")

    def test_update_place_invalid_price(self):
        """Test updating place with invalid price."""
        place_data = {
            "title": "Original Place", "description": "Desc", "price": 100,
            "latitude": 10, "longitude": 10, "owner_id": self.user_id
        }
        create_response = self.client.post('/api/v1/places/', json=place_data)
        place_id = json.loads(create_response.data)['id']

        update_data = {"price": -50.0}
        response = self.client.put(f'/api/v1/places/{place_id}', json=update_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Price must be a non-negative number.", data['message'])

    def test_update_place_not_found(self):
        """Test updating a non-existent place."""
        response = self.client.put('/api/v1/places/non-existent-id', json={"title": "Test"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)['message'], 'Place not found')

    def test_delete_place_success(self):
        """Test successful place deletion."""
        place_data = {
            "title": "Delete Me", "description": "Desc", "price": 100,
            "latitude": 10, "longitude": 10, "owner_id": self.user_id
        }
        create_response = self.client.post('/api/v1/places/', json=place_data)
        place_id = json.loads(create_response.data)['id']

        response = self.client.delete(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], 'Place deleted successfully')

        # Verify deletion
        get_response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(get_response.status_code, 404)

    def test_delete_place_not_found(self):
        """Test deleting a non-existent place."""
        response = self.client.delete('/api/v1/places/non-existent-id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)['message'], 'Place not found')

    def test_place_amenity_association(self):
        """Test associating and disassociating amenities."""
        place_data = {
            "title": "Amenity Test Place", "description": "Desc", "price": 100,
            "latitude": 10, "longitude": 10, "owner_id": self.user_id,
            "amenities": [self.amenity_id]
        }
        create_response = self.client.post('/api/v1/places/', json=place_data)
        place_id = json.loads(create_response.data)['id']

        get_response = self.client.get(f'/api/v1/places/{place_id}')
        data = json.loads(get_response.data)
        self.assertEqual(len(data['amenities']), 1)
        self.assertEqual(data['amenities'][0]['id'], self.amenity_id)

        # Update to remove amenities
        update_response = self.client.put(f'/api/v1/places/{place_id}', json={"amenities": []})
        self.assertEqual(update_response.status_code, 200)
        get_response = self.client.get(f'/api/v1/places/{place_id}')
        data = json.loads(get_response.data)
        self.assertEqual(len(data['amenities']), 0)
