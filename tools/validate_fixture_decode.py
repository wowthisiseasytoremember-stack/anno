#!/usr/bin/env python3
"""Validate that a normalized Anno fixture matches the Swift AnnoEntry decoder.

This is the blocking gate between Engine B/normalizer output and the native app.
It intentionally mirrors `Anno/Models/AnnoEntry.swift` — including the non-optional
`ArtworkCandidate`, numeric `SacredPlace` coordinates, `ConfidenceLevel` enums,
and the five calendar strings — rather than merely checking key presence.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = ROOT / "Anno/Resources/anno_unified_2026.json"

CONFIDENCE_LEVELS = {"confirmed", "traditional", "disputed", "contextual"}
CALENDAR_FIELDS = ("julian", "hebrew", "islamic_umm_al_qura", "coptic", "ethiopian")
ARTWORK_FIELDS = ("title", "maker", "date_label", "source_url", "status")
APP_HOOK_FIELDS = ("hero_line_en", "hero_line_vi", "prayer_prompt_en", "prayer_prompt_vi")
SOURCE_FIELDS = ("label", "url", "type")
TOP_ENTRY_FIELDS = ("id", "date", "weekday", "mock_priority")
PRIMARY_FIELDS = (
    "type",
    "title_en",
    "title_vi",
    "summary_en",
    "summary_vi",
    "confidence",
    "confidence_note_en",
    "confidence_note_vi",
    "body_en",
    "body_vi",
)
LITURGICAL_FIELDS = ("rank", "color", "title_en", "title_vi")


def _is_string(value: Any) -> bool:
    return isinstance(value, str)


def _is_number(value: Any) -> bool:
    """JSON numeric value Swift can decode into Double."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _validate_place(entry_id: str, place: Any) -> list[str]:
    if place is None:
        return []
    issues: list[str] = []
    if not isinstance(place, dict):
        return [f"{entry_id}: place must be an object or null"]
    if not _is_string(place.get("name")):
        issues.append(f"{entry_id}: place.name is not a string")
    if not _is_string(place.get("source_url")):
        issues.append(f"{entry_id}: place.source_url is not a string")
    for field in ("latitude", "longitude"):
        if not _is_number(place.get(field)):
            issues.append(f"{entry_id}: place.{field} is not a number")
    if place.get("confidence") not in CONFIDENCE_LEVELS:
        issues.append(f"{entry_id}: place.confidence is not a supported enum")
    return issues


def validate_fixture(data: dict) -> list[str]:
    issues: list[str] = []
    if not isinstance(data, dict):
        return ["fixture root must be an object"]

    if not _is_string(data.get("schema_version")):
        issues.append("schema_version is not a string")
    if not _is_string(data.get("generated_on")):
        issues.append("generated_on is not a string")

    entries = data.get("entries")
    if not isinstance(entries, list):
        issues.append("entries is not an array")
        return issues
    if not entries:
        issues.append("entries is empty")

    for index, entry in enumerate(entries):
        entry_id = entry.get("id") if isinstance(entry, dict) else None
        prefix = f"entry[{index}]"
        if isinstance(entry_id, str):
            prefix = f"entry[{index}] {entry_id}"
        if not isinstance(entry, dict):
            issues.append(f"{prefix}: entry must be an object")
            continue

        for field in TOP_ENTRY_FIELDS:
            if not _is_string(entry.get(field)):
                issues.append(f"{prefix}: {field} is not a string")

        liturgical = entry.get("liturgical")
        if not isinstance(liturgical, dict):
            issues.append(f"{prefix}: liturgical is not an object")
        else:
            for field in LITURGICAL_FIELDS:
                if not _is_string(liturgical.get(field)):
                    issues.append(f"{prefix}: liturgical.{field} is not a string")

        calendars = entry.get("calendars")
        if not isinstance(calendars, dict):
            issues.append(f"{prefix}: calendars is not an object")
        else:
            for field in CALENDAR_FIELDS:
                if not _is_string(calendars.get(field)):
                    issues.append(f"{prefix}: calendars.{field} is not a string")

        primary = entry.get("primary")
        if not isinstance(primary, dict):
            issues.append(f"{prefix}: primary is not an object")
        else:
            for field in PRIMARY_FIELDS:
                if not _is_string(primary.get(field)):
                    issues.append(f"{prefix}: primary.{field} is not a string")
            if primary.get("confidence") not in CONFIDENCE_LEVELS:
                issues.append(f"{prefix}: primary.confidence is not a supported enum")

        artwork = entry.get("artwork")
        if not isinstance(artwork, dict):
            issues.append(f"{prefix}: artwork is not an object")
        else:
            for field in ARTWORK_FIELDS:
                if not _is_string(artwork.get(field)):
                    issues.append(f"{prefix}: artwork.{field} is not a string")

        sources = entry.get("sources")
        if not isinstance(sources, list):
            issues.append(f"{prefix}: sources is not an array")
        else:
            for source_index, source in enumerate(sources):
                if not isinstance(source, dict):
                    issues.append(f"{prefix}: sources[{source_index}] is not an object")
                    continue
                for field in SOURCE_FIELDS:
                    if not _is_string(source.get(field)):
                        issues.append(f"{prefix}: sources[{source_index}].{field} is not a string")

        app_hooks = entry.get("app_hooks")
        if not isinstance(app_hooks, dict):
            issues.append(f"{prefix}: app_hooks is not an object")
        else:
            for field in APP_HOOK_FIELDS:
                if not _is_string(app_hooks.get(field)):
                    issues.append(f"{prefix}: app_hooks.{field} is not a string")

        issues.extend(_validate_place(prefix, entry.get("place")))

    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an Anno fixture against the Swift Codable contract")
    parser.add_argument(
        "--fixture",
        type=Path,
        default=DEFAULT_FIXTURE,
        help=f"Fixture path (default: {DEFAULT_FIXTURE})",
    )
    args = parser.parse_args()

    try:
        data = json.loads(args.fixture.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"VALIDATION FAILED - could not read fixture {args.fixture}: {exc}", file=sys.stderr)
        raise SystemExit(1)

    issues = validate_fixture(data)
    if issues:
        print(f"VALIDATION FAILED - {len(issues)} Swift AnnoEntry contract violation(s) in {args.fixture}", file=sys.stderr)
        for issue in issues:
            print(f"  {issue}", file=sys.stderr)
        raise SystemExit(1)

    entries = data.get("entries", [])
    span = ""
    if entries and isinstance(entries[0], dict) and isinstance(entries[-1], dict):
        span = f" ({entries[0].get('date', '?')} -> {entries[-1].get('date', '?')})"
    print(f"Swift fixture decode contract OK: {len(entries)} entries{span} in {args.fixture}")


if __name__ == "__main__":
    main()
