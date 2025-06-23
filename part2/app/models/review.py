# part2/app/models/review.py
from datetime import datetime
import uuid

class Review:
    def __init__(self, user_id, place_id, rating, text):
        # Validation for required fields and ranges
        if not user_id: # Validity checked by facade
            raise ValueError("User ID cannot be empty.")
        if not place_id: # Validity checked by facade
            raise ValueError("Place ID cannot be empty.")
        if not (isinstance(rating, int) and 1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
        if not text or not isinstance(text, str) or text.strip() == "":
            raise ValueError("Review text cannot be empty.")

        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating
        self.text = text.strip()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, data):
        if 'rating' in data:
            if not (isinstance(data['rating'], int) and 1 <= data['rating'] <= 5):
                raise ValueError("Rating must be an integer between 1 and 5.")
            self.rating = data['rating']
        if 'text' in data:
            if not data['text'] or not isinstance(data['text'], str) or data['text'].strip() == "":
                raise ValueError("Review text cannot be empty.")
            self.text = data['text'].strip()

        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'rating': self.rating,
            'text': self.text,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
