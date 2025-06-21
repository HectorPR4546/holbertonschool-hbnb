"""Business logic services for HBnB."""

from typing import Any, Dict, Type, TypeVar, Generic
from datetime import datetime
from models.base_model import BaseModel

T = TypeVar('T', bound=BaseModel)

class HBNBService:
    """Service class containing business logic methods."""
    
    def __init__(self, facade):
        """Initialize with a facade instance."""
        self.facade = facade
    
    def create_object(self, model_class: Type[T], obj_data: Dict[str, Any]) -> T:
        """Create a new object of specified model class using the repository."""
        obj = model_class(**obj_data)
        self.facade.repository.create(obj)
        return obj
    
    def get_object(self, model_class: Type[T], obj_id: str) -> T:
        """Retrieve an object by ID."""
        return self.facade.repository.get(model_class, obj_id)
    
    def get_all_objects(self, model_class: Type[T]) -> Dict[str, T]:
        """Retrieve all objects of specified model class."""
        return self.facade.repository.get_all(model_class)
    
    def update_object(self, model_class: Type[T], obj_id: str, 
                     update_data: Dict[str, Any]) -> T:
        """Update an existing object."""
        obj = self.get_object(model_class, obj_id)
        if obj:
            for key, value in update_data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            obj.updated_at = datetime.now()
            self.facade.repository.update(obj)
        return obj
    
    def delete_object(self, model_class: Type[T], obj_id: str) -> bool:
        """Delete an object by ID."""
        return self.facade.repository.delete(model_class, obj_id)
