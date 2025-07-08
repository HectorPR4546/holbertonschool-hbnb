import uuid
from datetime import datetime

class BaseModel:
    """Base class for shared attributes and methods."""
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Updates the updated_at timestamp."""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update attributes using a dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
