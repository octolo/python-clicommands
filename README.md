# clicommands

Lightweight Python library for managing command-line commands with automatic discovery.

## Features

- **Automatic command discovery** via `commands/` directory or `.commands.json`
- **Two ways to define commands**: function suffixed with `_command` or `Command` class
- **Argument parsing API**: `classify_args`, `parse_args_from_config`
- **Envfile loading**: `ENVFILE_PATH` support for loading `.env`
- **Built-in commands**: `version`, `copy`, `varenv`

## Installation

```bash
pip install clicommands
```

## Quick Start

1. Create a `cli.py` in your package:

```python
import sys
from pathlib import Path
from clicommands.helpers import cli_main

def main(argv=None):
    cli_file_path = Path(__file__)
    result = cli_main(cli_file_path, argv)
    return int(result) if isinstance(result, (int, bool)) else (0 if result else 1)

if __name__ == "__main__":
    sys.exit(main())
```

2. Add a `commands/` directory with your commands:

```python
# commands/hello.py
def hello_command(args: list[str]) -> bool:
    """Say hello."""
    print("Hello, world!")
    return True
```

3. Run: `python -m mypackage.cli hello`

## .commands.json Configuration

```json
{
  "packages": ["other_package"],
  "directories": ["commands"],
  "commands": []
}
```

- `packages`: Packages to import commands from
- `directories`: Paths to command directories
- `commands`: Additional commands

## CI

CI runs the Python test matrix, Ruff, Bandit (medium/high confidence and
severity), runtime dependency advisories, and package builds.

## Documentation

- `docs/purpose.md` — Purpose and use cases
- `docs/structure.md` — Project organization
- `docs/development.md` — Development guidelines
- `docs/AI.md` — AI assistant contract

## Local audit

Install the project's development/test dependencies (including both local
packages where applicable), plus the audit tools:

```bash
python -m pip install ruff mypy bandit pip-audit vulture radon xenon pytest pytest-django pytest-cov build twine
make audit
```

Use the activated environment's Python, or pass `make audit PYTHON=/path/to/python`.
On systems without Make, run `python scripts/audit.py` directly. Git is required;
the geoaddress widget tests also require Node.js. The audit reports missing test
suites and runs all available checks even when earlier checks fail.
Xenon checks the absolute C, module B, and average A complexity thresholds. Existing
lint, typing, security, dependency, or test findings can make the audit fail.
CI also runs this audit as a non-blocking job and separately reports Radon maintainability without imposing a threshold.
