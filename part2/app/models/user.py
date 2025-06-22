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
        if not isinstance(value, str) or not value.strip():
            raise ValueError("First name must be a non-empty string")
        if len(value.strip()) > 50:
            raise ValueError("First name too long (max 50 chars)")
        self._first_name = value.strip()

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Last name must be a non-empty string")
        if len(value.strip()) > 50:
            raise ValueError("Last name too long (max 50 chars)")
        self._last_name = value.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if value is None:
            raise ValueError("Email must be a string")
        if not isinstance(value, str):
            raise ValueError("Email must be a string")
        if not value.strip():
            raise ValueError("Email must not be empty")
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value.strip()):
            raise ValueError("Invalid email format")
        if len(value.strip()) > 120:
            raise ValueError("Email too long (max 120 chars)")
        self._email = value.strip()

    def __str__(self):
        return f"[User] {self.first_name} {self.last_name} <{self.email}>"
