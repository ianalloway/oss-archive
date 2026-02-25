# Contributing to odds-cli

Thank you for your interest in contributing to odds-cli! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git

### Development Setup

1. Fork and clone the repository:

```bash
git clone https://github.com/your-username/odds-cli.git
cd odds-cli
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode with dev dependencies:

```bash
pip install -e ".[dev]"
```

4. Verify everything works:

```bash
odds nba
pytest
flake8 odds_cli/
mypy odds_cli/
```

## Development Workflow

### Branching

- Create a feature branch from `main`:
  ```bash
  git checkout -b feature/your-feature-name
  ```
- Use descriptive branch names: `feature/add-parlay-calc`, `fix/kelly-negative-odds`, `docs/update-readme`

### Making Changes

1. Write your code following the existing style
2. Add or update tests for any new functionality
3. Ensure all tests pass: `pytest`
4. Run the linter: `flake8 odds_cli/`
5. Run the type checker: `mypy odds_cli/`

### Commit Messages

Follow conventional commit format:

```
feat: add parlay odds calculator
fix: correct Kelly criterion for negative odds
docs: update API configuration section
refactor: extract table rendering into display module
test: add tests for odds conversion edge cases
```

### Pull Requests

1. Push your branch to your fork
2. Open a Pull Request against `main`
3. Fill out the PR template with a clear description
4. Ensure CI checks pass
5. Wait for review

## Project Structure

```
odds-cli/
├── odds_cli/
│   ├── __init__.py      # Package init, version
│   ├── main.py          # CLI entry point, argparse, command handlers
│   ├── odds.py          # Core odds math (conversions, Kelly, EV)
│   └── display.py       # Terminal display (colors, tables, box drawing)
├── tests/
│   └── test_odds.py     # Unit tests
├── setup.py             # Package setup
├── pyproject.toml        # Modern Python packaging
├── requirements.txt     # Runtime dependencies
└── README.md
```

## Code Style

- Follow PEP 8 with a max line length of 120 characters
- Use type hints for all function signatures
- Write docstrings for all public functions (Google style)
- Use `from __future__ import annotations` for modern type hint syntax
- No heavy dependencies -- keep the CLI lightweight

## Adding a New Sport

1. Add the sport key mapping in `main.py` `_fetch_live_data()` sport_keys dict
2. Add sample data in `SAMPLE_DATA` for offline demo mode
3. Update the argparse subparsers in `build_parser()`
4. Update README.md with the new sport code
5. Add tests

## Adding a New Command

1. Create a `cmd_yourcommand()` function in `main.py`
2. Add a subparser in `build_parser()`
3. Add dispatch logic in `main()`
4. Update the README usage section
5. Add tests

## Testing

Run the full test suite:

```bash
pytest -v
```

Run with coverage:

```bash
pytest --cov=odds_cli --cov-report=term-missing
```

## Reporting Issues

- Use the GitHub issue templates (bug report or feature request)
- Include your Python version and OS
- For bugs, include the full command and output
- For feature requests, describe the use case

## Code of Conduct

Be respectful and constructive. We are all here to build something useful for the sports betting community.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
