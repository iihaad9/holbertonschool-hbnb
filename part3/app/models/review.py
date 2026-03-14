#!/usr/bin/python3
"""Review model"""

from app import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    """Review class"""

    __tablename__ = "reviews"
    repository = None

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)

    user = db.relationship("User", back_populates="reviews")
    place = db.relationship("Place", back_populates="reviews")

    def __init__(self, text, rating, user_id=None, place_id=None, user=None, place=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating

        if user is not None:
            self.user = user
            self.user_id = user.id
        else:
            self.user_id = user_id

        if place is not None:
            self.place = place
            self.place_id = place.id
        else:
            self.place_id = place_id

        self._validate()

    def _validate(self):
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("text cannot be empty")

        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("rating must be an integer between 1 and 5")

        if not isinstance(self.user_id, str) or not self.user_id.strip():
            raise ValueError("user_id is required")

        if not isinstance(self.place_id, str) or not self.place_id.strip():
            raise ValueError("place_id is required")

    @classmethod
    def set_repository(cls, repo):
        cls.repository = repo

    @classmethod
    def _repo(cls):
        if cls.repository is None:
            raise RuntimeError(
                "Review.repository is not set. Call Review.set_repository(repo) first."
            )
        return cls.repository

    @classmethod
    def create(
        cls,
        text,
        rating,
        user=None,
        place=None,
        user_id=None,
        place_id=None,
    ):
        if user is not None and place is not None and hasattr(user, "id") and hasattr(place, "id"):
            review = cls(text=text, rating=rating, user=user, place=place)
        else:
            resolved_user_id = user_id if user_id is not None else user
            resolved_place_id = place_id if place_id is not None else place
            review = cls(
                text=text,
                rating=rating,
                user_id=resolved_user_id,
                place_id=resolved_place_id,
            )

        cls._repo().add(review)
        return review

    @classmethod
    def get(cls, obj_id):
        return cls._repo().get(obj_id)

    @classmethod
    def get_all(cls):
        return cls._repo().get_all()

    @classmethod
    def update(cls, obj_id, data: dict):
        return cls._repo().update(obj_id, data)

    @classmethod
    def delete(cls, obj_id):
        return cls._repo().delete(obj_id)

    def apply_update(self, data: dict):
        super().apply_update(data)
        self._validate()
        return self

    def to_dict(self):
        data = super().to_dict()
        data.update(
            {
                "text": self.text,
                "rating": self.rating,
                "user_id": self.user_id,
                "place_id": self.place_id,
            }
        )
        return data
