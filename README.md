# oss-archive

Snapshots of Ian’s **archived** public GitHub repositories (migration 2026-04-02).

- **Layout:** `archive/<repository-name>` = that repo’s default branch at archive time.
- **Browse:** [All branches](https://github.com/ianalloway/oss-archive/branches/all)

## Index

| Former repo | Branch |
|-------------|--------|
| [`allowayai`](https://github.com/ianalloway/allowayai) | [`archive/allowayai`](https://github.com/ianalloway/oss-archive/tree/archive/allowayai) |
| [`allowayai-demo`](https://github.com/ianalloway/allowayai-demo) | [`archive/allowayai-demo`](https://github.com/ianalloway/oss-archive/tree/archive/allowayai-demo) |
| [`assignment12-rmarkdown`](https://github.com/ianalloway/assignment12-rmarkdown) | [`archive/assignment12-rmarkdown`](https://github.com/ianalloway/oss-archive/tree/archive/assignment12-rmarkdown) |
| [`awesome-sports-betting`](https://github.com/ianalloway/awesome-sports-betting) | [`archive/awesome-sports-betting`](https://github.com/ianalloway/oss-archive/tree/archive/awesome-sports-betting) |
| [`backtest-report-gen`](https://github.com/ianalloway/backtest-report-gen) | [`archive/backtest-report-gen`](https://github.com/ianalloway/oss-archive/tree/archive/backtest-report-gen) |
| [`closing-line-archive`](https://github.com/ianalloway/closing-line-archive) | [`archive/closing-line-archive`](https://github.com/ianalloway/oss-archive/tree/archive/closing-line-archive) |
| [`code-stash`](https://github.com/ianalloway/code-stash) | [`archive/code-stash`](https://github.com/ianalloway/oss-archive/tree/archive/code-stash) |
| [`deathcon-api`](https://github.com/ianalloway/deathcon-api) | [`archive/deathcon-api`](https://github.com/ianalloway/oss-archive/tree/archive/deathcon-api) |
| [`friedman`](https://github.com/ianalloway/friedman) | [`archive/friedman`](https://github.com/ianalloway/oss-archive/tree/archive/friedman) |
| [`lis4805`](https://github.com/ianalloway/lis4805) | [`archive/lis4805`](https://github.com/ianalloway/oss-archive/tree/archive/lis4805) |
| [`macos-disk-cleanup`](https://github.com/ianalloway/macos-disk-cleanup) | [`archive/macos-disk-cleanup`](https://github.com/ianalloway/oss-archive/tree/archive/macos-disk-cleanup) |
| [`metric-regression-gate`](https://github.com/ianalloway/metric-regression-gate) | [`archive/metric-regression-gate`](https://github.com/ianalloway/oss-archive/tree/archive/metric-regression-gate) |
| [`nba-clv-dashboard`](https://github.com/ianalloway/nba-clv-dashboard) | [`archive/nba-clv-dashboard`](https://github.com/ianalloway/oss-archive/tree/archive/nba-clv-dashboard) |
| [`nba-edge`](https://github.com/ianalloway/nba-edge) | [`archive/nba-edge`](https://github.com/ianalloway/oss-archive/tree/archive/nba-edge) |
| [`odds-cli`](https://github.com/ianalloway/odds-cli) | [`archive/odds-cli`](https://github.com/ianalloway/oss-archive/tree/archive/odds-cli) |
| [`odds-drift-watch`](https://github.com/ianalloway/odds-drift-watch) | [`archive/odds-drift-watch`](https://github.com/ianalloway/oss-archive/tree/archive/odds-drift-watch) |
| [`openclaw-patches`](https://github.com/ianalloway/openclaw-patches) | [`archive/openclaw-patches`](https://github.com/ianalloway/oss-archive/tree/archive/openclaw-patches) |
| [`openclaw-skills`](https://github.com/ianalloway/openclaw-skills) | [`archive/openclaw-skills`](https://github.com/ianalloway/oss-archive/tree/archive/openclaw-skills) |
| [`portfolio-ship-week`](https://github.com/ianalloway/portfolio-ship-week) | [`archive/portfolio-ship-week`](https://github.com/ianalloway/oss-archive/tree/archive/portfolio-ship-week) |
| [`repo-health`](https://github.com/ianalloway/repo-health) | [`archive/repo-health`](https://github.com/ianalloway/oss-archive/tree/archive/repo-health) |
| [`snake-game`](https://github.com/ianalloway/snake-game) | [`archive/snake-game`](https://github.com/ianalloway/oss-archive/tree/archive/snake-game) |
| [`stock-sentiment-analyzer`](https://github.com/ianalloway/stock-sentiment-analyzer) | [`archive/stock-sentiment-analyzer`](https://github.com/ianalloway/oss-archive/tree/archive/stock-sentiment-analyzer) |
| [`taskmaster`](https://github.com/ianalloway/taskmaster) | [`archive/taskmaster`](https://github.com/ianalloway/oss-archive/tree/archive/taskmaster) |
| [`weather-dashboard-cli`](https://github.com/ianalloway/weather-dashboard-cli) | [`archive/weather-dashboard-cli`](https://github.com/ianalloway/oss-archive/tree/archive/weather-dashboard-cli) |


## Restore a project

1. Clone this repository:

```bash
git clone https://github.com/ianalloway/oss-archive.git
cd oss-archive
```

2. Check out a frozen project branch:

```bash
git checkout archive/<repo-name>
```

3. Optional: re-home the project into a fresh repo.

- **Simple path:** create a new GitHub repo and push this checked-out branch.
- **Subtree path:** import into another monorepo under a subdirectory:

```bash
git subtree add --prefix=apps/<repo-name> https://github.com/ianalloway/oss-archive.git archive/<repo-name>
```
