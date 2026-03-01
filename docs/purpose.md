# Project Purpose

**clicommands** is a lightweight Python library for managing command-line commands with automatic discovery.

## Features

1. **Command discovery** — Via `commands/` directory or `.commands.json` (packages, directories, commands)
2. **Command definition** — Functions `*_command` or `Command` class, signature `(args: list[str]) -> bool`
3. **Utilities** — `classify_args`, `parse_args_from_config`, `.env` loading via `ENVFILE_PATH`
4. **Built-in commands** — version, copy, varenv

## Architecture

- Entry point via `cli_main(cli_file_path, argv)` in consumer packages
- Discovery by convention (`commands/`) or configuration (`.commands.json`)

## Use Cases

- Expose development tools as CLI
- Maintenance or administration scripts
- Base for complex CLIs (e.g. qualitybase, providerkit)
