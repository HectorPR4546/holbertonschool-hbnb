#!/usr/bin/python3
"""Amenity class implementation."""
from models.base_model import BaseModel

class Amenity(BaseModel):
    """Represents an amenity offered by places in HBnB.
    
    Attributes:
        name (str): Name of the amenity
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize Amenity instance."""
        super().__init__(*args, **kwargs)
        self.name = ""
