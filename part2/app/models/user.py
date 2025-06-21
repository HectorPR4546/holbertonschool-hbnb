#!/usr/bin/python3
"""User class implementation."""
from models.base_model import BaseModel

class User(BaseModel):
    """Represents a user in the HBnB application.
    
    Attributes:
        email (str): User's email address
        password (str): User's password
        first_name (str): User's first name
        last_name (str): User's last name
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize User instance."""
        super().__init__(*args, **kwargs)
        self.email = ""
        self.password = ""
        self.first_name = ""
        self.last_name = ""
