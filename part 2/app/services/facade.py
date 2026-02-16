# app/services/facade.py
from app.persistence.repository import InMemoryRepository
from app.models.user import User

class Facade:
    def __init__(self):
        # ✅ Repo واحد فقط طول عمر التطبيق
        self.user_repo = InMemoryRepository()

        # ✅ اربط User بهذا الريبو مرة واحدة
        User.set_repository(self.user_repo)

    def create_user(self, data):
        return User.create(
            data["first_name"],
            data["last_name"],
            data["email"],
            password=data.get("password", ""),
            is_admin=data.get("is_admin", False),
        )

    def get_user(self, user_id):
        return User.get(user_id)

    def get_all_users(self):
        return User.get_all()

    def get_user_by_email(self, email):
        return User.get_by_attribute("email", email)

    def update_user(self, user_id, data):
        User.update(user_id, data)
        return User.get(user_id)

    def delete_user(self, user_id):
        return User.delete(user_id)

# ✅ هذا أهم سطر: instance واحد ثابت
facade = Facade()
