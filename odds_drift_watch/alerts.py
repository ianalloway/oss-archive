"""Outbound webhooks."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

import httpx


def send_webhook(url: str, payload: dict[str, Any], timeout: float = 15.0) -> int:
    with httpx.Client(timeout=timeout) as client:
        r = client.post(
            url,
            content=json.dumps(payload),
            headers={"Content-Type": "application/json"},
        )
        return r.status_code


def build_alert_payload(
    *,
    watch_id: int,
    sport_key: str,
    home_team: str,
    away_team: str,
    bookmaker_key: str,
    outcome_name: str,
    old_american: float | None,
    new_american: float,
    line_shock_index: float,
) -> dict[str, Any]:
    """line_shock_index: abs(delta) — a marketable name for the same number."""
    return {
        "alert": "odds_drift_watch",
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "watch_id": watch_id,
        "sport_key": sport_key,
        "matchup": f"{away_team} @ {home_team}",
        "book": bookmaker_key,
        "outcome": outcome_name,
        "old_american": old_american,
        "new_american": new_american,
        "delta": (new_american - old_american) if old_american is not None else None,
        "line_shock_index": line_shock_index,
    }
