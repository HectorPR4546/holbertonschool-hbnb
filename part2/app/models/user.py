from uuid import uuid4
from datetime import datetime

class User:
    def __init__(self, first_name, last_name, email, id=None):
        self.id = id or str(uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
