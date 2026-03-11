# AI Assistant Contract — clicommands

**This document is the reference for all AI work on this repository.**  
In case of conflict, this document prevails.

---

## Absolute Rules

- Follow this file exactly
- Do not invent services, commands, abstractions, or architectures
- Do not refactor without explicit request
- Do not manipulate `sys.path`
- Do not hardcode secrets
- Comments only to resolve ambiguity
- Minimal dependencies, prefer standard library

---

## Required Rules

- **Language**: English for code, docstrings, logs, errors, documentation
- **Simplicity**: Write the simplest possible code

---

## Overview (informational)

**clicommands** is a lightweight CLI framework with automatic command discovery.

### Architecture

- Discovery via `commands/` or `.commands.json`
- Entry point: `cli_main(cli_file_path, argv)`
- Commands: `(args: list[str]) -> bool`
- Built-in: version, copy, varenv

### Structure

```
python-clicommands/
├── src/clicommands/
│   ├── cli.py
│   ├── helpers.py
│   └── commands/
├── tests/
├── docs/
└── pyproject.toml
```

---

## Command Creation (required)

- Use `Command` class or function suffixed with `_command`
- Signature: `(args: list[str]) -> bool`

---

## Integration (absolute)

- clicommands is an installed package
- Imports: `from clicommands.helpers import ...`, `from clicommands.commands import ...`

---

## Anti-Hallucination (absolute)

If a request is not covered or requires assumptions: stop, explain, ask for clarification.

---

## Resources (informational)

- `docs/purpose.md`, `docs/structure.md`, `docs/development.md`
- `README.md` at project root
