from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository
from app.services.repositories.user_repository import UserRepository
from app.services.repositories.amenity_repository import AmenityRepository
from app.services.repositories.place_repository import PlaceRepository
from app.services.repositories.review_repository import ReviewRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = AmenityRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()

    # User methods
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, update_data):
        self.user_repo.update(user_id, update_data)
        return {"message": "User updated successfully"}

    def get_user_by_email(self, email):
        """Retrieves a user by their email address."""
        return self.user_repo.get_user_by_email(email)

    # Amenity methods
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        self.amenity_repo.update(amenity_id, data)
        return {"message": "Amenity updated successfully"}

    # Place methods
    def create_place(self, place_data):
        owner_id = place_data.get("owner_id")
        if not self.user_repo.get(owner_id):
            raise ValueError("Invalid owner_id")
        
        amenity_ids = place_data.pop("amenities", [])
        place = Place(**place_data)
        
        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity ID {amenity_id} is invalid")
            place.amenities.append(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        self.place_repo.update(place_id, data)
        return {"message": "Place updated successfully"}

    # Review methods
    def create_review(self, review_data):
        user_id = review_data.get("user_id")
        if not self.user_repo.get(user_id):
            raise ValueError("Invalid user_id")
        place_id = review_data.get("place_id")
        if not self.place_repo.get(place_id):
            raise ValueError("Invalid place_id")
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        if not self.place_repo.get(place_id):
            raise ValueError("Place not found")
        return self.review_repo.get_reviews_by_place(place_id)

    def update_review(self, review_id, data):
        self.review_repo.update(review_id, data)
        return {"message": "Review updated successfully"}

    def delete_review(self, review_id):
        self.review_repo.delete(review_id)
        return {"message": "Review deleted successfully"}