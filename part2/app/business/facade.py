#!/usr/bin/python3
"""
Facade module
Provides a simplified interface to the business logic layer
"""
from app.persistence.in_memory_repository import InMemoryRepository

class BusinessFacade:
    """Facade for business operations"""
    
    def __init__(self):
        """Initialize with in-memory repository"""
        self._repository = InMemoryRepository()
    
    def get_all(self, model_class):
        """Get all objects of a given class"""
        return self._repository.all(model_class)
    
    def get_by_id(self, model_class, obj_id):
        """Get object by ID"""
        return self._repository.get(model_class, obj_id)
    
    def create(self, obj):
        """Create new object"""
        return self._repository.add(obj)
    
    def update(self, obj):
        """Update existing object"""
        return self._repository.update(obj)
    
    def delete(self, obj):
        """Delete object"""
        return self._repository.delete(obj)
