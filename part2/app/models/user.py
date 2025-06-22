from app.models.base_model import BaseModel
import re # We'll need this for email validation!

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self._first_name = None # Use private attributes to enforce validation via setters
        self._last_name = None
        self._email = None
        self._is_admin = False # Default to False

        # Assign through setters to trigger validation
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value:
            raise ValueError("First name is required.")
        if not isinstance(value, str):
            raise TypeError("First name must be a string.")
        if len(value) > 50:
            raise ValueError("First name cannot exceed 50 characters.")
        self._first_name = value
        self.save() # Update timestamp

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value:
            raise ValueError("Last name is required.")
        if not isinstance(value, str):
            raise TypeError("Last name must be a string.")
        if len(value) > 50:
            raise ValueError("Last name cannot exceed 50 characters.")
        self._last_name = value
        self.save() # Update timestamp

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not value:
            raise ValueError("Email is required.")
        if not isinstance(value, str):
            raise TypeError("Email must be a string.")
        # Basic email format validation using regex
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format.")
        # NOTE: Uniqueness check will be done by the repository/facade,
        # as the model itself doesn't have access to all stored users.
        self._email = value
        self.save() # Update timestamp

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise TypeError("is_admin must be a boolean.")
        self._is_admin = value
        self.save() # Update timestamp

    def to_dict(self):
        """Returns a dictionary representation of the User instance."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"User(id='{self.id}', email='{self.email}')"

    def update(self, data):
        """
        Updates the user attributes based on the provided dictionary.
        This overrides BaseModel's update to use setters for validation.
        """
        super_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key in super_keys:
                continue # Don't allow direct update of these BaseModel attributes

            if hasattr(self, key):
                setattr(self, key, value) # Use the property setters for validation
            else:
                print(f"Warning: Attempted to update non-existent attribute '{key}' for User.")
        self.save() # Update the updated_at timestamp
