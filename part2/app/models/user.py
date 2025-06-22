import re
from datetime import datetime
from . import BaseModel

class User(BaseModel):
    """User model with comprehensive validation"""
    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initialize User instance
        
        Args:
            first_name (str): User's first name
            last_name (str): User's last name
            email (str): Valid email address
            is_admin (bool): Admin status
        """
        super().__init__()
        self.first_name = first_name  # Uses first_name setter
        self.last_name = last_name    # Uses last_name setter
        self.email = email            # Uses email setter
        self.is_admin = is_admin

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value or not isinstance(value, str) or len(value) > 50:
            raise ValueError("First name must be 1-50 characters")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value or not isinstance(value, str) or len(value) > 50:
            raise ValueError("Last name must be 1-50 characters")
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Email must be a non-empty string")
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value.strip()):
            raise ValueError("Invalid email format")
        if len(value) > 120:
            raise ValueError("Email too long (max 120 chars)")
        self._email = value.strip()

    def __str__(self):
        return f"[User] {self.first_name} {self.last_name} <{self.email}>"
