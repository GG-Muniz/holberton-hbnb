from app.models.base_model import BaseModel

class Review(BaseModel):
    """Review model"""

    def __init__(self, place_id, user_id, rating, comment):
        super().__init__()
        # validate inputs
        if not place_id or not user_id:
            raise ValueError("Place ID and User ID are required")
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        if not comment or len(comment.strip()) == 0:
            raise ValueError("Review comment cannot be empty")

        self.place_id = place_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment

    def to_dict(self):
        """Convert review object to dictionary"""
        review_dict = super().to_dict()
        review_dict.update({
            'place_id': self.place_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'comment': self.comment
        })
        return review_dict
