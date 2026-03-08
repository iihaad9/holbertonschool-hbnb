import unittest
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class TestRelationships(unittest.TestCase):
    def setUp(self):
        User.set_repository(InMemoryRepository())
        Place.set_repository(InMemoryRepository())
        Review.set_repository(InMemoryRepository())
        Amenity.set_repository(InMemoryRepository())

    def _get_id(self, obj):
        return getattr(obj, "id", None)

    def _review_user_id(self, review):
        # supports either review.user_id or review.user.id
        if hasattr(review, "user_id"):
            return getattr(review, "user_id")
        u = getattr(review, "user", None)
        return self._get_id(u) if u else None

    def _review_place_id(self, review):
        # supports either review.place_id or review.place.id
        if hasattr(review, "place_id"):
            return getattr(review, "place_id")
        p = getattr(review, "place", None)
        return self._get_id(p) if p else None

    def test_place_add_amenity(self):
        owner = User.create("O", "W", "owner_rel@ex.com", "123456")
        place = Place.create("T", "D", 100, 24.7, 46.7, owner)
        a = Amenity.create("WiFi", "Fast")

        place.add_amenity(a)

        amenities = getattr(place, "amenities", [])
        self.assertTrue(any(getattr(x, "id", None) == a.id for x in amenities))

    def test_add_review_flow(self):
        user = User.create("U", "R", "user_rel@ex.com", "123456")
        owner = User.create("O2", "W2", "owner_rel2@ex.com", "123456")
        place = Place.create("T", "D", 100, 24.7, 46.7, owner)

        r = Review.create("Nice", 5, user, place)

        self.assertEqual(self._review_user_id(r), user.id)
        self.assertEqual(self._review_place_id(r), place.id)

if __name__ == "__main__":
    unittest.main()
