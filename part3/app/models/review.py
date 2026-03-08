#!/usr/bin/python3
"""Review model"""

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    """Review class"""

    repository = None

    def __init__(self, text, rating, user, place, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating
        self.user = user
        self.place = place
        self._validate()

    def _validate(self):
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("text cannot be empty")

        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("rating must be an integer between 1 and 5")

        if not isinstance(self.user, User):
            raise ValueError("user must be a User instance")

        if not isinstance(self.place, Place):
            raise ValueError("place must be a Place instance")

    def apply_update(self, data: dict):
        if "text" in data:
            self.text = data["text"]
        if "rating" in data:
            self.rating = data["rating"]

        self._validate()
        self.touch()
        return self

    @classmethod
    def set_repository(cls, repo):
        cls.repository = repo

    @classmethod
    def _repo(cls):
        if cls.repository is None:
            raise ValueError("Repository not set")
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
        review = cls.get(obj_id)
        if not review:
            return None
        review.apply_update(data)
        cls._repo().update(obj_id, data)
        return review

    @classmethod
    def delete(cls, obj_id):
        return cls._repo().delete(obj_id)

    def to_dict(self):
        data = super().to_dict()
        data.update(
            {
                "text": self.text,
                "rating": self.rating,
                "user_id": self.user.id if self.user else None,
                "place_id": self.place.id if self.place else None,
            }
        )
        return data
