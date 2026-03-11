#!/usr/bin/python3
"""Review model"""
from app import db
from app.models.base_model import BaseModel
class Review(BaseModel):
    __tablename__ = "reviews"
    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)
    def __init__(self, text, rating, user_id, place_id, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating
        self.user_id = user_id
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
    def apply_update(self, data: dict):
        if "text" in data:
            self.text = data["text"]
        if "rating" in data:
            self.rating = data["rating"]
        self._validate()
        self.touch()
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
