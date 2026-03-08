import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_create_user_success(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test_user@example.com",
            "password": "123456"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)

    def test_create_user_duplicate_email(self):
        self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "duplicate@example.com",
            "password": "123456"
        })
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "duplicate@example.com",
            "password": "123456"
        })
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
