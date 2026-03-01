import unittest
import uuid
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

        # Create amenity
        amenity_resp = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi",
            "description": "Fast internet"
        })
        self.assertEqual(amenity_resp.status_code, 201)
        self.amenity_id = amenity_resp.get_json()["id"]

        # Create user (unique email each run)
        unique_email = f"owner_{uuid.uuid4().hex}@example.com"
        user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": unique_email,
            "password": "123456"
        })
        self.assertEqual(user_resp.status_code, 201, msg=user_resp.get_data(as_text=True))
        self.user_id = user_resp.get_json()["id"]

    def test_create_place_success(self):
        resp = self.client.post('/api/v1/places/', json={
            "title": "Test place",
            "description": "Nice",
            "price": 100,
            "latitude": 24.7,
            "longitude": 46.7,
            "owner_id": self.user_id,
            "amenities": [self.amenity_id],
        })
        self.assertEqual(resp.status_code, 201, msg=resp.get_data(as_text=True))
        data = resp.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["title"], "Test place")
        self.assertTrue("amenities" in data and isinstance(data["amenities"], list))

    def test_create_place_invalid_owner(self):
        resp = self.client.post('/api/v1/places/', json={
            "title": "Bad owner place",
            "description": "Nice",
            "price": 100,
            "latitude": 24.7,
            "longitude": 46.7,
            "owner_id": "does-not-exist",
            "amenities": [self.amenity_id],
        })
        self.assertEqual(resp.status_code, 404, msg=resp.get_data(as_text=True))

if __name__ == "__main__":
    unittest.main()
