from uuid import uuid4
from datetime import datetime

class Amenity:
    def __init__(self, name, id=None):
        self.id = id if id else str(uuid4())
        self.name = name
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
