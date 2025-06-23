from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity # Make sure Amenity is imported!
from datetime import datetime # Ensure datetime is imported if BaseModel uses it directly

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository() # Our Amenity repository

    # --- User Methods (Existing) ---
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if user:
            user.update(user_data)
            return user
        return None

    # --- Amenity Methods (NEW) ---
    def create_amenity(self, amenity_data):
        """Creates a new amenity instance and adds it to the repository."""
        amenity = Amenity(**amenity_data) # Instantiate Amenity object
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieves an amenity by its ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieves all amenities from the repository."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Updates an existing amenity's information."""
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            # The Amenity model's update method handles validation and timestamping
            amenity.update(amenity_data)
            return amenity
        return None # Return None if amenity not found

    # --- Placeholder method for fetching a place by ID (from previous task) ---
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass
