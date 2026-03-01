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

## Documentation

- `docs/purpose.md` — Purpose and use cases
- `docs/structure.md` — Project organization
- `docs/development.md` — Development guidelines
- `docs/AI.md` — AI assistant contract
