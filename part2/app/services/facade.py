# services/facade.py
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
import uuid

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Example existing user methods (add your previous ones here)...
    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    # --- Review methods ---
    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        text = review_data.get('text')
        rating = review_data.get('rating')

        if not user_id or not place_id or text is None or rating is None:
            raise ValueError("user_id, place_id, text and rating are required")

        if not (1 <= rating <= 5):
            raise ValueError("rating must be between 1 and 5")

        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} does not exist")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"Place with id {place_id} does not exist")

        new_review = Review(
            id=str(uuid.uuid4()),
            text=text,
            rating=rating,
            user_id=user_id,
            place_id=place_id
        )

        self.review_repo.add(new_review)
        return new_review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.all()

    def get_reviews_by_place(self, place_id):
        return [r for r in self.review_repo.all() if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        text = review_data.get('text')
        rating = review_data.get('rating')

        if text is not None:
            review.text = text
        if rating is not None:
            if not (1 <= rating <= 5):
                raise ValueError("rating must be between 1 and 5")
            review.rating = rating

        self.review_repo.update(review_id, review)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True
