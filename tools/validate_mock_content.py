#!/usr/bin/env python3
"""Validate Anno mock content fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORTNIGHT = ROOT / "data/mock/anno_fortnight_2026-07-03_2026-07-16.json"
WEEK = ROOT / "data/mock/anno_week_2026-07-03_2026-07-09.json"
CLEARANCE = ROOT / "data/assets/artwork_clearance_queue_2026-07-03_2026-07-16.json"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def require(value: object, message: str) -> None:
    if not value:
        fail(message)


def main() -> None:
    fortnight = json.loads(FORTNIGHT.read_text())
    week = json.loads(WEEK.read_text())
    entries = fortnight.get("entries", [])
    require(len(entries) == 14, f"expected 14 fortnight entries, found {len(entries)}")

    ids = {entry.get("id") for entry in entries}
    require(len(ids) == len(entries), "entry ids must be unique")

    for entry in entries:
        eid = entry.get("id", "<missing>")
        require(entry.get("date"), f"{eid}: missing date")
        require(entry.get("liturgical", {}).get("title_en"), f"{eid}: missing English liturgical title")
        require(entry.get("liturgical", {}).get("title_vi"), f"{eid}: missing Vietnamese liturgical title")
        require(entry.get("primary", {}).get("summary_en"), f"{eid}: missing English summary")
        require(entry.get("primary", {}).get("summary_vi"), f"{eid}: missing Vietnamese summary")
        require(entry.get("primary", {}).get("confidence") in {"confirmed", "traditional", "disputed"}, f"{eid}: invalid confidence")
        require(len(entry.get("sources", [])) >= 2, f"{eid}: expected at least two sources")
        calendars = entry.get("calendars", {})
        for key in ("julian", "hebrew", "islamic_umm_al_qura", "coptic", "ethiopian"):
            require(calendars.get(key), f"{eid}: missing calendar conversion {key}")
        hooks = entry.get("app_hooks", {})
        require(hooks.get("hero_line_en") and hooks.get("hero_line_vi"), f"{eid}: missing bilingual hero line")

    week_ids = week.get("entry_ids", [])
    require(len(week_ids) == 7, f"expected 7 week entries, found {len(week_ids)}")
    missing = [eid for eid in week_ids if eid not in ids]
    require(not missing, f"week file references missing ids: {missing}")

    if CLEARANCE.exists():
        clearance = json.loads(CLEARANCE.read_text())
        clearance_items = clearance.get("items", [])
        clearance_ids = {item.get("entry_id") for item in clearance_items}
        require(len(clearance_items) == len(entries), "clearance queue must have one item per entry")
        require(clearance_ids == ids, "clearance queue entry ids must match fixture ids")
        require(
            clearance.get("summary", {}).get("total_items") == len(entries),
            "clearance summary total_items must match fixture entry count",
        )

    print("OK: 14 fortnight entries, 7 week entries, bilingual copy, calendars, sources, and clearance coverage validated.")


if __name__ == "__main__":
    main()
