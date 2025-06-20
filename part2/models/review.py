"""Review model implementation."""

from models.base_model import BaseModel
from typing import Optional

class Review(BaseModel):
    """Review class that represents user reviews of places.
    
    Attributes:
        place_id (str): ID of the place being reviewed
        user_id (str): ID of the user who wrote the review
        text (str): The review text content
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize a Review instance."""
        super().__init__(*args, **kwargs)
        self.place_id: Optional[str] = kwargs.get('place_id', "")
        self.user_id: Optional[str] = kwargs.get('user_id', "")
        self.text: Optional[str] = kwargs.get('text', "")
