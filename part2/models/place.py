"""Place model implementation."""

from models.base_model import BaseModel
from typing import Optional, List

class Place(BaseModel):
    """Place class that represents rental properties on HBnB.
    
    Attributes:
        city_id (str): ID of the city where the place is located
        user_id (str): ID of the user who owns the place
        name (str): Name of the place
        description (str): Description of the place
        number_rooms (int): Number of rooms
        number_bathrooms (int): Number of bathrooms
        max_guest (int): Maximum number of guests
        price_by_night (int): Price per night
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
        amenity_ids (List[str]): List of amenity IDs
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize a Place instance."""
        super().__init__(*args, **kwargs)
        self.city_id: Optional[str] = kwargs.get('city_id', "")
        self.user_id: Optional[str] = kwargs.get('user_id', "")
        self.name: Optional[str] = kwargs.get('name', "")
        self.description: Optional[str] = kwargs.get('description', "")
        self.number_rooms: int = kwargs.get('number_rooms', 0)
        self.number_bathrooms: int = kwargs.get('number_bathrooms', 0)
        self.max_guest: int = kwargs.get('max_guest', 0)
        self.price_by_night: int = kwargs.get('price_by_night', 0)
        self.latitude: float = kwargs.get('latitude', 0.0)
        self.longitude: float = kwargs.get('longitude', 0.0)
        self.amenity_ids: List[str] = kwargs.get('amenity_ids', [])
