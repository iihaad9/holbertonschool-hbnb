from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app import db


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        User.set_repository(self.user_repo)

        self.place_repo = PlaceRepository()
        Place.set_repository(self.place_repo)

        self.review_repo = ReviewRepository()
        Review.set_repository(self.review_repo)

        self.amenity_repo = AmenityRepository()
        Amenity.set_repository(self.amenity_repo)

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        return self.user_repo.update(user_id, data)

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def create_amenity(self, data):
        return Amenity.create(
            name=data.get("name"),
            description=data.get("description"),
        )

    def get_amenity(self, amenity_id):
        return Amenity.get(amenity_id)

    def get_all_amenities(self):
        return Amenity.get_all()

    def update_amenity(self, amenity_id, data):
        return Amenity.update(amenity_id, data)

    def delete_amenity(self, amenity_id):
        return Amenity.delete(amenity_id)

    def _resolve_amenities(self, amenity_ids):
        if amenity_ids is None:
            return [], None

        if not isinstance(amenity_ids, list):
            return None, "invalid_amenities"

        amenities = []
        for amenity_id in amenity_ids:
            if not isinstance(amenity_id, str) or not amenity_id.strip():
                return None, "invalid_amenities"

            amenity = self.get_amenity(amenity_id)
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
                owner_id=owner_id,
            )

            for amenity in amenities:
                place.add_amenity(amenity)

            db.session.commit()
            return place, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    def get_place(self, place_id):
        return Place.get(place_id)

    def get_all_places(self):
        return Place.get_all()

    def update_place(self, place_id, data):
        place = self.get_place(place_id)
        if not place:
            return None, "place_not_found"

        data = dict(data)
        amenity_ids = None

        if "amenities" in data:
            amenity_ids = data.pop("amenities")

        if "owner_id" in data:
            owner = self.get_user(data["owner_id"])
            if not owner:
                return None, "owner_not_found"

        try:
            updated = Place.update(place_id, data)
            if not updated:
                return None, "place_not_found"

            place = updated

            if amenity_ids is not None:
                amenities, err = self._resolve_amenities(amenity_ids)
                if err:
                    return None, err

                place.amenities = []
                for amenity in amenities:
                    place.add_amenity(amenity)

            db.session.commit()
            return place, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    def delete_place(self, place_id):
        return Place.delete(place_id)

    def create_review(self, data):
        user_id = data.get("user_id")
        place_id = data.get("place_id")

        user = self.get_user(user_id) if user_id else None
        if not user:
            return None, "user_not_found"

        place = self.get_place(place_id) if place_id else None
        if not place:
            return None, "place_not_found"

        try:
            review = Review.create(
                text=data.get("text"),
                rating=data.get("rating"),
                user_id=user_id,
                place_id=place_id,
            )
            return review, None
        except Exception as e:
            return None, str(e)

    def get_review(self, review_id):
        return Review.get(review_id)

    def get_all_reviews(self):
        return Review.get_all()

    def update_review(self, review_id, data):
        review = Review.update(review_id, data)
        if not review:
            return None, "review_not_found"
        return review, None

    def delete_review(self, review_id):
        return Review.delete(review_id)


facade = HBnBFacade()
