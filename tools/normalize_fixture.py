#!/usr/bin/env python3
"""Normalize all Anno content tracks into one continuous Swift-fixture-ready dataset.

Tracks (July 3, 2026 – December 31, 2026 = 182 days):
  - data/mock/anno_fortnight_2026-07-03_2026-07-16.json  (14 entries, EN+VI, verified sources)
  - data/research_results/2026-07-{17..31}_result.json (Engine B July track)
  - data/mock/anno_august_2026.json (31 entries, EN+VI, verified sources)
  - data/research_results/2026-{09..12}-*_result.json (Engine B Sep-Dec track, 122 days)

Output: Anno/Resources/anno_unified_2026.json -- a single {"schema_version","generated_on","entries":[...]}
shaped to match the Swift AnnoEntry decoder (see export_swift_fixture.py header).
The normalizer now sanitizes optional place data and coerces artwork fields to the
non-optional Swift contract, then runs a blocking decode-contract validator before write.
"""
from __future__ import annotations
import json, re, shutil
from datetime import date, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FORTNIGHT = ROOT / "data/mock/anno_fortnight_2026-07-03_2026-07-16.json"
AUGUST = ROOT / "data/mock/anno_august_2026.json"
RESEARCH = ROOT / "data/research_results"
OUT = ROOT / "Anno/Resources/anno_unified_2026.json"

# 8 major feasts requiring VI (only those in Jul 3 - Dec 31 2026 range are enforced)
VI_REQUIRED_DATES = {
    "2026-08-15",  # Assumption of the Blessed Virgin Mary
    "2026-11-22",  # Christ the King
    "2026-12-08",  # Immaculate Conception
    "2026-12-25",  # Christmas
    # Easter, Pentecost, Divine Mercy, Epiphany fall outside Jul 3 - Dec 31 2026 range
}

TYPE_MAP = {
    "saint": "saint", "feast": "feast", "memorial": "memorial",
    "optional memorial": "memorial", "solemnity": "solemnity",
    "liturgical_day": "liturgical_day", "feria": "liturgical_day",
}
RANK_MAP = {
    "solemnity": "Solemnity", "feast": "Feast", "memorial": "Memorial",
    "optional memorial": "Optional Memorial", "optional_memorial": "Optional Memorial",
    "feria": "Feria", "sunday": "Sunday",
}
COLOR_OK = {"white", "red", "green", "purple", "gold", "rose", "verdigris", "black"}
CONFIDENCE_OK = {"confirmed", "traditional", "disputed", "contextual"}
ARTWORK_STATUS_MAP = {
    "public domain": "public_domain",
    "public-domain": "public_domain",
    "publicdomain": "public_domain",
    "placeholder": "placeholder_only",
    "placeholder_only": "placeholder_only",
    "cleared": "cleared",
    "unavailable": "unavailable",
}


def load(p: Path | str) -> Any:
    return json.loads(Path(p).read_text(encoding="utf-8"))


def norm_id(raw: str, date_str: str) -> str:
    m = re.match(r"(\d{4}-\d{2}-\d{2})", raw)
    if m:
        return f"anno-{m.group(1)}"
    return f"anno-{date_str}" if date_str else raw


def map_type(val: str) -> str:
    v = (val or "").strip().lower()
    return TYPE_MAP.get(v, "liturgical_day")


def merge_vi(entry_en: dict, vi: dict | None) -> dict:
    if not vi:
        return entry_en
    out = json.loads(json.dumps(entry_en))  # deep copy

    def fill(section, key):
        vi_key = f"{key}_vi"
        if section in vi and vi_key in vi.get(section, {}):
            out.setdefault(section, {})[vi_key] = vi[section][vi_key]

    fill("liturgical", "title")
    fill("primary", "title")
    fill("primary", "summary")
    fill("primary", "body")
    fill("primary", "confidence_note")
    fill("app_hooks", "hero_line")
    fill("app_hooks", "prayer_prompt")
    return out


def normalize_sources(sources: list) -> list[dict]:
    out = []
    for s in sources:
        if isinstance(s, list) and len(s) >= 3:
            stype = s[2]
            if stype in ("official", "magisterial"):
                stype = "vatican"
            elif stype == "reference":
                stype = "encyclopedia"
            elif stype == "liturgical_resource":
                stype = "liturgical_calendar"
            out.append({"label": s[0], "url": s[1], "type": stype})
        elif isinstance(s, dict):
            stype = s.get("type", "liturgical_calendar")
            if stype in ("official", "magisterial"):
                stype = "vatican"
            elif stype == "reference":
                stype = "encyclopedia"
            elif stype == "liturgical_resource":
                stype = "liturgical_calendar"
            out.append({
                "label": s.get("label", ""),
                "url": s.get("url", ""),
                "type": stype,
            })
    return out


def map_confidence(val: Any) -> str:
    if isinstance(val, (int, float)):
        if val >= 0.8:
            return "confirmed"
        elif val >= 0.5:
            return "traditional"
        else:
            return "disputed"
    if isinstance(val, str):
        v = val.strip().lower()
        if v in {"confirmed", "traditional", "disputed", "contextual"}:
            return v
    return "confirmed"


def normalize_engine_b(en_path: Path) -> dict:
    d = load(en_path)
    date_str = d.get("date", "")
    vi_path = None
    nm = en_path.name
    if nm.endswith("_result_en.json"):
        vi_path = en_path.with_name(nm.replace("_result_en.json", "_result_vi.json"))
    elif nm.endswith("_result.json"):
        vi_path = en_path.with_name(nm.replace("_result.json", "_result_vi.json"))
    vi = load(vi_path) if vi_path and vi_path.exists() else None
    e = merge_vi(d, vi)
    e["id"] = norm_id(d.get("id", ""), date_str)
    e["mock_priority"] = "engine_b_v1"  # pipeline-version marker required by the validation gate
    e["primary"]["type"] = map_type(e["primary"].get("type"))
    rank = (e.get("liturgical", {}).get("rank") or "").strip().lower()
    if rank in RANK_MAP:
        e["liturgical"]["rank"] = RANK_MAP[rank]
    if "confidence" in e.get("primary", {}):
        e["primary"]["confidence"] = map_confidence(e["primary"]["confidence"])
    if isinstance(e.get("place"), dict) and "confidence" in e["place"]:
        e["place"]["confidence"] = map_confidence(e["place"]["confidence"])
    color = e.get("liturgical", {}).get("color", "")
    if color and color.lower() not in COLOR_OK:
        raise ValueError(f"unknown liturgical color {color!r} for {date_str}")
    e["liturgical"]["color"] = color.strip().lower()
    if "sources" in e and isinstance(e["sources"], list):
        e["sources"] = normalize_sources(e["sources"])
    return e


def validate_required_feast_vi(entry: dict) -> None:
    """Do not mask missing major-feast Vietnamese copy by copying English into it.

    This intentionally validates the raw source/overlay before ensure_vi fallback,
    because the normalizer still permits EN fallback on non-priority weekdays.
    """
    day = entry.get("date")
    if day not in VI_REQUIRED_DATES:
        return
    for section, key in (
        ("liturgical", "title"), ("primary", "title"),
        ("primary", "summary"), ("primary", "body"),
        ("primary", "confidence_note"),
        ("app_hooks", "hero_line"), ("app_hooks", "prayer_prompt"),
    ):
        values = entry.get(section) or {}
        en = values.get(f"{key}_en", "")
        vi = values.get(f"{key}_vi", "")
        if not isinstance(vi, str) or not vi.strip():
            raise ValueError(f"{day}: required {section}.{key}_vi is empty")
        if not isinstance(en, str) or not en.strip():
            raise ValueError(f"{day}: required {section}.{key}_en is empty")
        if vi.strip().casefold() == en.strip().casefold():
            raise ValueError(f"{day}: English copied into required {section}.{key}_vi")
        if re.search(r"\b(?:Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday)\b",
                     vi, re.IGNORECASE):
            raise ValueError(f"{day}: untranslated weekday in {section}.{key}_vi")


def _string(value: Any) -> str:
    """Coerce a Swift-compatible String value to a JSON string."""
    return value.strip() if isinstance(value, str) else ""


def _number(value: Any) -> float | None:
    """Return a JSON number that Swift can decode as Double, or None."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def sanitize_place(entry: dict) -> None:
    """Emit a place only when every Swift-required field is usable.

    `SacredPlace` is optional in Swift, but when present its name, coordinates,
    confidence and sourceUrl are all non-optional. A partial object would make
    the whole fixture undecodable.
    """
    place = entry.get("place")
    if not isinstance(place, dict):
        entry["place"] = None
        return

    name = _string(place.get("name"))
    latitude = _number(place.get("latitude"))
    longitude = _number(place.get("longitude"))
    confidence = map_confidence(place.get("confidence"))
    source_url = _string(place.get("source_url"))

    if not name or latitude is None or longitude is None or confidence not in CONFIDENCE_OK or not source_url:
        entry["place"] = None
        return

    entry["place"] = {
        "name": name,
        "latitude": latitude,
        "longitude": longitude,
        "confidence": confidence,
        "source_url": source_url,
    }


def sanitize_artwork(entry: dict) -> None:
    """Emit an artwork object matching Swift's non-optional String contract."""
    artwork = entry.get("artwork") if isinstance(entry.get("artwork"), dict) else {}
    status_raw = _string(artwork.get("status")).lower().replace(" ", "_")
    status = ARTWORK_STATUS_MAP.get(status_raw, "placeholder_only")
    entry["artwork"] = {
        "title": _string(artwork.get("title")),
        "maker": _string(artwork.get("maker")),
        "date_label": _string(artwork.get("date_label")),
        "source_url": _string(artwork.get("source_url")),
        "status": status,
    }


def sanitize_sources(entry: dict) -> None:
    """Keep only source refs with the three non-optional Swift fields."""
    sources = entry.get("sources")
    if not isinstance(sources, list):
        entry["sources"] = []
        return

    sanitized = []
    for source in sources:
        if not isinstance(source, dict):
            continue
        label = _string(source.get("label"))
        url = _string(source.get("url"))
        type_ = _string(source.get("type")) or "reference"
        if not label:
            label = url
        if label and url:
            sanitized.append({"label": label, "url": url, "type": type_})
    entry["sources"] = sanitized


def validate_entry_contract(entry: dict) -> list[str]:
    """Validate the exact JSON shape required by AnnoEntry's Codable contract."""
    issues: list[str] = []

    def require_dict(section: str) -> dict:
        value = entry.get(section)
        if not isinstance(value, dict):
            issues.append(f"{section}: not an object")
            return {}
        return value

    def require_string(section: dict, field: str) -> None:
        value = section.get(field)
        if not isinstance(value, str):
            issues.append(f"{field}: not a string")

    for field in ("id", "date", "weekday", "mock_priority"):
        require_string(entry, field)

    liturgical = require_dict("liturgical")
    for field in ("rank", "color", "title_en", "title_vi"):
        require_string(liturgical, field)

    calendars = require_dict("calendars")
    for field in ("julian", "hebrew", "islamic_umm_al_qura", "coptic", "ethiopian"):
        require_string(calendars, field)

    primary = require_dict("primary")
    for field in ("type", "title_en", "title_vi", "summary_en", "summary_vi",
                  "confidence", "confidence_note_en", "confidence_note_vi",
                  "body_en", "body_vi"):
        require_string(primary, field)
    if primary.get("confidence") not in CONFIDENCE_OK:
        issues.append(f"primary.confidence: {primary.get('confidence')!r} is not a supported enum")

    place = entry.get("place")
    if place is not None:
        if not isinstance(place, dict):
            issues.append("place: not an object")
        else:
            require_string(place, "name")
            require_string(place, "source_url")
            for field in ("latitude", "longitude"):
                value = place.get(field)
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    issues.append(f"place.{field}: not a number")
            if place.get("confidence") not in CONFIDENCE_OK:
                issues.append(f"place.confidence: {place.get('confidence')!r} is not a supported enum")

    artwork = require_dict("artwork")
    for field in ("title", "maker", "date_label", "source_url", "status"):
        require_string(artwork, field)

    sources = entry.get("sources")
    if not isinstance(sources, list):
        issues.append("sources: not an array")
    else:
        for i, source in enumerate(sources):
            if not isinstance(source, dict):
                issues.append(f"sources[{i}]: not an object")
                continue
            for field in ("label", "url", "type"):
                if not isinstance(source.get(field), str):
                    issues.append(f"sources[{i}].{field}: not a string")

    app_hooks = require_dict("app_hooks")
    for field in ("hero_line_en", "hero_line_vi", "prayer_prompt_en", "prayer_prompt_vi"):
        require_string(app_hooks, field)

    return issues


def ensure_vi(entry: dict) -> dict:
    """Guarantee every *_vi AND *_en leaf exists. If one locale is missing, fall back
    to the other so the Swift decoder never sees an empty string in either language."""
    def fill(section, key):
        sec = entry.get(section)
        if not isinstance(sec, dict):
            return
        en = sec.get(f"{key}_en", "")
        vi = sec.get(f"{key}_vi", "")
        if not (isinstance(en, str) and en.strip()):
            sec[f"{key}_en"] = vi
        if not (isinstance(vi, str) and vi.strip()):
            sec[f"{key}_vi"] = en
    fill("liturgical", "title")
    fill("primary", "title")
    fill("primary", "summary")
    fill("primary", "body")
    fill("primary", "confidence_note")
    fill("app_hooks", "hero_line")
    fill("app_hooks", "prayer_prompt")
    return entry


def ingest_range(start_date: date, end_date: date) -> list:
    """Ingest every research_results/<date>_result.json in [start,end] (with _vi overlay)."""
    entries = []
    cur = start_date
    while cur <= end_date:
        d_str = cur.isoformat()
        p_en = RESEARCH / f"{d_str}_result_en.json"
        p_raw = RESEARCH / f"{d_str}_result.json"
        p = p_en if p_en.exists() else p_raw
        if p.exists():
            entries.append(normalize_engine_b(p))
        cur += timedelta(days=1)
    return entries


def normalize_generic_entry(entry: dict, date_str: str) -> dict:
    """Apply standard normalization to any entry (fortnight, august, engine_b)."""
    e = json.loads(json.dumps(entry))  # deep copy
    e["id"] = norm_id(e.get("id", ""), date_str)
    e["mock_priority"] = e.get("mock_priority", "fortnight_mock" if "fortnight" in date_str else "august_mock")
    e["primary"]["type"] = map_type(e["primary"].get("type"))
    rank = (e.get("liturgical", {}).get("rank") or "").strip().lower()
    if rank in RANK_MAP:
        e["liturgical"]["rank"] = RANK_MAP[rank]
    if "confidence" in e.get("primary", {}):
        e["primary"]["confidence"] = map_confidence(e["primary"]["confidence"])
    if isinstance(e.get("place"), dict) and "confidence" in e["place"]:
        e["place"]["confidence"] = map_confidence(e["place"]["confidence"])
    color = e.get("liturgical", {}).get("color", "")
    if color and color.lower() not in COLOR_OK:
        raise ValueError(f"unknown liturgical color {color!r} for {date_str}")
    e["liturgical"]["color"] = color.strip().lower()
    if "sources" in e and isinstance(e["sources"], list):
        e["sources"] = normalize_sources(e["sources"])
    return e


def main() -> None:
    import argparse
    import sys
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, default=2026, help="Year to build a fixture for (default 2026)")
    ap.add_argument("--out", type=str, default=None, help="Output path (default Anno/Resources/anno_unified_<year>.json)")
    args = ap.parse_args()

    entries = []
    if args.year == 2026:
        # Preserve the exact 2026 construction (fortnight + august mock + Sep–Dec research).
        # BUT: normalize ALL tracks consistently.
        fort = load(FORTNIGHT)
        for e in fort["entries"]:
            entries.append(normalize_generic_entry(e, e.get("date", "")))
        for day in range(17, 32):
            p_en = RESEARCH / f"2026-07-{day:02d}_result_en.json"
            p_raw = RESEARCH / f"2026-07-{day:02d}_result.json"
            p = p_en if p_en.exists() else p_raw
            if p.exists():
                entries.append(normalize_engine_b(p))
        aug = load(AUGUST)
        assert isinstance(aug, list), "august file should be a list"
        for e in aug:
            entries.append(normalize_generic_entry(e, e.get("date", "")))
        entries.extend(ingest_range(date(2026, 9, 1), date(2026, 12, 31)))
    else:
        # Any other year: ingest the whole year from research_results.
        entries.extend(ingest_range(date(args.year, 1, 1), date(args.year, 12, 31)))

    # Dedupe by id (keep first), sort chronologically by date
    by_id = {}
    for e in entries:
        by_id.setdefault(e["id"], e)
    sorted_entries = sorted(by_id.values(), key=lambda e: e.get("date", ""))
    if args.year == 2026:
        observed_required = {e.get("date") for e in sorted_entries} & VI_REQUIRED_DATES
        if observed_required != VI_REQUIRED_DATES:
            raise ValueError(f"Missing major feast source dates: {sorted(VI_REQUIRED_DATES - observed_required)}")
    for e in sorted_entries:
        validate_required_feast_vi(e)
    final = [ensure_vi(e) for e in sorted_entries]
    for entry in final:
        sanitize_place(entry)
        sanitize_artwork(entry)
        sanitize_sources(entry)

    # BLOCKING VALIDATOR: exact Swift Codable contract, not just key presence.
    contract_issues = []
    for entry in final:
        issues = validate_entry_contract(entry)
        for issue in issues:
            contract_issues.append(f"Entry (id={entry.get('id')}): {issue}")

    if contract_issues:
        print("VALIDATION FAILED - fixture violates Swift AnnoEntry contract:", file=sys.stderr)
        for msg in contract_issues:
            print(f"  {msg}", file=sys.stderr)
        sys.exit(1)

    # Validate VI completeness (only enforce for VI_REQUIRED_DATES)
    vi_empty = 0
    vi_tot = 0
    no_src = 0

    def walk(x):
        nonlocal vi_empty, vi_tot
        if isinstance(x, dict):
            for k, v in x.items():
                if k.endswith("_vi"):
                    vi_tot += 1
                    if not (isinstance(v, str) and v.strip()):
                        vi_empty += 1
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    for e in final:
        if len(e.get("sources", [])) < 2:
            no_src += 1
        # Only enforce VI completeness for required dates
        entry_date = e.get("date", "")
        if entry_date in VI_REQUIRED_DATES:
            walk(e)
        else:
            # For non-required dates, just count but don't fail on empty VI
            def walk_count(x):
                nonlocal vi_tot
                if isinstance(x, dict):
                    for k, v in x.items():
                        if k.endswith("_vi"):
                            vi_tot += 1
                        walk_count(v)
                elif isinstance(x, list):
                    for v in x:
                        walk_count(v)
            walk_count(e)

    # Fail only on required-date VI empties
    if vi_empty > 0:
        print(f"VALIDATION FAILED - {vi_empty} empty *_vi fields on required dates", file=sys.stderr)
        sys.exit(1)

    if no_src > 0:
        print(f"VALIDATION FAILED - {no_src} entries with <2 sources", file=sys.stderr)
        sys.exit(1)

    OUT = Path(args.out) if args.out else (ROOT / f"Anno/Resources/anno_unified_{args.year}.json")
    # Swift requires generatedOn. Use the last fixture date as a deterministic marker
    # instead of wall-clock time, so regeneration remains byte-identical.
    generated_on = final[-1].get("date", "") if final else ""
    out = {
        "schema_version": "1.0",
        "generated_on": generated_on,
        "total_entries": len(final),
        "entries": final,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # Determinism: build metadata (incl. any volatile timestamp) lives in a sidecar
    # so the fixture itself regenerates byte-identically.
    meta_path = OUT.parent / (OUT.stem + ".meta.json")
    meta = {"generated_on": date.today().isoformat(), "total_entries": len(final),
            "source": OUT.name}
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
        f.write("\n")

    span = f"{final[0].get('date','?')} -> {final[-1].get('date','?')}" if final else "n/a"
    print(f"Master Unified Fixture ({args.year}): {len(final)} entries ({span})")
    print(f"  VI fields: {vi_tot} total, {vi_empty} empty")
    print(f"  Entries with <2 sources: {no_src}")
    print(f"  Written: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
