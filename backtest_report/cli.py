"""CLI for backtest-report-gen."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from backtest_report.render import build_html
from backtest_report.schema import validate_payload


def main() -> None:
    p = argparse.ArgumentParser(description="Build static HTML backtest report from eval JSON.")
    p.add_argument("input", type=Path, help="Path to metrics JSON (e.g. from nba-clv-dashboard shape)")
    p.add_argument("-o", "--output", type=Path, default=Path("report.html"), help="Output HTML path")
    args = p.parse_args()

    raw = args.input.read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        print("error: JSON root must be an object", file=sys.stderr)
        sys.exit(2)
    issues = validate_payload(data)
    if issues:
        for i in issues:
            print(f"error: {i}", file=sys.stderr)
        sys.exit(2)

    html = build_html(data)
    args.output.write_text(html, encoding="utf-8")
    print(f"wrote {args.output}")
