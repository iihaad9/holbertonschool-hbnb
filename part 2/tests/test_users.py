import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_create_user_success(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test_user@example.com"
        })

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)

if __name__ == "__main__":
    unittest.main()
    def test_create_user_duplicate_email(self):
        # Create first user
        self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "duplicate@example.com"
        })

        # Try creating same email again
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "duplicate@example.com"
        })

        self.assertEqual(response.status_code, 400)
