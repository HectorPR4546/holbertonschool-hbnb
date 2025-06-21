from datetime import datetime
from app.models.user import User
from app.persistence.repository import InMemoryRepository
from app.models.amenity import Amenity

class HBnBFacade:
    """Facade pattern implementation for HBnB services"""
    def __init__(self):
        """Initialize all repositories"""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create a new user
        Args:
            user_data (dict): Dictionary containing user attributes
        Returns:
            User: The created user object
        """
        # Set default values if not provided
        user_data.setdefault('is_admin', False)
        user_data.setdefault('created_at', datetime.now())
        user_data.setdefault('updated_at', datetime.now())
        
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get a user by ID
        Args:
            user_id (str): The user's UUID
        Returns:
            User: The user object or None if not found
        """
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """Get all users
        Returns:
            list: List of all user objects
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user's information
        Args:
            user_id (str): The user's UUID
            user_data (dict): Dictionary of attributes to update
        Returns:
            User: The updated user object or None if not found
        """
        user = self.user_repo.get(user_id)
        if user:
            user_data['updated_at'] = datetime.now()
            user.update(user_data)
            return user
        return None

    def get_user_by_email(self, email):
        """Get a user by email address
        Args:
            email (str): The email address to search for
        Returns:
            User: The user object or None if not found
        """
        return self.user_repo.get_by_attribute('email', email)

    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)
            return amenity
        return None
