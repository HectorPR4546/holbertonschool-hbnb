from . import BaseModel

class User(BaseModel):
    """User model representing an HBnB user"""
    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initialize User instance
        
        Args:
            first_name (str): User's first name
            last_name (str): User's last name
            email (str): User's email address
            is_admin (bool): Whether user has admin privileges
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    def __str__(self):
        """String representation of User"""
        return f"[User] {self.first_name} {self.last_name} <{self.email}>"
