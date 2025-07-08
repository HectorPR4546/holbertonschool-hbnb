from app.extensions import db
from .baseclass import BaseModel

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), nullable=False)

    def __init__(self, title, price, latitude, longitude, owner_id,
                 description="", amenities=None, id=None):
        super().__init__(id=id)
        # Cast numeric values to correct types before validating
        try:
            price = float(price)
            latitude = float(latitude)
            longitude = float(longitude)
        except (ValueError, TypeError):
            raise ValueError("Price, latitude, and longitude must be numbers")

        if not title:
            raise ValueError("Title cannot be empty")
        if price <= 0:
            raise ValueError("Price must be a positive number")
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = amenities or []

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id
        }
