#!/usr/bin/python3
"""Business logic implementation."""
from app.repository.memory_repo import MemoryRepository
from app.models import User, Place, Review, Amenity  # NEW: Added model imports

class BusinessLogic:
    """Facade class to handle business operations."""
    
    def __init__(self):
        """Initialize with in-memory repository and model references."""
        self.repo = MemoryRepository()
        # NEW: Added model references for type checking
        self.models = {
            'User': User,
            'Place': Place,
            'Review': Review,
            'Amenity': Amenity
        }
    
    def add(self, obj):
        """Add a new object."""
        return self.repo.add(obj)
    
    def get(self, obj_id):
        """Get an object by ID."""
        return self.repo.get(obj_id)
    
    def all(self):
        """Get all stored objects."""
        return self.repo.all()
