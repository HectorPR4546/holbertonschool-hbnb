from app.models.base import BaseModel

class User(BaseModel):
    """User model with basic info and admin flag."""
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        if not first_name or len(first_name) > 50:
            raise ValueError("first_name is required and must be under 50 characters")
        if not last_name or len(last_name) > 50:
            raise ValueError("last_name is required and must be under 50 characters")
        if not email or "@" not in email:
            raise ValueError("A valid email is required")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
