"""Repository interface definition."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Type, TypeVar
from models.base_model import BaseModel

T = TypeVar('T', bound=BaseModel)

class Repository(ABC):
    """Abstract base class for repository implementations."""
    
    @abstractmethod
    def create(self, obj: T) -> T:
        """Create a new object."""
        pass
    
    @abstractmethod
    def get(self, model_class: Type[T], obj_id: str) -> T:
        """Get an object by ID."""
        pass
    
    @abstractmethod
    def get_all(self, model_class: Type[T]) -> Dict[str, T]:
        """Get all objects of a specific model class."""
        pass
    
    @abstractmethod
    def update(self, obj: T) -> T:
        """Update an existing object."""
        pass
    
    @abstractmethod
    def delete(self, model_class: Type[T], obj_id: str) -> bool:
        """Delete an object by ID."""
        pass
