#!/usr/bin/env python3
"""
tools/merge_anno_full_year.py
Merges all Engine B dossiers from data/research_results into
Anno/Resources/anno_full_2026.json (replaces placeholder file).

Expects: research_results/{date}_result.json + {date}_result_vi.json for full coverage.
Output schema (matches anno_unified_2026.json):
  schema_version: "1.0"
  generated_on: ISO date
  total_entries: int
  entries: list of {date:..., primary:..., liturgical:..., calendars:..., place:..., artwork:..., sources:..., app_hooks:...}

NOTE: This merges Jan 1 - Jul 2, 2026 (183 days from batch_generate_engine_b_jan_jun.py).
For Jul 3 - Dec 31, 2026 (182 days), use anno_unified_2026.json directly.
"""

from __future__ import annotations

import json, os, sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data/research_results"
DEST = ROOT / "Anno/Resources/anno_full_2026.json"


def main() -> None:
    start = date(2026, 1, 1)
    end = date(2026, 12, 31)
    cur = start
    entries: list[dict] = []
    missing: list[str] = []
    by_month: dict[str, int] = {}

    while cur <= end:
        d_str = cur.isoformat()
        month_key = d_str[:7]
        en_path = OUT_DIR / f"{d_str}_result.json"

        if not en_path.exists() or en_path.stat().st_size < 100:
            missing.append(d_str)
            cur += timedelta(days=1)
            continue

        try:
            with open(en_path, "r", encoding="utf-8") as f:
                entry = json.load(f)
        except json.JSONDecodeError as e:
            print(f"  JSON error in {d_str}: {e}")
            missing.append(d_str)
            cur += timedelta(days=1)
            continue

        # Validate required fields
        required = ["id", "date", "weekday", "liturgical", "calendars", "primary", "sources", "app_hooks"]
        if not all(k in entry for k in required):
            print(f"  Missing fields in {d_str}: required={required}, found={list(entry.keys())}")
            missing.append(d_str)
            cur += timedelta(days=1)
            continue

        # Light schema validation
        for subkey in ("liturgical", "calendars", "primary"):
            if subkey not in entry:
                missing.append(d_str)
                break
        else:
            entries.append(entry)
            by_month[month_key] = by_month.get(month_key, 0) + 1

        cur += timedelta(days=1)

    # Sort by date
    entries.sort(key=lambda e: e["date"])

    if missing:
        print(f"⚠️  Missing/Invalid {len(missing)} dates:")
        for m in missing[:10]:
            print(f"    {m}")
        if len(missing) > 10:
            print(f"    ... and {len(missing) - 10} more")

    # Write merged file
    dest_data = {
        "schema_version": "1.0",
        "generated_on": datetime.utcnow().strftime("%Y-%m-%d"),
        "total_entries": len(entries),
        "entries": entries
    }

    DEST.parent.mkdir(parents=True, exist_ok=True)
    with open(DEST, "w", encoding="utf-8") as f:
        json.dump(dest_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Merged {len(entries)} entries → {DEST}")
    print(f"\nBy month:")
    for month in sorted(by_month.keys()):
        print(f"  {month}: {by_month[month]}")


if __name__ == "__main__":
    main()