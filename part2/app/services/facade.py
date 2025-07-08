from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository
from app.services.repositories.user_repository import UserRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenities = {}
        self.places = {}
        self.reviews = {}

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
        self.amenities[amenity.id] = amenity
        return amenity.to_dict()

    def get_amenity(self, amenity_id):
        amenity = self.amenities.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        return amenity.to_dict()

    def get_all_amenities(self):
        return [a.to_dict() for a in self.amenities.values()]

    def update_amenity(self, amenity_id, data):
        amenity = self.amenities.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        if 'name' in data:
            amenity.name = data['name']
        amenity.updated_at = datetime.utcnow()
        return {"message": "Amenity updated successfully"}

    # Place methods
    def create_place(self, place_data):
        owner_id = place_data.get("owner_id")
        # This check will need to be updated to use the user_repo
        if not self.user_repo.get(owner_id):
            raise ValueError("Invalid owner_id")
        for amenity_id in place_data.get("amenities", []):
            if amenity_id not in self.amenities:
                raise ValueError(f"Amenity ID {amenity_id} is invalid")
        place = Place(**place_data)
        self.places[place.id] = place
        return place.to_dict()

    def get_place(self, place_id):
        place = self.places.get(place_id)
        if not place:
            raise ValueError("Place not found")

        place_dict = place.to_dict()

    # Add owner info
        owner = self.user_repo.get(place.owner_id)
        place_dict["owner"] = owner.to_dict() if owner else None

    # Add amenities info
        place_dict["amenities"] = [
        self.amenities[a_id].to_dict()
        for a_id in place.amenities
        if a_id in self.amenities
    ]

    # Add reviews info
        place_dict["reviews"] = [
        r.to_dict()
        for r in self.reviews.values()
        if r.place_id == place.id
    ]

        return place_dict

    def get_all_places(self):
        return [p.to_dict() for p in self.places.values()]

    def update_place(self, place_id, data):
        place = self.places.get(place_id)
        if not place:
            raise ValueError("Place not found")
        for key, value in data.items():
            if hasattr(place, key):
                setattr(place, key, value)
        place.updated_at = datetime.utcnow()
        return {"message": "Place updated successfully"}

    # Review methods
    def create_review(self, review_data):
        user_id = review_data.get("user_id")
        # This check will need to be updated to use the user_repo
        if not self.user_repo.get(user_id):
            raise ValueError("Invalid user_id")
        place_id = review_data.get("place_id")
        if place_id not in self.places:
            raise ValueError("Invalid place_id")
        review = Review(**review_data)
        self.reviews[review.id] = review
        return review.to_dict()

    def get_review(self, review_id):
        review = self.reviews.get(review_id)
        if not review:
            raise ValueError("Review not found")
        return review.to_dict()

    def get_all_reviews(self):
        return [r.to_dict() for r in self.reviews.values()]

    def get_reviews_by_place(self, place_id):
        if place_id not in self.places:
            raise ValueError("Place not found")
        return [r.to_dict() for r in self.reviews.values() if r.place_id == place_id]

    def update_review(self, review_id, data):
        review = self.reviews.get(review_id)
        if not review:
            raise ValueError("Review not found")
        if 'text' in data:
            review.text = data['text']
        if 'rating' in data:
            review.rating = data['rating']
        review.updated_at = datetime.utcnow()
        return {"message": "Review updated successfully"}

    def delete_review(self, review_id):
        if review_id not in self.reviews:
            raise ValueError("Review not found")
        del self.reviews[review_id]
        return {"message": "Review deleted successfully"}
