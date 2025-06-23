from uuid import uuid4
from datetime import datetime

class User:
    def __init__(self, first_name, last_name, email, password, id=None):
        self.id = id if id else str(uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password  # Store hashed in real app
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            # Do not return password in dict for security
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
