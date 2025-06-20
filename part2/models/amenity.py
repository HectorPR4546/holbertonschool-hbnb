"""Amenity model implementation."""

from models.base_model import BaseModel
from typing import Optional

class Amenity(BaseModel):
    """Amenity class that represents property amenities.
    
    Attributes:
        name (str): Name of the amenity
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize an Amenity instance."""
        super().__init__(*args, **kwargs)
        self.name: Optional[str] = kwargs.get('name', "")
