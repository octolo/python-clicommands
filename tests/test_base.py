"""Tests for commands.base."""

from __future__ import annotations

from clicommands.commands.base import Command


def _dummy_command(args: list[str]) -> bool:
    """Dummy command for testing."""
    return len(args) == 0


def _failing_command(_args: list[str]) -> bool:
    """Always fails."""
    return False


class TestCommand:
    def test_init_description_explicit(self) -> None:
        cmd = Command(_dummy_command, description="Explicit desc")
        assert cmd.description == "Explicit desc"
        assert cmd.inherit is True

    def test_init_description_from_docstring(self) -> None:
        cmd = Command(_dummy_command)
        assert "Dummy command" in cmd.description

    def test_init_inherit_false(self) -> None:
        cmd = Command(_dummy_command, inherit=False)
        assert cmd.inherit is False

    def test_call_returns_func_result(self) -> None:
        cmd = Command(_dummy_command)
        assert cmd([]) is True
        assert cmd(["x"]) is False

    def test_call_failing(self) -> None:
        cmd = Command(_failing_command)
        assert cmd([]) is False
