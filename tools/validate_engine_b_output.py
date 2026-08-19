#!/usr/bin/env python3
"""
Engine B Source Validation Gate — Anno
Verifies each generated Engine B entry before merging into the app fixture.

Usage:
    python3 tools/validate_engine_b_output.py --fixture path/to/generated.json
    python3 tools/validate_engine_b_output.py --fixture path/to/generated.json --strict --check-sources
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ── Valid Values ──────────────────────────────────────────────

VALID_RANKS = {"Solemnity", "Feast", "Memorial", "Optional Memorial", "Feria", "Sunday"}
VALID_COLORS = {"white", "red", "green", "purple", "rose", "gold", "verdigris"}
VALID_CONFIDENCE = {"confirmed", "traditional", "disputed", "contextual"}
VALID_TYPES = {"saint", "liturgical_day", "historical_event", "feast", "solemnity"}
VALID_SOURCE_TYPES = {
    "liturgical_calendar", "vatican", "encyclopedia", "academic", "news", "devotional"
}

# ── Results ───────────────────────────────────────────────────

results: list[dict] = []
errors = 0
warnings = 0


def fail(entry_id: str, check: str, detail: str) -> None:
    global errors
    errors += 1
    results.append({"entry": entry_id, "severity": "FAIL", "check": check, "detail": detail})
    print(f"  FAIL [{entry_id}] {check}: {detail}")


def warn(entry_id: str, check: str, detail: str) -> None:
    global warnings
    warnings += 1
    results.append({"entry": entry_id, "severity": "WARN", "check": check, "detail": detail})
    print(f"  WARN [{entry_id}] {check}: {detail}")


def ok(entry_id: str, check: str) -> None:
    results.append({"entry": entry_id, "severity": "OK", "check": check, "detail": ""})


# ── Checks ────────────────────────────────────────────────────


def check_required_fields(entry: dict) -> None:
    eid = entry.get("id", "<missing>")
    required = [
        ("id", str),
        ("date", str),
        ("weekday", str),
        ("mock_priority", str),
    ]
    for field, ftype in required:
        val = entry.get(field)
        if val is None:
            fail(eid, "required_field", f"Missing '{field}'")
            continue
        if not isinstance(val, ftype):
            fail(eid, "required_field", f"'{field}' should be {ftype.__name__}, got {type(val).__name__}")
            continue
        ok(eid, f"required_field.{field}")

    # ID format
    if not re.match(r"^anno-\d{4}-\d{2}-\d{2}$", entry.get("id", "")):
        fail(eid, "id_format", "ID must match 'anno-YYYY-MM-DD'")

    # Date must match ID
    if entry.get("id", "").replace("anno-", "") != entry.get("date", ""):
        warn(eid, "date_match", "ID date and 'date' field don't match")


def check_liturgical(entry: dict) -> None:
    eid = entry.get("id", "<missing>")
    lit = entry.get("liturgical", {})
    if not lit:
        fail(eid, "liturgical", "Missing 'liturgical' object")
        return
    if lit.get("rank") not in VALID_RANKS:
        fail(eid, "liturgical.rank", f"Invalid rank '{lit.get('rank')}'")
    if lit.get("color") not in VALID_COLORS:
        fail(eid, "liturgical.color", f"Invalid color '{lit.get('color')}'")
    if not lit.get("title_en"):
        fail(eid, "liturgical.title_en", "Missing English title")
    if not lit.get("title_vi"):
        fail(eid, "liturgical.title_vi", "Missing Vietnamese title")


def check_primary(entry: dict) -> None:
    eid = entry.get("id", "<missing>")
    pri = entry.get("primary", {})
    if not pri:
        fail(eid, "primary", "Missing 'primary' object")
        return
    if pri.get("type") not in VALID_TYPES:
        fail(eid, "primary.type", f"Invalid type '{pri.get('type')}'")
    if not pri.get("title_en"):
        fail(eid, "primary.title_en", "Missing English title")
    if not pri.get("title_vi"):
        fail(eid, "primary.title_vi", "Missing Vietnamese title")
    if not pri.get("summary_en"):
        fail(eid, "primary.summary_en", "Missing English summary")
    if not pri.get("summary_vi"):
        fail(eid, "primary.summary_vi", "Missing Vietnamese summary")

    # Summary length: 2-4 sentences approximately
    summary = pri.get("summary_en", "")
    summary_sentences = len(re.findall(r"[.!?]+", summary))
    if summary_sentences < 2:
        warn(eid, "primary.summary_length", f"English summary has {summary_sentences} sentence(s), expected at least 2")

    if pri.get("confidence") not in VALID_CONFIDENCE:
        fail(eid, "primary.confidence", f"Invalid confidence '{pri.get('confidence')}'")
    if not pri.get("confidence_note_en"):
        fail(eid, "primary.confidence_note_en", "Missing English confidence note")
    if not pri.get("confidence_note_vi"):
        fail(eid, "primary.confidence_note_vi", "Missing Vietnamese confidence note")

    # Body check: at least substantive if present
    body = pri.get("body_en", "")
    if body:
        paragraphs = [p for p in body.split("\n") if p.strip()]
        if len(paragraphs) < 3:
            warn(eid, "primary.body_paragraphs", f"Body has {len(paragraphs)} paragraph(s), expected at least 3")
        word_count = len(body.split())
        if word_count < 100:
            warn(eid, "primary.body_length", f"Body has {word_count} words, expected at least 100")
    else:
        warn(eid, "primary.body_en", "Body missing (acceptable for feria days)")


def check_sources(entry: dict, strict: bool = False) -> None:
    eid = entry.get("id", "<missing>")
    sources = entry.get("sources", [])
    if len(sources) < 2:
        fail(eid, "sources.count", f"Expected at least 2 sources, found {len(sources)}")
    else:
        ok(eid, "sources.count")
    if len(sources) < 3:
        warn(eid, "sources.count", "Only 2 sources, 3 preferred for non-feria entries")

    for src in sources:
        url = src.get("url", "")
        if not url:
            fail(eid, "sources.url", "Source entry missing URL")
            continue
        if "example.com" in url:
            fail(eid, "sources.example", f"Placeholder URL: {url}")
        if src.get("type") not in VALID_SOURCE_TYPES:
            fail(eid, "sources.type", f"Invalid source type '{src.get('type')}'")
        if not src.get("label"):
            fail(eid, "sources.label", "Source entry missing label")
        if strict:
            try:
                req = urllib.request.Request(url, method="HEAD")
                req.add_header("User-Agent", "Anno-Validator/1.0")
                resp = urllib.request.urlopen(req, timeout=5)
                if resp.status >= 400:
                    warn(eid, "sources.reachable", f"Source URL returned {resp.status}: {url}")
            except Exception as exc:
                warn(eid, "sources.reachable", f"Source URL unreachable: {url} — {exc}")


def check_calendars(entry: dict) -> None:
    eid = entry.get("id", "<missing>")
    cals = entry.get("calendars", {})
    required_cals = {"julian", "hebrew", "islamic_umm_al_qura", "coptic", "ethiopian"}
    for key in required_cals:
        if not cals.get(key):
            fail(eid, f"calendars.{key}", f"Missing calendar conversion '{key}'")


def check_bilingual(entry: dict) -> None:
    eid = entry.get("id", "<missing>")

    # Top-level bilingual pairs in app_hooks
    hooks = entry.get("app_hooks", {})
    for field in ("hero_line_en", "hero_line_vi", "prayer_prompt_en", "prayer_prompt_vi"):
        if not hooks.get(field):
            fail(eid, f"app_hooks.{field}", f"Missing '{field}'")

    # Check for placeholder/generic content
    generic_patterns = [
        "A day of ordinary time",
        "Reflect on this day's grace",
        "placeholder",
        "example.com",
    ]
    for section_name, section in [("primary", entry.get("primary", {})),
                                    ("app_hooks", hooks)]:
        for key, value in section.items():
            if isinstance(value, str):
                for pattern in generic_patterns:
                    if pattern.lower() in value.lower():
                        fail(eid, f"placeholder.{section_name}.{key}",
                              f"Contains placeholder text: '{pattern}'")
                        break


def check_confidence_consistency(entry: dict) -> None:
    """Solemnities/Feasts must be 'confirmed'."""
    eid = entry.get("id", "<missing>")
    rank = entry.get("liturgical", {}).get("rank", "")
    confidence = entry.get("primary", {}).get("confidence", "")
    if rank in ("Solemnity", "Feast") and confidence != "confirmed":
        warn(eid, "confidence_consistency",
             f"Rank is '{rank}' but confidence is '{confidence}'. Should be 'confirmed'.")


def check_place(entry: dict) -> None:
    eid = entry.get("id", "<missing>")
    place = entry.get("place")
    if place is None:
        ok(eid, "place.null")
        return
    if not place.get("name"):
        fail(eid, "place.name", "Place object present but missing 'name'")

    pconf = place.get("confidence")
    if pconf not in VALID_CONFIDENCE:
        fail(eid, "place.confidence", f"Invalid place confidence '{pconf}'")

    lat = place.get("latitude")
    lon = place.get("longitude")
    if lat is not None and lon is not None:
        if not (-90 <= lat <= 90):
            fail(eid, "place.latitude", f"Latitude out of range: {lat}")
        if not (-180 <= lon <= 180):
            fail(eid, "place.longitude", f"Longitude out of range: {lon}")
    elif lat is not None or lon is not None:
        fail(eid, "place.coordinates", "Only one coordinate provided, need both lat and lon")


# ── Main ───────────────────────────────────────────────────────


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Validate Engine B output for Anno")
    parser.add_argument("--fixture", required=True, help="Path to generated fixture JSON")
    parser.add_argument("--strict", action="store_true", help="Enable source URL reachability checks")
    parser.add_argument("--check-sources", action="store_true", help="Run source reachability checks regardless of strict mode")
    args = parser.parse_args()

    fixture_path = Path(args.fixture)
    if not fixture_path.exists():
        print(f"ERROR: Fixture file not found: {fixture_path}", file=sys.stderr)
        raise SystemExit(1)

    with open(fixture_path) as f:
        fixture = json.load(f)

    # Engine B result files are a single entry dict, OR a {"entries": [...]} batch.
    if isinstance(fixture, dict) and "entries" in fixture:
        entries = fixture["entries"]
    elif isinstance(fixture, list):
        entries = fixture
    elif isinstance(fixture, dict) and "id" in fixture:
        # Single-entry result file (one date).
        entries = [fixture]
    else:
        entries = []
    if not entries:
        print("ERROR: Fixture has no entries")
        raise SystemExit(1)

    print(f"Anno Engine B Validation Gate")
    print(f"Fixture: {fixture_path}")
    print(f"Entries: {len(entries)}")
    print(f"Schema: {fixture.get('schema_version', 'unknown')}")
    print(f"---")

    check_sources_flag = args.strict or args.check_sources

    for entry in entries:
        eid = entry.get("id", "<missing>")
        print(f"[{eid}]")
        check_required_fields(entry)
        check_liturgical(entry)
        check_primary(entry)
        check_sources(entry, strict=check_sources_flag)
        check_calendars(entry)
        check_bilingual(entry)
        check_confidence_consistency(entry)
        check_place(entry)
        print()

    summary = {
        "entries": len(entries),
        "errors": errors,
        "warnings": warnings,
        "pass_without_issues": len(entries) - len(set(r["entry"] for r in results if r["severity"] != "OK")),
    }

    print(f"=== Summary ===")
    print(f"  Entries:    {summary['entries']}")
    print(f"  Errors:     {summary['errors']}")
    print(f"  Warnings:   {summary['warnings']}")
    print(f"  Clean:      {summary['pass_without_issues']}/{summary['entries']}")

    verdict = "PASS" if errors == 0 else "REVISE"
    if errors == 0 and warnings == 0:
        verdict = "PASS (clean)"
    elif errors == 0:
        verdict = "PASS with warnings"

    print(f"  Verdict:    {verdict}")

    if errors > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
