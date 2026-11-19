#!/usr/bin/env python3
"""Fail-closed freshness/coverage gate for Anno unified fixtures.

Asserts that a committed fixture covers exactly the researched dates in its declared
window, matches root Engine A on all five Swift calendar fields, has >=2 sources per
entry, and satisfies the Swift AnnoEntry decode contract.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "data" / "research_results"
# 2026 is intentionally the Jul 3 - Dec 31 v1 production window; 2027 now covers the full year.
EXPECTED_WINDOWS = {
    2026: ("2026-07-03", "2026-12-31"),
    2027: ("2027-01-01", "2027-12-31"),
}
CALENDAR_FIELDS = ("julian", "hebrew", "islamic_umm_al_qura", "coptic", "ethiopian")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def research_dates(year: int) -> set[str]:
    pattern = re.compile(rf"^{year}-\d{{2}}-\d{{2}}_result(?:_en|_auto)?\.json$")
    return {
        p.name[:10]
        for p in RESEARCH.iterdir()
        if p.is_file() and pattern.match(p.name)
    }


def mock_dates_2026() -> set[str]:
    """The 2026 fixture also layers the committed fortnight and August mock tracks."""
    dates: set[str] = set()
    for name in (
        "anno_fortnight_2026-07-03_2026-07-16.json",
        "anno_august_2026.json",
    ):
        path = ROOT / "data" / "mock" / name
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        entries = data.get("entries", []) if isinstance(data, dict) else data
        dates.update(e["date"] for e in entries if isinstance(e, dict) and "date" in e)
    return dates


def main() -> None:
    parser = argparse.ArgumentParser(description="Check one Anno fixture against its research corpus")
    parser.add_argument("--year", type=int, required=True, choices=(2026, 2027))
    parser.add_argument("--fixture", type=Path, default=None)
    args = parser.parse_args()

    year = args.year
    fixture = args.fixture or ROOT / f"Anno/Resources/anno_unified_{year}.json"
    expected_start, expected_end = EXPECTED_WINDOWS[year]
    errors: list[str] = []

    try:
        data = json.loads(fixture.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FRESHNESS FAILED - cannot read {fixture}: {exc}", file=sys.stderr)
        raise SystemExit(1)

    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        print("FRESHNESS FAILED - entries missing or empty", file=sys.stderr)
        raise SystemExit(1)

    fixture_dates = [e.get("date") for e in entries if isinstance(e, dict)]
    if len(fixture_dates) != len(set(fixture_dates)):
        errors.append("fixture contains duplicate dates")

    observed_min, observed_max = min(fixture_dates), max(fixture_dates)
    if (observed_min, observed_max) != (expected_start, expected_end):
        errors.append(
            f"date range {observed_min}..{observed_max} != expected {expected_start}..{expected_end}"
        )

    source_dates = research_dates(year)
    if year == 2026:
        source_dates |= mock_dates_2026()
    expected = {
        d for d in source_dates
        if expected_start <= d <= expected_end
    }
    actual = set(fixture_dates)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        errors.append(f"{len(missing)} researched dates missing from fixture: {missing[:10]}")
    if extra:
        errors.append(f"{len(extra)} fixture dates have no research file: {extra[:10]}")

    contract = load_module(
        "validate_fixture_decode", ROOT / "tools" / "validate_fixture_decode.py"
    )
    contract_issues = contract.validate_fixture(data)
    if contract_issues:
        errors.append(f"{len(contract_issues)} Swift decode contract violations: {contract_issues[:10]}")

    engine = load_module("calendar_engine", ROOT / "calendar_engine.py")
    for entry in entries:
        day = entry.get("date", "?")
        try:
            converted = engine.convert_date(date.fromisoformat(day))
        except (ValueError, TypeError):
            errors.append(f"{day}: unparsable date")
            continue
        for field in CALENDAR_FIELDS:
            expected_value = converted[field]["date"]
            actual_value = entry.get("calendars", {}).get(field)
            if actual_value != expected_value:
                errors.append(f"{day}: calendars.{field}={actual_value!r}, engine={expected_value!r}")
        if len(entry.get("sources", [])) < 2:
            errors.append(f"{day}: fewer than 2 sources")

    if errors:
        print(f"FRESHNESS FAILED - {fixture}: {len(errors)} issue(s)", file=sys.stderr)
        for message in errors[:60]:
            print(f"  {message}", file=sys.stderr)
        raise SystemExit(1)

    print(f"Fixture freshness OK: {year} {len(entries)} entries {observed_min} -> {observed_max}")


if __name__ == "__main__":
    main()
