from __future__ import annotations

import json
from pathlib import Path

import pytest

from backtest_report.render import build_html
from backtest_report.schema import validate_payload


def demo_metrics() -> dict:
    return {
        "model_name": "Test",
        "overall_accuracy": 0.65,
        "brier": 0.22,
        "n_test": 100,
        "calibration": [
            {"bin_mid": 0.3, "pred_mean": 0.32, "obs_freq": 0.30, "n": 40},
            {"bin_mid": 0.7, "pred_mean": 0.68, "obs_freq": 0.70, "n": 60},
        ],
        "rolling_accuracy": [{"week": 1, "acc": 0.62}, {"week": 2, "acc": 0.68}],
        "clv_summary": {"mean_clv_cents": 0.5, "pct_bets_positive_clv": 0.5, "closing_line_value_note": "demo"},
        "bets": [
            {"stake": 1.0, "won": True, "odds_american": -110},
            {"stake": 1.0, "won": False, "odds_american": -110},
        ],
    }


def test_validate_ok():
    assert validate_payload(demo_metrics()) == []


def test_validate_missing():
    assert any("model_name" in m for m in validate_payload({}))


def test_html_contains_key_chunks():
    html = build_html(demo_metrics())
    assert "Test" in html
    assert "Chart" in html
    assert "65.0%" in html or "65%" in html
    assert "Calibration" in html


def test_cli_roundtrip(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from backtest_report.cli import main

    inp = tmp_path / "m.json"
    out = tmp_path / "r.html"
    inp.write_text(json.dumps(demo_metrics()), encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["backtest-report", str(inp), "-o", str(out)])
    main()
    assert out.exists()
    assert "Chart" in out.read_text(encoding="utf-8")
