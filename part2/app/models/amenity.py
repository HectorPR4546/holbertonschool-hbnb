from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __repr__(self):
        return f"<Amenity {self.id} ({self.name})>"
