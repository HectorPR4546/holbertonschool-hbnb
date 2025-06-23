from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# Create dummy user
user = User("John", "Doe", "john@example.com")

# Create dummy place
place = Place("Nice Spot", "Great view", 150.0, 18.0, -66.0, user.id)

# Create dummy review
review = Review("Amazing experience", 5, user.id, place.id)

# Create dummy amenity
amenity = Amenity("Free Parking")

print("User:", user.first_name, user.email)
print("Place:", place.title, place.owner_id)
print("Review:", review.text, review.rating)
print("Amenity:", amenity.name)
