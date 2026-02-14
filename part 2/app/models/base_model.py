import uuid
from datetime import datetime

class BaseModel:
    """Base model class to use for stamps and id."""

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", uuid.uuid4().hex)

        created_at = kwargs.get("created_at")
        updated_at = kwargs.get("updated_at")

        self.created_at = self._parse_dt(created_at) if created_at else datetime.now()
        self.updated_at = self._parse_dt(updated_at) if updated_at else datetime.now()

    def touch(self):
        self.updated_at = datetime.now()

    def save(self):
        self.touch()

    def apply_update(self, data: dict):
        """Default update behavior: set attributes from dict, then touch()."""
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")

        for k, v in data.items():
            if k in ("id", "created_at", "updated_at"):
                continue
            if hasattr(self, k):
                setattr(self, k, v)

        self.touch()

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def _parse_dt(value):
        if isinstance(value, datetime):
            return value
        # ISO format string
        return datetime.fromisoformat(value)
