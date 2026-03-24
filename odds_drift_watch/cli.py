"""CLI: run one poll tick (for cron)."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from odds_drift_watch.engine import run_tick


def main() -> None:
    p = argparse.ArgumentParser(description="Poll The Odds API and send drift webhooks.")
    p.add_argument(
        "command",
        choices=["tick"],
        help="tick: fetch all watches once",
    )
    p.add_argument("--db", type=Path, default=Path(os.environ.get("ODDS_DRIFT_DB", "odds_drift.db")))
    args = p.parse_args()

    key = os.environ.get("THE_ODDS_API_KEY", "")
    if not key:
        print("error: set THE_ODDS_API_KEY", file=sys.stderr)
        sys.exit(2)

    if args.command == "tick":
        stats = run_tick(db_path=args.db, api_key=key)
        print(stats, file=sys.stderr)


if __name__ == "__main__":
    main()
