from app.models.base import BaseModel

class Review(BaseModel):
    """Review model with text, rating, and references to place and user."""
    def __init__(self, text, rating, place, user):
        super().__init__()

        if not text:
            raise ValueError("text is required")
        if not (1 <= rating <= 5):
            raise ValueError("rating must be between 1 and 5")

        self.text = text
        self.rating = rating
        self.place = place  # Must be a Place instance
        self.user = user    # Must be a User instance
