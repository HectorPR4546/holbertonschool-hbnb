# test_models.py
# Run this from the 'part2/' directory: python test_models.py

import sys
import os

# Add the 'app' directory to the Python path so we can import our modules
# Make sure this points to the directory containing 'models', 'services', etc.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

# --- NEW IMPORTS ---
# Change these imports to be more explicit, using the full path from the added sys.path
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
# --- END NEW IMPORTS ---

from datetime import datetime
import uuid

print("--- Starting Model Tests ---")

def run_test(test_func):
    """Helper to run a test function and catch errors."""
    print(f"\nRunning: {test_func.__name__}...")
    try:
        test_func()
        print(f"✅ {test_func.__name__} passed!")
    except Exception as e:
        print(f"❌ {test_func.__name__} failed: {e}")

# --- Test User Class ---
def test_user_creation():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False
    assert isinstance(user.id, str)
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)
    assert user.created_at <= user.updated_at
    # Test to_dict
    user_dict = user.to_dict()
    assert user_dict['first_name'] == "John"
    assert 'id' in user_dict
    assert 'created_at' in user_dict

def test_user_update():
    user = User(first_name="Jane", last_name="Smith", email="jane.smith@example.com")
    old_updated_at = user.updated_at
    user.update({"first_name": "Janet", "email": "janet.smith@example.com"})
    assert user.first_name == "Janet"
    assert user.email == "janet.smith@example.com"
    assert user.updated_at > old_updated_at # Check if timestamp updated

def test_user_validation_errors():
    try:
        User(first_name="", last_name="Doe", email="test@example.com")
        assert False, "Should have raised ValueError for empty first_name"
    except ValueError as e:
        assert "First name is required." in str(e)

    try:
        User(first_name="TooLongNameForAUser" * 3, last_name="Doe", email="test@example.com")
        assert False, "Should have raised ValueError for long first_name"
    except ValueError as e:
        assert "50 characters" in str(e)

    try:
        User(first_name="John", last_name="Doe", email="bad-email")
        assert False, "Should have raised ValueError for invalid email"
    except ValueError as e:
        assert "Invalid email format." in str(e)

    user = User(first_name="Valid", last_name="User", email="valid@example.com")
    old_updated = user.updated_at
    try:
        user.update({"email": "bad"})
        assert False, "Should have raised ValueError for invalid email on update"
    except ValueError as e:
        assert "Invalid email format." in str(e)
    assert user.updated_at == old_updated # Timestamp should not change if update fails

# --- Test Amenity Class ---
def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    assert isinstance(amenity.id, str)
    assert isinstance(amenity.created_at, datetime)
    assert isinstance(amenity.updated_at, datetime)
    amenity_dict = amenity.to_dict()
    assert amenity_dict['name'] == "Wi-Fi"

def test_amenity_update():
    amenity = Amenity(name="Pool")
    old_updated_at = amenity.updated_at
    amenity.update({"name": "Swimming Pool"})
    assert amenity.name == "Swimming Pool"
    assert amenity.updated_at > old_updated_at

def test_amenity_validation_errors():
    try:
        Amenity(name="")
        assert False, "Should have raised ValueError for empty name"
    except ValueError as e:
        assert "Amenity name is required." in str(e)

    try:
        Amenity(name="SuperLongAmenityNameThatExceedsTheFiftyCharacterLimit" * 2)
        assert False, "Should have raised ValueError for long name"
    except ValueError as e:
        assert "50 characters" in str(e)

# --- Test Place Class ---
def test_place_creation_and_relationships():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100.0,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )

    assert place.title == "Cozy Apartment"
    assert place.description == "A nice place to stay"
    assert place.price == 100.0
    assert place.latitude == 37.7749
    assert place.longitude == -122.4194
    assert place.owner.id == owner.id
    assert isinstance(place.id, str)
    assert isinstance(place.created_at, datetime)
    assert isinstance(place.updated_at, datetime)
    assert len(place.reviews) == 0 # Initially no reviews
    assert len(place.amenities) == 0 # Initially no amenities

    # Adding amenities
    amenity1 = Amenity(name="Wi-Fi")
    amenity2 = Amenity(name="Parking")
    place.add_amenity(amenity1)
    place.add_amenity(amenity2)
    assert len(place.amenities) == 2
    assert amenity1 in place.amenities
    assert amenity2 in place.amenities

    # Test adding duplicate amenity (should not add)
    place.add_amenity(amenity1)
    assert len(place.amenities) == 2 # Still 2, not 3

    # Test removing amenity
    removed = place.remove_amenity(amenity1.id)
    assert removed is True
    assert len(place.amenities) == 1
    assert amenity1 not in place.amenities

    removed = place.remove_amenity("non-existent-id")
    assert removed is False
    assert len(place.amenities) == 1 # Still 1

    # Test to_dict
    place_dict = place.to_dict()
    assert place_dict['title'] == "Cozy Apartment"
    assert place_dict['owner_id'] == owner.id
    assert place_dict['owner_email'] == owner.email
    assert len(place_dict['amenities_ids']) == 1
    assert place_dict['amenities_ids'][0] == amenity2.id # Amenity2 should remain

def test_place_validation_errors():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")

    # Invalid price
    try:
        Place("Title", "Desc", -50, 0, 0, owner)
        assert False, "Should have raised ValueError for negative price"
    except ValueError as e:
        assert "Price must be a positive value." in str(e)

    # Invalid latitude
    try:
        Place("Title", "Desc", 100, 95.0, 0, owner)
        assert False, "Should have raised ValueError for invalid latitude"
    except ValueError as e:
        assert "Latitude must be between -90.0 and 90.0." in str(e)

    # Invalid longitude
    try:
        Place("Title", "Desc", 100, 0, -185.0, owner)
        assert False, "Should have raised ValueError for invalid longitude"
    except ValueError as e:
        assert "Longitude must be between -180.0 and 180.0." in str(e)

    # Invalid owner type
    try:
        Place("Title", "Desc", 100, 0, 0, "not a user")
        assert False, "Should have raised TypeError for invalid owner type"
    except TypeError as e:
        assert "Owner must be an instance of User." in str(e)

    place = Place(title="Test", description="Desc", price=100, latitude=0, longitude=0, owner=owner)
    old_updated = place.updated_at
    try:
        place.update({"price": "not-a-number"})
        assert False, "Should have raised TypeError for invalid price on update"
    except TypeError as e:
        assert "Price must be a number." in str(e)
    assert place.updated_at == old_updated # Timestamp should not change if update fails

# --- Test Review Class ---
def test_review_creation_and_place_relationship():
    reviewer = User(first_name="Bob", last_name="Johnson", email="bob.j@example.com")
    owner = User(first_name="Host", last_name="Person", email="host@example.com")
    place = Place(title="Mountain Cabin", description="Secluded getaway", price=200, latitude=40.0, longitude=-105.0, owner=owner)

    initial_reviews_count = len(place.reviews)
    review = Review(text="Amazing place, loved it!", rating=5, place=place, user=reviewer)

    assert review.text == "Amazing place, loved it!"
    assert review.rating == 5
    assert review.place.id == place.id
    assert review.user.id == reviewer.id
    assert isinstance(review.id, str)
    assert isinstance(review.created_at, datetime)
    assert isinstance(review.updated_at, datetime)

    # Check if the review was automatically added to the place's reviews list
    assert len(place.reviews) == initial_reviews_count + 1
    assert review in place.reviews
    assert place.reviews[initial_reviews_count].id == review.id # Check the specific review object

    # Test to_dict
    review_dict = review.to_dict()
    assert review_dict['text'] == "Amazing place, loved it!"
    assert review_dict['place_id'] == place.id
    assert review_dict['user_id'] == reviewer.id

def test_review_update():
    reviewer = User(first_name="Updater", last_name="Guy", email="updater@example.com")
    owner = User(first_name="Host", last_name="Person", email="host2@example.com")
    place = Place(title="City Loft", description="Modern living", price=150, latitude=34.0, longitude=-118.0, owner=owner)
    review = Review(text="Good place", rating=4, place=place, user=reviewer)
    old_updated_at = review.updated_at
    
    review.update({"text": "Very good place, highly recommend!", "rating": 5})
    assert review.text == "Very good place, highly recommend!"
    assert review.rating == 5
    assert review.updated_at > old_updated_at

def test_review_validation_errors():
    user = User(first_name="Bad", last_name="Reviewer", email="bad@example.com")
    owner = User(first_name="Host", last_name="Person", email="host3@example.com")
    place = Place(title="Small Room", description="Cozy", price=50, latitude=0, longitude=0, owner=owner)

    # Invalid rating (too low)
    try:
        Review("Ok", 0, place, user)
        assert False, "Should have raised ValueError for rating < 1"
    except ValueError as e:
        assert "Rating must be between 1 and 5." in str(e)

    # Invalid rating (too high)
    try:
        Review("Ok", 6, place, user)
        assert False, "Should have raised ValueError for rating > 5"
    except ValueError as e:
        assert "Rating must be between 1 and 5." in str(e)

    # Invalid place type
    try:
        Review("Text", 3, "not a place", user)
        assert False, "Should have raised TypeError for invalid place type"
    except TypeError as e:
        assert "Place must be an instance of Place." in str(e)

    # Invalid user type
    try:
        Review("Text", 3, place, "not a user")
        assert False, "Should have raised TypeError for invalid user type"
    except TypeError as e:
        assert "User must be an instance of User." in str(e)

    review = Review(text="Test", rating=3, place=place, user=user)
    old_updated = review.updated_at
    try:
        review.update({"rating": 0})
        assert False, "Should have raised ValueError for invalid rating on update"
    except ValueError as e:
        assert "Rating must be between 1 and 5." in str(e)
    assert review.updated_at == old_updated # Timestamp should not change if update fails


# Run all tests
run_test(test_user_creation)
run_test(test_user_update)
run_test(test_user_validation_errors)

run_test(test_amenity_creation)
run_test(test_amenity_update)
run_test(test_amenity_validation_errors)

run_test(test_place_creation_and_relationships)
run_test(test_place_validation_errors)

run_test(test_review_creation_and_place_relationship)
run_test(test_review_update)
run_test(test_review_validation_errors)

print("\n--- All Model Tests Completed ---")
