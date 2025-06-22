from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self._name = None # Use private attribute for setter validation
        self.name = name # Assign through setter to trigger validation

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Amenity name is required.")
        if not isinstance(value, str):
            raise TypeError("Amenity name must be a string.")
        if len(value) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters.")
        self._name = value
        self.save() # Update timestamp

    def to_dict(self):
        """Returns a dictionary representation of the Amenity instance."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"Amenity(id='{self.id}', name='{self.name}')"

    def update(self, data):
        """
        Updates the amenity attributes based on the provided dictionary.
        This overrides BaseModel's update to use setters for validation.
        """
        super_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key in super_keys:
                continue # Don't allow direct update of these BaseModel attributes

            if hasattr(self, key):
                setattr(self, key, value) # Use the property setters for validation
            else:
                print(f"Warning: Attempted to update non-existent attribute '{key}' for Amenity.")
        self.save() # Update the updated_at timestamp
