# part2/app/models/amenity.py

from app.models.base_model import BaseModel
from datetime import datetime

class Amenity(BaseModel):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self._name = None
        self.name = name # Use the setter for validation

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Validation: Not empty
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Amenity name cannot be empty.")
        self._name = value.strip()

    def update(self, data):
        """Updates Amenity attributes, using setters for validation."""
        if 'name' in data:
            self.name = data['name']
        self.updated_at = datetime.now()

    def to_dict(self):
        """Returns a dictionary representation of the Amenity instance."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
