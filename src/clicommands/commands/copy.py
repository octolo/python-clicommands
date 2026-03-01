"""Copy Python file command."""

from __future__ import annotations

import shutil
from pathlib import Path

from clicommands.commands.base import Command
from clicommands.utils import print_info, print_warning


_COPY_PY = {
    "cli": "cli.py:cli.py",
    "django": "manage.py:templates/django.py",
    "django_ngrok": "manage.py:templates/django_ngrok.py",
}


def _copy_command(args: list[str]) -> bool:
    """Copy template file. Usage: copy <key> [dest_dir]."""
    if not args:
        print_info("Usage: copy <key> [dest_dir]")
        print_info("\nAvailable:")
        for key, spec in sorted(_COPY_PY.items()):
            dest_name = spec.split(":")[0] if ":" in spec else spec
            print_info(f"  {key:<12} -> {dest_name}")
        return False

    key = args[0]
    dest_dir = Path(args[1]) if len(args) > 1 else Path.cwd()

    if key not in _COPY_PY:
        print_warning(f"Unknown key: {key}. Available: {', '.join(_COPY_PY)}")
        return False

    spec = _COPY_PY[key]
    parts = spec.split(":")
    if len(parts) != 2:
        print_warning(f"Invalid spec for {key}")
        return False

    dest_filename, source_path = parts[0], parts[1]

    pkg_dir = Path(__file__).resolve().parent.parent
    source = pkg_dir / source_path
    dest = dest_dir.resolve() / dest_filename

    if not source.exists():
        print_warning(f"Source not found: {source}")
        return False

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(source, dest)
    print_info(f"Copied {source_path} -> {dest}")
    return True


copy_command = Command(_copy_command, "Copy python file", inherit=False)
