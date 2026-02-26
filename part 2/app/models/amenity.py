#!/usr/bin/python3
"""Amenity model"""

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity entity"""
    repository = None

    def __init__(self, name, description=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
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
    def _validate(name, description=None):
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("name must be a non-empty string")
        if description is not None and not isinstance(description, str):
            raise ValueError("description must be a string or None")

    # ---------- CRUD via Repository ----------
    @classmethod
    def create(cls, name, description=None):
        cls._validate(name, description)
        amenity = cls(name=name.strip(), description=description)
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

        if "name" in data:
            cls._validate(data["name"], data.get("description"))

        if "description" in data and data["description"] is not None and not isinstance(
            data["description"], str
        ):
            raise ValueError("description must be a string or None")

        return cls._repo().update(obj_id, data)

    @classmethod
    def delete(cls, obj_id):
        return cls._repo().delete(obj_id)

    @classmethod
    def get_by_attribute(cls, attr_name, attr_value):
        return cls._repo().get_by_attribute(attr_name, attr_value)

    def to_dict(self):
        data = super().to_dict()
        data.update(
            {
                "name": self.name,
                "description": self.description,
            }
        )
        return data
