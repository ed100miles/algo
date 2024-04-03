from unittest import TestCase
from fastapi.testclient import TestClient
from algo.api import app

client = TestClient(app)


class APITest(TestCase):
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello"}
