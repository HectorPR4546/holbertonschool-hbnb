import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        if not isinstance(data, dict):
            raise TypeError("Update data must be a dictionary.")

        for key, value in data.items():
            # We'll be a bit careful here, only allowing updates to existing attributes
            # and making sure not to change the 'id' or 'created_at' directly
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp
