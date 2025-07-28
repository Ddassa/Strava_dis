import hmac
import hashlib
import json
from fastapi.testclient import TestClient
import pytest


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("STRAVA_WEBHOOK_SECRET", "secret")
    from trailmetrics.app.main import app
    return TestClient(app)


def test_webhook_signature(client):
    payload = {"elevation_data": [0, 10], "time_data": ["2024-01-01T00:00:00", "2024-01-01T00:10:00"], "total_elevation": 10, "distance_km": 1}
    body = json.dumps(payload).encode()
    signature = hmac.new(b"secret", body, hashlib.sha256).hexdigest()
    headers = {"X-Strava-Signature": signature}
    resp = client.post("/webhook", data=body, headers=headers)
    assert resp.status_code == 200
    assert "vam" in resp.json()


