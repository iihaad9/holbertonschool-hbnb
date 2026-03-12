#!/usr/bin/python3
"""Place model"""

from app import db
from app.models.base_model import BaseModel


class Place(BaseModel):
    """Place entity"""

    __tablename__ = "places"
    repository = None

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), nullable=False)

    def __init__(
        self,
        title,
        description,
        price,
        latitude,
        longitude,
        owner_id,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self._validate()

    def _validate(self):
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("title is required")
        if len(self.title.strip()) > 100:
            raise ValueError("title max length is 100")

        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("description must be a string")

        if not isinstance(self.price, (int, float)) or float(self.price) <= 0:
            raise ValueError("price must be a positive number")

        if not isinstance(self.latitude, (int, float)) or not (
            -90.0 <= float(self.latitude) <= 90.0
        ):
            raise ValueError("latitude must be between -90.0 and 90.0")

        if not isinstance(self.longitude, (int, float)) or not (
            -180.0 <= float(self.longitude) <= 180.0
        ):
            raise ValueError("longitude must be between -180.0 and 180.0")

        if not isinstance(self.owner_id, str) or not self.owner_id.strip():
            raise ValueError("owner_id is required")

    @classmethod
    def set_repository(cls, repo):
        cls.repository = repo

    @classmethod
    def _repo(cls):
        if cls.repository is None:
            raise RuntimeError(
                "Place.repository is not set. Call Place.set_repository(repo) first."
            )
        return cls.repository

    @classmethod
    def create(cls, title, description, price, latitude, longitude, owner_id):
        place = cls(title, description, price, latitude, longitude, owner_id)
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
        return self

    def to_dict(self):
        data = super().to_dict()
        data.update(
            {
                "title": self.title,
                "description": self.description,
                "price": float(self.price),
                "latitude": float(self.latitude),
                "longitude": float(self.longitude),
                "owner_id": self.owner_id,
            }
        )
        return data
