"""Business logic services for HBnB."""

from typing import Any, Dict
from models.base_model import BaseModel

class HBNBService:
    """Service class containing business logic methods."""
    
    def __init__(self, facade):
        """Initialize with a facade instance."""
        self.facade = facade
    
    def create_object(self, obj_data: Dict[str, Any]) -> BaseModel:
        """Create a new object using the repository."""
        return self.facade.repository.create(obj_data)
    
    def get_object(self, obj_id: str) -> BaseModel:
        """Retrieve an object by ID."""
        return self.facade.repository.get(obj_id)
    
    def get_all_objects(self) -> Dict[str, BaseModel]:
        """Retrieve all objects."""
        return self.facade.repository.get_all()
