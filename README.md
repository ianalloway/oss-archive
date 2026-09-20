# oss-archive

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Archived projects](https://img.shields.io/badge/archived_projects-24-blue)](STATUS.md)

**Frozen snapshots** of completed projects — one `archive/<name>` branch each. This `main` branch is only the index and revive guide. Project source does not live here.

Looking for active work? Start with the [live repos](#live-work--not-in-this-archive) below, not the archive branches.

Tip dates, file counts, and SHA for every frozen branch: **[STATUS.md](STATUS.md)** (regenerate with `./scripts/generate-status.sh`).

---

## Live work — not in this archive

Active development lives in sibling public repos. Dig there first; only come here for historical snapshots.

| Repo | What it is |
|------|------------|
| [ai-advantage](https://github.com/ianalloway/ai-advantage) | Sports betting platform — ML predictions, Kelly sizing, live odds, daily AI picks |
| [kelly-js](https://github.com/ianalloway/kelly-js) | Kelly Criterion calculator (TypeScript) — CLV, bankroll, odds conversion |
| [juryrig](https://github.com/ianalloway/juryrig) | Audit LLM judges — bias, agreement, panels, calibration (PyPI: `juryrig`) |
| [solvent-agent](https://github.com/ianalloway/solvent-agent) | Offline-first self-funding analyst agent demo (Stripe + Nemotron) |
| [ian-web-forge](https://github.com/ianalloway/ian-web-forge) | Portfolio site — live at [ianalloway.xyz](https://ianalloway.xyz) |

---

## Archive layout

| What | Where |
|------|--------|
| This index (`README.md`, `STATUS.md`, community files, scripts) | `main` |
| Each archived project’s full history | `archive/<project-name>` |
| Links in the catalog below | `…/tree/archive/<name>` (opens that branch on GitHub) |

Branches are the permanent record — do not delete or force-push `archive/*`. There is no CI on `main` (docs-only hub).

---

## Revive one-liner

Clone a single frozen branch into a new directory (skips `main`):

```bash
git clone --branch archive/<name> --single-branch \
  https://github.com/ianalloway/oss-archive.git <name> && cd <name>
```

Example — revive `odds-cli` and publish it as its own repo:

```bash
git clone --branch archive/odds-cli --single-branch \
  https://github.com/ianalloway/oss-archive.git odds-cli && cd odds-cli
gh repo create ianalloway/odds-cli --public --source=. --remote=origin --push
```

Already have this repo cloned?

```bash
git fetch origin archive/<name> && git checkout archive/<name>
```

Pull into a monorepo as a subdirectory:

```bash
git subtree add --prefix=apps/<name> \
  https://github.com/ianalloway/oss-archive.git archive/<name>
```

---

## Frozen catalog

24 projects. Each line is one `archive/<name>` branch. Revive with the one-liner above.

### Sports & markets

| Project | What it does |
|---------|-------------|
| [nba-edge](https://github.com/ianalloway/oss-archive/tree/archive/nba-edge) | Live odds → ML power ratings; flags where your number beats the book |
| [odds-cli](https://github.com/ianalloway/oss-archive/tree/archive/odds-cli) | Pull lines across books and size Kelly bets from the terminal |
| [odds-drift-watch](https://github.com/ianalloway/oss-archive/tree/archive/odds-drift-watch) | Poll matchups; webhook when Line Shock Index crosses threshold |
| [closing-line-archive](https://github.com/ianalloway/oss-archive/tree/archive/closing-line-archive) | Normalized odds snapshots to SQLite; open vs close comparison |
| [nba-clv-dashboard](https://github.com/ianalloway/oss-archive/tree/archive/nba-clv-dashboard) | FastAPI + Chart.js: calibration, rolling accuracy, CLV |
| [backtest-report-gen](https://github.com/ianalloway/oss-archive/tree/archive/backtest-report-gen) | Turn `metrics.json` into a shareable static HTML report |
| [metric-regression-gate](https://github.com/ianalloway/oss-archive/tree/archive/metric-regression-gate) | CI gate: exit 1 if metrics regress past tolerance |
| [awesome-sports-betting](https://github.com/ianalloway/oss-archive/tree/archive/awesome-sports-betting) | Curated list of tools, APIs, datasets, and libraries |

### Agents & OpenClaw

| Project | What it does |
|---------|-------------|
| [deathcon-api](https://github.com/ianalloway/oss-archive/tree/archive/deathcon-api) | Claude wrapper + webhook router (GitHub, Telegram, n8n) |
| [openclaw-patches](https://github.com/ianalloway/oss-archive/tree/archive/openclaw-patches) | Personal OpenClaw fork with custom modifications |
| [openclaw-skills](https://github.com/ianalloway/oss-archive/tree/archive/openclaw-skills) | Custom TypeScript skills for OpenClaw |
| [portfolio-ship-week](https://github.com/ianalloway/oss-archive/tree/archive/portfolio-ship-week) | Skill for last-mile portfolio shipping (DNS, SEO, outreach) |

### Tools

| Project | What it does |
|---------|-------------|
| [repo-health](https://github.com/ianalloway/oss-archive/tree/archive/repo-health) | Score any GitHub repo on docs, maintenance, and hygiene |
| [code-stash](https://github.com/ianalloway/oss-archive/tree/archive/code-stash) | CLI snippet manager with Ollama-powered search |
| [taskmaster](https://github.com/ianalloway/oss-archive/tree/archive/taskmaster) | AI-assisted task manager for the terminal |
| [stock-sentiment-analyzer](https://github.com/ianalloway/oss-archive/tree/archive/stock-sentiment-analyzer) | News NLP sentiment for any stock or crypto ticker |
| [macos-disk-cleanup](https://github.com/ianalloway/oss-archive/tree/archive/macos-disk-cleanup) | Clear regenerable macOS caches without touching important data |
| [weather-dashboard-cli](https://github.com/ianalloway/oss-archive/tree/archive/weather-dashboard-cli) | City name in → current conditions out |

### Coursework & R

| Project | What it does |
|---------|-------------|
| [allowayai](https://github.com/ianalloway/oss-archive/tree/archive/allowayai) | R package: ML evaluation and sports analytics utilities |
| [allowayai-demo](https://github.com/ianalloway/oss-archive/tree/archive/allowayai-demo) | Demo application for the allowayai package |
| [friedman](https://github.com/ianalloway/oss-archive/tree/archive/friedman) | R package for Friedman’s nonparametric two-way ANOVA by ranks |
| [assignment12-rmarkdown](https://github.com/ianalloway/oss-archive/tree/archive/assignment12-rmarkdown) | Introduction to R Markdown — `.Rmd` source and rendered HTML |
| [lis4805](https://github.com/ianalloway/oss-archive/tree/archive/lis4805) | LIS 4805 — Debugging and Defensive Programming coursework |
| [snake-game](https://github.com/ianalloway/oss-archive/tree/archive/snake-game) | Classic Snake in plain HTML, CSS, and JavaScript |

---

## Maintaining the index

After adding or updating an `archive/*` branch, refresh the tip table:

```bash
./scripts/generate-status.sh
```

Then commit the updated `STATUS.md` on `main`. See [CONTRIBUTING.md](CONTRIBUTING.md) for PR targeting rules (`main` for the index; `archive/<name>` for project fixes).
