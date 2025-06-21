import re
from datetime import datetime
from . import BaseModel

class User(BaseModel):
    """User model with enhanced validation"""
    def __init__(self, first_name, last_name, email, is_admin=False):
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
            raise ValueError("First name must be a non-empty string (max 50 chars)")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value or not isinstance(value, str) or len(value) > 50:
            raise ValueError("Last name must be a non-empty string (max 50 chars)")
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        self._email = value
