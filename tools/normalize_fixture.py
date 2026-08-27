#!/usr/bin/env python3
"""Normalize all Anno content tracks into one continuous Swift-fixture-ready dataset.

Tracks (July 3, 2026 – December 31, 2026 = 182 days):
  - data/mock/anno_fortnight_2026-07-03_2026-07-16.json  (14 entries, EN+VI, verified sources)
  - data/research_results/2026-07-{17..31}_result.json (Engine B July track)
  - data/mock/anno_august_2026.json (31 entries, EN+VI, verified sources)
  - data/research_results/2026-{09..12}-*_result.json (Engine B Sep-Dec track, 122 days)

Output: Anno/Resources/anno_unified_2026.json -- a single {"schema_version","generated_on","entries":[...]}
shaped to match the Swift AnnoEntry decoder (see export_swift_fixture.py header).
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
        e["liturgical"]["color"] = color.lower()
    if "sources" in e and isinstance(e["sources"], list):
        e["sources"] = normalize_sources(e["sources"])
    return e


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


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, default=2026, help="Year to build a fixture for (default 2026)")
    ap.add_argument("--out", type=str, default=None, help="Output path (default Anno/Resources/anno_unified_<year>.json)")
    args = ap.parse_args()

    entries = []
    if args.year == 2026:
        # Preserve the exact 2026 construction (fortnight + august mock + Sep–Dec research).
        fort = load(FORTNIGHT)
        for e in fort["entries"]:
            entries.append(e)
        for day in range(17, 32):
            p_en = RESEARCH / f"2026-07-{day:02d}_result_en.json"
            p_raw = RESEARCH / f"2026-07-{day:02d}_result.json"
            p = p_en if p_en.exists() else p_raw
            if p.exists():
                entries.append(normalize_engine_b(p))
        aug = load(AUGUST)
        assert isinstance(aug, list), "august file should be a list"
        entries.extend(aug)
        entries.extend(ingest_range(date(2026, 9, 1), date(2026, 12, 31)))
    else:
        # Any other year: ingest the whole year from research_results.
        entries.extend(ingest_range(date(args.year, 1, 1), date(args.year, 12, 31)))

    # Dedupe by id (keep first), sort chronologically by date
    by_id = {}
    for e in entries:
        by_id.setdefault(e["id"], e)
    final = [ensure_vi(e) for e in sorted(by_id.values(), key=lambda e: e.get("date", ""))]

    OUT = Path(args.out) if args.out else (ROOT / f"Anno/Resources/anno_unified_{args.year}.json")
    out = {
        "schema_version": "1.0",
        "generated_on": date.today().isoformat(),
        "total_entries": len(final),
        "entries": final,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    # Report validation metrics
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
        walk(e)

    span = f"{final[0].get('date','?')} -> {final[-1].get('date','?')}" if final else "n/a"
    print(f"Master Unified Fixture ({args.year}): {len(final)} entries ({span})")
    print(f"  VI fields: {vi_tot} total, {vi_empty} empty")
    print(f"  Entries with <2 sources: {no_src}")
    print(f"  Written: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
