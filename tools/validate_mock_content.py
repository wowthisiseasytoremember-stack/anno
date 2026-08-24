#!/usr/bin/env python3
"""Validate Anno mock content fixtures and unified datasets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FORTNIGHT = ROOT / "data/mock/anno_fortnight_2026-07-03_2026-07-16.json"
WEEK = ROOT / "data/mock/anno_week_2026-07-03_2026-07-09.json"
CLEARANCE = ROOT / "data/assets/artwork_clearance_queue_2026-07-03_2026-07-16.json"

VALID_CONFIDENCE = {"confirmed", "traditional", "disputed", "contextual"}
VALID_SOURCE_TYPES = {
    "liturgical_calendar",
    "vatican",
    "encyclopedia",
    "academic",
    "news",
    "devotional",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def require(value: object, message: str) -> None:
    if not value:
        fail(message)


def validate_entry(entry: dict[str, Any], index: int | str = "") -> None:
    eid = entry.get("id", f"<entry #{index}>")

    require(entry.get("id"), f"{eid}: missing id")
    require(entry.get("date"), f"{eid}: missing date")

    # Liturgical
    lit = entry.get("liturgical", {})
    require(isinstance(lit, dict), f"{eid}: 'liturgical' must be an object")
    require(lit.get("title_en"), f"{eid}: missing English liturgical title (liturgical.title_en)")
    require(lit.get("title_vi"), f"{eid}: missing Vietnamese liturgical title (liturgical.title_vi)")

    # Primary
    pri = entry.get("primary", {})
    require(isinstance(pri, dict), f"{eid}: 'primary' must be an object")
    require(pri.get("summary_en"), f"{eid}: missing English summary (primary.summary_en)")
    require(pri.get("summary_vi"), f"{eid}: missing Vietnamese summary (primary.summary_vi)")
    require(
        pri.get("confidence") in VALID_CONFIDENCE,
        f"{eid}: invalid confidence '{pri.get('confidence')}', expected one of {VALID_CONFIDENCE}",
    )

    # Sources
    sources = entry.get("sources")
    require(isinstance(sources, list), f"{eid}: 'sources' must be a list")
    require(len(sources) >= 2, f"{eid}: expected at least 2 sources, found {len(sources)}")
    for i, src in enumerate(sources):
        require(isinstance(src, dict), f"{eid}: source #{i} must be an object, got {type(src).__name__}")
        require(src.get("label"), f"{eid}: source #{i} missing 'label'")
        url = src.get("url", "")
        require(url, f"{eid}: source #{i} missing 'url'")
        require("example.com" not in url, f"{eid}: source #{i} uses invalid placeholder URL '{url}'")
        stype = src.get("type", "")
        require(
            stype in VALID_SOURCE_TYPES,
            f"{eid}: source #{i} has invalid type '{stype}', expected one of {sorted(VALID_SOURCE_TYPES)}",
        )

    # Calendars
    cals = entry.get("calendars", {})
    require(isinstance(cals, dict), f"{eid}: 'calendars' must be an object")
    for key in ("julian", "hebrew", "islamic_umm_al_qura", "coptic", "ethiopian"):
        require(cals.get(key), f"{eid}: missing calendar conversion '{key}'")

    # App Hooks
    hooks = entry.get("app_hooks", {})
    require(isinstance(hooks, dict), f"{eid}: 'app_hooks' must be an object")
    require(hooks.get("hero_line_en"), f"{eid}: missing English hero line (app_hooks.hero_line_en)")
    require(hooks.get("hero_line_vi"), f"{eid}: missing Vietnamese hero line (app_hooks.hero_line_vi)")


def validate_file(path: Path) -> None:
    if not path.exists():
        fail(f"file not found: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"failed to parse JSON from {path}: {e}")

    if isinstance(data, dict) and "entries" in data:
        entries = data["entries"]
    elif isinstance(data, list):
        entries = data
    elif isinstance(data, dict) and "id" in data:
        entries = [data]
    else:
        fail(f"{path}: unable to extract entries from JSON structure")

    require(len(entries) > 0, f"{path}: no entries found")

    ids = [entry.get("id") for entry in entries if isinstance(entry, dict)]
    require(len(ids) == len(entries), f"{path}: some entries missing 'id'")
    require(len(set(ids)) == len(ids), f"{path}: entry ids must be unique (found duplicates)")

    for idx, entry in enumerate(entries):
        if not isinstance(entry, dict):
            fail(f"{path}: entry #{idx} is not an object")
        validate_entry(entry, index=idx)

    print(f"OK: Validated {len(entries)} entries in {path}")


def validate_default() -> None:
    print("=== Validating Fortnight Fixture ===")
    fortnight = json.loads(FORTNIGHT.read_text(encoding="utf-8"))
    week = json.loads(WEEK.read_text(encoding="utf-8"))
    entries = fortnight.get("entries", [])
    require(len(entries) == 14, f"expected 14 fortnight entries, found {len(entries)}")

    ids = {entry.get("id") for entry in entries}
    require(len(ids) == len(entries), "entry ids must be unique")

    for idx, entry in enumerate(entries):
        validate_entry(entry, index=idx)

    week_ids = week.get("entry_ids", [])
    require(len(week_ids) == 7, f"expected 7 week entries, found {len(week_ids)}")
    missing = [eid for eid in week_ids if eid not in ids]
    require(not missing, f"week file references missing ids: {missing}")

    if CLEARANCE.exists():
        clearance = json.loads(CLEARANCE.read_text(encoding="utf-8"))
        clearance_items = clearance.get("items", [])
        clearance_ids = {item.get("entry_id") for item in clearance_items}
        require(len(clearance_items) == len(entries), "clearance queue must have one item per entry")
        require(clearance_ids == ids, f"clearance queue entry ids must match fixture ids: {clearance_ids ^ ids}")
        require(
            clearance.get("summary", {}).get("total_items") == len(entries),
            "clearance summary total_items must match fixture entry count",
        )

    print("OK: 14 fortnight entries, 7 week entries, bilingual copy, calendars, sources, and clearance coverage validated.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Anno mock content fixtures and datasets.")
    parser.add_argument(
        "target",
        nargs="?",
        default=None,
        help="Path to fixture JSON to validate. If omitted, validates default fortnight, week, and clearance queue.",
    )
    args = parser.parse_args()

    if args.target:
        target_path = Path(args.target)
        if not target_path.is_absolute():
            target_path = Path.cwd() / target_path
        validate_file(target_path)
    else:
        validate_default()


if __name__ == "__main__":
    main()
