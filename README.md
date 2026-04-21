# oss-archive

> 24 repos. One archive. Frozen at 2026-04-02.

Ian's public GitHub history consolidated into a single repo — one branch per project, zero noise. The through-line across most of it: **betting markets as a proving ground for ML and data engineering ideas.**

Browse all branches → [github.com/ianalloway/oss-archive/branches/all](https://github.com/ianalloway/oss-archive/branches/all)

---

## The Betting Stack

A suite of tools built around one question: *can you beat the closing line consistently, and can you actually prove it?*

| | Project | What it does |
|---|---------|-------------|
| 📊 | [nba-clv-dashboard](https://github.com/ianalloway/oss-archive/tree/archive/nba-clv-dashboard) | FastAPI + Chart.js eval dashboard — calibration curves, rolling accuracy, CLV |
| 📄 | [backtest-report-gen](https://github.com/ianalloway/oss-archive/tree/archive/backtest-report-gen) | `metrics.json` → shareable static HTML report in one command |
| 🚦 | [metric-regression-gate](https://github.com/ianalloway/oss-archive/tree/archive/metric-regression-gate) | CI gate: model PRs can't silently regress on eval metrics |
| 🗄️ | [closing-line-archive](https://github.com/ianalloway/oss-archive/tree/archive/closing-line-archive) | SQLite store for odds snapshots; tracks whether you beat the close |
| 🎯 | [nba-edge](https://github.com/ianalloway/oss-archive/tree/archive/nba-edge) | Legacy CLI: live odds + ML power ratings → surface value bets |
| 📡 | [odds-cli](https://github.com/ianalloway/oss-archive/tree/archive/odds-cli) | Terminal odds checker across books with Kelly sizing, zero config |
| 🚨 | [odds-drift-watch](https://github.com/ianalloway/oss-archive/tree/archive/odds-drift-watch) | Webhook alerts when lines move past a threshold (Line Shock Index) |
| 📚 | [awesome-sports-betting](https://github.com/ianalloway/oss-archive/tree/archive/awesome-sports-betting) | Curated tools, APIs, datasets, and resources for quantitative bettors |

---

## AI & Developer Tools

| | Project | What it does |
|---|---------|-------------|
| 🤖 | [deathcon-api](https://github.com/ianalloway/oss-archive/tree/archive/deathcon-api) | Claude wrapper + webhook handler for GitHub, Telegram, and n8n |
| 📋 | [code-stash](https://github.com/ianalloway/oss-archive/tree/archive/code-stash) | CLI snippet manager with local Ollama-powered search |
| ✅ | [taskmaster](https://github.com/ianalloway/oss-archive/tree/archive/taskmaster) | AI-powered terminal task manager |
| 🏥 | [repo-health](https://github.com/ianalloway/oss-archive/tree/archive/repo-health) | Scores GitHub repos on docs, maintenance, and hygiene signals |
| 📰 | [stock-sentiment-analyzer](https://github.com/ianalloway/oss-archive/tree/archive/stock-sentiment-analyzer) | NLP news sentiment scoring for stocks and crypto tickers |
| 🧹 | [macos-disk-cleanup](https://github.com/ianalloway/oss-archive/tree/archive/macos-disk-cleanup) | Safely clears regenerable caches on macOS (Homebrew, pip, Chrome...) |
| 🌤️ | [weather-dashboard-cli](https://github.com/ianalloway/oss-archive/tree/archive/weather-dashboard-cli) | Real-time weather by city in the terminal |

---

## R & Statistics

| | Project | What it does |
|---|---------|-------------|
| 📦 | [allowayai](https://github.com/ianalloway/oss-archive/tree/archive/allowayai) | R package — ML eval and sports analytics utilities for betting workflows |
| 🎨 | [allowayai-demo](https://github.com/ianalloway/oss-archive/tree/archive/allowayai-demo) | Demo application for the allowayai package |
| 📐 | [friedman](https://github.com/ianalloway/oss-archive/tree/archive/friedman) | R package for Friedman's nonparametric two-way ANOVA by ranks |
| 📝 | [assignment12-rmarkdown](https://github.com/ianalloway/oss-archive/tree/archive/assignment12-rmarkdown) | R Markdown intro — .Rmd source and rendered HTML |

---

## OpenClaw

[OpenClaw](https://github.com/openclaw/openclaw) is an open-source AI assistant. These are Ian's contributions.

| | Project | What it does |
|---|---------|-------------|
| 🦞 | [openclaw-patches](https://github.com/ianalloway/oss-archive/tree/archive/openclaw-patches) | Personal fork with custom patches |
| 🛠️ | [openclaw-skills](https://github.com/ianalloway/oss-archive/tree/archive/openclaw-skills) | Custom TypeScript skills for the assistant |
| 🚀 | [portfolio-ship-week](https://github.com/ianalloway/oss-archive/tree/archive/portfolio-ship-week) | Skill for launching portfolios: DNS, SEO, outreach |

---

## Everything Else

| | Project | What it does |
|---|---------|-------------|
| 🐍 | [snake-game](https://github.com/ianalloway/oss-archive/tree/archive/snake-game) | Classic Snake in plain HTML, CSS, and JavaScript |
| 🎓 | [lis4805](https://github.com/ianalloway/oss-archive/tree/archive/lis4805) | LIS 4805 — Debugging & Defensive Programming coursework |

---

## Restore a project

```bash
# 1. clone the archive
git clone https://github.com/ianalloway/oss-archive.git && cd oss-archive

# 2. check out any frozen branch
git checkout archive/<repo-name>
```

To re-home into its own repo: create a new GitHub repo, then push the checked-out branch.

To pull into a monorepo as a subdirectory:

```bash
git subtree add --prefix=apps/<repo-name> \
  https://github.com/ianalloway/oss-archive.git archive/<repo-name>
```
