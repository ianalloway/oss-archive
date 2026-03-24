"""SQLite persistence."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Generator

SCHEMA = """
CREATE TABLE IF NOT EXISTS watches (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sport_key TEXT NOT NULL,
  home_team TEXT NOT NULL,
  away_team TEXT NOT NULL,
  bookmaker_key TEXT NOT NULL,
  market_key TEXT NOT NULL DEFAULT 'h2h',
  outcome_name TEXT NOT NULL,
  min_american_delta REAL NOT NULL DEFAULT 5,
  webhook_url TEXT NOT NULL,
  last_american REAL,
  last_updated TEXT,
  active INTEGER NOT NULL DEFAULT 1
);
"""


@dataclass
class Watch:
    id: int
    sport_key: str
    home_team: str
    away_team: str
    bookmaker_key: str
    market_key: str
    outcome_name: str
    min_american_delta: float
    webhook_url: str
    last_american: float | None
    last_updated: str | None
    active: bool


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)


@contextmanager
def session(db_path: Path) -> Generator[sqlite3.Connection, None, None]:
    conn = connect(db_path)
    try:
        init_db(conn)
        yield conn
        conn.commit()
    finally:
        conn.close()


def row_to_watch(row: sqlite3.Row) -> Watch:
    return Watch(
        id=row["id"],
        sport_key=row["sport_key"],
        home_team=row["home_team"],
        away_team=row["away_team"],
        bookmaker_key=row["bookmaker_key"],
        market_key=row["market_key"] or "h2h",
        outcome_name=row["outcome_name"],
        min_american_delta=float(row["min_american_delta"]),
        webhook_url=row["webhook_url"],
        last_american=float(row["last_american"]) if row["last_american"] is not None else None,
        last_updated=row["last_updated"],
        active=bool(row["active"]),
    )


def list_watches(conn: sqlite3.Connection, active_only: bool = True) -> list[Watch]:
    q = "SELECT * FROM watches"
    if active_only:
        q += " WHERE active = 1"
    q += " ORDER BY id"
    return [row_to_watch(r) for r in conn.execute(q)]


def insert_watch(
    conn: sqlite3.Connection,
    *,
    sport_key: str,
    home_team: str,
    away_team: str,
    bookmaker_key: str,
    market_key: str,
    outcome_name: str,
    min_american_delta: float,
    webhook_url: str,
) -> int:
    cur = conn.execute(
        """
        INSERT INTO watches (
          sport_key, home_team, away_team, bookmaker_key, market_key,
          outcome_name, min_american_delta, webhook_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            sport_key.strip(),
            home_team.strip(),
            away_team.strip(),
            bookmaker_key.strip().lower(),
            (market_key or "h2h").strip().lower(),
            outcome_name.strip(),
            min_american_delta,
            webhook_url.strip(),
        ),
    )
    return int(cur.lastrowid)


def update_last_quote(
    conn: sqlite3.Connection,
    watch_id: int,
    american: float,
    iso_ts: str,
) -> None:
    conn.execute(
        """
        UPDATE watches SET last_american = ?, last_updated = ? WHERE id = ?
        """,
        (american, iso_ts, watch_id),
    )


def delete_watch(conn: sqlite3.Connection, watch_id: int) -> bool:
    cur = conn.execute("DELETE FROM watches WHERE id = ?", (watch_id,))
    return cur.rowcount > 0
