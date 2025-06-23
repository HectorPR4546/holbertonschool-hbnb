# part2/app/models/user.py

from app.models.base_model import BaseModel
from datetime import datetime

# Use direct module import to break circular dependency
import app.models.review  # Import the review module
import app.models.place   # Import the place module

class User(BaseModel):
    def __init__(self, email, first_name, last_name, **kwargs):
        super().__init__(**kwargs)
        self._email = None
        self._first_name = None
        self._last_name = None
        self._reviews = [] # Initialize reviews list
        self._places = [] # Initialize places list (for places owned by user)

        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    # --- Properties with Getters and Setters for Validation ---

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or "@" not in value or "." not in value:
            raise ValueError("Invalid email format.")
        self._email = value

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("First name cannot be empty.")
        self._first_name = value.strip()

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Last name cannot be empty.")
        self._last_name = value.strip()

    @property
    def reviews(self):
        return list(self._reviews) # Return a copy

    def add_review(self, review):
        # Refer to Review using its module prefix
        if not isinstance(review, app.models.review.Review):
            raise TypeError("Cannot add non-Review object to user's reviews.")
        if review not in self._reviews:
            self._reviews.append(review)

    def remove_review(self, review_id):
        """Removes a review from the user's collection by its ID."""
        self._reviews = [r for r in self._reviews if r.id != review_id]

    @property
    def places(self):
        return list(self._places) # Return a copy

    def add_place(self, place):
        # Refer to Place using its module prefix
        if not isinstance(place, app.models.place.Place):
            raise TypeError("Cannot add non-Place object to user's places.")
        if place not in self._places:
            self._places.append(place)

    def remove_place(self, place_id):
        self._places = [p for p in self._places if p.id != place_id]

    # --- Update and to_dict Methods ---

    def update(self, data):
        """Updates User attributes, using setters for validation."""
        if 'email' in data:
            self.email = data['email']
        if 'first_name' in data:
            self.first_name = data['first_name']
        if 'last_name' in data:
            self.last_name = data['last_name']
        self.updated_at = datetime.now()

    def to_dict(self):
        """Returns a dictionary representation of the User instance."""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
