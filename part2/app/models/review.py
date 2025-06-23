from uuid import uuid4
from datetime import datetime

class Review:
    def __init__(self, text, rating, user_id, place_id, id=None):
        if not text:
            raise ValueError("Review text cannot be empty")
        if not user_id:
            raise ValueError("User ID is required")
        if not place_id:
            raise ValueError("Place ID is required")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        self.id = id or str(uuid4())
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
