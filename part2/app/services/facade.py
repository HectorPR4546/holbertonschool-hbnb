from datetime import datetime
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    """Facade pattern implementation for HBnB services"""
    def __init__(self):
        """Initialize all repositories"""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User Methods
    def create_user(self, user_data):
        """Create a new user with validation"""
        try:
            # Remove auto-generated fields
            user_data = {k: v for k, v in user_data.items() 
                        if k not in ['id', 'created_at', 'updated_at']}
            
            # Validate required fields
            required = ['first_name', 'last_name', 'email']
            if not all(field in user_data for field in required):
                raise ValueError("Missing required fields: first_name, last_name, email")

            user = User(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                is_admin=user_data.get('is_admin', False)
            )
            self.user_repo.add(user)
            return user
        except ValueError as e:
            return {
                'error': True,
                'message': str(e),
                'field': 'email' if 'email' in str(e).lower() else None
            }

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if user:
            try:
                user.update(user_data)
                return user
            except ValueError as e:
                return {'error': True, 'message': str(e)}
        return None

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)


facade = HBnBFacade()
