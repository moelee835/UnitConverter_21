"""Golden Master helpers — fixed contract format (reference: golden-master/reference.md)."""

from __future__ import annotations

import difflib
import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).resolve().parent / "golden"


def format_contract_output(
    *,
    input_raw: str,
    status: str,
    error: str,
    output_lines: list[str],
    canonical_from: str | None = None,
    canonical_to: str | None = None,
    hint: str | None = None,
) -> str:
    parts = [
        f"input: {input_raw}",
        f"status: {status}",
        f"error: {error}",
        "lines:",
        *output_lines,
        f"line_count: {len(output_lines)}",
    ]
    if canonical_from is not None:
        parts.append(f"canonical_from: {canonical_from}")
    if canonical_to is not None:
        parts.append(f"canonical_to: {canonical_to}")
    if hint is not None:
        parts.append(f"hint: {hint}")
    return "\n".join(parts) + "\n"


def assert_matches_golden(actual: str, relative: str) -> None:
    golden_path = GOLDEN_DIR / relative
    if os.environ.get("UPDATE_GOLDEN") == "1":
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(actual, encoding="utf-8", newline="\n")
        return

    if not golden_path.exists():
        raise AssertionError(
            f"Golden file missing: {golden_path}. Run with UPDATE_GOLDEN=1 first."
        )

    expected = golden_path.read_text(encoding="utf-8")
    if expected == actual:
        return

    diff = difflib.unified_diff(
        expected.splitlines(keepends=True),
        actual.splitlines(keepends=True),
        fromfile=f"golden/{relative}",
        tofile="actual",
    )
    raise AssertionError("Golden mismatch:\n" + "".join(diff))
