from app.extensions import db
from .baseclass import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), nullable=False)
    place_id = db.Column(db.String(36), nullable=False)

    def __init__(self, text, rating, user_id, place_id, id=None):
        super().__init__(id=id)
        if not text:
            raise ValueError("Review text cannot be empty")
        if not user_id:
            raise ValueError("User ID is required")
        if not place_id:
            raise ValueError("Place ID is required")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
