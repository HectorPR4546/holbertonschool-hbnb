from app.models.base import BaseModel

class Place(BaseModel):
    """Place model with location, price, and relationships."""
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        if not title or len(title) > 100:
            raise ValueError("title is required and must be under 100 characters")
        if price <= 0:
            raise ValueError("price must be positive")
        if latitude < -90.0 or latitude > 90.0:
            raise ValueError("latitude must be between -90.0 and 90.0")
        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("longitude must be between -180.0 and 180.0")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner  # Must be a User instance
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)
