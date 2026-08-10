#!/usr/bin/env python3
"""
Merge content batches into anno_week_current.json for the Anno MVP.
Usage:
  python tools/merge_content.py data/content_batch_1/jul_03-09.json data/content_batch_2/jul_10-16.json
  python tools/merge_content.py data/content_batch_1/*.json data/content_batch_2/*.json
"""
import json
import sys
from pathlib import Path
from datetime import datetime

def load_entries(path):
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "entries" in data:
        return data["entries"]
    raise ValueError(f"{path}: expected array or object with 'entries' key")

def validate_entry(entry, path):
    required = ["id", "date", "weekday", "liturgical", "calendars", "primary", "artwork", "sources", "appHooks"]
    missing = [k for k in required if k not in entry]
    if missing:
        return [f"  {entry.get('id', '?')}: missing fields {missing}"]
    errors = []
    if not entry["primary"].get("summary_en"):
        errors.append(f"  {entry['id']}: empty summary_en")
    if not entry["primary"].get("summary_vi"):
        errors.append(f"  {entry['id']}: empty summary_vi")
    if entry["artwork"].get("source_url", "").startswith("https://example.com"):
        errors.append(f"  {entry['id']}: artwork URL is placeholder (example.com)")
    for src in entry.get("sources", []):
        if src.get("url", "").startswith("https://example.com"):
            errors.append(f"  {entry['id']}: source URL is placeholder (example.com)")
    return errors

def main():
    if len(sys.argv) < 2:
        print("Usage: merge_content.py <batch1.json> [batch2.json] ...")
        sys.exit(1)

    all_entries = []
    all_errors = []

    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"  SKIP: {path} not found")
            continue
        entries = load_entries(path)
        print(f"  {path.name}: {len(entries)} entries")
        for e in entries:
            errs = validate_entry(e, path.name)
            all_errors.extend(errs)
            all_entries.append(e)

    if all_errors:
        print(f"\nVALIDATION ERRORS ({len(all_errors)}):")
        for err in all_errors:
            print(err)
        print("\nFix errors before merging. Aborting.")
        sys.exit(1)

    # Deduplicate by date (last wins)
    seen = {}
    for e in all_entries:
        seen[e["date"]] = e
    deduped = sorted(seen.values(), key=lambda x: x["date"])

    print(f"\n  Total unique entries: {len(deduped)}")
    print(f"  Date range: {deduped[0]['date']} to {deduped[-1]['date']}")

    output = {
        "schema_version": "anno.mvp.v1",
        "generated_on": datetime.utcnow().strftime("%Y-%m-%d"),
        "description": "MVP week fixture for Anno Catholic Daily Devotional",
        "entries": deduped
    }

    out_path = Path("Anno/Resources/anno_week_current.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"  Wrote: {out_path}")
    print("  DONE")

if __name__ == "__main__":
    main()
