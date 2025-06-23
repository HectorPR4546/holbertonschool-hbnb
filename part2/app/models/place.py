# part2/app/models/place.py

from app.models.base_model import BaseModel
import uuid
from datetime import datetime

# Use direct module imports to break potential circular dependencies
import app.models.user    # Import user module
import app.models.amenity # Import amenity module
import app.models.review  # Import review module

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner, **kwargs):
        super().__init__(**kwargs)
        # Initialize internal attributes to None or empty lists
        self._title = None
        self._description = None
        self._price = None
        self._latitude = None
        self._longitude = None
        self._owner = None
        self._amenities = [] # Initialize as empty list
        self._reviews = [] # Initialize as empty list

        # Assign values using setters to trigger validation
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner # This will call the owner setter

    # --- Properties with Getters and Setters for Validation ---

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # Validation: Not empty
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title cannot be empty.")
        self._title = value.strip()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        # Description can be None or an empty string, but if present, must be string
        if value is not None:
            if not isinstance(value, str):
                raise TypeError("Description must be a string or None.")
            self._description = value.strip() if value.strip() else None
        else:
            self._description = None

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number.")
        if value < 0: # Ensures positive or zero
            raise ValueError("Price must be a non-negative number.")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number.")
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number.")
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        self._longitude = float(value)

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        # Refer to User using its module prefix
        if not isinstance(value, app.models.user.User):
            raise TypeError("Owner must be an instance of User.")
        self._owner = value

    @property
    def amenities(self):
        return list(self._amenities) # Return a copy to prevent external modification

    def add_amenity(self, amenity):
        # Refer to Amenity using its module prefix
        if not isinstance(amenity, app.models.amenity.Amenity):
            raise TypeError(f"Cannot add non-Amenity object: {type(amenity)}")
        if amenity not in self._amenities:
            self._amenities.append(amenity)

    def remove_amenity(self, amenity_id):
        self._amenities = [a for a in self._amenities if a.id != amenity_id]

    @property
    def reviews(self):
        return list(self._reviews) # Return a copy

    def add_review(self, review):
        # Refer to Review using its module prefix
        if not isinstance(review, app.models.review.Review):
            raise TypeError("Cannot add non-Review object to reviews.")
        if review not in self._reviews:
            self._reviews.append(review)

    def remove_review(self, review_id):
        """Removes a review from the place's collection by its ID."""
        self._reviews = [r for r in self._reviews if r.id != review_id]

    # --- Update and to_dict Methods ---

    def update(self, data):
        """Updates Place attributes, using setters for validation."""
        if 'title' in data:
            self.title = data['title']
        if 'description' in data:
            self.description = data['description']
        if 'price' in data:
            self.price = data['price']
        if 'latitude' in data:
            self.latitude = data['latitude']
        if 'longitude' in data:
            self.longitude = data['longitude']
        self.updated_at = datetime.now()

    def to_dict(self, include_relationships=False):
        """
        Returns a dictionary representation of the Place instance.
        If include_relationships is True, includes nested owner, amenities, and reviews details.
        """
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner.id if self.owner else None, # Safely access owner.id
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "reviews": [review.id for review in self.reviews] # Default to showing review IDs
        }

        if include_relationships:
            # Include full owner object if requested
            if self.owner:
                data["owner"] = self.owner.to_dict()
            else:
                data["owner"] = None

            # Include full amenities list if requested
            data["amenities"] = [amenity.to_dict() for amenity in self.amenities]

            # Include full reviews list if requested, using their nested dict format
            data["reviews"] = [review.to_nested_dict() for review in self.reviews]


        return data
