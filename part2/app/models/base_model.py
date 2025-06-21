#!/usr/bin/python3
"""Base model for all HBnB objects."""
import uuid
from datetime import datetime

class BaseModel:
    """Defines common attributes/methods for other classes."""
    
    def __init__(self, *args, **kwargs):
        """Initialize base model."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != '__class__':
                    setattr(self, key, value)
    
    def to_dict(self):
        """Convert instance to dictionary."""
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        return new_dict
