from uuid import uuid4
from datetime import datetime

class Place:
    def __init__(self, title, price, latitude, longitude, owner_id,
                 description=None, amenities=None, id=None):
        self.id = id if id else str(uuid4())
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = amenities if amenities else []
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'amenities': self.amenities,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
