"""The Odds API v4 client (BYOK)."""

from __future__ import annotations

from typing import Any

import httpx

BASE = "https://api.the-odds-api.com/v4"


def fetch_event_odds(
    api_key: str,
    sport_key: str,
    *,
    regions: str = "us",
    markets: str = "h2h",
    odds_format: str = "american",
    timeout: float = 30.0,
) -> list[dict[str, Any]]:
    url = f"{BASE}/sports/{sport_key}/odds"
    params = {
        "apiKey": api_key,
        "regions": regions,
        "markets": markets,
        "oddsFormat": odds_format,
    }
    with httpx.Client(timeout=timeout) as client:
        r = client.get(url, params=params)
        r.raise_for_status()
        data = r.json()
    if not isinstance(data, list):
        raise ValueError("unexpected API response shape")
    return data


def find_american_price(
    events: list[dict[str, Any]],
    *,
    home_team: str,
    away_team: str,
    bookmaker_key: str,
    market_key: str,
    outcome_name: str,
) -> float | None:
    h, a = home_team.strip().lower(), away_team.strip().lower()
    bk = bookmaker_key.strip().lower()
    mk = market_key.strip().lower()
    on = outcome_name.strip().lower()

    for ev in events:
        if ev.get("home_team", "").strip().lower() != h:
            continue
        if ev.get("away_team", "").strip().lower() != a:
            continue
        for book in ev.get("bookmakers") or []:
            if str(book.get("key", "")).lower() != bk:
                continue
            for m in book.get("markets") or []:
                if str(m.get("key", "")).lower() != mk:
                    continue
                for out in m.get("outcomes") or []:
                    if str(out.get("name", "")).strip().lower() == on:
                        p = out.get("price")
                        if p is None:
                            return None
                        return float(p)
    return None
