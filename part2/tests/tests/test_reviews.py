import unittest
from app import create_app

class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

        user = self.client.post('/api/v1/users/', json={
            "first_name": "Review",
            "last_name": "Owner",
            "email": "review_owner@example.com"
        })
        self.user_id = user.get_json()["id"]

        place = self.client.post('/api/v1/places/', json={
            "title": "Place For Review",
            "description": "Test",
            "price": 100,
            "latitude": 20.0,
            "longitude": 30.0,
            "owner_id": self.user_id
        })
        self.place_id = place.get_json()["id"]

    def test_create_review_success(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)

    def test_create_review_invalid_rating(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Bad rating",
            "rating": 10,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertIn(response.status_code, [400, 422])

if __name__ == "__main__":
    unittest.main()
