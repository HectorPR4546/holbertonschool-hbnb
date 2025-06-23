# part2/app/models/amenity.py
from datetime import datetime
import uuid

class Amenity:
    def __init__(self, name):
        if not name or not isinstance(name, str) or name.strip() == "":
            raise ValueError("Amenity name cannot be empty.")
        self.id = str(uuid.uuid4())
        self.name = name.strip()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, data):
        if 'name' in data:
            if not data['name'] or not isinstance(data['name'], str) or data['name'].strip() == "":
                raise ValueError("Amenity name cannot be empty.")
            self.name = data['name'].strip()
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
