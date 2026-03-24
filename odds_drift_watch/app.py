"""FastAPI service: CRUD watches + cron tick."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from dataclasses import asdict
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from odds_drift_watch.engine import run_tick
from odds_drift_watch.store import connect, delete_watch, init_db, insert_watch, list_watches, row_to_watch

@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = connect(get_db_path())
    try:
        init_db(conn)
    finally:
        conn.close()
    yield


APP = FastAPI(title="Odds Drift Watch", version="0.1.0", lifespan=lifespan)


def get_db_path() -> Path:
    p = os.environ.get("ODDS_DRIFT_DB", "odds_drift.db")
    return Path(p)


def get_api_key_odds() -> str:
    k = os.environ.get("THE_ODDS_API_KEY", "")
    if not k:
        raise HTTPException(500, "THE_ODDS_API_KEY not configured")
    return k


def verify_service_token(authorization: str | None = Header(None)) -> None:
    expected = os.environ.get("ODDS_DRIFT_SERVICE_TOKEN", "")
    if not expected:
        return
    if authorization != f"Bearer {expected}":
        raise HTTPException(401, "invalid or missing service token")


class WatchCreate(BaseModel):
    sport_key: str = Field(examples=["basketball_nba"])
    home_team: str
    away_team: str
    bookmaker_key: str = Field(examples=["draftkings"])
    market_key: str = "h2h"
    outcome_name: str
    min_american_delta: float = 5.0
    webhook_url: str


class WatchOut(BaseModel):
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


@APP.get("/health")
def health():
    return {"status": "ok"}


@APP.post("/watches", dependencies=[Depends(verify_service_token)], response_model=WatchOut)
def create_watch(body: WatchCreate):
    conn = connect(get_db_path())
    try:
        init_db(conn)
        wid = insert_watch(
            conn,
            sport_key=body.sport_key,
            home_team=body.home_team,
            away_team=body.away_team,
            bookmaker_key=body.bookmaker_key,
            market_key=body.market_key,
            outcome_name=body.outcome_name,
            min_american_delta=body.min_american_delta,
            webhook_url=body.webhook_url,
        )
        conn.commit()
        row = conn.execute("SELECT * FROM watches WHERE id = ?", (wid,)).fetchone()
        return WatchOut(**asdict(row_to_watch(row)))
    finally:
        conn.close()


@APP.get("/watches", dependencies=[Depends(verify_service_token)], response_model=list[WatchOut])
def get_watches(active_only: bool = True):
    conn = connect(get_db_path())
    try:
        init_db(conn)
        return [WatchOut(**asdict(w)) for w in list_watches(conn, active_only=active_only)]
    finally:
        conn.close()


@APP.delete("/watches/{watch_id}", dependencies=[Depends(verify_service_token)])
def remove_watch(watch_id: int):
    conn = connect(get_db_path())
    try:
        init_db(conn)
        if not delete_watch(conn, watch_id):
            raise HTTPException(404, "watch not found")
        conn.commit()
    finally:
        conn.close()
    return {"deleted": watch_id}


@APP.post("/tick", dependencies=[Depends(verify_service_token)])
def tick():
    api_key = get_api_key_odds()
    stats = run_tick(db_path=get_db_path(), api_key=api_key)
    return stats
