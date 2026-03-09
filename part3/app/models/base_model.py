from app import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def apply_update(self, data: dict):
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")

        for k, v in data.items():
            if k in ("id", "created_at", "updated_at"):
                continue
            if hasattr(self, k):
                setattr(self, k, v)

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }