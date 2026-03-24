# backtest-report-gen

[![CI](https://github.com/ianalloway/backtest-report-gen/actions/workflows/ci.yml/badge.svg)](https://github.com/ianalloway/backtest-report-gen/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Problem:** Execs remember charts, not your notebook. You already have eval JSON — you need a **shareable, static** report (email, PDF, artifact).

**Solution:** One command: **`metrics.json` → single `report.html`** (Chart.js over CDN): calibration vs observed, rolling accuracy, CLV KPIs, optional bet-ledger ROI.

JSON shape matches **[nba-clv-dashboard](https://github.com/ianalloway/nba-clv-dashboard)** `demo_metrics` (`model_name`, `overall_accuracy`, `brier`, `calibration[]`, optional `rolling_accuracy`, `clv_summary`, optional `bets`).

```bash
pip install -e .
backtest-report path/to/metrics.json -o report.html
# open report.html → Print → Save as PDF
```

## Optional `bets` array

Each row: `stake`, `won`, `odds_american` (profit computed with standard American payout math), or precomputed `ev_units` times stake.

## Non-goals

- **No** cloud upload — file output only.
- **No** bundled data — bring your own eval JSON.

## License

MIT
