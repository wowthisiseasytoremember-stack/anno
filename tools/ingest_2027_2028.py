#!/usr/bin/env python3
"""Ingest Anno 2027-2028: merge seed catalog with Engine B research returns.

Takes the seed (data/seed/anno_seed_2027_2028.json, 731 day objects with
date/weekday/liturgical/calendars) plus one or more returned Engine B JSON
files (data/research_tentative/2027_2028/anno_handoff_<chunk>.json), matched
by date.

Per returned entry we keep the seed's `liturgical` + `calendars`, and adopt
the returned `primary`, `place`, `artwork`, `sources`, `app_hooks`,
`weekday`, `mock_priority`.

Emits Anno/Resources/anno_unified_2027_2028.json in the SAME top-level shape
as anno_unified_2026.json ({"schema_version","generated_on","total_entries",
"entries":[...]}), guaranteeing 100% of `*_vi` leaves (fallback to EN).

Does NOT crash on empty input: if no returned research exists yet, it emits a
seed-only scaffold (all dates present, primary marked "PENDING_RESEARCH").
"""
from __future__ import annotations

import argparse
import glob
import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SEED = ROOT / "data/seed/anno_seed_2027_2028.json"
DEFAULT_IN_DIR = ROOT / "data/research_tentative/2027_2028"
DEFAULT_OUT = ROOT / "Anno/Resources/anno_unified_2027_2028.json"

PENDING = "PENDING_RESEARCH"


def load(p: Path) -> Any:
    return json.loads(Path(p).read_text(encoding="utf-8"))


def norm_id(raw: str, date_str: str) -> str:
    import re
    m = re.match(r"(\d{4}-\d{2}-\d{2})", raw or "")
    if m:
        return f"anno-{m.group(1)}"
    return f"anno-{date_str}" if date_str else raw


# reflects normalize_fixture.ensure_vi: guarantee every *_vi leaf exists,
# defaulting to its *_en sibling so the Swift decoder never KeyError's.
VI_FIELDS = [
    ("liturgical", "title"),
    ("primary", "title"),
    ("primary", "summary"),
    ("primary", "body"),
    ("primary", "confidence_note"),
    ("app_hooks", "hero_line"),
    ("app_hooks", "prayer_prompt"),
]


def ensure_vi(entry: dict) -> dict:
    for section, key in VI_FIELDS:
        sec = entry.get(section)
        if not isinstance(sec, dict):
            continue
        en = sec.get(f"{key}_en", "")
        if not sec.get(f"{key}_vi"):
            sec[f"{key}_vi"] = en
    return entry


def pending_entry(seed: dict) -> dict:
    """Seed-only scaffold entry: obvious non-shippable marker."""
    d = seed["date"]
    return {
        "id": norm_id(seed.get("id", ""), d),
        "date": d,
        "weekday": seed.get("weekday", ""),
        "mock_priority": PENDING,
        "liturgical": json.loads(json.dumps(seed.get("liturgical", {}))),
        "calendars": json.loads(json.dumps(seed.get("calendars", {}))),
        "primary": {
            "type": "liturgical_day",
            "title_en": PENDING,
            "title_vi": PENDING,
            "summary_en": PENDING,
            "summary_vi": PENDING,
            "body_en": PENDING,
            "body_vi": PENDING,
            "confidence": "confirmed",
            "confidence_note_en": PENDING,
            "confidence_note_vi": PENDING,
        },
        "place": None,
        "artwork": {
            "title": PENDING,
            "maker": PENDING,
            "date_label": PENDING,
            "source_url": "",
            "status": "placeholder_only",
        },
        "sources": [],
        "app_hooks": {
            "hero_line_en": PENDING,
            "hero_line_vi": PENDING,
            "prayer_prompt_en": PENDING,
            "prayer_prompt_vi": PENDING,
        },
    }


def merge_entry(seed: dict, ret: dict) -> dict:
    d = seed["date"]
    out = {
        "id": norm_id(ret.get("id", ""), d),
        "date": d,
        "weekday": ret.get("weekday", seed.get("weekday", "")),
        "mock_priority": ret.get("mock_priority", PENDING),
        "liturgical": json.loads(json.dumps(seed.get("liturgical", {}))),
        "calendars": json.loads(json.dumps(seed.get("calendars", {}))),
        "primary": json.loads(json.dumps(ret.get("primary", {}))),
        "place": ret.get("place"),
        "artwork": json.loads(json.dumps(ret.get("artwork", {}))),
        "sources": json.loads(json.dumps(ret.get("sources", []))),
        "app_hooks": json.loads(json.dumps(ret.get("app_hooks", {}))),
    }
    return out


def load_research(in_files: list[Path]) -> dict[str, dict]:
    """Returned Engine B entries keyed by date."""
    by_date: dict[str, dict] = {}
    for f in in_files:
        data = load(f)
        if isinstance(data, dict) and "entries" in data:
            items = data["entries"]
        elif isinstance(data, list):
            items = data
        else:
            items = []
        for e in items:
            if isinstance(e, dict) and e.get("date"):
                by_date[e["date"]] = e
    return by_date


def collect_in_files(args: argparse.Namespace) -> list[Path]:
    files: list[Path] = []
    if args.in_file:
        for p in args.in_file:
            files.append(Path(p))
    if args.in_dir:
        d = Path(args.in_dir)
        if d.exists():
            files.extend(Path(p) for p in sorted(glob.glob(str(d / "anno_handoff_*.json"))))
            # also accept a pre-made sample/array chunk file for dry-runs
            files.extend(Path(p) for p in sorted(glob.glob(str(d / "sample_chunk*.json"))))
    # de-dup
    seen = set()
    uniq = []
    for p in files:
        if str(p) not in seen:
            seen.add(str(p))
            uniq.append(p)
    return uniq


def main() -> None:
    ap = argparse.ArgumentParser(description="Ingest Anno 2027-2028 seed + Engine B research")
    ap.add_argument("--seed", default=str(DEFAULT_SEED), help="Seed catalog JSON")
    ap.add_argument("--in-dir", default=str(DEFAULT_IN_DIR), help="Dir of returned Engine B handoff files")
    ap.add_argument("--in-file", action="append", default=[], help="Explicit returned Engine B file (repeatable)")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="Output unified JSON path")
    args = ap.parse_args()

    seed = load(args.seed)
    if isinstance(seed, dict) and "entries" in seed:
        seed_list = seed["entries"]
    elif isinstance(seed, list):
        seed_list = seed
    else:
        raise SystemExit("Seed must be a list or {'entries': [...]}")

    in_files = collect_in_files(args)
    research = load_research(in_files)

    entries = []
    with_research = 0
    for s in seed_list:
        d = s.get("date")
        if not d:
            continue
        if d in research:
            entries.append(merge_entry(s, research[d]))
            with_research += 1
        else:
            entries.append(pending_entry(s))

    for e in entries:
        ensure_vi(e)

    entries.sort(key=lambda e: e.get("date", ""))

    # metrics
    vi_empty = 0
    vi_tot = 0

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

    for e in entries:
        walk(e)

    out = {
        "schema_version": "1.0",
        "generated_on": date.today().isoformat(),
        "total_entries": len(entries),
        "entries": entries,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    pending = len(entries) - with_research
    print(f"Ingest 2027-2028: {len(entries)} total dates")
    print(f"  With research:    {with_research}")
    print(f"  Pending research: {pending}")
    print(f"  *_vi leaves:      {vi_tot} total, {vi_empty} empty")
    if vi_empty:
        print("  WARNING: missing *_vi present!")
    try:
        disp = out_path.relative_to(ROOT)
    except ValueError:
        disp = out_path
    print(f"  Written: {disp}")


if __name__ == "__main__":
    main()
