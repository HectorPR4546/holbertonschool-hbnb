from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    """Facade for HBnB application services"""
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
