# oss-archive

*Can a sports model beat the closing line — and can you prove it under scrutiny?*

That question built most of this. 24 repos, each a frozen branch: `archive/<name>`.

---

## The System

Markets are honest. They punish bad models with money. That makes them a better proving ground than any benchmark dataset.

**1. Find the edge**
[nba-edge](https://github.com/ianalloway/oss-archive/tree/archive/nba-edge) feeds live odds into ML power ratings and flags where your number beats the book. [odds-cli](https://github.com/ianalloway/oss-archive/tree/archive/odds-cli) pulls lines across books and sizes Kelly bets from the terminal, zero config.

**2. Watch the lines move**
[odds-drift-watch](https://github.com/ianalloway/oss-archive/tree/archive/odds-drift-watch) polls prices for the matchups you care about and fires a webhook with a Line Shock Index when odds drift past your threshold.

**3. Archive the history**
[closing-line-archive](https://github.com/ianalloway/oss-archive/tree/archive/closing-line-archive) writes normalized odds snapshots to SQLite, one row per quote. Append from cron. Compare open vs. close to see whether your price beat what the market settled at.

**4. Evaluate honestly**
[nba-clv-dashboard](https://github.com/ianalloway/oss-archive/tree/archive/nba-clv-dashboard) is a FastAPI + Chart.js dashboard for calibration curves, rolling accuracy, and CLV. [backtest-report-gen](https://github.com/ianalloway/oss-archive/tree/archive/backtest-report-gen) turns a `metrics.json` into a shareable static HTML report in one command.

**5. Guard the model**
[metric-regression-gate](https://github.com/ianalloway/oss-archive/tree/archive/metric-regression-gate) compares baseline vs. current metrics JSON and exits 1 if anything regressed past tolerance. Model PRs can't silently get worse.

**6. Know the landscape**
[awesome-sports-betting](https://github.com/ianalloway/oss-archive/tree/archive/awesome-sports-betting) is the curated list — tools, APIs, datasets, and libraries for anyone working in this domain.

---

## The Toolkit

A Claude webhook wrapper, a snippet manager with local Ollama search, repo scoring, a task manager, news sentiment on tickers, a macOS cache cleaner, weather in the terminal.

| Project | What it does |
|---------|-------------|
| [deathcon-api](https://github.com/ianalloway/oss-archive/tree/archive/deathcon-api) | Claude wrapper + webhook router for GitHub, Telegram, and n8n. Streaming supported. |
| [repo-health](https://github.com/ianalloway/oss-archive/tree/archive/repo-health) | Scores any GitHub repo on docs, maintenance, and hygiene. |
| [code-stash](https://github.com/ianalloway/oss-archive/tree/archive/code-stash) | CLI snippet manager. Save locally, retrieve with Ollama-powered search. |
| [taskmaster](https://github.com/ianalloway/oss-archive/tree/archive/taskmaster) | AI-assisted task manager for the terminal. |
| [stock-sentiment-analyzer](https://github.com/ianalloway/oss-archive/tree/archive/stock-sentiment-analyzer) | Fetches news and scores NLP sentiment for any stock or crypto ticker. |
| [macos-disk-cleanup](https://github.com/ianalloway/oss-archive/tree/archive/macos-disk-cleanup) | Clears regenerable caches on macOS — Homebrew, pip, Chrome, Docker, Go — without touching anything important. |
| [weather-dashboard-cli](https://github.com/ianalloway/oss-archive/tree/archive/weather-dashboard-cli) | City name in. Current conditions out. |

---

## R Work

Two packages — one for ML evaluation and sports analytics, one for nonparametric statistics — plus coursework.

| Project | What it does |
|---------|-------------|
| [allowayai](https://github.com/ianalloway/oss-archive/tree/archive/allowayai) | R package: ML evaluation and sports analytics utilities for prediction and betting workflows. |
| [allowayai-demo](https://github.com/ianalloway/oss-archive/tree/archive/allowayai-demo) | Demo application for the allowayai package. |
| [friedman](https://github.com/ianalloway/oss-archive/tree/archive/friedman) | R package for Friedman's nonparametric two-way ANOVA by ranks. Full workflow, documented. |
| [assignment12-rmarkdown](https://github.com/ianalloway/oss-archive/tree/archive/assignment12-rmarkdown) | Introduction to R Markdown — .Rmd source and rendered HTML. |

---

## OpenClaw

[OpenClaw](https://github.com/openclaw/openclaw) is an open-source AI assistant. These are contributions to that ecosystem.

| Project | What it does |
|---------|-------------|
| [openclaw-patches](https://github.com/ianalloway/oss-archive/tree/archive/openclaw-patches) | Personal fork with custom modifications. |
| [openclaw-skills](https://github.com/ianalloway/oss-archive/tree/archive/openclaw-skills) | Custom TypeScript skills for the assistant. |
| [portfolio-ship-week](https://github.com/ianalloway/oss-archive/tree/archive/portfolio-ship-week) | Skill for shipping a portfolio: DNS, SEO, outreach — all the last-mile steps. |

---

## Odds & Ends

| Project | What it does |
|---------|-------------|
| [snake-game](https://github.com/ianalloway/oss-archive/tree/archive/snake-game) | Classic Snake. Plain HTML, CSS, and JavaScript. |
| [lis4805](https://github.com/ianalloway/oss-archive/tree/archive/lis4805) | LIS 4805 — Debugging and Defensive Programming coursework. |

---

## Thaw a project

```bash
git clone https://github.com/ianalloway/oss-archive.git
cd oss-archive
git checkout archive/<repo-name>
```

Re-home to its own repo: push the checked-out branch to a new GitHub repo.

Pull into a monorepo as a subdirectory:

```bash
git subtree add --prefix=apps/<repo-name> \
  https://github.com/ianalloway/oss-archive.git archive/<repo-name>
```
