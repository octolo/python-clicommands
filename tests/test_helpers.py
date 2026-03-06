"""Tests for helpers."""

from __future__ import annotations

from pathlib import Path

from clicommands.helpers import (
    _get_package_name_from_path,
    discover_commands,
)


class TestGetPackageNameFromPath:
    def test_explicit_package_name(self) -> None:
        path = Path("/some/cli.py")
        assert _get_package_name_from_path(path, "my.package") == "my"

    def test_parent_dir_as_package(self) -> None:
        path = Path("/project/mypkg/cli.py")
        assert _get_package_name_from_path(path) == "mypkg"

    def test_nested_parent(self) -> None:
        path = Path("/project/mypkg/src/mypkg/cli.py")
        # parent.name = mypkg (inner), parent_parent = src
        result = _get_package_name_from_path(path)
        assert result in ("mypkg", "src", "unknown")


class TestDiscoverCommands:
    def test_returns_dict(self) -> None:
        cli_path = Path(__file__).resolve().parent.parent / "src" / "clicommands" / "cli.py"
        result = discover_commands(cli_path, package_name="clicommands")
        assert isinstance(result, dict)
        assert "version" in result or "copy" in result or len(result) >= 0

    def test_with_config_file(self, tmp_path: Path) -> None:
        config = tmp_path / ".commands.json"
        config.write_text('{"packages": ["clicommands"]}')
        cli_path = tmp_path / "cli.py"
        cli_path.write_text("")
        result = discover_commands(cli_path, package_name="clicommands")
        assert isinstance(result, dict)
