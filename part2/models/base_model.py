"""Base model class for HBnB objects."""

import uuid
from datetime import datetime
from typing import Dict, Any

class BaseModel:
    """Base class for all HBnB models."""
    
    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        if kwargs:
            for key, value in kwargs.items():
                if key in ['created_at', 'updated_at']:
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != '__class__':
                    setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the object to a dictionary."""
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict
    
    def __str__(self) -> str:
        """Return string representation of the object."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
