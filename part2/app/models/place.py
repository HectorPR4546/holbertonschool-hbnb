from . import BaseModel

class Place(BaseModel):
    """Place model with complete validation"""
    def __init__(self, title, price, latitude, longitude, owner_id, description=""):
        """
        Initialize Place instance with validation
        
        Args:
            title (str): Non-empty property title
            price (float): Positive number
            latitude (float): Between -90 and 90
            longitude (float): Between -180 and 180
            owner_id (str): Valid user ID
            description (str): Optional description
        """
        super().__init__()
        self.title = title  # Uses title setter
        self.description = description
        self.price = price  # Uses price setter
        self.latitude = latitude  # Uses latitude setter
        self.longitude = longitude  # Uses longitude setter
        self.owner_id = owner_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if value is None:
            raise ValueError("Title must be a string")
        if not isinstance(value, str):
            raise ValueError("Title must be a string")
        if not value.strip():
            raise ValueError("Title must not be empty")
        self._title = value.strip()

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
        if not isinstance(value, (int, float)) or not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)

    def update(self, data):
        """Update place with validation"""
        if 'title' in data:
            self.title = data['title']
        if 'price' in data:
            self.price = data['price']
        if 'latitude' in data:
            self.latitude = data['latitude']
        if 'longitude' in data:
            self.longitude = data['longitude']
        super().update(data)
