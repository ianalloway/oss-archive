# Contributing to oss-archive

This repository is a **frozen archive** of completed projects. Each project lives on its own branch (`archive/<name>`). The `main` branch is the index only.

Active / live work is **not** here — it lives in sibling public repos (see the “Live work” section in `README.md`). Prefer those repos for new features; use this archive for historical snapshots and revive workflows.

## What’s on `main`

- `README.md` — catalog (live vs frozen), grouped one-liners, revive workflow
- `STATUS.md` — generated tip table (SHA, dates, file counts)
- `scripts/generate-status.sh` — regenerates `STATUS.md`
- Community files: `LICENSE`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, issue templates

## How to contribute

### Fixing an archived project

1. Check out the relevant branch: `git checkout archive/<project-name>`
2. Make your fix
3. Open a PR targeting that branch (not `main`)

### Adding a new project to the archive

1. Create a new branch: `git checkout -b archive/<new-project-name>`
2. Add the project files and push
3. On `main`, add a one-line entry to `README.md` under the right frozen group (sports, agents, tools, coursework)
4. Run `./scripts/generate-status.sh` and commit the updated `STATUS.md`
5. Open a PR against `main` for the index changes

### Updating the README or status table

1. Edit on a feature branch off `main`
2. Keep project blurbs to one concise line; keep live-repo links accurate
3. Re-run `./scripts/generate-status.sh` if archive tips changed
4. Open a PR against `main`

## Guidelines

- **Do not** delete archived branches — they are the permanent record
- **Do not** force-push to `archive/*` branches
- Prefer the revive one-liner in the README over copying files by hand
