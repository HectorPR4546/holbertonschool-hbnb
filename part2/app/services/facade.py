from datetime import datetime
from app.models.user import User
from app.persistence.repository import InMemoryRepository
from app.models.amenity import Amenity
from app.models.place import Place

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

    def create_place(self, place_data):
        """Create a new place with validation"""
        try:
            place = Place(
                title=place_data['title'],
                description=place_data.get('description', ''),
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner_id=place_data['owner_id']
            )
            self.place_repo.add(place)
            return place
        except ValueError as e:
            raise ValueError(f"Invalid place data: {str(e)}")

    def get_place(self, place_id):
        """Get place by ID with owner details"""
        place = self.place_repo.get(place_id)
        if place:
            place.owner = self.user_repo.get(place.owner_id)
            place.amenities = [self.amenity_repo.get(aid) for aid in place.amenity_ids]
        return place

    def get_all_places(self):
        """Get all places with basic info"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update place information"""
        place = self.place_repo.get(place_id)
        if place:
            try:
                place.update(place_data)
                return place
            except ValueError as e:
                raise ValueError(f"Invalid update data: {str(e)}")
        return None

    def add_amenity_to_place(self, place_id, amenity_id):
        """Add amenity to a place"""
        place = self.place_repo.get(place_id)
        amenity = self.amenity_repo.get(amenity_id)
        if place and amenity and amenity_id not in place.amenity_ids:
            place.amenity_ids.append(amenity_id)
            return True
        return False
