from app.persistence.repository import InMemoryRepository
from app.models.user import User # We need to import User to instantiate it
from app.models.place import Place # Needed for Place repo, even if not used by user methods yet
from app.models.review import Review # Needed for Review repo
from app.models.amenity import Amenity # Needed for Amenity repo


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        # We need to make sure we're creating a User object here
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # --- NEW METHOD: Get all users ---
    def get_all_users(self):
        return self.user_repo.get_all()
    # --- END NEW METHOD ---

    # --- NEW METHOD: Update a user ---
    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if user:
            # The User model's update method handles validation and timestamping
            user.update(user_data)
            return user
        return None # Return None if user not found
    # --- END NEW METHOD ---

    # Placeholder method for fetching a place by ID (from previous task)
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass
