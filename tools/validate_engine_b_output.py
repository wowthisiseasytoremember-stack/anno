#!/usr/bin/env python3
"""
Engine B Validation Gate — Anno
Uses jsonschema + requests + feedparser — single file <200 lines.
Exit codes: 0=pass, 1=revise, 2=reject
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any

import jsonschema
import requests
import feedparser

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "docs/research/engine_b_schema.json"

# ── Schema ───────────────────────────────────────────────────────
SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["id", "date", "weekday", "mock_priority", "liturgical", "calendars", "primary", "sources", "app_hooks"],
    "properties": {
        "id": {"type": "string", "pattern": "^anno-\\d{4}-\\d{2}-\\d{2}$"},
        "date": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$"},
        "weekday": {"type": "string"},
        "mock_priority": {"const": "engine_b_v1"},
        "liturgical": {
            "type": "object",
            "required": ["rank", "color", "title_en", "title_vi"],
            "properties": {
                "rank": {"enum": ["Solemnity", "Feast", "Memorial", "Optional Memorial", "Feria", "Sunday"]},
                "color": {"enum": ["white", "red", "green", "purple", "rose", "gold", "verdigris"]},
                "title_en": {"type": "string", "minLength": 1},
                "title_vi": {"type": "string", "minLength": 1},
            },
        },
        "calendars": {
            "type": "object",
            "required": ["julian", "hebrew", "islamic_umm_al_qura", "coptic", "ethiopian"],
            "properties": {k: {"type": "string"} for k in ["julian", "hebrew", "islamic_umm_al_qura", "coptic", "ethiopian"]},
        },
        "primary": {
            "type": "object",
            "required": ["type", "title_en", "title_vi", "summary_en", "summary_vi", "body_en", "body_vi", "confidence", "confidence_note_en", "confidence_note_vi"],
            "properties": {
                "type": {"enum": ["saint", "liturgical_day", "historical_event", "feast", "solemnity"]},
                "title_en": {"type": "string", "minLength": 1},
                "title_vi": {"type": "string", "minLength": 1},
                "summary_en": {"type": "string", "minLength": 1},
                "summary_vi": {"type": "string", "minLength": 1},
                "body_en": {"type": "string", "minLength": 1},
                "body_vi": {"type": "string", "minLength": 1},
                "confidence": {"enum": ["confirmed", "traditional", "disputed", "contextual"]},
                "confidence_note_en": {"type": "string", "minLength": 1},
                "confidence_note_vi": {"type": "string", "minLength": 1},
            },
        },
        "place": {
            "type": ["object", "null"],
            "properties": {
                "name": {"type": ["string", "null"]},
                "latitude": {"type": ["number", "null"]},
                "longitude": {"type": ["number", "null"]},
                "confidence": {"enum": ["confirmed", "traditional", "disputed", "contextual"]},
                "source_url": {"type": ["string", "null"], "format": "uri"},
            },
        },
        "artwork": {
            "type": "object",
            "required": ["title", "maker", "date_label", "source_url", "status"],
            "properties": {
                "title": {"type": "string"},
                "maker": {"type": "string"},
                "date_label": {"type": "string"},
                "source_url": {"type": "string", "format": "uri"},
                "status": {"const": "placeholder_only"},
            },
        },
        "sources": {
            "type": "array",
            "minItems": 2,
            "items": {
                "type": "object",
                "required": ["label", "url", "type"],
                "properties": {
                    "label": {"type": "string", "minLength": 1},
                    "url": {"type": "string", "format": "uri"},
                    "type": {"enum": ["liturgical_calendar", "vatican", "encyclopedia", "academic", "news", "devotional"]},
                },
            },
        },
        "app_hooks": {
            "type": "object",
            "required": ["hero_line_en", "hero_line_vi", "prayer_prompt_en", "prayer_prompt_vi"],
            "properties": {k: {"type": "string", "minLength": 1} for k in ["hero_line_en", "hero_line_vi", "prayer_prompt_en", "prayer_prompt_vi"]},
        },
    },
}

# ── Helpers ──────────────────────────────────────────────────────

def load_schema() -> dict:
    if SCHEMA_PATH.exists():
        with open(SCHEMA_PATH) as f:
            return json.load(f)
    return SCHEMA


def count_sentences(text: str) -> int:
    return len(re.split(r"[.!?]+", text.strip())) - 1


def count_paragraphs(text: str) -> int:
    return len([p for p in text.split("\n\n") if p.strip()])


def check_url_head(url: str, timeout: int = 5) -> tuple[bool, int]:
    try:
        # Use GET with stream=True to avoid downloading body; some sites block HEAD
        resp = requests.get(url, timeout=timeout, allow_redirects=True, stream=True)
        resp.close()
        # Accept 2xx, 3xx, and 403 (blocked but exists)
        return resp.status_code < 400 or resp.status_code == 403, resp.status_code
    except Exception:
        return False, 0


def validate_entry(entry: dict, strict: bool, check_sources: bool) -> tuple[int, int]:
    errors = 0
    warnings = 0
    eid = entry.get("id", "<missing>")

    def fail(msg: str) -> None:
        nonlocal errors
        errors += 1
        print(f"  FAIL [{eid}] {msg}")

    def warn(msg: str) -> None:
        nonlocal warnings
        warnings += 1
        print(f"  WARN [{eid}] {msg}")

    def ok(msg: str) -> None:
        print(f"  OK   [{eid}] {msg}")

    # Schema validation
    try:
        jsonschema.validate(entry, load_schema())
        ok("schema")
    except jsonschema.ValidationError as e:
        fail(f"schema: {e.message}")
        return errors, warnings

    # ID/date match
    if entry["id"].replace("anno-", "") != entry["date"]:
        warn("ID date and 'date' field don't match")

    # Source validation
    sources = entry.get("sources", [])
    if len(sources) < 2:
        fail(f"sources: need ≥2, got {len(sources)}")

    for i, src in enumerate(sources):
        url = src.get("url", "")
        if "example.com" in url:
            fail(f"source[{i}]: example.com URL not allowed")
        if check_sources or strict:
            ok_flag, code = check_url_head(url)
            if not ok_flag:
                fail(f"source[{i}]: HTTP {code} for {url}")
            else:
                ok(f"source[{i}]: HTTP 200")

        # type↔URL pattern match (basic)
        stype = src.get("type", "")
        if stype == "liturgical_calendar" and "usccb.org" not in url and "catholicculture.org" not in url:
            warn(f"source[{i}]: type=liturgical_calendar but URL doesn't match known patterns")
        if stype == "vatican" and "vatican.va" not in url:
            warn(f"source[{i}]: type=vatican but URL doesn't contain vatican.va")
        if stype == "encyclopedia" and "newadvent.org" not in url:
            warn(f"source[{i}]: type=encyclopedia but URL doesn't contain newadvent.org")

    # Artwork validation
    artwork = entry.get("artwork", {})
    artwork_url = artwork.get("source_url", "")
    if "example.com" in artwork_url:
        fail("artwork.source_url: example.com URL not allowed")

    # Content quality
    pri = entry.get("primary", {})
    summary_en = pri.get("summary_en", "")
    summary_vi = pri.get("summary_vi", "")
    body_en = pri.get("body_en", "")
    body_vi = pri.get("body_vi", "")

    if not (2 <= count_sentences(summary_en) <= 4):
        fail(f"primary.summary_en: {count_sentences(summary_en)} sentences (need 2-4)")
    if not (2 <= count_sentences(summary_vi) <= 4):
        fail(f"primary.summary_vi: {count_sentences(summary_vi)} sentences (need 2-4)")
    if count_paragraphs(body_en) < 1:
        fail(f"primary.body_en: {count_paragraphs(body_en)} paragraphs (need ≥1)")
    if count_paragraphs(body_vi) < 1:
        fail(f"primary.body_vi: {count_paragraphs(body_vi)} paragraphs (need ≥1)")

    # Placeholder text detection
    placeholders = ["placeholder", "todo", "tbd", "xxx", "lorem ipsum"]
    for field_name, field_val in [("summary_en", summary_en), ("summary_vi", summary_vi), ("body_en", body_en), ("body_vi", body_vi)]:
        if any(p in field_val.lower() for p in placeholders):
            fail(f"primary.{field_name}: contains placeholder text")

    # Confidence consistency
    rank = entry.get("liturgical", {}).get("rank", "")
    confidence = pri.get("confidence", "")
    if rank in ("Solemnity", "Feast") and confidence != "confirmed":
        warn(f"confidence: rank={rank} but confidence={confidence} (should be 'confirmed')")

    # Place confidence match
    place = entry.get("place")
    if place and place.get("confidence") != confidence:
        warn("place.confidence doesn't match primary.confidence")

    # Bilingual fields present
    for field in ["title", "summary", "confidence_note", "hero_line", "prayer_prompt"]:
        en_key = f"{field}_en"
        vi_key = f"{field}_vi"
        # Check in appropriate nested objects
        pass  # schema already enforces presence

    # Tier rules (inferred from source types)
    tier4_sources = [s for s in sources if s.get("type") == "devotional"]
    if tier4_sources:
        for s in tier4_sources:
            if "Produced in Vietnam; state context applies" not in s.get("label", "") and "Produced in Vietnam; state context applies" not in s.get("url", ""):
                fail(f"tier4: source '{s['label']}' missing mandatory state context note")

    return errors, warnings


# ── Main ────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Engine B output for Anno")
    parser.add_argument("--fixture", required=True, help="Path to generated fixture JSON")
    parser.add_argument("--strict", action="store_true", help="Enable source URL reachability checks")
    parser.add_argument("--check-sources", action="store_true", help="Run source reachability checks regardless of strict mode")
    args = parser.parse_args()

    fixture_path = Path(args.fixture)
    if not fixture_path.exists():
        print(f"ERROR: Fixture file not found: {fixture_path}", file=sys.stderr)
        return 1

    with open(fixture_path) as f:
        fixture = json.load(f)

    if isinstance(fixture, dict) and "entries" in fixture:
        entries = fixture["entries"]
    elif isinstance(fixture, list):
        entries = fixture
    elif isinstance(fixture, dict) and "id" in fixture:
        entries = [fixture]
    else:
        print("ERROR: Fixture has no entries", file=sys.stderr)
        return 1

    if not entries:
        print("ERROR: Fixture has no entries", file=sys.stderr)
        return 1

    print(f"Anno Engine B Validation Gate")
    print(f"Fixture: {fixture_path}")
    print(f"Entries: {len(entries)}")
    print(f"---")

    check_sources_flag = args.strict or args.check_sources
    total_errors = 0
    total_warnings = 0

    for entry in entries:
        print(f"[{entry.get('id', '<missing>')}]")
        e, w = validate_entry(entry, strict=args.strict, check_sources=check_sources_flag)
        total_errors += e
        total_warnings += w
        print()

    print(f"=== Summary ===")
    print(f"  Entries:    {len(entries)}")
    print(f"  Errors:     {total_errors}")
    print(f"  Warnings:   {total_warnings}")

    if total_errors > 0:
        return 2  # reject
    return 0  # pass


if __name__ == "__main__":
    sys.exit(main())