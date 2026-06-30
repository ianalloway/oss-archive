# Contributing to oss-archive

This repository is a **frozen archive** of completed projects. Each project lives on its own branch (`archive/<name>`).

## How to Contribute

### Fixing an archived project

1. Check out the relevant branch: `git checkout archive/<project-name>`
2. Make your fix
3. Open a PR targeting that branch (not `main`)

### Adding a new project to the archive

1. Create a new branch: `git checkout -b archive/<new-project-name>`
2. Add the project files
3. Update `README.md` on `main` with a one-line entry in the appropriate table
4. Open a PR

### Updating the README

The `main` branch only contains `README.md`, `.gitignore`, and `SECURITY.md`. To update the index:

1. Edit `README.md` on a feature branch
2. Follow the existing table format (project link + one-line description)
3. Open a PR against `main`

## Guidelines

- **Do not** delete archived branches — they are the permanent record
- **Do not** force-push to `archive/*` branches
- Keep README entries to one concise line
