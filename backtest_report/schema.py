"""Expected JSON shape — aligned with nba-clv-dashboard demo_metrics."""

from __future__ import annotations

from typing import Any, TypedDict


class CalBin(TypedDict, total=False):
    bin_mid: float
    pred_mean: float
    obs_freq: float
    n: int


class RollingPoint(TypedDict, total=False):
    week: int
    acc: float


class ClvSummary(TypedDict, total=False):
    mean_clv_cents: float
    pct_bets_positive_clv: float
    closing_line_value_note: str


class BetRow(TypedDict, total=False):
    """Optional ledger for simple stake / PnL summary."""

    stake: float
    p_model: float
    won: bool
    odds_american: int
    ev_units: float  # optional precomputed profit in stake units


def validate_payload(d: dict[str, Any]) -> list[str]:
    """Return human-readable issues; empty if OK for report generation."""
    issues: list[str] = []
    for key in ("model_name", "overall_accuracy", "brier", "calibration"):
        if key not in d:
            issues.append(f"missing required field: {key}")
    cal = d.get("calibration")
    if not isinstance(cal, list) or len(cal) < 2:
        issues.append("calibration must be a list with at least 2 bins")
    elif cal:
        for i, row in enumerate(cal):
            if not isinstance(row, dict):
                issues.append(f"calibration[{i}] must be an object")
                break
    return issues
