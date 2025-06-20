"""User model implementation."""

from models.base_model import BaseModel
from typing import Optional

class User(BaseModel):
    """User class that represents users of the HBnB platform.
    
    Attributes:
        email (str): User's email address
        password (str): User's password
        first_name (str): User's first name
        last_name (str): User's last name
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize a User instance."""
        super().__init__(*args, **kwargs)
        self.email: Optional[str] = kwargs.get('email', "")
        self.password: Optional[str] = kwargs.get('password', "")
        self.first_name: Optional[str] = kwargs.get('first_name', "")
        self.last_name: Optional[str] = kwargs.get('last_name', "")
