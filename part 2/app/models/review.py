from app.models.base_model import BaseModel

class Review(BaseModel):
    REPOSITORY = None  

    def __init__(self, rating, comment, **kwargs):
        super().__init__(**kwargs)

        self.set_rating(rating)
        self.set_comment(comment)

    
    def set_rating(self, rating):
        if rating is None:
            raise ValueError("Rating is required")
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        self.rating = rating
        self.touch()

    def set_comment(self, comment):
        if not comment or not comment.strip():
            raise ValueError("Comment cannot be empty")
        self.comment = comment.strip()
        self.touch()

    
    def apply_update(self, data):
        if "rating" in data:
            self.set_rating(data["rating"])

        if "comment" in data:
            self.set_comment(data["comment"])

        return self

    
    @classmethod
    def set_repository(cls, repo):
        cls.REPOSITORY = repo

    @classmethod
    def create(cls, rating, comment):
        if cls.REPOSITORY is None:
            raise RuntimeError("Repository not set for Review model")

        review = cls(rating, comment)
        cls.REPOSITORY.add(review)
        return review

    @classmethod
    def get(cls, obj_id):
        return cls.REPOSITORY.get(obj_id)

    @classmethod
    def get_all(cls):
        return cls.REPOSITORY.get_all()

    @classmethod
    def update(cls, obj_id, data):
        return cls.REPOSITORY.update(obj_id, data)

    @classmethod
    def delete(cls, obj_id):
        return cls.REPOSITORY.delete(obj_id)

    @classmethod
    def get_by_attribute(cls, attr, value):
        return cls.REPOSITORY.get_by_attribute(attr, value)
