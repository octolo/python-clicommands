#!/usr/bin/env python3
"""CLI service for running library CLI commands."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from typing import NotRequired, TypedDict

    class CommandInfo(TypedDict):
        """Command func + description."""

        func: Callable[[list[str]], bool]
        description: str
        inherit: NotRequired[bool]
else:
    from typing import NotRequired, TypedDict

    class CommandInfo(TypedDict):
        """Command func + description."""

        func: Callable[[list[str]], bool]
        description: str
        inherit: NotRequired[bool]


_CLI_CONTEXT: dict[str, Path | None] = {"cli_file_path": None}  # CLI context


def _find_cli_path_from_caller() -> Path | None:
    """Detect cli.py path from caller stack."""
    import inspect

    frame = inspect.currentframe()
    clicommands_cli_path = Path(__file__).resolve()
    for _ in range(20):
        if not frame:
            break
        frame = frame.f_back
        if frame:
            frame_file = frame.f_globals.get("__file__")
            if frame_file:
                frame_path = Path(frame_file).resolve()
                if "cli.py" in frame_file and frame_path != clicommands_cli_path:
                    return frame_path
    return None


def _get_package_name_from_path(
    cli_file_path: Path, package_name: str | None = None
) -> str:
    """Deduce package name from cli path or explicit package_name."""
    if package_name:
        return package_name.split(".")[0]

    try:
        parent_dir = cli_file_path.parent.name
        if parent_dir and parent_dir != "cli.py":
            return parent_dir
        parent_parent = cli_file_path.parent.parent.name
        if parent_parent:
            return parent_parent
    except Exception:  # nosec B110
        pass

    return cli_file_path.parent.name if cli_file_path.parent.name else "unknown"


def _get_command_class(base_package: str):
    """Resolve Command class from package or clicommands fallback."""
    import importlib

    try:
        base_module = importlib.import_module(  # nosec B307 # nosemgrep
            f"{base_package}.commands.base"
        )
        return base_module.Command
    except (ImportError, AttributeError):
        try:
            from clicommands.commands.base import Command
            return Command
        except ImportError:
            return None


def _first_line(text: str) -> str:
    """First line of text, stripped."""
    return text.split("\n")[0].strip() if text else ""


def _discover_from_module(module, Command) -> dict[str, CommandInfo]:
    """Discover commands from a single module (functions + Command instances)."""
    import inspect

    result: dict[str, CommandInfo] = {}

    for name, obj in inspect.getmembers(module, inspect.isfunction):
        if name.endswith("_command") and not name.startswith("_"):
            desc = _first_line(inspect.getdoc(obj) or "")
            result[name[:-8]] = {
                "func": obj,
                "description": desc,
                "inherit": True,
            }

    if Command:
        for name, obj in inspect.getmembers(module):
            if not isinstance(obj, Command) or name.startswith("_"):
                continue
            if name.endswith("_command"):
                cmd_name = name[:-8]
            elif name.endswith("Command"):
                cmd_name = name[:-7].lower()
            else:
                cmd_name = name.lower()
            desc = obj.description or _first_line(inspect.getdoc(obj) or "")
            result[cmd_name] = {
                "func": obj,
                "description": desc,
                "inherit": getattr(obj, "inherit", True),
            }
    return result


def _discover_from_path(
    commands_path: Path, package_name: str
) -> dict[str, CommandInfo]:
    """Discover commands from a directory."""
    import importlib

    result: dict[str, CommandInfo] = {}
    if not commands_path.exists():
        return result

    base_package = (
        package_name.rsplit(".", 1)[0] if "." in package_name else package_name
    )
    Command = _get_command_class(base_package)

    for py_file in commands_path.glob("*.py"):
        if py_file.stem == "__init__":
            continue
        module = importlib.import_module(  # nosec B307 # nosemgrep
            f"{base_package}.commands.{py_file.stem}"
        )
        result.update(_discover_from_module(module, Command))

    return result


def _discover_from_package(package: str) -> dict[str, CommandInfo]:
    """Discover commands from a package."""
    import importlib

    try:
        commands_module = importlib.import_module(  # nosec B307 # nosemgrep
            f"{package}.commands"
        )
        commands_path = (
            Path(commands_module.__file__).parent
            if commands_module.__file__
            else Path()
        )
        package_name = (
            commands_module.__package__
            if hasattr(commands_module, "__package__")
            else package
        )
        return _discover_from_path(commands_path, package_name or package)
    except ImportError:
        return {}


def _discover_from_command(command: str | dict) -> dict[str, CommandInfo]:
    """Discover a single command from config."""
    if isinstance(command, str):
        return _discover_from_package(command)
    return {}


def _find_config_file(cli_file_path: Path) -> Path | None:
    """Locate .commands.json (cwd first, then cli parent)."""
    config = Path(".commands.json")
    if config.exists():
        return config
    config = cli_file_path.parent / ".commands.json"
    return config if config.exists() else None


def _discover_from_config(
    config: dict, config_dir: Path, package: str
) -> dict[str, CommandInfo]:
    """Discover commands from config (packages, directories, commands)."""
    result: dict[str, CommandInfo] = {}
    if "packages" in config:
        for pkg in config["packages"]:
            cmds = _discover_from_package(pkg)
            result.update({k: v for k, v in cmds.items() if v.get("inherit", True)})
    if "directories" in config:
        for directory in config["directories"]:
            path = config_dir / directory if not Path(directory).is_absolute() else Path(directory)
            result.update(_discover_from_path(path, package))
    if "commands" in config:
        for command in config["commands"]:
            result.update(_discover_from_command(command))
    return result


def discover_commands(
    cli_file_path: Path,
    package_name: str | None = None,
    _commands_dir: str | Path | None = None,
) -> dict[str, CommandInfo]:
    """Discover commands via config or commands dir."""
    import json

    package = package_name or _get_package_name_from_path(cli_file_path)
    config_file = _find_config_file(cli_file_path)

    if config_file:
        with open(config_file, encoding="utf-8") as f:
            result = _discover_from_config(json.load(f), config_file.parent.resolve(), package)
    else:
        result = {}

    if not result:
        fallback = cli_file_path.parent / "commands"
        if fallback.exists():
            result.update(_discover_from_path(fallback, package))

    return result


def _discover_commands(cli_file_path: Path | None = None) -> dict[str, CommandInfo]:
    """Discover commands, auto-detect cli path if None."""
    if cli_file_path is None:
        cli_file_path = _find_cli_path_from_caller()
        if cli_file_path is None:
            raise ValueError("Could not detect cli_file_path automatically")
    return discover_commands(cli_file_path)


def load_envfile_from_path(env_path: Path, project_root: Path) -> None:
    """Load .env file into os.environ. Path is relative to project_root if not absolute."""
    import os

    path = env_path if env_path.is_absolute() else project_root / env_path
    if not path.exists():
        return
    try:
        from dotenv import load_dotenv
        load_dotenv(path, override=False)
    except ImportError:
        # Minimal fallback: parse KEY=VALUE lines
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, val = line.partition("=")
                    key = key.strip()
                    if key and key not in os.environ:
                        os.environ[key] = val.strip().strip('"').strip("'")


def _load_envfile() -> None:
    """Load envfile from ENVFILE_PATH if set."""
    import os

    path = os.environ.get("ENVFILE_PATH")
    if not path:
        return
    try:
        load_envfile_from_path(Path(path), Path.cwd())
    except (OSError, Exception):
        pass


def _print_usage_content(package_name: str, commands: dict[str, CommandInfo]) -> None:
    """Print usage and available commands."""
    print(f"Usage: {package_name} <command> [args...]")
    print("\nCommands:")
    for cmd_name, cmd_info in sorted(commands.items()):
        print(f"  {cmd_name:<12} {cmd_info['description']}")
    print("\nExamples:")
    for cmd_name in list(commands.keys())[:3]:
        print(f"  {package_name} {cmd_name}")


def _print_usage(package_name: str, commands: dict[str, CommandInfo]) -> int:
    """Print usage and available commands. Returns 1."""
    _print_usage_content(package_name, commands)
    return 1


def _run_command(
    cmd_func: object, cmd_args: list[str], command: str
) -> int:
    """Execute command, return exit code. Handles exceptions."""
    from typing import cast

    if isinstance(cmd_func, str):
        print(f"Invalid command function for '{command}'", file=sys.stderr)
        return 1
    func = cast("Callable[[list[str]], bool]", cmd_func)
    try:
        return 0 if func(cmd_args) else 1
    except Exception as exc:
        print(f"Error executing command '{command}': {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def cli_main(
    cli_file_path: Path, argv: Sequence[str] | None = None
) -> int:
    """Entry point: run discovered command, return exit code."""
    _CLI_CONTEXT["cli_file_path"] = cli_file_path

    _load_envfile()

    args = list(argv if argv is not None else sys.argv[1:])
    commands = discover_commands(cli_file_path)

    if not args:
        return _print_usage(_get_package_name_from_path(cli_file_path), commands)

    command = args[0].lower()
    if command in commands:
        return _run_command(
            commands[command]["func"],
            args[1:] if len(args) > 1 else [],
            command,
        )

    print(f"Unknown command: {command}", file=sys.stderr)
    print(f"Available commands: {', '.join(sorted(commands.keys()))}")
    return 1


def main() -> int:
    """Entry point for clicommands CLI."""
    cli_file_path = Path(__file__)
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    return cli_main(cli_file_path, args)


if __name__ == "__main__":
    sys.exit(main())
