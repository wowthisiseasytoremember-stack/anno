#!/usr/bin/env python3
"""Offline editorial gate for all four 2026 v1-required bilingual major feasts.

Native data flow: source JSON -> normalize_fixture.py -> anno_unified_2026.json.
No network, licensed images, Mac, Xcode, or proprietary dependencies are required.

  python3 tools/major_feast_editorial.py audit
  python3 tools/major_feast_editorial.py new --date 2027-01-06 --output /tmp/feast.json

A PASS means pinned factual metadata and source/data parity, NOT theological,
historical, Vietnamese-human, copyright, or device review sign-off.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "Anno/Resources/anno_unified_2026.json"
AUGUST = ROOT / "data/mock/anno_august_2026.json"
RESEARCH = ROOT / "data/research_results"

# Explicit editorial authority decisions; dates for the other four v1 feasts
# fall outside the July 3 - December 31 2026 fixture.
REQUIRED = {
    "2026-08-15": {
        "title_en": "The Assumption of the Blessed Virgin Mary",
        "title_vi": "Đức Maria Hồn Xác Lên Trời",
        "usccb": "https://bible.usccb.org/bible/readings/081526.cfm",
    },
    "2026-11-22": {
        "title_en": "Our Lord Jesus Christ, King of the Universe",
        "title_vi": "Chúa Giêsu Kitô Vua Vũ Trụ",
        "usccb": "https://bible.usccb.org/bible/readings/112226.cfm",
    },
    "2026-12-08": {
        "title_en": "Solemnity of the Immaculate Conception of the Blessed Virgin Mary",
        "title_vi": "Đại Lễ Đức Mẹ Vô Nhiễm Nguyên Tội",
        "usccb": "https://bible.usccb.org/bible/readings/120826.cfm",
    },
    "2026-12-25": {
        "title_en": "The Nativity of the Lord (Christmas)",
        "title_vi": "Đại Lễ Giáng Sinh — Mừng Chúa Giáng Sinh",
        "usccb": "https://bible.usccb.org/bible/readings/122526.cfm",
    },
}
TEXT = (
    ("liturgical", "title"), ("primary", "title"), ("primary", "summary"),
    ("primary", "body"), ("primary", "confidence_note"),
    ("app_hooks", "hero_line"), ("app_hooks", "prayer_prompt"),
)
COPY_FIELDS = ("type", "title_en", "title_vi", "summary_en", "summary_vi",
               "body_en", "body_vi", "confidence", "confidence_note_en",
               "confidence_note_vi")
ART_STATUS = {"placeholder_only", "cleared", "pending_clearance"}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_entries(august=AUGUST, research=RESEARCH):
    aug = read_json(august)
    if not isinstance(aug, list):
        raise ValueError("August source must be a JSON array")
    aug_hits = [e for e in aug if e.get("date") == "2026-08-15"]
    if len(aug_hits) != 1:
        raise ValueError("Expected exactly one August 15 source entry")
    data = {"2026-08-15": aug_hits[0]}
    for day in ("2026-11-22", "2026-12-08", "2026-12-25"):
        path = research / f"{day}_result.json"
        data[day] = read_json(path)
    return data


def get_vi_overlay(path: Path):
    return read_json(path)


def validate_fixture(fixture, upstream, vi_overlay, *,
                     expected=REQUIRED) -> list[str]:
    errors = []
    items = fixture.get("entries")
    if not isinstance(items, list):
        return ["Fixture needs an entries array"]
    if fixture.get("total_entries") != len(items):
        errors.append("total_entries does not match entries array")
    dates = [e.get("date") for e in items]
    if len(dates) != len(set(dates)):
        errors.append("Duplicate dates in normalized fixture")

    for day, spec in expected.items():
        hits = [e for e in items if e.get("date") == day]
        if len(hits) != 1:
            errors.append(f"{day}: expected exactly one normalized record, found {len(hits)}")
            continue
        e = hits[0]
        raw = upstream.get(day)
        if not raw:
            errors.append(f"{day}: upstream source record missing")
            continue
        if e.get("id") != f"anno-{day}" or raw.get("date") != day:
            errors.append(f"{day}: id/date mismatch")
        if e.get("weekday") != date.fromisoformat(day).strftime("%A"):
            errors.append(f"{day}: weekday differs from actual date")
        lit = e.get("liturgical", {})
        if (lit.get("rank"), lit.get("color")) != ("Solemnity", "white"):
            errors.append(f"{day}: expected Solemnity and liturgical white")
        if e.get("primary", {}).get("type") != "solemnity":
            errors.append(f"{day}: primary.type must be solemnity")
        for lang in ("en", "vi"):
            field = f"title_{lang}"
            title = lit.get(field, "")
            if title != spec[field]:
                errors.append(f"{day}: {field} mismatch against approved title authority")
        sources = e.get("sources", [])
        urls = [src.get("url") for src in sources if isinstance(src, dict)]
        if spec["usccb"] not in urls:
            errors.append(f"{day}: dated USCCB source missing")
        if len(urls) < 2 or len(urls) != len(set(urls)):
            errors.append(f"{day}: need at least two distinct source URLs")
        for url in urls:
            p = urlsplit(url or "")
            if p.scheme != "https" or not p.netloc or "example." in p.netloc:
                errors.append(f"{day}: invalid or placeholder source URL {url!r}")
        if e.get("artwork", {}).get("status") not in ART_STATUS:
            errors.append(f"{day}: invalid artwork provenance status")
        for section, key in TEXT:
            group = e.get(section) or {}
            en, vi = group.get(key + "_en"), group.get(key + "_vi")
            if not isinstance(en, str) or not en.strip():
                errors.append(f"{day}: missing {section}.{key}_en")
            if not isinstance(vi, str) or not vi.strip():
                errors.append(f"{day}: missing {section}.{key}_vi")
            if (isinstance(en, str) and isinstance(vi, str)
                    and en.strip().casefold() == vi.strip().casefold()):
                errors.append(f"{day}: English copied into {section}.{key}_vi")
            if isinstance(en, str) and re.search(r"\\b33th\\b", en, re.I):
                errors.append(f"{day}: invalid English ordinal 33th")
            if isinstance(vi, str) and re.search(r"\\b(?:Sunday|Saturday|Friday)\\b", vi, re.I):
                errors.append(f"{day}: untranslated English weekday in {section}.{key}_vi")
        if "_editorial" in e:
            errors.append(f"{day}: editorial draft metadata leaked into runtime fixture")
        if e.get("sources") != raw.get("sources"):
            errors.append(f"{day}: normalized sources differ from upstream sources")
        for key in ("rank", "color", "title_en"):
            if lit.get(key) != raw.get("liturgical", {}).get(key):
                errors.append(f"{day}: liturgical.{key} differs from upstream source")
        for field in COPY_FIELDS:
            if e.get("primary", {}).get(field) != raw.get("primary", {}).get(field):
                if field.endswith("_vi") and day == "2026-11-22":
                    # The dated research _vi file is the canonical VI overlay.
                    expected_vi = vi_overlay.get("primary", {}).get(field)
                    if e["primary"].get(field) == expected_vi:
                        continue
                errors.append(f"{day}: primary.{field} differs from upstream source")
        for section in ("liturgical", "app_hooks"):
            for field in e.get(section, {}):
                if field not in raw.get(section, {}) and not field.endswith("_vi"):
                    continue
                if e[section][field] == raw.get(section, {}).get(field):
                    continue
                if (field.endswith("_vi") and day == "2026-11-22"
                        and e[section][field] == vi_overlay.get(section, {}).get(field)):
                    continue
                errors.append(f"{day}: {section}.{field} differs from upstream source")
        # Disallow an overlooked _vi overlay silently replacing the corrected raw copy.
        if day == "2026-11-22":
            for section in ("liturgical", "primary", "app_hooks"):
                for field, value in vi_overlay.get(section, {}).items():
                    if field.endswith("_vi") and e.get(section, {}).get(field) != value:
                        errors.append(f"{day}: normalized {section}.{field} differs from VI overlay")
    return errors


def new_entry(day: str, output: Path) -> None:
    date.fromisoformat(day)
    if output.exists():
        raise FileExistsError(f"Refusing to replace {output}")
    todo = "TODO: source-backed, separately edited text"
    entry = {
        "id": f"anno-{day}", "date": day, "weekday": date.fromisoformat(day).strftime("%A"),
        "mock_priority": "engine_b_v1",
        "liturgical": {"rank": "Solemnity", "color": "white",
                       "title_en": todo, "title_vi": todo},
        "calendars": {key: todo for key in
                      ("julian", "hebrew", "islamic_umm_al_qura", "coptic", "ethiopian")},
        "primary": {"type": "solemnity", "confidence": "confirmed",
                    **{f"{key}_{lang}": todo for key in
                       ("title", "summary", "body", "confidence_note")
                       for lang in ("en", "vi")}},
        "place": None,
        "artwork": {"title": "TODO: optional art", "maker": "Unassigned",
                    "date_label": "Unknown", "source_url": "",
                    "status": "placeholder_only"},
        "sources": [
            {"label": todo, "url": "TODO: day-specific USCCB URL",
             "type": "liturgical_calendar"},
            {"label": todo, "url": "TODO: relevant Vatican/primary source",
             "type": "vatican"},
        ],
        "app_hooks": {f"{key}_{lang}": todo
                      for key in ("hero_line", "prayer_prompt") for lang in ("en", "vi")},
        "_editorial": {
            "status": "draft_do_not_ship",
            "checklist": [
                "Verify exact Gregorian date, liturgical rank, color, English/Vietnamese names",
                "Check each historical statement and quotation against primary sources",
                "Distinguish dogma, tradition, scholarly hypothesis, and geography",
                "Confirm a date-specific official liturgical source and a second independent source",
                "Human Catholic theological and Vietnamese language review",
                "Review summary and hook for clarity and devotional usefulness",
                "Never treat image placeholder as a rights-cleared artwork",
                "Check native Dynamic Type, VoiceOver, contrast and source affordances before release",
                "Normalize and run python3 tools/major_feast_editorial.py audit before merge",
            ],
            "assets": {"image_path": None, "license": None,
                       "caption_en": None, "caption_vi": None,
                       "alt_en": None, "alt_vi": None},
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    print(f"Draft only; must remove _editorial and all TODOs before ingestion: {output}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("audit", help="Offline audit of every 2026 required bilingual feast")
    create = sub.add_parser("new", help="Create one NON-shipping source JSON draft")
    create.add_argument("--date", required=True)
    create.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        if args.cmd == "new":
            new_entry(args.date, Path(args.output))
            return 0
        fixture = read_json(FIXTURE)
        upstream = source_entries()
        overlay = get_vi_overlay(RESEARCH / "2026-11-22_result_vi.json")
        errors = validate_fixture(fixture, upstream, overlay)
        for error in errors:
            print("FAIL:", error, file=sys.stderr)
        if errors:
            print(f"REJECT: {len(errors)} data/authority failures across 4 required feast records",
                  file=sys.stderr)
            return 1
        print("PASS: all 4 required 2026 feast dates, source parity, EN/VI and dated USCCB references")
        print("NOT VERIFIED: human theological/language review, asset rights, external link uptime, native UI")
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as e:
        print(f"FAIL: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
