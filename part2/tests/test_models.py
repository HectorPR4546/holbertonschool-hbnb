from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def test_models():
    # Test User
    user = User("John", "Doe", "john@example.com")
    print(user)
    assert user.first_name == "John"
    assert user.email == "john@example.com"
    
    # Test Place
    place = Place("Cozy Cabin", "Nice woods view", 99.99, 37.7749, -122.4194, user)
    print(place)
    assert place.title == "Cozy Cabin"
    assert place.owner == user
    
    # Test Review
    review = Review("Great stay!", 5, place, user)
    place.add_review(review)
    print(review)
    assert review.rating == 5
    assert len(place.reviews) == 1
    
    # Test Amenity
    amenity = Amenity("Wi-Fi")
    place.add_amenity(amenity)
    print(amenity)
    assert amenity.name == "Wi-Fi"
    assert len(place.amenities) == 1
    
    print("All tests passed!")

if __name__ == "__main__":
    test_models()
