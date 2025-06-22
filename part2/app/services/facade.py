from datetime import datetime
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    """Facade pattern implementation for HBnB services"""
    def __init__(self):
        """Initialize all repositories"""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User Methods
    def create_user(self, user_data):
        """Create a new user with validation"""
        # Remove any auto-generated fields that might come from API
        user_data.pop('id', None)
        user_data.pop('created_at', None)
        user_data.pop('updated_at', None)
        
        try:
            user = User(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                is_admin=user_data.get('is_admin', False)
            )
            self.user_repo.add(user)
            return user
        except ValueError as e:
            raise ValueError(f"Invalid user data: {str(e)}")

    def get_user(self, user_id):
        """Get user by ID"""
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """Get all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update user information"""
        user = self.user_repo.get(user_id)
        if user:
            try:
                user.update(user_data)
                return user
            except ValueError as e:
                raise ValueError(f"Invalid update data: {str(e)}")
        return None

    def get_user_by_email(self, email):
        """Get user by email address"""
        return self.user_repo.get_by_attribute('email', email)

    # Place Methods
    def create_place(self, place_data):
        """Create a new place with validation"""
        place_data.pop('id', None)
        place_data.pop('created_at', None)
        place_data.pop('updated_at', None)
        
        try:
            place = Place(
                title=place_data['title'],
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner_id=place_data['owner_id'],
                description=place_data.get('description', '')
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
        return place

    def get_all_places(self):
        """Get all places"""
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

    # Review Methods
    def create_review(self, review_data):
        """Create a new review with validation"""
        review_data.pop('id', None)
        review_data.pop('created_at', None)
        review_data.pop('updated_at', None)
        
        try:
            review = Review(
                text=review_data['text'],
                rating=review_data['rating'],
                user_id=review_data['user_id'],
                place_id=review_data['place_id']
            )
            self.review_repo.add(review)
            return review
        except ValueError as e:
            raise ValueError(f"Invalid review data: {str(e)}")

    def get_review(self, review_id):
        """Get review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a place"""
        return [r for r in self.review_repo.get_all() if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        """Update review information"""
        review = self.review_repo.get(review_id)
        if review:
            try:
                review.update(review_data)
                return review
            except ValueError as e:
                raise ValueError(f"Invalid update data: {str(e)}")
        return None

    def delete_review(self, review_id):
        """Delete a review"""
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.delete(review_id)
            return True
        return False

    # Amenity Methods
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        amenity_data.pop('id', None)
        amenity_data.pop('created_at', None)
        amenity_data.pop('updated_at', None)
        
        try:
            amenity = Amenity(
                name=amenity_data['name']
            )
            self.amenity_repo.add(amenity)
            return amenity
        except ValueError as e:
            raise ValueError(f"Invalid amenity data: {str(e)}")

    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update amenity information"""
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            try:
                amenity.update(amenity_data)
                return amenity
            except ValueError as e:
                raise ValueError(f"Invalid update data: {str(e)}")
        return None

# Singleton instance of the facade
facade = HBnBFacade()
