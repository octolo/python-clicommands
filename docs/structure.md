# Project Structure

```
python-clicommands/
├── src/clicommands/
│   ├── __init__.py
│   ├── cli.py              # CLI entry point
│   ├── helpers.py          # Discovery and execution
│   ├── commands/           # Built-in commands (base, args, version, copy, varenv)
│   ├── templates/          # CLI templates (django, django_ngrok)
│   └── .commands.json      # Command configuration
├── tests/
├── docs/
├── pyproject.toml
└── README.md
```

### Key Files

- `helpers.py`: `discover_commands`, `cli_main`, `load_envfile_from_path`
- `commands/base.py`: `Command` class
- `commands/args.py`: `classify_args`, `parse_args_from_config`
