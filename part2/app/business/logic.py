#!/usr/bin/python3
"""Business logic implementation."""
from app.repository.memory_repo import MemoryRepository

class BusinessLogic:
    """Facade class to handle business operations."""
    
    def __init__(self):
        """Initialize with in-memory repository."""
        self.repo = MemoryRepository()
    
    def add(self, obj):
        """Add a new object."""
        return self.repo.add(obj)
    
    def get(self, obj_id):
        """Get an object by ID."""
        return self.repo.get(obj_id)
    
    def all(self):
        """Get all objects."""
        return self.repo.all()
