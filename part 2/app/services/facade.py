from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place   # ⬅️ أضفنا هذا

class Facade:
    def __init__(self):
        # Users Repo
        self.user_repo = InMemoryRepository()
        User.set_repository(self.user_repo)

        # Places Repo ⬅️ أضفنا هذا
        self.place_repo = InMemoryRepository()
        Place.set_repository(self.place_repo)

    # -------- USERS --------

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

    # -------- PLACES --------

    def create_place(self, data):
        owner_id = data.get("owner_id")
        owner = self.get_user(owner_id)

        if not owner:
            return None, "owner_not_found"

        try:
            place = Place.create(
                title=data["title"],
                description=data.get("description"),
                price=data["price"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                owner=owner
            )
            return place, None
        except Exception as e:
            return None, str(e)

    def get_place(self, place_id):
        return Place.get(place_id)

    def get_all_places(self):
        return Place.get_all()

    def update_place(self, place_id, data):
        if "owner_id" in data:
            owner = self.get_user(data["owner_id"])
            if not owner:
                return None, "owner_not_found"
            data["owner"] = owner
            data.pop("owner_id")

        try:
            Place.update(place_id, data)
            return Place.get(place_id), None
        except Exception as e:
            return None, str(e)

    def delete_place(self, place_id):
        return Place.delete(place_id)


facade = Facade()
