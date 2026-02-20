import unittest
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_create_amenity_success(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)

    def test_create_amenity_missing_name(self):
        response = self.client.post('/api/v1/amenities/', json={})
        self.assertIn(response.status_code, [400, 422])

if __name__ == "__main__":
    unittest.main()
