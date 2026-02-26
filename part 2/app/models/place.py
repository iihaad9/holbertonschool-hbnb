from app.models.base_model import BaseModel
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity


class Place(BaseModel):
    repository = None

    def __init__(self, title, description, price, latitude, longitude, owner, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

        self.reviews = []
        self.amenities = []

        self._validate()

    def _validate(self):
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("title is required")
        if len(self.title) > 100:
            raise ValueError("title max length is 100")

        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("description must be a string")

        if not isinstance(self.price, (int, float)) or float(self.price) <= 0:
            raise ValueError("price must be a positive number")

        if not isinstance(self.latitude, (int, float)) or not (-90.0 <= float(self.latitude) <= 90.0):
            raise ValueError("latitude must be between -90.0 and 90.0")

        if not isinstance(self.longitude, (int, float)) or not (-180.0 <= float(self.longitude) <= 180.0):
            raise ValueError("longitude must be between -180.0 and 180.0")

        if not isinstance(self.owner, User):
            raise ValueError("owner must be a User instance")

        if not isinstance(self.reviews, list):
            raise ValueError("reviews must be a list")
        if not all(isinstance(r, Review) for r in self.reviews):
            raise ValueError("reviews must contain Review instances")

        if not isinstance(self.amenities, list):
            raise ValueError("amenities must be a list")
        if not all(isinstance(a, Amenity) for a in self.amenities):
            raise ValueError("amenities must contain Amenity instances")

    def add_review(self, review):
        if not isinstance(review, Review):
            raise ValueError("review must be a Review instance")
        if review not in self.reviews:
            self.reviews.append(review)
            self.touch()

    def add_amenity(self, amenity):
        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be an Amenity instance")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.touch()

    @classmethod
    def set_repository(cls, repo):
        cls.repository = repo

    @classmethod
    def _repo(cls):
        if cls.repository is None:
            raise RuntimeError("Place.repository is not set. Call Place.set_repository(repo) first.")
        return cls.repository

    @classmethod
    def create(cls, title, description, price, latitude, longitude, owner):
        place = cls(title, description, price, latitude, longitude, owner)
        cls._repo().add(place)
        return place

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

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "title": self.title,
            "description": self.description,
            "price": float(self.price),
            "latitude": float(self.latitude),
            "longitude": float(self.longitude),
            "owner": self.owner.to_dict(),
            "reviews": [r.to_dict() for r in self.reviews],
            "amenities": [a.to_dict() for a in self.amenities],
        })
        return data
