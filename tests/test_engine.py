from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from odds_drift_watch.engine import run_tick
from odds_drift_watch.store import connect, init_db, insert_watch


def sample_events(home="Lakers", away="Celtics", price=-110.0):
    return [
        {
            "home_team": home,
            "away_team": away,
            "bookmakers": [
                {
                    "key": "draftkings",
                    "markets": [
                        {
                            "key": "h2h",
                            "outcomes": [
                                {"name": home, "price": price},
                                {"name": away, "price": 100.0},
                            ],
                        }
                    ],
                }
            ],
        }
    ]


def test_tick_baseline_then_alert(tmp_path: Path):
    db = tmp_path / "t.db"
    conn = connect(db)
    init_db(conn)
    insert_watch(
        conn,
        sport_key="basketball_nba",
        home_team="Lakers",
        away_team="Celtics",
        bookmaker_key="draftkings",
        market_key="h2h",
        outcome_name="Lakers",
        min_american_delta=5.0,
        webhook_url="https://example.com/hook",
    )
    conn.commit()
    conn.close()

    with patch("odds_drift_watch.engine.fetch_event_odds") as m_fetch, patch(
        "odds_drift_watch.engine.send_webhook"
    ) as m_hook:
        m_fetch.return_value = sample_events(price=-110)
        s1 = run_tick(db_path=db, api_key="fake")
        assert s1["alerts_sent"] == 0
        m_fetch.return_value = sample_events(price=-120)
        s2 = run_tick(db_path=db, api_key="fake")
        assert s2["alerts_sent"] == 1
        m_hook.assert_called_once()
