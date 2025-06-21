import uuid
from datetime import datetime

class BaseModel:
    """Base class for all models"""
    def __init__(self):
        """Initializes base model with id and timestamps"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Updates the updated_at timestamp"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Updates model attributes"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
