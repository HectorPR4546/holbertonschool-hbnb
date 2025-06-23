from app.models.base_model import BaseModel
from app.models.user import User # We need to import User for type checking!
from app.models.amenity import Amenity # We need to import Amenity for type checking!

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self._title = None
        self._description = None # Optional, can be None
        self._price = None
        self._latitude = None
        self._longitude = None
        self._owner = None # This will hold a User object

        # Assign through setters to trigger validation
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner # This setter will validate it's a User

        # Initialize lists for relationships
        self._reviews = []  # List to store related Review objects
        self._amenities = [] # List to store related Amenity objects


    def to_dict(self, include_relationships=False):
        """
        Returns a dictionary representation of the Place instance.
        If include_relationships is True, includes nested owner and amenities details.
        """
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner.id, # Always include owner_id
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            # Reviews are not detailed here yet, just showing their IDs for completeness.
            # They will be nested fully in a later task.
            "reviews": [review.id for review in self.reviews] # List of review IDs
        }

        if include_relationships:
            # Include full owner object if requested
            if self.owner:
                data["owner"] = self.owner.to_dict() # Recursively call to_dict on owner

            # Include full amenities list if requested
            data["amenities"] = [amenity.to_dict() for amenity in self.amenities] # Recursively call to_dict on amenities

        return data

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value:
            raise ValueError("Place title is required.")
        if not isinstance(value, str):
            raise TypeError("Place title must be a string.")
        if len(value) > 100:
            raise ValueError("Place title cannot exceed 100 characters.")
        self._title = value
        self.save()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("Place description must be a string or None.")
        self._description = value
        self.save()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number.")
        if value <= 0:
            raise ValueError("Price must be a positive value.")
        self._price = float(value) # Ensure it's a float
        self.save()

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number.")
        if not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        self._latitude = float(value)
        self.save()

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number.")
        if not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0.")
        self._longitude = float(value)
        self.save()

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise TypeError("Owner must be an instance of User.")
        # We might add a check here in a real scenario to ensure the user exists
        # in the repository, but for now, just checking the type is enough.
        self._owner = value
        self.save()

    @property
    def reviews(self):
        return self._reviews

    @property
    def amenities(self):
        return self._amenities

    def add_review(self, review):
        """Add a review to this place. Expects a Review object."""
        # We will add a type check here when the Review class is defined.
        # For now, let's assume valid input.
        self._reviews.append(review)
        self.save() # Update timestamp on the Place when a review is added

    def remove_review(self, review_id):
        """Remove a review from this place by its ID."""
        original_len = len(self._reviews)
        self._reviews = [r for r in self._reviews if r.id != review_id]
        if len(self._reviews) < original_len:
            self.save() # Update timestamp if a review was removed
            return True
        return False

    def add_amenity(self, amenity):
        """Add an amenity to this place. Expects an Amenity object."""
        if not isinstance(amenity, Amenity):
            raise TypeError("Amenity must be an instance of Amenity.")
        if amenity not in self._amenities: # Prevent duplicates
            self._amenities.append(amenity)
            self.save() # Update timestamp on the Place when an amenity is added

    def remove_amenity(self, amenity_id):
        """Remove an amenity from this place by its ID."""
        original_len = len(self._amenities)
        self._amenities = [a for a in self._amenities if a.id != amenity_id]
        if len(self._amenities) < original_len:
            self.save() # Update timestamp if an amenity was removed
            return True
        return False

    def to_dict(self):
        """Returns a dictionary representation of the Place instance."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner.id, # Store owner's ID, not the object
            "owner_email": self.owner.email, # Maybe add email for convenience
            "reviews_ids": [r.id for r in self.reviews], # Store review IDs
            "amenities_ids": [a.id for a in self.amenities], # Store amenity IDs
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"Place(id='{self.id}', title='{self.title}', owner='{self.owner.email}')"

    def update(self, data):
        """
        Updates the place attributes based on the provided dictionary.
        This overrides BaseModel's update to use setters for validation.
        """
        super_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key in super_keys:
                continue

            # Special handling for owner, reviews, and amenities if they were to be updated directly
            # For now, we expect owner to be a User object, reviews/amenities to be managed by add/remove methods
            if key == 'owner':
                self.owner = value # Use the setter
            elif key == 'reviews' or key == 'amenities':
                print(f"Warning: '{key}' should be updated via add/remove methods, not directly.")
                continue
            elif hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"Warning: Attempted to update non-existent attribute '{key}' for Place.")
        self.save()
