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

