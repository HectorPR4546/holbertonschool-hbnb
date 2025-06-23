# part2/app/models/review.py

from app.models.base_model import BaseModel
from app.models.user import User  # Import User for type checking
from app.models.place import Place  # Import Place for type checking
from datetime import datetime

class Review(BaseModel):
    def __init__(self, text, rating, user, place, **kwargs):
        super().__init__(**kwargs)
        # Initialize internal attributes
        self._text = None
        self._rating = None
        self._user = None
        self._place = None

        # Assign values using setters to trigger validation
        self.text = text
        self.rating = rating
        self.user = user
        self.place = place

    # --- Properties with Getters and Setters for Validation ---

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Review text cannot be empty.")
        self._text = value.strip()

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise TypeError("Rating must be an integer.")
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        self._rating = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        if not isinstance(value, User):
            raise TypeError("Review user must be an instance of User.")
        self._user = value

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        if not isinstance(value, Place):
            raise TypeError("Review place must be an instance of Place.")
        self._place = value

    # --- Update and to_dict Methods ---

    def update(self, data):
        """Updates Review attributes, using setters for validation."""
        if 'text' in data:
            self.text = data['text']
        if 'rating' in data:
            self.rating = data['rating']
        # user and place relationships are not updated via this method
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        Returns a dictionary representation of the Review instance.
        Relationships (user and place) are represented by their IDs only.
        """
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user.id if self.user else None,
            "place_id": self.place.id if self.place else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def to_nested_dict(self):
        """Returns a simplified dictionary for nested review display (e.g., within a Place)."""
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating
        }
