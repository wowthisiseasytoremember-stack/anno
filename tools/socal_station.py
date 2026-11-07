#!/usr/bin/env python3
"""Draft one SoCal exemplar station, or audit every station in the live content pack.

Usage:
  python3 tools/socal_station.py new --id example_station --title-en "Example" --output /tmp/example_station.json
  python3 tools/socal_station.py audit
The output of 'new' is a DRAFT; do not copy it into shipping resources until reviewed.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "Anno/Resources/socal_la_vang_exemplar_content_v1.json"
ROUTE = ROOT / "Anno/Resources/PilgrimageRoutes/socal_vietnamese_catholic_pilgrimage_la_vang.json"
MARKERS = ROOT / "Anno/Resources/socal_la_vang_physical_markers_v1.json"
MOMENTS = ROOT / "Anno/Resources/pilgrimage_moments_v1.json"
SOURCE_NOTES = ROOT / "docs/EXEMPLAR_SOCAL_SOURCE_NOTES.md"
STEPS = ("arrive", "look", "know", "pray", "continue")
LEVELS = ("reflection", "highlight", "climax", "context")
CHECKLIST = [
    "ARRIVE: orient a visitor without promising access",
    "LOOK: one observable feature, with a nonvisual alternative where useful",
    "KNOW: one sourced durable claim; distinguish Catholic tradition from documented fact",
    "PRAY: respectful opt-in reflection, not reward/scoring language",
    "CONTINUE: next physical/spiritual action without invented timing",
    "EN and VI independently reviewed by Vietnamese Catholic readers",
    "Official link resolves; cite each historic or geographic claim in source notes",
    "No stale hours, Mass times, parking restrictions, or tour availability",
    "VoiceOver/Dynamic Type/contrast and physical accessibility tested on device",
    "Images, if used, have rights, source/caption, and bilingual alt text",
    "Route/marker IDs unchanged or deliberately migrated and tested",
]


def new_station(args):
    if not re.fullmatch(r"[a-z][a-z0-9_]*", args.id):
        raise ValueError("station id must be lowercase snake_case")
    path = Path(args.output)
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite {path}")
    station = {
        "station_id": args.id,
        "station_role": args.role,
        "moment_level": args.level,
        "moment_label_en": "TODO: English presentation label",
        "moment_label_vi": "TODO: Vietnamese presentation label",
        "title_en": args.title_en,
        "title_vi": "TODO: Vietnamese Catholic title",
    }
    for step in STEPS:
        station[f"{step}_en"] = f"TODO: {step.upper()} English — distinct purpose"
        station[f"{step}_vi"] = f"TODO: {step.upper()} Vietnamese — independently authored"
    station["official_url"] = "https://example.org/REPLACE_WITH_OFFICIAL_SOURCE"
    station["_editorial"] = {
        "status": "draft_do_not_ship",
        "chapter_id": "TODO: existing chapter id",
        "source_claims": [
            {"claim": "TODO: claim to verify", "official_url": "TODO: link", "checked_on": "TODO: YYYY-MM-DD"}
        ],
        "human_review": ["Vietnamese Catholic copy", "physical access", "cultural and theological nuance"],
        "assets": {
            "image_path": None,
            "credit_or_license": None,
            "caption_en": None,
            "caption_vi": None,
            "alt_en": None,
            "alt_vi": None,
        },
        "checklist": CHECKLIST,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(station, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Draft station created: {path} (NOT shipping-ready)")


def validate(content_path=CONTENT, route_path=ROUTE, *, markers_path=MARKERS,
             moments_path=MOMENTS, notes_path=SOURCE_NOTES):
    content = json.loads(Path(content_path).read_text(encoding="utf-8"))
    route = json.loads(Path(route_path).read_text(encoding="utf-8"))
    markers = json.loads(Path(markers_path).read_text(encoding="utf-8"))
    moments = json.loads(Path(moments_path).read_text(encoding="utf-8"))
    sources = Path(notes_path).read_text(encoding="utf-8")
    errors = []
    core = next((v for v in content.get("variants", []) if v.get("id") == "core"), None)
    chapters = content.get("chapters", [])
    if not core:
        errors.append("Missing core variant")
        core_ids = []
    else:
        core_ids = core.get("chapter_ids", [])
    if len(chapters) != 5 or len(set(c["id"] for c in chapters)) != 5:
        errors.append("Expected five unique geographic chapters")
    if [c["id"] for c in chapters] != core_ids:
        errors.append("Core chapter order differs from content chapters")
    all_stations = [s for c in chapters for s in c.get("stations", [])]
    core_stations = [s for s in all_stations if s.get("station_role") != "optional_context"]
    optional_stations = [s for s in all_stations if s.get("station_role") == "optional_context"]
    if len(core_stations) != 7 or len(optional_stations) != 1:
        errors.append("Expected seven core and one optional station")
    ids = [s.get("waypoint_id") or s.get("station_id") for s in all_stations]
    if len(ids) != len(set(ids)) or None in ids:
        errors.append("Station IDs must be present and unique")
    waypoints = route.get("waypoints", [])
    route_ids = [w.get("waypoint_id") for w in waypoints]
    core_station_ids = [s.get("waypoint_id") or s.get("station_id") for s in core_stations]
    if core_station_ids != route_ids:
        errors.append("Core station order/IDs differ from live route waypoints")
    # The app also reads history and prayer from the map-waypoint records.
    # Any duplicate drifting makes the same place tell two different stories.
    station_by_id = {s.get("waypoint_id") or s.get("station_id"): s for s in core_stations}
    for waypoint in waypoints:
        sid = waypoint.get("waypoint_id")
        station = station_by_id.get(sid)
        if station is None:
            continue
        for route_key, exemplar_key in (
            ("historical_summary_en", "know_en"),
            ("historical_summary_vi", "know_vi"),
            ("suggested_prayer_en", "pray_en"),
            ("suggested_prayer_vi", "pray_vi"),
        ):
            if waypoint.get(route_key) != station.get(exemplar_key):
                errors.append(f"{sid}: route {route_key} differs from station {exemplar_key}")
    if content.get("route_id") != route.get("route_id"):
        errors.append("Exemplar route id mismatch")
    # Release-invariant identities: the seven live waypoints power persisted progress,
    # deep links, QR/NFC markers, and route/presentation lookup.
    marker_items = markers.get("markers", [])
    marker_ids = [m.get("station_id") for m in marker_items]
    if marker_ids != route_ids:
        errors.append("Marker station order/IDs differ from live route waypoints")
    if [m.get("marker_index") for m in marker_items] != list(range(1, len(route_ids) + 1)):
        errors.append("Marker indices must be sequential from one")
    for marker in marker_items:
        ix = marker.get("marker_index")
        if marker.get("payload") != f"anno://p/lv/{ix}":
            errors.append(f"Marker {ix}: invalid deep-link payload")
    so_cal_moments = [m for m in moments.get("moments", [])
                      if m.get("route_id") == route.get("route_id")]
    by_id = {m.get("waypoint_id"): m for m in so_cal_moments}
    if len(by_id) != len(so_cal_moments):
        errors.append("Repeated SoCal moment identifiers")
    if set(by_id) != {s.get("waypoint_id") or s.get("station_id") for s in core_stations
                       if s.get("moment_level") in ("climax", "highlight")}:
        errors.append("Presentation moment registry differs from core highlight/climax stations")
    for station in core_stations:
        sid = station.get("waypoint_id") or station.get("station_id")
        if sid in by_id and station.get("moment_level") != by_id[sid].get("level"):
            errors.append(f"{sid}: moment level differs from presentation registry")
    variants = {v.get("id"): v for v in content.get("variants", [])}
    if set(variants) != {"quick", "core", "extended"}:
        errors.append("Expected three distinct quick/core/extended variants")
    elif (variants["quick"].get("chapter_ids") != core_ids[:1]
          or variants["extended"].get("chapter_ids") != core_ids
          or variants["extended"].get("include_optional_station_ids")
          != [s.get("station_id") for s in optional_stations]):
        errors.append("Quick/extended chapter or optional-station membership drifted")
    status = content.get("translation_status", "")
    if "needs_human_catholic_review" not in status:
        errors.append("Vietnamese copy requires explicit pending-human-review status")
    if content.get("volatile_data_policy", {}).get("embed_current_schedules") is not False:
        errors.append("Durable prose must not embed current visitor schedules")
    for station in all_stations:
        sid = station.get("waypoint_id") or station.get("station_id") or "<missing id>"
        if station.get("moment_level") not in LEVELS:
            errors.append(f"{sid}: invalid presentation level")
        for field in ("title_en", "title_vi", "official_url"):
            val = station.get(field)
            if not isinstance(val, str) or not val.strip() or "TODO" in val:
                errors.append(f"{sid}: missing/unreviewed {field}")
        for step in STEPS:
            for lang in ("en", "vi"):
                field = f"{step}_{lang}"
                val = station.get(field)
                if not isinstance(val, str) or not val.strip() or "TODO" in val:
                    errors.append(f"{sid}: missing/unreviewed {field}")
        url = urlparse(station.get("official_url") or "")
        if url.scheme != "https" or not url.hostname or url.hostname.endswith("example.org"):
            errors.append(f"{sid}: official source must use real HTTPS URL")
        if station.get("official_url") not in sources:
            errors.append(f"{sid}: official URL absent from canonical source notes")
        # Programmatic time strings are an immediate red flag in durable copy.
        # This does not establish the accuracy of other prose, which stays under human review.
        for field, value in station.items():
            if (field.endswith(("_en", "_vi"))
                    and isinstance(value, str)
                    and re.search(r"(?<![0-9])(?:[01]?[0-9]|2[0-3]):[0-5][0-9](?: *(?:am|pm|a.m.|p.m.))?(?![0-9])",
                                  value, re.IGNORECASE)):
                errors.append(f"{sid}: clock time in durable {field}; link live schedule instead")
        if "_editorial" in station and station["_editorial"].get("status") == "draft_do_not_ship":
            errors.append(f"{sid}: scaffold draft cannot ship")
    if content.get("opening", {}).get("title_en") != route.get("title_en"):
        errors.append("Opening and route titles disagree")
    return errors, len(core_stations), len(optional_stations)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    new = sub.add_parser("new", help="Scaffold a NON-shipping one-station JSON draft")
    new.add_argument("--id", required=True)
    new.add_argument("--title-en", required=True)
    new.add_argument("--role", default="reflection")
    new.add_argument("--level", choices=LEVELS, default="reflection")
    new.add_argument("--output", required=True)
    audit = sub.add_parser("audit", help="Validate every SoCal station and cross-file invariants")
    audit.add_argument("--content", type=Path, default=CONTENT)
    audit.add_argument("--route", type=Path, default=ROUTE)
    audit.add_argument("--markers", type=Path, default=MARKERS)
    audit.add_argument("--moments", type=Path, default=MOMENTS)
    audit.add_argument("--notes", type=Path, default=SOURCE_NOTES)
    args = parser.parse_args()
    try:
        if args.command == "new":
            new_station(args)
            return 0
        errors, core, optional = validate(
            args.content, args.route, markers_path=args.markers,
            moments_path=args.moments, notes_path=args.notes
        )
        if errors:
            for error in errors:
                print("FAIL:", error, file=sys.stderr)
            return 1
        print(f"PASS: {core} core + {optional} optional SoCal stations; sources indexed; moments and QR markers aligned")
        print("NOT VERIFIED: links alive, historical accuracy, Vietnamese localization, physical/device access")
        return 0
    except (ValueError, FileExistsError, OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
