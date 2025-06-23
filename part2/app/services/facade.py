# part2/app/services/facade.py

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from datetime import datetime

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository() # Not used yet, but initialized
        self.amenity_repo = InMemoryRepository()

    # --- User Methods ---
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

    # --- Amenity Methods ---
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)
            return amenity
        return None

    # --- Place Methods ---
    def create_place(self, place_data):
        """
        Creates a new place instance.
        Expects owner_id and a list of amenity_ids in place_data.
        Raises ValueError for business logic errors (e.g., owner not found).
        """
        owner_id = place_data.pop('owner_id', None)
        amenity_ids = place_data.pop('amenities', []) # 'amenities' will be a list of IDs

        if not owner_id:
            raise ValueError("Owner ID is required to create a place.")

        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError(f"Owner with ID '{owner_id}' not found.")

        # Ensure all required place attributes are passed, even if None for optional ones
        # The Place model's __init__ and setters will validate their types and values
        place_creation_data = {
            'title': place_data.get('title'),
            'description': place_data.get('description'),
            'price': place_data.get('price'),
            'latitude': place_data.get('latitude'),
            'longitude': place_data.get('longitude'),
            'owner': owner # Pass the actual User object
        }
        
        place = Place(**place_creation_data) # This will call setters and can raise Value/TypeErrors

        # Add amenities to the place object
        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                print(f"Warning: Amenity with ID '{amenity_id}' not found. Skipping.")
                # Depending on requirements, you might want to raise an error here
                continue
            place.add_amenity(amenity) # add_amenity in Place class handles duplicates

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieves a place by its ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieves all places from the repository."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Updates an existing place's information.
        Handles updating owner and amenities relationships separately.
        Raises ValueError for business logic errors (e.g., owner not found).
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None # Indicate place not found

        # Handle owner_id update
        if 'owner_id' in place_data:
            new_owner_id = place_data.pop('owner_id')
            if new_owner_id != (place.owner.id if place.owner else None): # Only update if changing
                new_owner = self.user_repo.get(new_owner_id)
                if not new_owner:
                    raise ValueError(f"New owner with ID '{new_owner_id}' not found.")
                place.owner = new_owner # Use the setter to update owner

        # Handle amenities update (replace existing ones with new list)
        if 'amenities' in place_data:
            new_amenity_ids = place_data.pop('amenities')
            
            # Clear existing amenities first
            # Iterate over a copy to avoid issues while modifying the list
            for existing_amenity in list(place.amenities):
                place.remove_amenity(existing_amenity.id)

            for amenity_id in new_amenity_ids:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    print(f"Warning: Amenity with ID '{amenity_id}' not found during update. Skipping.")
                    continue
                place.add_amenity(amenity)

        # Update other attributes using the Place model's update method
        # This will call the setters for title, description, price, lat, long
        # Any ValueError/TypeError from setters will propagate
        place.update(place_data)

        return place

    # Placeholder method for fetching a review by ID (from previous task)
    def get_review(self, review_id):
        pass # To be implemented later
