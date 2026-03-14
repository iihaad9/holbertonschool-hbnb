#!/usr/bin/python3
"""Place model"""

from app import db
from app.models.base_model import BaseModel
from app.models.place_amenity import place_amenity


class Place(BaseModel):
    """Place entity"""

    __tablename__ = "places"
    repository = None

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    owner = db.relationship("User", back_populates="places")
    reviews = db.relationship(
        "Review",
        back_populates="place",
        cascade="all, delete-orphan",
    )
    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        back_populates="places",
    )

    def __init__(
        self,
        title,
        description,
        price,
        latitude,
        longitude,
        owner_id=None,
        owner=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

        if owner is not None:
            self.owner = owner
            self.owner_id = owner.id
        else:
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

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)
        return amenity

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
    def create(
        cls,
        title,
        description,
        price,
        latitude,
        longitude,
        owner=None,
        owner_id=None,
    ):
        if owner is not None and hasattr(owner, "id"):
            place = cls(
                title=title,
                description=description,
                price=price,
                latitude=latitude,
                longitude=longitude,
                owner=owner,
            )
        else:
            resolved_owner_id = owner_id if owner_id is not None else owner
            place = cls(
                title=title,
                description=description,
                price=price,
                latitude=latitude,
                longitude=longitude,
                owner_id=resolved_owner_id,
            )

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
                "amenities": [amenity.id for amenity in self.amenities],
            }
        )
        return data
