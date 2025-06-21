#!/usr/bin/python3
"""Review class implementation."""
from models.base_model import BaseModel

class Review(BaseModel):
    """Represents a review for a place in HBnB.
    
    Attributes:
        place_id (str): ID of the place being reviewed
        user_id (str): ID of the user who wrote the review
        text (str): The review text content
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize Review instance."""
        super().__init__(*args, **kwargs)
        self.place_id = ""
        self.user_id = ""
        self.text = ""
