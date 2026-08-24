#!/usr/bin/env python3
"""Validate the 365-day Catholic devotional pool fixture."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POOL_PATH = ROOT / "Anno/Resources/anno_devotional_pool_365.json"

REQUIRED_FIELDS = [
    "day_of_year",
    "theme_en",
    "theme_vi",
    "scripture_reference",
    "scripture_text_en",
    "scripture_text_vi",
    "reflection_title_en",
    "reflection_title_vi",
    "reflection_body_en",
    "reflection_body_vi",
    "author_or_source",
    "daily_prayer_en",
    "daily_prayer_vi",
]

VI_DIACRITICS = set("áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ"
                    "ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴĐ")


def validate_devotional_pool(path: Path = POOL_PATH) -> int:
    if not path.exists():
        print(f"FAIL: File not found: {path}", file=sys.stderr)
        return 1

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAIL: Invalid JSON in {path}: {e}", file=sys.stderr)
        return 1

    if isinstance(data, dict) and "devotionals" in data:
        devotionals = data["devotionals"]
    elif isinstance(data, list):
        devotionals = data
    else:
        print(f"FAIL: Unrecognized structure in {path}", file=sys.stderr)
        return 1

    if len(devotionals) != 365:
        print(f"FAIL: Expected exactly 365 entries, got {len(devotionals)}", file=sys.stderr)
        return 1

    errors = 0
    seen_days = set()

    for idx, item in enumerate(devotionals, start=1):
        day = item.get("day_of_year")
        if day is None or not isinstance(day, int):
            print(f"FAIL [Item {idx}]: Missing or invalid day_of_year: {day}", file=sys.stderr)
            errors += 1
            continue

        if day in seen_days:
            print(f"FAIL [Day {day}]: Duplicate day_of_year found", file=sys.stderr)
            errors += 1
        seen_days.add(day)

        for field in REQUIRED_FIELDS:
            val = item.get(field)
            if val is None or (isinstance(val, str) and not val.strip()):
                print(f"FAIL [Day {day}]: Missing or empty field '{field}'", file=sys.stderr)
                errors += 1

        # Check Vietnamese diacritics
        vi_text = f"{item.get('theme_vi', '')} {item.get('reflection_title_vi', '')} {item.get('reflection_body_vi', '')} {item.get('daily_prayer_vi', '')}"
        if not any(char in VI_DIACRITICS for char in vi_text):
            print(f"FAIL [Day {day}]: Vietnamese fields appear to lack proper diacritics", file=sys.stderr)
            errors += 1

    expected_days = set(range(1, 366))
    if seen_days != expected_days:
        missing_days = expected_days - seen_days
        print(f"FAIL: Missing days of year: {sorted(missing_days)[:10]}...", file=sys.stderr)
        errors += 1

    if errors == 0:
        print(f"OK: Validated all 365 devotional entries in {path.relative_to(ROOT)} (100% complete EN/VI, verified diacritics)")
        return 0
    else:
        print(f"FAIL: Validation completed with {errors} errors", file=sys.stderr)
        return 1


def main() -> None:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else POOL_PATH
    sys.exit(validate_devotional_pool(target))


if __name__ == "__main__":
    main()
