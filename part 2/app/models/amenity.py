#!/usr/bin/python3
"""Amenity model"""

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity entity"""

    repository = None

    def __init__(self, name, description=None, **kwargs):
        super().__init__(**kwargs)
        self._validate(name=name, description=description)
        self.name = name.strip()
        self.description = description

    @classmethod
    def set_repository(cls, repo):
        cls.repository = repo

    @classmethod
    def _repo(cls):
        if cls.repository is None:
            raise RuntimeError(
                "Amenity.repository is not set. Call Amenity.set_repository(repo) first."
            )
        return cls.repository

    @staticmethod
    def _validate(name=None, description=None):
        if name is not None:
            if not isinstance(name, str) or not name.strip():
                raise ValueError("name must be a non-empty string")
            if len(name.strip()) > 50:
                raise ValueError("name max length is 50")

        if description is not None and not isinstance(description, str):
            raise ValueError("description must be a string or None")

    @classmethod
    def create(cls, name, description=None):
        amenity = cls(name=name, description=description)
        cls._repo().add(amenity)
        return amenity

    @classmethod
    def get(cls, obj_id):
        return cls._repo().get(obj_id)

    @classmethod
    def get_all(cls):
        return cls._repo().get_all()

    @classmethod
    def update(cls, obj_id, data: dict):
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")

        cls._validate(name=data.get("name"), description=data.get("description"))
        return cls._repo().update(obj_id, data)

    @classmethod
    def delete(cls, obj_id):
        return cls._repo().delete(obj_id)

    @classmethod
    def get_by_attribute(cls, attr_name, attr_value):
        return cls._repo().get_by_attribute(attr_name, attr_value)

    def apply_update(self, data: dict):
        super().apply_update(data)
        self._validate(name=self.name, description=self.description)

    def to_dict(self):
        data = super().to_dict()
        data.update(
            {
                "name": self.name,
                "description": self.description,
            }
        )
        return data
