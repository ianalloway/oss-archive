# odds-drift-watch

[![CI](https://github.com/ianalloway/odds-drift-watch/actions/workflows/ci.yml/badge.svg)](https://github.com/ianalloway/odds-drift-watch/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**What it is:** A small **line-move radar**. You bring **[The Odds API](https://the-odds-api.com/)** key (BYOK). It polls prices for matchups you care about, remembers the last print, and **POSTs JSON to your webhook** (Discord, Slack incoming webhook, n8n, your own API) when American odds move by at least **Δ** — packaged as a **`Line Shock Index`** in the payload for messaging.

**Honest revenue framing:** No tool “prints money.” Income comes from **solving a painful alert problem** for a niche that already pays for data: serious bettors, content creators, and small syndicates who want **proactive** moves instead of staring at screens. This repo is the **MVP**; money comes from **hosted tiers**, **setup fees**, or **distribution** (below).

---

## Quick start

```bash
pip install -e .
export THE_ODDS_API_KEY="your_key"
export ODDS_DRIFT_DB="/tmp/drift.db"
# optional: protect HTTP API
# export ODDS_DRIFT_SERVICE_TOKEN="long-random"

uvicorn odds_drift_watch.app:APP --reload --port 8766
```

- `POST /watches` — register a watch (see OpenAPI at `/docs`).
- `POST /tick` — run one poll cycle (hook **GitHub Actions**, **Railway cron**, or **Uptime Kuma** to hit this every N minutes).
- `odds-drift-watch tick --db ./odgs.db` — same poll from cron without HTTP.

**Auth:** If `ODDS_DRIFT_SERVICE_TOKEN` is set, pass `Authorization: Bearer <token>` on mutating routes and `/tick`.

---

## Why this can earn (strategy, not a promise)

| Lever | Idea |
|--------|------|
| **Hosted “Pulse” tier** | Deploy for customers; they pay **$19–79/mo** for managed polling + Discord delivery + retention. You absorb Odds API usage into your plan math. |
| **Lifetime / founder deal** | **$99–249** one-time on X / Discord for “unlimited watches” on a shared worker until you cap capacity — classic indie liquidity event. |
| **Creator affiliate** | Pair with Odds API referral + your **closing-line-archive** story: “drift alerts + historical archive pack.” |
| **B2B n8n recipe** | Sell a **workflow template** + 1h onboarding call: “line shock → Slack → sheet” for $500 flat. |

**Compliance:** You’re not taking bets; you’re alerting on **public quotes**. Still: respect **The Odds API** ToS, local gambling **advertising** rules if you market to bettors, and don’t imply ROI.

---

## Payload shape (webhook)

```json
{
  "alert": "odds_drift_watch",
  "ts": "2026-03-24T12:00:00Z",
  "watch_id": 1,
  "sport_key": "basketball_nba",
  "matchup": "Celtics @ Lakers",
  "book": "draftkings",
  "outcome": "Lakers",
  "old_american": -110,
  "new_american": -120,
  "delta": -10,
  "line_shock_index": 10
}
```

---

## Stack

Python 3.10+ · FastAPI · httpx · SQLite

---

## License

MIT
