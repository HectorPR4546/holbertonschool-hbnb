from . import BaseModel

class Review(BaseModel):
    """Review model representing a user's review of a place"""
    def __init__(self, text, rating, place, user):
        """
        Initialize Review instance
        
        Args:
            text (str): Review content
            rating (int): Rating (1-5)
            place (Place): Reviewed place
            user (User): Review author
        """
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def __str__(self):
        """String representation of Review"""
        return f"[Review] {self.rating}/5 by {self.user.first_name}"
