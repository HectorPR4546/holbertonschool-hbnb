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
    review = Review(**review_data)
    self.review_repo.save(review)
    return review.to_dict()

def get_review(self, review_id):
    review = self.review_repo.get(review_id)
    return review.to_dict() if review else None

def get_all_reviews(self):
    return [r.to_dict() for r in self.review_repo.all()]

def get_reviews_by_place(self, place_id):
    return [r.to_dict() for r in self.review_repo.all() if r.place_id == place_id]

def update_review(self, review_id, review_data):
    review = self.review_repo.get(review_id)
    if not review:
        raise ValueError("Review not found")
    for key, value in review_data.items():
        setattr(review, key, value)
    self.review_repo.save(review)
    return True

def delete_review(self, review_id):
    review = self.review_repo.get(review_id)
    if review:
        self.review_repo.delete(review_id)
        return True
    return False
