import httpx
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_histogram_endpoint():
    category = 'travel'
    response = client.get(f"/histogram/{category}")

    assert response.status_code == 200
    assert response.headers['content-type'] == 'image/png'
