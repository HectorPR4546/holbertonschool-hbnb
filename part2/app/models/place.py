from uuid import uuid4
from datetime import datetime

class Place:
    def __init__(self, title, price, latitude, longitude, owner_id,
                 description="", amenities=None, id=None, created_at=None, updated_at=None):
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

        self.id = id or str(uuid4())
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = amenities or []
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
