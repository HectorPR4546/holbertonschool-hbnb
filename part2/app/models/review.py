from datetime import datetime
from . import BaseModel

class Review(BaseModel):
    """Review model with validation"""
    def __init__(self, text, rating, user_id, place_id):
        """
        Initialize Review instance
        
        Args:
            text (str): Review content
            rating (int): Rating (1-5)
            user_id (str): ID of reviewing user
            place_id (str): ID of reviewed place
        """
        super().__init__()
        self.text = text
        self.rating = rating  # Uses rating setter
        self.user_id = user_id
        self.place_id = place_id

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not 1 <= value <= 5:
            raise ValueError("Rating must be integer between 1 and 5")
        self._rating = value

    def update(self, data):
        """Update review with validation"""
        if 'rating' in data:
            self.rating = data['rating']
        if 'text' in data:
            self.text = data['text']
        self.save()

    def to_dict(self):
        """Return dictionary representation"""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
