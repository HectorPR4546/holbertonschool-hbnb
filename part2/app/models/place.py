# part2/app/models/place.py
from datetime import datetime
import uuid

class Place:
    def __init__(self, title, description, latitude, longitude, price_per_night,
                 number_of_rooms, number_of_bathrooms, max_guests, owner_id,
                 city_id, amenities=None): # amenities is a list of amenity IDs

        # Validation for required fields and types/ranges
        if not title or not isinstance(title, str) or title.strip() == "":
            raise ValueError("Title cannot be empty.")
        if not (isinstance(latitude, (int, float)) and -90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (isinstance(longitude, (int, float)) and -180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        if not (isinstance(price_per_night, (int, float)) and price_per_night >= 0):
            raise ValueError("Price per night must be a non-negative number.")
        if not (isinstance(number_of_rooms, int) and number_of_rooms >= 0):
            raise ValueError("Number of rooms must be a non-negative integer.")
        if not (isinstance(number_of_bathrooms, int) and number_of_bathrooms >= 0):
            raise ValueError("Number of bathrooms must be a non-negative integer.")
        if not (isinstance(max_guests, int) and max_guests >= 1):
            raise ValueError("Max guests must be a positive integer.")
        if not owner_id: # Validity of owner_id itself checked by facade
            raise ValueError("Owner ID cannot be empty.")
        if not city_id: # Validity of city_id itself checked by facade
            raise ValueError("City ID cannot be empty.")


        self.id = str(uuid.uuid4())
        self.title = title.strip()
        self.description = description.strip() if description else ""
        self.latitude = latitude
        self.longitude = longitude
        self.price_per_night = price_per_night
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_of_bathrooms
        self.max_guests = max_guests
        self.owner_id = owner_id
        self.city_id = city_id
        self.amenities = list(amenities) if amenities is not None else [] # Store amenity IDs as a list
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, data):
        # Update logic with validation
        if 'title' in data:
            if not data['title'] or not isinstance(data['title'], str) or data['title'].strip() == "":
                raise ValueError("Title cannot be empty.")
            self.title = data['title'].strip()
        if 'description' in data:
            self.description = data['description'].strip() if data['description'] else ""
        if 'latitude' in data:
            if not (isinstance(data['latitude'], (int, float)) and -90 <= data['latitude'] <= 90):
                raise ValueError("Latitude must be between -90 and 90.")
            self.latitude = data['latitude']
        if 'longitude' in data:
            if not (isinstance(data['longitude'], (int, float)) and -180 <= data['longitude'] <= 180):
                raise ValueError("Longitude must be between -180 and 180.")
            self.longitude = data['longitude']
        if 'price_per_night' in data:
            if not (isinstance(data['price_per_night'], (int, float)) and data['price_per_night'] >= 0):
                raise ValueError("Price per night must be a non-negative number.")
            self.price_per_night = data['price_per_night']
        if 'number_of_rooms' in data:
            if not (isinstance(data['number_of_rooms'], int) and data['number_of_rooms'] >= 0):
                raise ValueError("Number of rooms must be a non-negative integer.")
            self.number_of_rooms = data['number_of_rooms']
        if 'number_of_bathrooms' in data:
            if not (isinstance(data['number_of_bathrooms'], int) and data['number_of_bathrooms'] >= 0):
                raise ValueError("Number of bathrooms must be a non-negative integer.")
            self.number_of_bathrooms = data['number_of_bathrooms']
        if 'max_guests' in data:
            if not (isinstance(data['max_guests'], int) and data['max_guests'] >= 1):
                raise ValueError("Max guests must be a positive integer.")
            self.max_guests = data['max_guests']
        if 'owner_id' in data:
            if not data['owner_id']:
                raise ValueError("Owner ID cannot be empty.")
            self.owner_id = data['owner_id']
        if 'city_id' in data:
            if not data['city_id']:
                raise ValueError("City ID cannot be empty.")
            self.city_id = data['city_id']
        if 'amenities' in data:
            if not isinstance(data['amenities'], list):
                raise ValueError("Amenities must be a list of IDs.")
            # You might want to validate if amenity IDs exist in amenity_repo here,
            # but for now, just assign the list.
            self.amenities = list(data['amenities'])

        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'price_per_night': self.price_per_night,
            'number_of_rooms': self.number_of_rooms,
            'number_of_bathrooms': self.number_of_bathrooms,
            'max_guests': self.max_guests,
            'owner_id': self.owner_id,
            'city_id': self.city_id,
            'amenities': self.amenities, # List of amenity IDs
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
