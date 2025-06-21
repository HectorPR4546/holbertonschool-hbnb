#!/usr/bin/python3
"""Repository model references."""
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# NEW: Centralized model references
models = {
    'User': User,
    'Place': Place,
    'Review': Review,
    'Amenity': Amenity
}
