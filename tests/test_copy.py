"""Tests for commands.copy."""

from __future__ import annotations

from pathlib import Path

import pytest

from clicommands.commands.copy import _copy_command


class TestCopyCommand:
    def test_no_args_returns_false(self, capsys: pytest.CaptureFixture[str]) -> None:
        assert _copy_command([]) is False
        out = capsys.readouterr()
        assert "Usage" in out.out or "Available" in out.out

    def test_unknown_key_returns_false(self, capsys: pytest.CaptureFixture[str]) -> None:
        assert _copy_command(["unknown_key"]) is False
        out = capsys.readouterr()
        assert "Unknown" in out.out or "unknown" in out.out.lower()

    def test_copy_cli(self, tmp_path: Path) -> None:
        result = _copy_command(["cli", str(tmp_path)])
        assert result is True
        dest = tmp_path / "cli.py"
        assert dest.exists()
        content = dest.read_text()
        assert "cli_main" in content or "main" in content

    def test_copy_django(self, tmp_path: Path) -> None:
        result = _copy_command(["django", str(tmp_path)])
        assert result is True
        dest = tmp_path / "manage.py"
        assert dest.exists()

    def test_copy_django_ngrok(self, tmp_path: Path) -> None:
        result = _copy_command(["django_ngrok", str(tmp_path)])
        assert result is True
        dest = tmp_path / "manage.py"
        assert dest.exists()
        content = dest.read_text()
        assert "ngrok" in content
