import unittest
from app.models.user import User
from app.models.place import Place

class TestModels(unittest.TestCase):
    def test_create_user(self):
        user = User("John", "Doe", "john@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john@example.com")

    def test_create_place(self):
        user = User("John", "Doe", "john@example.com")
        place = Place("Nice Spot", "Great view", 150.0, 18.0, -66.0, user.id)
        self.assertEqual(place.title, "Nice Spot")
        self.assertEqual(place.owner_id, user.id)

    def test_place_invalid_price(self):
        user = User("John", "Doe", "john@example.com")
        with self.assertRaises(ValueError):
            Place("Cheap Place", "Bad area", -20, 18.0, -66.0, user.id)

    def test_place_invalid_latitude(self):
        user = User("John", "Doe", "john@example.com")
        with self.assertRaises(ValueError):
            Place("Wrong Latitude", "Invalid", 100.0, 200.0, -66.0, user.id)

    def test_place_invalid_longitude(self):
        user = User("John", "Doe", "john@example.com")
        with self.assertRaises(ValueError):
            Place("Wrong Longitude", "Invalid", 100.0, 18.0, -200.0, user.id)
