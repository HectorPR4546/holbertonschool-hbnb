from app.models.base import BaseModel

class Amenity(BaseModel):
    """Amenity model with a name."""
    def __init__(self, name):
        super().__init__()
        if not name or len(name) > 50:
            raise ValueError("name is required and must be under 50 characters")
        self.name = name
