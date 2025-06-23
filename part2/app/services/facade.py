from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place # Make sure Place is imported!
from app.models.review import Review
from app.models.amenity import Amenity # Make sure Amenity is imported!
from datetime import datetime # Ensure datetime is imported if BaseModel uses it directly

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
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

    # --- Place Methods (NEW) ---
    def create_place(self, place_data):
        """
        Creates a new place instance.
        Expects owner_id and a list of amenity_ids in place_data.
        """
        owner_id = place_data.pop('owner_id', None)
        amenity_ids = place_data.pop('amenities', []) # 'amenities' will be a list of IDs

        if not owner_id:
            raise ValueError("Owner ID is required to create a place.")

        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError(f"Owner with ID {owner_id} not found.")

        # Instantiate Place with required arguments first
        # Use a copy of place_data to avoid modifying the original when popping
        place_creation_data = {
            'title': place_data.get('title'),
            'description': place_data.get('description'),
            'price': place_data.get('price'),
            'latitude': place_data.get('latitude'),
            'longitude': place_data.get('longitude'),
            'owner': owner # Pass the actual User object
        }
        place = Place(**place_creation_data)

        # Add amenities to the place object
        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                # Decide if you want to fail creation or just skip invalid amenities
                print(f"Warning: Amenity with ID {amenity_id} not found. Skipping.")
                continue
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieves a place by its ID."""
        return self.place_repo.get(place_id) # Returns the Place object, which has owner and amenities already linked

    def get_all_places(self):
        """Retrieves all places from the repository."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Updates an existing place's information.
        Handles updating owner_id and amenity_ids separately.
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # Handle owner_id update
        if 'owner_id' in place_data:
            new_owner_id = place_data.pop('owner_id')
            if new_owner_id != place.owner.id: # Only update if changing
                new_owner = self.user_repo.get(new_owner_id)
                if not new_owner:
                    raise ValueError(f"New owner with ID {new_owner_id} not found.")
                place.owner = new_owner # Use the setter to update owner

        # Handle amenities update (replace existing ones with new list)
        if 'amenities' in place_data:
            new_amenity_ids = place_data.pop('amenities')
            
            # Clear existing amenities first
            # NOTE: A more robust approach might compare and add/remove only changes
            # but for simplicity, we'll clear and re-add for now.
            # To clear, we need to iterate over a copy of the list.
            for existing_amenity in list(place.amenities):
                place.remove_amenity(existing_amenity.id)

            for amenity_id in new_amenity_ids:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    print(f"Warning: Amenity with ID {amenity_id} not found during update. Skipping.")
                    continue
                place.add_amenity(amenity) # add_amenity already prevents duplicates

        # Update other attributes using the Place model's update method
        # This will call the setters for title, description, price, lat, long
        try:
            place.update(place_data)
        except (ValueError, TypeError) as e:
            # Re-raise or handle specific validation errors from the model
            raise e # Let the API layer catch this and return 400

        return place
