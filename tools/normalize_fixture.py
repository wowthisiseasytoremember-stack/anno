#!/usr/bin/env python3
"""Normalize the three Anno content tracks into one Swift-fixture-ready dataset.

Tracks (date-disjoint):
  - data/mock/anno_fortnight_2026-07-03_2026-07-16.json  (14 entries, EN+VI, 0 sources)
  - data/research_results/2026-07-{17..30}_result_en.json (Engine B, EN only)
        + sibling _result_vi.json for Vietnamese
  - data/mock/anno_august_2026.json                        (31 entries, EN+VI, 0 sources)

Output: Anno/Resources/anno_unified_2026.json  -- a single {"schema_version","generated_on","entries":[...]}
shaped to match the Swift AnnoEntry decoder (see export_swift_fixture.py header).

Engine B quirks handled:
  - id format "2026-07-18-bvm-saturday" -> normalized to "anno-2026-07-18"
  - primary.type sometimes holds a rank ("Optional Memorial"); remapped to a type when recognized
  - liturgical.color capitalized ("White") -> lowercase
  - *_vi pulled from the sibling _result_vi.json
"""
from __future__ import annotations
import json, re, shutil
from datetime import date
from pathlib import Path

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
COLOR_OK = {"white", "red", "green", "purple", "gold", "rose", "verdigris", "black"}


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def norm_id(raw: str, date_str: str) -> str:
    # Engine B uses "2026-07-18-bvm-saturday"; normalize to anno-YYYY-MM-DD
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


def normalize_engine_b(en_path: Path) -> dict:
    d = load(en_path)
    date_str = d.get("date", "")
    vi_path = None
    nm = en_path.name
    if nm.endswith("_result_en.json"):
        vi_path = en_path.with_name(nm.replace("_result_en.json", "_result_vi.json"))
    elif nm.endswith("_result.json"):
        vi_path = en_path.with_name(nm.replace("_result.json", "_result_vi.json"))
    vi = load(vi_path) if vi_path.exists() else None
    e = merge_vi(d, vi)
    e["id"] = norm_id(d.get("id", ""), date_str)
    e["primary"]["type"] = map_type(e["primary"].get("type"))
    color = e.get("liturgical", {}).get("color", "")
    if color and color.lower() not in COLOR_OK:
        e["liturgical"]["color"] = color.lower()
    return e


def ensure_vi(entry: dict) -> dict:
    """Guarantee every *_vi leaf exists (defaults to EN sibling) so the
    Swift decoder never KeyError's on missing Vietnamese."""
    def fill(section, key):
        sec = entry.get(section)
        if not isinstance(sec, dict):
            return
        en = sec.get(f"{key}_en", "")
        if not sec.get(f"{key}_vi"):
            sec[f"{key}_vi"] = en
    fill("liturgical", "title")
    fill("primary", "title")
    fill("primary", "summary")
    fill("primary", "body")
    fill("primary", "confidence_note")
    fill("app_hooks", "hero_line")
    fill("app_hooks", "prayer_prompt")
    return entry


def main() -> None:
    entries = []

    # 1. Fortnight (already EN+VI)
    fort = load(FORTNIGHT)
    for e in fort["entries"]:
        entries.append(e)

    # 2. Engine B 07-17..07-30
    for day in range(17, 31):
        p_en = RESEARCH / f"2026-07-{day:02d}_result_en.json"
        p_raw = RESEARCH / f"2026-07-{day:02d}_result.json"
        p = p_en if p_en.exists() else p_raw
        if p.exists():
            entries.append(normalize_engine_b(p))

    # 3. August (already EN+VI, VN-complete after fold)
    aug = load(AUGUST)
    assert isinstance(aug, list), "august file should be a list"
    entries.extend(aug)

    # Dedupe by id (keep first), sort by date
    by_id = {}
    for e in entries:
        by_id.setdefault(e["id"], e)
    final = [ensure_vi(e) for e in sorted(by_id.values(), key=lambda e: e.get("date", ""))]

    out = {
        "schema_version": "1.0",
        "generated_on": date.today().isoformat(),
        "entries": final,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=2)

    # Report
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
    print(f"Unified fixture: {len(final)} entries")
    print(f"  VI fields: {vi_tot} total, {vi_empty} empty")
    print(f"  Entries with <2 sources: {no_src}")
    print(f"  Written: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
