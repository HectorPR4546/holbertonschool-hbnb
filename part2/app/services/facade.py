# part2/app/services/facade.py
from app.persistence.in_memory_repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
# Import Werkzeug exceptions for standardized HTTP error handling
from werkzeug.exceptions import Conflict, NotFound, BadRequest

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        # Add other repositories if you have them (e.g., City, Country)

    # --- User Methods ---
    def create_user(self, data):
        try:
            # Check for duplicate email before creating
            if self.user_repo.get_by_attribute('email', data['email']):
                raise Conflict("User with this email already exists.")
            
            user = User(**data) # Model constructor handles basic validation
            self.user_repo.add(user)
            return user.to_dict() # Return serialized dictionary including ID
        except ValueError as e:
            raise BadRequest(str(e)) # Convert model validation error to HTTP 400
        except Conflict as e:
            raise e # Re-raise conflict for Flask-RESTx to handle

    def get_user(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            raise NotFound("User not found")
        return user.to_dict()

    def get_all_users(self):
        return [user.to_dict() for user in self.user_repo.get_all()]

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            raise NotFound("User not found")
        try:
            # Check for duplicate email if updating email to an existing one
            if 'email' in data and data['email'] != user.email:
                if self.user_repo.get_by_attribute('email', data['email']):
                    raise Conflict("User with this email already exists.")
            user.update(data) # Model update method handles validation
            return user.to_dict()
        except ValueError as e:
            raise BadRequest(str(e)) # Convert model validation error to HTTP 400
        except Conflict as e:
            raise e

    def delete_user(self, user_id):
        if not self.user_repo.delete(user_id):
            raise NotFound("User not found")
        return True # Indicate success

    # --- Amenity Methods ---
    def create_amenity(self, data):
        try:
            if self.amenity_repo.get_by_attribute('name', data['name']):
                raise Conflict("Amenity with this name already exists.")
            amenity = Amenity(**data)
            self.amenity_repo.add(amenity)
            return amenity.to_dict()
        except ValueError as e:
            raise BadRequest(str(e))
        except Conflict as e:
            raise e

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise NotFound("Amenity not found")
        return amenity.to_dict()

    def get_all_amenities(self):
        return [amenity.to_dict() for amenity in self.amenity_repo.get_all()]

    def update_amenity(self, amenity_id, data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise NotFound("Amenity not found")
        try:
            if 'name' in data and data['name'] != amenity.name:
                if self.amenity_repo.get_by_attribute('name', data['name']):
                    raise Conflict("Amenity with this name already exists.")
            amenity.update(data)
            return amenity.to_dict()
        except ValueError as e:
            raise BadRequest(str(e))
        except Conflict as e:
            raise e

    def delete_amenity(self, amenity_id):
        if not self.amenity_repo.delete(amenity_id):
            raise NotFound("Amenity not found")
        return True

    # --- Place Methods ---
    def create_place(self, data):
        try:
            # Validate owner_id existence
            owner = self.user_repo.get(data['owner_id'])
            if not owner:
                raise BadRequest(f"Owner with ID '{data['owner_id']}' not found.")

            place = Place(**data) # Model constructor handles basic validation
            self.place_repo.add(place)
            return place.to_dict()
        except ValueError as e:
            raise BadRequest(str(e))
        except BadRequest as e: # Catch BadRequest from owner/city checks
            raise e
        except Exception as e: # Catch other potential errors
            raise BadRequest("An unexpected error occurred during place creation: " + str(e))

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise NotFound("Place not found")
        return place.to_dict()

    def get_all_places(self):
        return [place.to_dict() for place in self.place_repo.get_all()]

    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not place:
            raise NotFound("Place not found")
        try:
            if 'owner_id' in data and data['owner_id'] != place.owner_id:
                new_owner = self.user_repo.get(data['owner_id'])
                if not new_owner:
                    raise BadRequest(f"Owner with ID '{data['owner_id']}' not found.")
            place.update(data) # Model update method handles validation
            return place.to_dict()
        except ValueError as e:
            raise BadRequest(str(e))
        except BadRequest as e:
            raise e
        except Exception as e:
            raise BadRequest("An unexpected error occurred during place update: " + str(e))

    def delete_place(self, place_id):
        if not self.place_repo.delete(place_id):
            raise NotFound("Place not found")
        return True

    # Methods for Place Amenities (add/remove amenity to/from place)
    def add_amenity_to_place(self, place_id, amenity_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise NotFound("Place not found")
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise NotFound("Amenity not found")
        if amenity.id not in place.amenities:
            place.amenities.append(amenity.id)
        return place.to_dict()

    def remove_amenity_from_place(self, place_id, amenity_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise NotFound("Place not found")
        if amenity_id in place.amenities:
            place.amenities.remove(amenity_id)
        return place.to_dict()

    # --- Review Methods ---
    def create_review(self, data):
        try:
            # Check user and place existence
            user = self.user_repo.get(data['user_id'])
            if not user:
                raise BadRequest(f"User with ID '{data['user_id']}' not found.")
            place = self.place_repo.get(data['place_id'])
            if not place:
                raise BadRequest(f"Place with ID '{data['place_id']}' not found.")

            review = Review(**data) # Model constructor handles basic validation
            self.review_repo.add(review)
            return review.to_dict()
        except ValueError as e:
            raise BadRequest(str(e))
        except BadRequest as e: # Catch BadRequest from user/place checks
            raise e
        except Exception as e:
            raise BadRequest("An unexpected error occurred during review creation: " + str(e))

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise NotFound("Review not found")
        return review.to_dict()

    def get_all_reviews(self):
        return [review.to_dict() for review in self.review_repo.get_all()]

    def get_reviews_for_place(self, place_id):
        # Check if place exists first
        place = self.place_repo.get(place_id)
        if not place:
            raise NotFound("Place not found")
        
        # Then get reviews for that place
        return [review.to_dict() for review in self.review_repo.get_by_attribute('place_id', place_id)]

    def update_review(self, review_id, data):
        review = self.review_repo.get(review_id)
        if not review:
            raise NotFound("Review not found")
        try:
            review.update(data) # Model update method handles validation
            return review.to_dict()
        except ValueError as e:
            raise BadRequest(str(e))
        except Exception as e:
            raise BadRequest("An unexpected error occurred during review update: " + str(e))

    def delete_review(self, review_id):
        if not self.review_repo.delete(review_id):
            raise NotFound("Review not found")
        return True
