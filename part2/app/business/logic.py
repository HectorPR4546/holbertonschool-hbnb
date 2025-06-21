#!/usr/bin/python3
"""Business logic implementation."""
from app.repository.memory_repo import MemoryRepository
from app.models import User, Place, Review, Amenity

class BusinessLogic:
    """Facade class to handle business operations."""
    
    def __init__(self):
        """Initialize with in-memory repository and model references."""
        self.repo = MemoryRepository()
        self.models = {
            'User': User,
            'Place': Place,
            'Review': Review,
            'Amenity': Amenity
        }
    
    def add(self, obj):
        """Add a new object to storage.
        
        Args:
            obj: The object to add
            
        Returns:
            str: ID of the added object
        """
        return self.repo.add(obj)
    
    def get(self, obj_id):
        """Get an object by ID.
        
        Args:
            obj_id: The object ID to retrieve
            
        Returns:
            object or None: The found object or None
        """
        return self.repo.get(obj_id)
    
    def all(self):
        """Get all stored objects.
        
        Returns:
            list: All objects in storage
        """
        return self.repo.all()

    # NEW: Added specialized place validation
    def add_place(self, place_data):
        """Add a new place with validation.
        
        Args:
            place_data (dict): Place attributes including:
                - price_by_night (int): Must be >= 0
                - latitude (float): Between -90 and 90
                - longitude (float): Between -180 and 180
                
        Returns:
            str: ID of the created place
            
        Raises:
            ValueError: If validation fails
        """
        # Validate price
        if 'price_by_night' in place_data and place_data['price_by_night'] < 0:
            raise ValueError("Price per night cannot be negative")
            
        # Validate coordinates
        if 'latitude' in place_data and not (-90 <= place_data['latitude'] <= 90):
            raise ValueError("Latitude must be between -90 and 90")
            
        if 'longitude' in place_data and not (-180 <= place_data['longitude'] <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        
        # Create and add the place
        place = self.models['Place'](**place_data)
        return self.add(place)
