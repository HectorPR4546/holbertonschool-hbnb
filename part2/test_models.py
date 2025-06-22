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

# ... (rest of the test_models.py code remains the same) ...

# Ensure you are replacing the top import section of your test_models.py file
# with the new imports above.
