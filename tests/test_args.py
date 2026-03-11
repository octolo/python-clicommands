"""Tests for commands.args."""

from __future__ import annotations

from clicommands.commands.args import classify_args, create_parser_from_config, parse_args_from_config


class TestClassifyArgs:
    def test_empty(self) -> None:
        assert classify_args([]) == {"args": [], "kwargs": {}}

    def test_positional_only(self) -> None:
        assert classify_args(["a", "b"]) == {"args": ["a", "b"], "kwargs": {}}

    def test_kwargs_only(self) -> None:
        assert classify_args(["x=1", "y=2"]) == {"args": [], "kwargs": {"x": "1", "y": "2"}}

    def test_mixed(self) -> None:
        assert classify_args(["a", "x=1", "b"]) == {
            "args": ["a", "b"],
            "kwargs": {"x": "1"},
        }

    def test_value_with_equals(self) -> None:
        assert classify_args(["key=val=ue"]) == {"args": [], "kwargs": {"key": "val=ue"}}


class TestCreateParserFromConfig:
    def test_store_true(self) -> None:
        config = {"flag": {"type": "store_true"}}
        parser = create_parser_from_config(config)
        parsed = parser.parse_args(["--flag"])
        assert parsed.flag is True

    def test_string_default(self) -> None:
        config = {"mode": {"type": str, "default": "lint"}}
        parser = create_parser_from_config(config)
        parsed = parser.parse_args([])
        assert parsed.mode == "lint"


class TestParseArgsFromConfig:
    def test_empty_config(self) -> None:
        result = parse_args_from_config([], {})
        assert result.get("args") == []

    def test_positionals_in_unknown(self) -> None:
        config = {"mode": {"type": str, "default": "lint"}}
        result = parse_args_from_config(["dir1", "dir2"], config)
        assert result["args"] == ["dir1", "dir2"]
        assert result["mode"] == "lint"

    def test_parsed_option_with_positionals(self) -> None:
        config = {"mode": {"type": str, "default": "lint"}}
        result = parse_args_from_config(["--mode", "cleanup", "src"], config)
        assert result.get("mode") == "cleanup"
        assert result.get("args") == ["src"]
