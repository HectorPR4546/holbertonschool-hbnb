#!/usr/bin/env python3
"""
Simple tests for the business logic models
"""

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def test_user_creation():
    """Test creating a user"""
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False  # Default value
    print("✓ User creation test passed!")

def test_amenity_creation():
    """Test creating an amenity"""
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    print("✓ Amenity creation test passed!")

def test_place_creation():
    """Test creating a place with relationships"""
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Cozy Apartment", description="A nice place to stay", 
                  price=100, latitude=37.7749, longitude=-122.4194, owner=owner)

    # Adding a review
    review = Review(text="Great stay!", rating=5, place=place, user=owner)
    place.add_review(review)

    # Adding an amenity
    wifi = Amenity(name="Wi-Fi")
    place.add_amenity(wifi)

    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    assert len(place.amenities) == 1
    assert place.amenities[0].name == "Wi-Fi"
    print("✓ Place creation and relationship test passed!")

def test_review_creation():
    """Test creating a review"""
    user = User(first_name="Bob", last_name="Wilson", email="bob@example.com")
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    place = Place(title="Nice Place", description="Good location", 
                  price=75, latitude=40.7128, longitude=-74.0060, owner=owner)
    
    review = Review(text="Amazing place!", rating=4, place=place, user=user)
    
    assert review.text == "Amazing place!"
    assert review.rating == 4
    assert review.place == place
    assert review.user == user
    print("✓ Review creation test passed!")

def test_update_functionality():
    """Test updating objects"""
    user = User(first_name="John", last_name="Doe", email="john@example.com")
    original_updated_at = user.updated_at
    
    # Update user data
    user.update({"first_name": "Jane", "last_name": "Smith"})
    
    assert user.first_name == "Jane"
    assert user.last_name == "Smith"
    assert user.updated_at > original_updated_at
    print("✓ Update functionality test passed!")

if __name__ == "__main__":
    print("Running model tests...")
    test_user_creation()
    test_amenity_creation()
    test_place_creation()
    test_review_creation()
    test_update_functionality()
    print("\n🎉 All tests passed! Your models are working correctly!")
