# Development Guidelines

## General Rules

- Use English for code (comments, docstrings, logs, error messages).
- Comments only when they resolve ambiguity.

## Simplicity and Dependencies

- Keep functions simple, minimize dependencies, prefer standard library.
- Avoid over-engineering.

## Code Quality

- Testing: pytest in `tests/`
- Type hints on public API
- Google-style docstrings
- Linting: ruff, mypy

## Integration

- clicommands is an installed package: `from clicommands.helpers import ...`
- Standard imports (no path manipulation)

## Configuration and Secrets

- Never hardcode secrets. Use environment variables or config files.

## Versioning

- Semantic Versioning (SemVer).
