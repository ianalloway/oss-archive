"""Render self-contained HTML (Chart.js via CDN)."""

from __future__ import annotations

import json
from typing import Any


def _bet_summary(bets: list[dict[str, Any]]) -> dict[str, float]:
    """Units = profit in 'stake units' using American odds convention."""
    total_stake = 0.0
    total_return = 0.0
    wins = 0
    for b in bets:
        stake = float(b.get("stake", 0))
        if stake <= 0:
            continue
        total_stake += stake
        won = bool(b.get("won", False))
        if won:
            wins += 1
        if "ev_units" in b:
            total_return += float(b["ev_units"]) * stake
            continue
        odds = int(b.get("odds_american", -110))
        if won:
            if odds > 0:
                total_return += stake * (odds / 100.0)
            else:
                total_return += stake * (100.0 / abs(odds))
        else:
            total_return -= stake
    n = len([b for b in bets if float(b.get("stake", 0)) > 0])
    roi = (total_return / total_stake) if total_stake > 0 else 0.0
    return {
        "n_bets": float(n),
        "total_stake": total_stake,
        "total_profit_units": total_return,
        "roi": roi,
        "win_rate": (wins / n) if n else 0.0,
    }


def build_html(payload: dict[str, Any]) -> str:
    cal = payload["calibration"]
    roll = payload.get("rolling_accuracy") or []
    clv = payload.get("clv_summary") or {}
    bets = payload.get("bets")
    bet_block = ""
    if isinstance(bets, list) and bets:
        s = _bet_summary(bets)
        bet_block = f"""
    <h2>Bet ledger (optional)</h2>
    <p class="muted">N = {int(s["n_bets"])} · Total stake (units) = {s["total_stake"]:.2f} ·
    Profit = {s["total_profit_units"]:.2f} · ROI = {s["roi"]*100:.1f}% · Win% = {s["win_rate"]*100:.1f}%</p>
"""

    safe_json = json.dumps(payload, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{_esc(str(payload.get("model_name", "Backtest report")))}</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 24px auto; max-width: 960px; color: #1a1a1a; }}
    h1 {{ font-size: 1.35rem; }}
    h2 {{ font-size: 1.05rem; margin-top: 2rem; border-bottom: 1px solid #ccc; padding-bottom: 4px; }}
    .kpis {{ display: flex; flex-wrap: wrap; gap: 16px; margin: 16px 0; }}
    .kpi {{ background: #f4f4f5; padding: 12px 16px; border-radius: 8px; min-width: 120px; }}
    .kpi span {{ display: block; font-size: 1.25rem; font-weight: 600; }}
    .muted {{ color: #555; font-size: 0.9rem; }}
    canvas {{ max-height: 320px; }}
    pre {{ background: #0b1020; color: #e2e8f0; padding: 12px; border-radius: 8px; overflow: auto; font-size: 11px; }}
  </style>
</head>
<body>
  <h1>{_esc(str(payload.get("model_name", "Backtest report")))}</h1>
  <p class="muted">Static report from <code>backtest-report-gen</code> · Print or Save as PDF from the browser.</p>
  <div class="kpis">
    <div class="kpi">Accuracy<span>{float(payload["overall_accuracy"])*100:.1f}%</span></div>
    <div class="kpi">Brier<span>{float(payload["brier"]):.4f}</span></div>
    <div class="kpi">N test<span>{int(payload.get("n_test", 0))}</span></div>
    <div class="kpi">Mean CLV (¢)<span>{float(clv.get("mean_clv_cents", 0)):.2f}</span></div>
    <div class="kpi">%+ CLV<span>{float(clv.get("pct_bets_positive_clv", 0))*100:.1f}%</span></div>
  </div>
  {bet_block}
  <h2>Calibration (predicted vs observed)</h2>
  <canvas id="calChart"></canvas>
  <h2>Rolling accuracy</h2>
  <canvas id="rollChart"></canvas>
  <h2>CLV note</h2>
  <p class="muted">{_esc(str(clv.get("closing_line_value_note", "—")))}</p>
  <h2>Source JSON</h2>
  <pre>{_esc(safe_json)}</pre>
  <script>
    const cal = {json.dumps(cal)};
    const roll = {json.dumps(roll)};
    const calLabels = cal.map(r => (r.pred_mean != null ? r.pred_mean : r.bin_mid).toFixed(2));
    new Chart(document.getElementById('calChart'), {{
      type: 'line',
      data: {{
        labels: calLabels,
        datasets: [
          {{ label: 'Predicted mean', data: cal.map(r => r.pred_mean), borderColor: '#2563eb', tension: 0.2 }},
          {{ label: 'Observed freq', data: cal.map(r => r.obs_freq), borderColor: '#16a34a', tension: 0.2 }},
        ]
      }},
      options: {{
        responsive: true,
        plugins: {{ legend: {{ position: 'bottom' }} }},
        scales: {{
          y: {{ min: 0, max: 1, title: {{ display: true, text: 'Probability' }} }},
          x: {{ title: {{ display: true, text: 'Bin (pred mean)' }} }}
        }}
      }}
    }});
    if (roll.length) {{
      new Chart(document.getElementById('rollChart'), {{
        type: 'line',
        data: {{
          labels: roll.map(r => 'W' + r.week),
          datasets: [{{ label: 'Accuracy', data: roll.map(r => r.acc), borderColor: '#9333ea', tension: 0.2 }}]
        }},
        options: {{
          responsive: true,
          scales: {{
            y: {{ min: 0, max: 1, title: {{ display: true, text: 'Accuracy' }} }},
          }}
        }}
      }});
    }}
  </script>
</body>
</html>
"""


def _esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
