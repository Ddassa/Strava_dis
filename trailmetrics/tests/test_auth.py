import os
from fastapi.testclient import TestClient
import httpx
import pytest


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("CLIENT_ID", "123")
    monkeypatch.setenv("CLIENT_SECRET", "456")
    monkeypatch.setenv("REDIRECT_URI", "http://localhost/callback")
    from trailmetrics.app.main import app
    return TestClient(app)


def test_authorize_redirect(client):
    resp = client.get("/authorize", allow_redirects=False)
    assert resp.status_code == 307
    assert "https://www.strava.com/oauth/authorize" in resp.headers["location"]


def test_callback(monkeypatch, client):
    async def fake_post(url, data):
        class Resp:
            status_code = 200
            def json(self):
                return {"access_token": "a", "refresh_token": "r"}
        return Resp()
    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)
    resp = client.get("/callback?code=abc")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Authorization successful"


