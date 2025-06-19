#!/usr/bin/python3
"""
In-memory repository implementation
Stores objects in memory with basic validation
"""
from typing import Dict, Type, List, Any

class InMemoryRepository:
    """In-memory storage for model objects"""
    
    def __init__(self):
        """Initialize storage dictionary"""
        self._storage: Dict[Type, Dict[str, Any]] = {}
    
    def all(self, model_class: Type) -> List[Any]:
        """Return all objects of given class"""
        return list(self._storage.get(model_class, {}).values())
    
    def get(self, model_class: Type, obj_id: str) -> Any:
        """Get object by ID"""
        return self._storage.get(model_class, {}).get(obj_id)
    
    def add(self, obj: Any) -> Any:
        """Add new object to storage"""
        if not hasattr(obj, 'id'):
            raise ValueError("Object must have 'id' attribute")
        
        model_class = type(obj)
        if model_class not in self._storage:
            self._storage[model_class] = {}
        
        self._storage[model_class][obj.id] = obj
        return obj
    
    def update(self, obj: Any) -> Any:
        """Update existing object"""
        model_class = type(obj)
        if model_class not in self._storage or obj.id not in self._storage[model_class]:
            raise ValueError("Object not found")
        
        self._storage[model_class][obj.id] = obj
        return obj
    
    def delete(self, obj: Any) -> None:
        """Delete object from storage"""
        model_class = type(obj)
        if model_class in self._storage and obj.id in self._storage[model_class]:
            del self._storage[model_class][obj.id]
