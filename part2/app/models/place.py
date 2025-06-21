from app.models import BaseModel
from datetime import datetime

class Place(BaseModel):
    """Place model representing a rental property"""
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        """
        Initialize Place instance with validation
        
        Args:
            title (str): Property title
            description (str): Property description
            price (float): Nightly price (must be positive)
            latitude (float): GPS latitude (-90 to 90)
            longitude (float): GPS longitude (-180 to 180)
            owner_id (str): ID of owner User
        """
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenity_ids = []

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a positive number")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)
