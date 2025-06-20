"""In-memory repository implementation."""

from typing import Dict, Any, Type, TypeVar
from models.base_model import BaseModel
from persistence.repository import Repository

T = TypeVar('T', bound=BaseModel)

class InMemoryRepository(Repository):
    """In-memory implementation of the Repository interface."""
    
    def __init__(self):
        """Initialize the repository."""
        self._objects: Dict[Type, Dict[str, BaseModel]] = {}
    
    def create(self, obj: T) -> T:
        """Create a new object."""
        if obj.__class__ not in self._objects:
            self._objects[obj.__class__] = {}
        self._objects[obj.__class__][obj.id] = obj
        return obj
    
    def get(self, model_class: Type[T], obj_id: str) -> T:
        """Get an object by ID."""
        if model_class in self._objects:
            return self._objects[model_class].get(obj_id)
        return None
    
    def get_all(self, model_class: Type[T]) -> Dict[str, T]:
        """Get all objects of a specific model class."""
        return self._objects.get(model_class, {}).copy()
    
    def update(self, obj: T) -> T:
        """Update an existing object."""
        if obj.__class__ in self._objects and obj.id in self._objects[obj.__class__]:
            self._objects[obj.__class__][obj.id] = obj
            return obj
        return None
    
    def delete(self, model_class: Type[T], obj_id: str) -> bool:
        """Delete an object by ID."""
        if model_class in self._objects and obj_id in self._objects[model_class]:
            del self._objects[model_class][obj_id]
            return True
        return False
