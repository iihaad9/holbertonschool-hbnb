from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    repository = None

    def __init__(self, text, rating, user, place, **kwargs):
        super().__init__(**kwargs)

        self.user = user
        self.place = place

        self.set_text(text)
        self.set_rating(rating)

        self._validate_relations()

    def _validate_relations(self):
        if not isinstance(self.user, User):
            raise ValueError("user must be a User instance")
        if not isinstance(self.place, Place):
            raise ValueError("place must be a Place instance")

    def set_rating(self, rating):
        if rating is None:
            raise ValueError("rating is required")
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("rating must be an integer between 1 and 5")
        self.rating = rating
        self.touch()

    def set_text(self, text):
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text cannot be empty")
        self.text = text.strip()
        self.touch()

    def apply_update(self, data):
        if "rating" in data:
            self.set_rating(data["rating"])
        if "text" in data:
            self.set_text(data["text"])
        return self

    @classmethod
    def set_repository(cls, repo):
        cls.repository = repo

    @classmethod
    def _repo(cls):
        if cls.repository is None:
            raise RuntimeError("Review.repository is not set. Call Review.set_repository(repo) first.")
        return cls.repository

    @classmethod
    def create(cls, text, rating, user, place):
        review = cls(text=text, rating=rating, user=user, place=place)
        cls._repo().add(review)
        return review

    @classmethod
    def get(cls, obj_id):
        return cls._repo().get(obj_id)

    @classmethod
    def get_all(cls):
        return cls._repo().get_all()

    @classmethod
    def update(cls, obj_id, data):
        return cls._repo().update(obj_id, data)

    @classmethod
    def delete(cls, obj_id):
        return cls._repo().delete(obj_id)

    @classmethod
    def get_by_attribute(cls, attr, value):
        return cls._repo().get_by_attribute(attr, value)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user.id,
            "place_id": self.place.id,
        })
        return data
