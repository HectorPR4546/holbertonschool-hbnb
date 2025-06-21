#!/usr/bin/python3
"""In-memory repository implementation."""
from typing import Dict, Any

class MemoryRepository:
    """Simple in-memory storage for objects."""
    
    def __init__(self):
        """Initialize empty storage."""
        self._objects: Dict[str, Any] = {}
    
    def add(self, obj) -> str:
        """Add an object to storage."""
        if not hasattr(obj, 'id'):
            raise ValueError("Object must have an 'id' attribute")
        self._objects[obj.id] = obj
        return obj.id
    
    def get(self, obj_id: str):
        """Retrieve an object by ID."""
        return self._objects.get(obj_id)
    
    def all(self) -> list:
        """Get all stored objects."""
        return list(self._objects.values())
