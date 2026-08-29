#!/usr/bin/env python3
"""
Merge mock data for Jul 3-16 and Aug 1-31 into anno_full_2026.json
"""

import json
from pathlib import Path
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "Anno/Resources/anno_full_2026.json"

# Load current
with open(DEST, "r", encoding="utf-8") as f:
    data = json.load(f)

# Load mock files
fortnight_path = ROOT / "data/mock/anno_fortnight_2026-07-03_2026-07-16.json"
august_path = ROOT / "data/mock/anno_august_2026.json"

with open(fortnight_path, "r", encoding="utf-8") as f:
    fortnight = json.load(f)

with open(august_path, "r", encoding="utf-8") as f:
    august = json.load(f)

# Build lookup by date for fast checking
existing = {e["date"]: e for e in data["entries"]}
added = 0

# Add Jul 3-16
for entry in fortnight["entries"]:
    d = entry["date"]
    if d not in existing:
        existing[d] = entry
        added += 1

# Add Aug 1-31
for entry in august:
    d = entry["date"]
    if d not in existing:
        existing[d] = entry
        added += 1

# Rebuild sorted entries
all_entries = [existing[d] for d in sorted(existing.keys())]

# Update data
data["entries"] = all_entries
data["total_entries"] = len(all_entries)

# Write back
with open(DEST, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Added {added} entries")
print(f"Total: {data['total_entries']}")

# Stats by month
from collections import Counter
months = Counter()
for e in all_entries:
    months[e["date"][:7]] += 1
for m in sorted(months):
    print(f"  {m}: {months[m]} days")