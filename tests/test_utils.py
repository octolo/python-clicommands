"""Tests for utils."""

from __future__ import annotations

import pytest

from clicommands.utils import format_tabulate, format_results_json, snake_to_camel, summarize_results


class TestFormatTabulate:
    def test_empty_data(self) -> None:
        assert format_tabulate([]) == "No data available."
        assert format_tabulate({}) == "No data available."

    def test_list_of_dicts(self) -> None:
        result = format_tabulate([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
        assert "a" in result and "b" in result
        assert "1" in result and "3" in result

    def test_dict_format(self) -> None:
        result = format_tabulate({"k1": {"x": 1}, "k2": "v2"})
        assert "key" in result
        assert "k1" in result


class TestSnakeToCamel:
    def test_simple(self) -> None:
        assert snake_to_camel("hello_world") == "HelloWorld"

    def test_single_word(self) -> None:
        assert snake_to_camel("hello") == "Hello"

    def test_empty(self) -> None:
        assert snake_to_camel("") == ""


class TestFormatResultsJson:
    def test_empty(self) -> None:
        assert format_results_json({}) == "{}"

    def test_bool_results(self) -> None:
        result = format_results_json({"ruff": True, "mypy": False})
        assert '"ruff"' in result
        assert '"mypy"' in result
        assert "true" in result and "false" in result


class TestSummarizeResults:
    def test_empty(self) -> None:
        out = summarize_results({})
        assert out["total"] == 0
        assert out["passed"] == 0
        assert out["failed"] == 0
        assert out["success_rate"] == 0

    def test_mixed(self) -> None:
        out = summarize_results({"a": True, "b": False, "c": True})
        assert out["total"] == 3
        assert out["passed"] == 2
        assert out["failed"] == 1
        assert out["success_rate"] == pytest.approx(66.67, rel=0.01)
