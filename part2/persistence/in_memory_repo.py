"""In-memory repository implementation."""

from typing import Dict, Any
from models.base_model import BaseModel
from persistence.repository import Repository

class InMemoryRepository(Repository):
    """In-memory implementation of the Repository interface."""
    
    def __init__(self):
        """Initialize the repository."""
        self._objects: Dict[str, BaseModel] = {}
    
    def create(self, obj_data: Dict[str, Any]) -> BaseModel:
        """Create a new object from data."""
        obj = BaseModel(**obj_data)
        self._objects[obj.id] = obj
        return obj
    
    def get(self, obj_id: str) -> BaseModel:
        """Get an object by ID."""
        return self._objects.get(obj_id)
    
    def get_all(self) -> Dict[str, BaseModel]:
        """Get all objects."""
        return self._objects.copy()
