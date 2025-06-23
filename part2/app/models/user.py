import re
from uuid import uuid4
from datetime import datetime

class User:
    def __init__(self, first_name, last_name, email, id=None):
        if not first_name or not last_name:
            raise ValueError("First name and last name cannot be empty")
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")

        self.id = id or str(uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def _is_valid_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
