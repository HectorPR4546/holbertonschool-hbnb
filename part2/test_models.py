from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# Test User
user = User("John", "Doe", "john@example.com")
print("User:", user.first_name, user.last_name, user.email)

# Test Place
place = Place("Nice Spot", "Great view", 150.0, 18.0, -66.0, user)
print("Place:", place.title, place.owner.email)

# Test Review
review = Review("Amazing place!", 5, place, user)
place.add_review(review)
print("Review count:", len(place.reviews))

# Test Amenity
wifi = Amenity("Wi-Fi")
place.add_amenity(wifi)
print("Amenities:", [a.name for a in place.amenities])
