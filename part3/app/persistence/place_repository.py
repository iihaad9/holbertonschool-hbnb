#!/usr/bin/python3
"""Place repository"""

from app.persistence.repository import SQLAlchemyRepository
from app.models.place import Place


class PlaceRepository(SQLAlchemyRepository):
    """Repository for Place entity"""

    def __init__(self):
        super().__init__(Place)

    def get_places_by_owner(self, owner_id):
        return self.model.query.filter_by(owner_id=owner_id).all()