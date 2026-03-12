#!/usr/bin/python3
"""Amenity repository"""

from app.persistence.repository import SQLAlchemyRepository
from app.models.amenity import Amenity


class AmenityRepository(SQLAlchemyRepository):
    """Repository for Amenity entity"""

    def __init__(self):
        super().__init__(Amenity)

    def get_amenity_by_name(self, name):
        """Get amenity by name"""
        return self.model.query.filter_by(name=name).first()