"""Version command."""

from __future__ import annotations

from clicommands.helpers import _CLI_CONTEXT, _get_package_name_from_path

from .base import Command


def _version_command(_args: list[str]) -> bool:
    """Show version information."""
    cli_path = _CLI_CONTEXT.get("cli_file_path")
    package_name = _get_package_name_from_path(cli_path) if cli_path else "unknown"

    try:
        package_module = __import__(package_name, fromlist=["__version__"])
        version = getattr(package_module, "__version__", "unknown")
        print(f"{package_name} version {version}")
        return True
    except ImportError:
        print(f"{package_name} version unknown")
        return False


version_command = Command(_version_command, "Show version information")
