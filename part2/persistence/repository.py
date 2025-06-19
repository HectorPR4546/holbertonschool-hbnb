"""Repository interface definition."""

from abc import ABC, abstractmethod
from typing import Dict, Any
from models.base_model import BaseModel

class Repository(ABC):
    """Abstract base class for repository implementations."""
    
    @abstractmethod
    def create(self, obj_data: Dict[str, Any]) -> BaseModel:
        """Create a new object from data."""
        pass
    
    @abstractmethod
    def get(self, obj_id: str) -> BaseModel:
        """Get an object by ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> Dict[str, BaseModel]:
        """Get all objects."""
        pass
