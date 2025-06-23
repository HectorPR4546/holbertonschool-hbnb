from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # -- User methods --

    def create_place(self, place_data):
        """Create a new place with validation and store it."""
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=self.get_user(place_data['owner_id'])
        )
        for amenity_id in place_data.get('amenities', []):
            am = self.get_amenity(amenity_id)
            if am:
                place.add_amenity(am)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None
        valid_keys = ['title', 'description', 'price', 'latitude', 'longitude']
        for key in valid_keys:
            if key in place_data:
                setattr(place, key, place_data[key])
        place.save()
        return place
