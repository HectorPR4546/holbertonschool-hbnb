# part2/app/models/user.py
from datetime import datetime
import uuid
import re # For email validation

class User:
    def __init__(self, email, password, first_name, last_name, is_admin=False):
        # Basic validation for init
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid or empty email format.")
        if not first_name:
            raise ValueError("First name cannot be empty.")
        if not last_name:
            raise ValueError("Last name cannot be empty.")
        # Password validation
        if not password:
            raise ValueError("Password cannot be empty.")

        self.id = str(uuid.uuid4())
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, data):
        """Updates user attributes based on a dictionary with validation."""
        if 'email' in data:
            if not data['email'] or not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
                raise ValueError("Invalid or empty email format.")
            self.email = data['email']
        if 'first_name' in data:
            if not data['first_name']:
                raise ValueError("First name cannot be empty.")
            self.first_name = data['first_name']
        if 'last_name' in data:
            if not data['last_name']:
                raise ValueError("Last name cannot be empty.")
            self.last_name = data['last_name']
        if 'password' in data:
            if not data['password']:
                raise ValueError("Password cannot be empty.")
            self.password = data['password']
        if 'is_admin' in data:
            # Ensure is_admin is a boolean
            if not isinstance(data['is_admin'], bool):
                raise ValueError("is_admin must be a boolean value.")
            self.is_admin = data['is_admin']
        self.updated_at = datetime.now()

    def to_dict(self):
        """Converts the User object to a dictionary for API response."""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
