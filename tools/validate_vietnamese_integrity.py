#!/usr/bin/env python3
"""Validate Vietnamese text integrity in an Anno fixture.

Walks the JSON tree and reports:
  - any string containing the Unicode replacement char U+FFFD (binary corruption)
  - any string key ending in `_vi` that is empty or whitespace-only

Also prints the total entry count and the date range for convenience.

Exit code 0 if clean, 1 if any problem is found.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def collect(node, path, problems):
    """Recursively walk node, recording problems with their JSON path."""
    if isinstance(node, dict):
        for key, value in node.items():
            child_path = f"{path}.{key}" if path else key
            if isinstance(value, str):
                if "\uFFFD" in value:
                    problems.append((child_path, "contains U+FFFD (corrupted)", value))
                if key.endswith("_vi") and not value.strip():
                    problems.append((child_path, "empty/whitespace _vi", value))
            else:
                collect(value, child_path, problems)
    elif isinstance(node, list):
        for idx, item in enumerate(node):
            collect(item, f"{path}[{idx}]", problems)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Vietnamese text integrity in an Anno fixture.")
    parser.add_argument(
        "--fixture",
        default="Anno/Resources/anno_unified_2026.json",
        help="Path to the fixture JSON (default: Anno/Resources/anno_unified_2026.json)",
    )
    args = parser.parse_args()

    fixture_path = Path(args.fixture)
    if not fixture_path.exists():
        print(f"ERROR: fixture not found: {fixture_path}", file=sys.stderr)
        return 1

    with open(fixture_path, encoding="utf-8") as f:
        data = json.load(f)

    problems = []
    collect(data, "", problems)

    # Entry count + date range
    if isinstance(data, dict) and isinstance(data.get("entries"), list):
        entries = data["entries"]
    elif isinstance(data, list):
        entries = data
    else:
        entries = []
    dates = [e.get("date", "") for e in entries if isinstance(e, dict) and e.get("date")]
    entry_count = len(entries)
    date_min = min(dates) if dates else "n/a"
    date_max = max(dates) if dates else "n/a"

    print(f"Fixture:        {fixture_path}")
    print(f"Total entries:  {entry_count}")
    print(f"Date range:     {date_min} -> {date_max}")
    print(f"Problems found: {len(problems)}")

    for ppath, kind, _val in problems:
        print(f"  [{kind}] {ppath}")

    if problems:
        print("RESULT: FAIL")
        return 1
    print("RESULT: CLEAN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
