#!/usr/bin/env python3
"""Utility functions for clicommands services."""

from __future__ import annotations

import json
import os
import platform
import sys
from typing import Any
from tabulate import tabulate  # type: ignore[import-untyped]

BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
NC = "\033[0m"

if platform.system() == "Windows" and not os.environ.get("ANSICON"):
    BLUE = GREEN = RED = YELLOW = CYAN = MAGENTA = NC = ""


def print_info(message: str) -> None:
    """Print an info message."""
    print(f"{BLUE}{message}{NC}")


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"{GREEN}{message}{NC}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"{RED}{message}{NC}", file=sys.stderr)


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"{YELLOW}{message}{NC}")


def print_header(message: str) -> None:
    """Print a header message."""
    print(f"{CYAN}{message}{NC}")


def print_separator(char: str = "=", length: int = 70) -> None:
    """Print a separator line."""
    print(char * length)


def format_results_table(
    results: dict[str, bool | dict[str, Any]],
    title: str | None = None,
    show_status: bool = True,
) -> str:
    """Format results as a table."""
    if not results:
        return "No results available."

    rows = []
    for tool, result in results.items():
        if isinstance(result, dict):
            status = result.get("status", False)
            details = result.get("details", "")
            errors = result.get("errors", 0)
            warnings = result.get("warnings", 0)
            if errors or warnings:
                details = f"Errors: {errors}, Warnings: {warnings}"
        else:
            status = bool(result)
            details = ""

        row_data = {"Tool": tool}
        if show_status:
            status_str = f"{GREEN}✓ PASS{NC}" if status else f"{RED}✗ FAIL{NC}"
            row_data["Status"] = status_str
        row_data["Details"] = details
        rows.append(row_data)

    table = format_tabulate(rows, empty_message="No results available.")

    if title:
        return f"\n{title}\n{'=' * 70}\n{table}"
    return table


def format_results_json(results: dict[str, bool | dict[str, Any]]) -> str:
    """Format results as JSON."""
    json_results = {}
    for tool, result in results.items():
        if isinstance(result, dict):
            json_results[tool] = result
        else:
            json_results[tool] = {"status": bool(result)}

    return json.dumps(json_results, indent=2)


def print_results(
    results: dict[str, bool | dict[str, Any]],
    title: str | None = None,
    fmt: str = "table",
    show_status: bool = True,
) -> None:
    """Print results in the specified format."""
    if fmt.lower() == "json":
        output = format_results_json(results)
        print(output)
    else:
        output = format_results_table(results, title=title, show_status=show_status)
        print(output)


def summarize_results(results: dict[str, bool | dict[str, Any]]) -> dict[str, Any]:
    """Summarize results into statistics."""
    total = len(results)
    passed = 0
    failed = 0
    total_errors = 0
    total_warnings = 0

    for _tool, result in results.items():
        if isinstance(result, dict):
            status = result.get("status", False)
            total_errors += result.get("errors", 0)
            total_warnings += result.get("warnings", 0)
        else:
            status = bool(result)

        if status:
            passed += 1
        else:
            failed += 1

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "success_rate": (passed / total * 100) if total > 0 else 0,
        "total_errors": total_errors,
        "total_warnings": total_warnings,
    }


def print_summary(summary: dict[str, Any]) -> None:
    """Print a summary of results."""
    print_separator()
    print_header("Summary")
    print_separator()
    print(f"Total tools: {summary['total']}")
    print(f"{GREEN}Passed: {summary['passed']}{NC}")
    print(f"{RED}Failed: {summary['failed']}{NC}")
    print(f"Success rate: {summary['success_rate']:.1f}%")
    if summary.get("total_errors", 0) > 0:
        print(f"{RED}Total errors: {summary['total_errors']}{NC}")
    if summary.get("total_warnings", 0) > 0:
        print(f"{YELLOW}Total warnings: {summary['total_warnings']}{NC}")
    print_separator()


def format_tabulate(
    data: dict[str, Any] | list[dict[str, Any]],
    empty_message: str = "No data available.",
) -> str:
    """Format data as a table using tabulate."""
    if not data:
        return empty_message

    if tabulate is None:
        raise ImportError("tabulate is required. Install it with: pip install tabulate")

    if isinstance(data, dict):
        rows = []
        for k, v in data.items():
            if isinstance(v, dict):
                rows.append({"key": k, **v})
            else:
                rows.append({"key": k, "value": v})
    else:
        rows = data

    if not rows:
        return empty_message

    result = tabulate(rows, headers="keys", tablefmt="grid")
    return str(result)  # type: ignore[no-any-return]


def snake_to_camel(snake_str):
    """Convert a snake string to a camel string."""
    return "".join(word.capitalize() for word in snake_str.split("_"))
