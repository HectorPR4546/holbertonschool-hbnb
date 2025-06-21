from . import BaseModel

class Amenity(BaseModel):
    """Amenity model representing a property feature"""
    def __init__(self, name):
        """
        Initialize Amenity instance
        
        Args:
            name (str): Name of the amenity
        """
        super().__init__()
        self.name = name

    def __str__(self):
        """String representation of Amenity"""
        return f"[Amenity] {self.name}"
