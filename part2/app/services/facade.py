from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create a new user and store it in the repository"""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email"""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieve all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update an existing user"""
        user = self.get_user(user_id)
        if user:
            user.update(user_data)
        return user

    def get_place(self, place_id):
        # Will be implemented later
        pass
