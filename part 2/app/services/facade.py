from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class Facade:
    def __init__(self):
        # -------- USERS REPO --------
        self.user_repo = InMemoryRepository()
        User.set_repository(self.user_repo)

        # -------- PLACES REPO --------
        self.place_repo = InMemoryRepository()
        Place.set_repository(self.place_repo)

        # -------- REVIEWS REPO --------
        self.review_repo = InMemoryRepository()
        Review.set_repository(self.review_repo)

        # -------- AMENITIES REPO --------
        self.amenity_repo = InMemoryRepository()
        Amenity.set_repository(self.amenity_repo)

    # ================================
    #             USERS
    # ================================
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

    # ================================
    #             PLACES
    # ================================
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

    # ================================
    #             REVIEWS
    # ================================
    def create_review(self, data):
        rating = data.get("rating")
        comment = data.get("comment")
        return Review.create(rating, comment)

    def get_review(self, review_id):
        return Review.get(review_id)

    def get_all_reviews(self):
        return Review.get_all()

    def update_review(self, review_id, data):
        Review.update(review_id, data)
        return Review.get(review_id)

    def delete_review(self, review_id):
        return Review.delete(review_id)

    # ================================
    #            AMENITIES
    # ================================
    def create_amenity(self, data):
        name = data.get("name")
        description = data.get("description")
        return Amenity.create(name=name, description=description)

    def get_amenity(self, amenity_id):
        return Amenity.get(amenity_id)

    def get_all_amenities(self):
        return Amenity.get_all()

    def update_amenity(self, amenity_id, data):
        Amenity.update(amenity_id, data)
        return Amenity.get(amenity_id)


facade = Facade()
