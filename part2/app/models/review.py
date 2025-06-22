from app.models.base_model import BaseModel
from app.models.place import Place # Need to import Place for type checking
from app.models.user import User   # Need to import User for type checking

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self._text = None
        self._rating = None
        self._place = None # Will hold a Place object
        self._user = None  # Will hold a User object

        # Assign through setters to trigger validation
        self.text = text
        self.rating = rating
        self.place = place # This setter will validate it's a Place
        self.user = user   # This setter will validate it's a User

        # Automatically add this review to the place's review list
        # This creates the one-to-many relationship from Place to Review
        if self.place: # Ensure place is not None after validation
            self.place.add_review(self)
            # Note: We update the place's timestamp when adding a review
            # The place.add_review method handles its own save()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not value:
            raise ValueError("Review text cannot be empty.")
        if not isinstance(value, str):
            raise TypeError("Review text must be a string.")
        self._text = value
        self.save()

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
        self.save()

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        if not isinstance(value, Place):
            raise TypeError("Place must be an instance of Place.")
        self._place = value
        self.save()

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        if not isinstance(value, User):
            raise TypeError("User must be an instance of User.")
        self._user = value
        self.save()

    def to_dict(self):
        """Returns a dictionary representation of the Review instance."""
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place.id, # Store place's ID
            "user_id": self.user.id,   # Store user's ID
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"Review(id='{self.id}', rating={self.rating}, place_id='{self.place.id}', user_id='{self.user.id}')"

    def update(self, data):
        """
        Updates the review attributes based on the provided dictionary.
        This overrides BaseModel's update to use setters for validation.
        """
        super_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key in super_keys:
                continue

            # Special handling for place and user if they were to be updated directly
            # For now, we expect them to be Place/User objects.
            if key == 'place':
                self.place = value # Use the setter
            elif key == 'user':
                self.user = value # Use the setter
            elif hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"Warning: Attempted to update non-existent attribute '{key}' for Review.")
        self.save()
