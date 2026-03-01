from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        User.set_repository(self.user_repo)

        self.place_repo = InMemoryRepository()
        Place.set_repository(self.place_repo)

        self.review_repo = InMemoryRepository()
        Review.set_repository(self.review_repo)

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

    # ================================
    #             PLACES
    # ================================
    def _resolve_amenities(self, amenity_ids):
        if amenity_ids is None:
            return [], None

        if not isinstance(amenity_ids, list):
            return None, "invalid_amenities"

        amenities = []
        for aid in amenity_ids:
            if not isinstance(aid, str) or not aid.strip():
                return None, "invalid_amenities"
            amenity = self.get_amenity(aid)
            if not amenity:
                return None, "amenity_not_found"
            amenities.append(amenity)

        return amenities, None

    def create_place(self, data):
        owner_id = data.get("owner_id")
        owner = self.get_user(owner_id)
        if not owner:
            return None, "owner_not_found"

        amenities, err = self._resolve_amenities(data.get("amenities"))
        if err:
            return None, err

        try:
            place = Place.create(
                title=data["title"],
                description=data.get("description"),
                price=data["price"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                owner=owner,
            )

            for a in amenities:
                place.add_amenity(a)

            return place, None
        except Exception as e:
            return None, str(e)

    def get_place(self, place_id):
        return Place.get(place_id)

    def get_all_places(self):
        return Place.get_all()

    def update_place(self, place_id, data):
        place = self.get_place(place_id)
        if not place:
            return None, "place_not_found"

        amenities_ids = None
        if "amenities" in data:
            amenities_ids = data.pop("amenities")

        if "owner_id" in data:
            owner = self.get_user(data["owner_id"])
            if not owner:
                return None, "owner_not_found"
            data["owner"] = owner
            data.pop("owner_id")

        try:
            Place.update(place_id, data)
            place = Place.get(place_id)

            if amenities_ids is not None:
                amenities, err = self._resolve_amenities(amenities_ids)
                if err:
                    return None, err
                place.amenities = []
                for a in amenities:
                    place.add_amenity(a)

            return place, None
        except Exception as e:
            return None, str(e)

    def delete_place(self, place_id):
        return Place.delete(place_id)

    # ================================
    #             REVIEWS
    # ================================
    def create_review(self, data):
        user_id = data.get("user_id")
        place_id = data.get("place_id")

        user = self.get_user(user_id) if user_id else None
        if not user:
            return None, "user_not_found"

        place = self.get_place(place_id) if place_id else None
        if not place:
            return None, "place_not_found"

        text = data.get("text")
        rating = data.get("rating")

        review = Review.create(text, rating, user, place)
        return review, None

    def get_review(self, review_id):
        return Review.get(review_id)

    def get_all_reviews(self):
        return Review.get_all()

    def update_review(self, review_id, data):
        Review.update(review_id, data)
        return Review.get(review_id)

    def delete_review(self, review_id):
        return Review.delete(review_id)


facade = HBnBFacade()
