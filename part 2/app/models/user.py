from app.models.base_model import BaseModel

class User(BaseModel):
    repository = None

    def __init__(self, first_name, last_name, email, password, is_admin=False, **kwargs):
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin


    @classmethod
    def set_repository(cls, repo):
        cls.repository = repo

    @classmethod
    def _repo(cls):
        if cls.repository is None:
            raise RuntimeError("User.repository is not set. Call User.set_repository(repo) first.")
        return cls.repository

    # ---------- CRUD via Repository ----------
    @classmethod
    def create(cls, first_name, last_name, email, password, is_admin=False):
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
        """
        Update user attributes through repository.
        Repository will call obj.apply_update(data).
        """
        return cls._repo().update(obj_id, data)

    @classmethod
    def delete(cls, obj_id):
        return cls._repo().delete(obj_id)

    @classmethod
    def get_by_attribute(cls, attr_name, attr_value):
        return cls._repo().get_by_attribute(attr_name, attr_value)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        })
        return data
