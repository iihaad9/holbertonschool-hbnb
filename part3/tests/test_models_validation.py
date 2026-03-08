import unittest
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class TestModelValidation(unittest.TestCase):
    def setUp(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

        User.set_repository(self.user_repo)
        Place.set_repository(self.place_repo)
        Review.set_repository(self.review_repo)
        Amenity.set_repository(self.amenity_repo)

    def test_user_create_invalid_email(self):
        with self.assertRaises(Exception):
            User.create("A", "B", "not-an-email", "123456")

    def test_user_create_empty_first_name(self):
        with self.assertRaises(Exception):
            User.create("", "B", "a@b.com", "123456")

    def test_amenity_create_empty_name(self):
        with self.assertRaises(Exception):
            Amenity.create("", "x")

    def test_place_create_invalid_price(self):
        owner = User.create("O", "W", "owner@ex.com", "123456")
        with self.assertRaises(Exception):
            Place.create("T", "D", -10, 24.7, 46.7, owner)

    def test_place_create_invalid_latitude(self):
        owner = User.create("O2", "W2", "owner2@ex.com", "123456")
        with self.assertRaises(Exception):
            Place.create("T", "D", 100, 120.0, 46.7, owner)

    def test_place_create_invalid_longitude(self):
        owner = User.create("O3", "W3", "owner3@ex.com", "123456")
        with self.assertRaises(Exception):
            Place.create("T", "D", 100, 24.7, 200.0, owner)

    def test_review_create_invalid_rating(self):
        user = User.create("U", "R", "u@r.com", "123456")
        owner = User.create("O4", "W4", "owner4@ex.com", "123456")
        place = Place.create("T", "D", 100, 24.7, 46.7, owner)
        with self.assertRaises(Exception):
            Review.create("Nice", 0, user, place)

    def test_review_create_empty_text(self):
        user = User.create("U2", "R2", "u2@r.com", "123456")
        owner = User.create("O5", "W5", "owner5@ex.com", "123456")
        place = Place.create("T", "D", 100, 24.7, 46.7, owner)
        with self.assertRaises(Exception):
            Review.create("", 5, user, place)

if __name__ == "__main__":
    unittest.main()
