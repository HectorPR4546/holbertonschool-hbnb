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

    # --- Place Methods ---
    def create_place(self, place_data):
        owner_id = place_data.pop('owner_id', None)
        amenity_ids = place_data.pop('amenities', [])

        if not owner_id:
            raise ValueError("Owner ID is required to create a place.")

        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError(f"Owner with ID '{owner_id}' not found.")

        place_creation_data = {
            'title': place_data.get('title'),
            'description': place_data.get('description'),
            'price': place_data.get('price'),
            'latitude': place_data.get('latitude'),
            'longitude': place_data.get('longitude'),
            'owner': owner
        }
        
        place = Place(**place_creation_data)

        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                print(f"Warning: Amenity with ID '{amenity_id}' not found. Skipping.")
                continue
            place.add_amenity(amenity)

        self.place_repo.add(place)
        # Link the place to its owner (User)
        owner.add_place(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # Handle owner_id update
        if 'owner_id' in place_data:
            new_owner_id = place_data.pop('owner_id')
            if new_owner_id != (place.owner.id if place.owner else None): # Only update if changing
                new_owner = self.user_repo.get(new_owner_id)
                if not new_owner:
                    raise ValueError(f"New owner with ID '{new_owner_id}' not found.")
                
                # Remove from old owner's places if applicable
                if place.owner:
                    place.owner.remove_place(place.id)
                place.owner = new_owner # Use the setter to update owner
                new_owner.add_place(place) # Add to new owner's places

        # Handle amenities update
        if 'amenities' in place_data:
            new_amenity_ids = place_data.pop('amenities')
            
            # Clear existing amenities first
            for existing_amenity in list(place.amenities): # Iterate over a copy
                place.remove_amenity(existing_amenity.id)

            for amenity_id in new_amenity_ids:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    print(f"Warning: Amenity with ID '{amenity_id}' not found during update. Skipping.")
                    continue
                place.add_amenity(amenity)

        # Update other attributes using the Place model's update method
        place.update(place_data)

        return place

    # --- Review Methods ---
    def create_review(self, review_data):
        """
        Creates a new review instance.
        Expects user_id, place_id, text, and rating in review_data.
        Associates the review with the user and place.
        """
        user_id = review_data.pop('user_id', None)
        place_id = review_data.pop('place_id', None)

        if not user_id:
            raise ValueError("User ID is required for a review.")
        if not place_id:
            raise ValueError("Place ID is required for a review.")

        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError(f"User with ID '{user_id}' not found for review.")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"Place with ID '{place_id}' not found for review.")

        review_creation_data = {
            'text': review_data.get('text'),
            'rating': review_data.get('rating'),
            'user': user,  # Pass the actual User object
            'place': place  # Pass the actual Place object
        }

        review = Review(**review_creation_data)
        self.review_repo.add(review)

        # Add review to the associated user and place collections
        user.add_review(review)
        place.add_review(review)

        return review

    def get_review(self, review_id):
        """Retrieves a review by its ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieves all reviews from the repository."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Retrieves all reviews for a specific place.
        Returns None if place not found.
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None # API layer will translate this to 404
        return place.reviews # Place.reviews property returns a list of Review objects

    def update_review(self, review_id, review_data):
        """
        Updates an existing review's information.
        Only text and rating are typically updatable.
        """
        review = self.review_repo.get(review_id)
        if not review:
            return None # Indicate review not found

        review.update(review_data)
        return review

    def delete_review(self, review_id):
        """
        Deletes a review.
        Also removes the review from associated user and place collections.
        """
        review = self.review_repo.get(review_id)
        if not review:
            return False # Indicate review not found

        # Remove review from associated user's reviews
        if review.user:
            review.user.remove_review(review.id)
        
        # Remove review from associated place's reviews
        if review.place:
            review.place.remove_review(review.id)

        self.review_repo.delete(review_id)
        return True # Indicate successful deletion
