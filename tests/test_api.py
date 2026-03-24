from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from odds_drift_watch.app import APP


@pytest.fixture
def client(tmp_path, monkeypatch):
    db = tmp_path / "api.db"
    monkeypatch.setenv("ODDS_DRIFT_DB", str(db))
    monkeypatch.delenv("ODDS_DRIFT_SERVICE_TOKEN", raising=False)
    monkeypatch.setenv("THE_ODDS_API_KEY", "test-key")
    with TestClient(APP) as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_list_watch(client):
    r = client.post(
        "/watches",
        json={
            "sport_key": "basketball_nba",
            "home_team": "Lakers",
            "away_team": "Celtics",
            "bookmaker_key": "draftkings",
            "outcome_name": "Lakers",
            "min_american_delta": 5,
            "webhook_url": "https://example.com/x",
        },
    )
    assert r.status_code == 200
    wid = r.json()["id"]
    r2 = client.get("/watches")
    assert r2.status_code == 200
    assert len(r2.json()) == 1
    assert r2.json()[0]["id"] == wid


def test_service_token_enforced(client, monkeypatch):
    monkeypatch.setenv("ODDS_DRIFT_SERVICE_TOKEN", "secret")
    r = client.get("/watches")
    assert r.status_code == 401
    r2 = client.get("/watches", headers={"Authorization": "Bearer secret"})
    assert r2.status_code == 200
