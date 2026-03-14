from app.models.base_model import BaseModel
from app import db, bcrypt
import re


class User(BaseModel):
    __tablename__ = "users"

    repository = None
    EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    places = db.relationship("Place", back_populates="owner", cascade="all, delete-orphan")
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, first_name, last_name, email, password, is_admin=False, **kwargs):
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        self.is_admin = is_admin
        self._validate()

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @classmethod
    def set_repository(cls, repo):
        cls.repository = repo

    @classmethod
    def _repo(cls):
        if cls.repository is None:
            raise RuntimeError("User.repository is not set. Call User.set_repository(repo) first.")
        return cls.repository

    @classmethod
    def _validate_email_format(cls, email):
        if not isinstance(email, str) or not email.strip():
            raise ValueError("email is required")
        email = email.strip()
        if not cls.EMAIL_RE.match(email):
            raise ValueError("invalid email format")
        return email

    @staticmethod
    def _validate_name(value, field_name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} is required")
        value = value.strip()
        if len(value) > 50:
            raise ValueError(f"{field_name} max length is 50")
        return value

    def _validate(self):
        self.first_name = self._validate_name(self.first_name, "first_name")
        self.last_name = self._validate_name(self.last_name, "last_name")
        self.email = self._validate_email_format(self.email)

        if not isinstance(self.is_admin, bool):
            raise ValueError("is_admin must be a boolean")

        if not isinstance(self.password_hash, str):
            raise ValueError("password_hash must be a string")

    @classmethod
    def _ensure_unique_email(cls, email, exclude_user_id=None):
        existing = cls.get_by_attribute("email", email)
        if existing and existing.id != exclude_user_id:
            raise ValueError("email already registered")

    @classmethod
    def create(cls, first_name, last_name, email, password, is_admin=False):
        email = cls._validate_email_format(email)
        cls._ensure_unique_email(email)

        user = cls(first_name, last_name, email, password, is_admin)
        cls._repo().add(user)
        return user

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

    @classmethod
    def get_by_attribute(cls, attr_name, attr_value):
        return cls._repo().get_by_attribute(attr_name, attr_value)

    def apply_update(self, data: dict):
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")

        data = dict(data)

        if "email" in data:
            new_email = self._validate_email_format(data["email"])
            self._ensure_unique_email(new_email, exclude_user_id=self.id)
            data["email"] = new_email

        if "password" in data:
            self.set_password(data.pop("password"))

        super().apply_update(data)
        self._validate()
        return self

    def to_dict(self):
        data = super().to_dict()
        data.update(
            {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "is_admin": self.is_admin,
            }
        )
        return data
