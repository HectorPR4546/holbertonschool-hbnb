class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create a new user"""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get a single user by ID"""
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """Get all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update an existing user"""
        user = self.user_repo.get(user_id)
        if user:
            user.update(user_data)
            return user
        return None

    def get_user_by_email(self, email):
        """Get user by email"""
        return self.user_repo.get_by_attribute('email', email)
