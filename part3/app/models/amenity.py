from app.extensions import db
from .baseclass import BaseModel

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(120), nullable=False, unique=True)

    def __init__(self, name, id=None):
        super().__init__(id=id)
        if not name:
            raise ValueError("Amenity name cannot be empty")
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
