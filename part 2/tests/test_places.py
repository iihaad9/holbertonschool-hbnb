import unittest
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

        user = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "Test",
            "email": "owner_place@example.com"
        })
        self.user_id = user.get_json()["id"]

    def test_create_place_success(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "Nice",
            "price": 100,
            "latitude": 20.0,
            "longitude": 30.0,
            "owner_id": self.user_id
        })
        self.assertEqual(response.status_code, 201)

    def test_create_place_invalid_owner(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "price": 100,
            "latitude": 20.0,
            "longitude": 30.0,
            "owner_id": "fake_id"
        })
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
