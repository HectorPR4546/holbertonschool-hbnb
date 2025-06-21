from . import BaseModel

class Place(BaseModel):
    """Place model representing a rental property"""
    def __init__(self, title, description, price, latitude, longitude, owner):
        """
        Initialize Place instance
        
        Args:
            title (str): Property title
            description (str): Property description
            price (float): Nightly price
            latitude (float): GPS latitude
            longitude (float): GPS longitude
            owner (User): Owner of the property
        """
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Add a review to this place"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to this place"""
        self.amenities.append(amenity)

    def __str__(self):
        """String representation of Place"""
        return f"[Place] {self.title} (${self.price}/night)"
