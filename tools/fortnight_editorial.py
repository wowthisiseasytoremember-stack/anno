#!/usr/bin/env python3
"""Editorial source / generated-fixture gate for ANNO's full July 3–16, 2026 tranche.

US Catholic observance ranks, colors and Gospel references come from the
USCCB 2026 calendar, July printed pp. 31–32:
  https://www.usccb.org/resources/2026cal.pdf

This gate checks exactly 14 records on Linux, offline. It does NOT establish
theological review, VI translation approval, art rights, URL reachability or
iOS VoiceOver/Dynamic Type validation.

  python3 tools/fortnight_editorial.py audit
  python3 tools/fortnight_editorial.py new --date 2027-07-03 --output /tmp/day.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/mock/anno_fortnight_2026-07-03_2026-07-16.json"
FIXTURE = ROOT / "Anno/Resources/anno_unified_2026.json"
CALENDAR_URL = "https://www.usccb.org/resources/2026cal.pdf"
USCCB_BASE = "https://bible.usccb.org/bible/readings/"

# Locks date-sensitive identity, instead of trusting fluent but incorrect
# generated copy. Optional US memorials (July 6, 9, 13, 16) are not mandatory.
# English / Vietnamese names are app display labels, not USCCB text quotations.
AUTHORITY = {
    "2026-07-03": ("Feast of Saint Thomas, Apostle", "Lễ kính Thánh Tôma Tông đồ", "Feast", "red", "feast", "John 20:24-29"),
    "2026-07-04": ("Saturday of the Thirteenth Week in Ordinary Time", "Thứ Bảy Tuần XIII Mùa Thường Niên", "Feria", "green", "liturgical_day", "Matthew 9:14-17"),
    "2026-07-05": ("Fourteenth Sunday in Ordinary Time", "Chúa Nhật XIV Mùa Thường Niên", "Sunday", "green", "liturgical_day", "Matthew 11:25-30"),
    "2026-07-06": ("Monday of the Fourteenth Week in Ordinary Time", "Thứ Hai Tuần XIV Mùa Thường Niên", "Feria", "green", "liturgical_day", "Matthew 9:18-26"),
    "2026-07-07": ("Tuesday of the Fourteenth Week in Ordinary Time", "Thứ Ba Tuần XIV Mùa Thường Niên", "Feria", "green", "liturgical_day", "Matthew 9:32-38"),
    "2026-07-08": ("Wednesday of the Fourteenth Week in Ordinary Time", "Thứ Tư Tuần XIV Mùa Thường Niên", "Feria", "green", "liturgical_day", "Matthew 10:1-7"),
    "2026-07-09": ("Thursday of the Fourteenth Week in Ordinary Time", "Thứ Năm Tuần XIV Mùa Thường Niên", "Feria", "green", "liturgical_day", "Matthew 10:7-15"),
    "2026-07-10": ("Friday of the Fourteenth Week in Ordinary Time", "Thứ Sáu Tuần XIV Mùa Thường Niên", "Feria", "green", "liturgical_day", "Matthew 10:16-23"),
    "2026-07-11": ("Memorial of Saint Benedict, Abbot", "Lễ nhớ Thánh Biển Đức, viện phụ", "Memorial", "white", "memorial", "Matthew 10:24-33"),
    "2026-07-12": ("Fifteenth Sunday in Ordinary Time", "Chúa Nhật XV Mùa Thường Niên", "Sunday", "green", "liturgical_day", "Matthew 13:1-23"),
    "2026-07-13": ("Monday of the Fifteenth Week in Ordinary Time", "Thứ Hai Tuần XV Mùa Thường Niên", "Feria", "green", "liturgical_day", "Matthew 10:34-11:1"),
    "2026-07-14": ("Memorial of Saint Kateri Tekakwitha, Virgin", "Lễ nhớ Thánh Kateri Tekakwitha, trinh nữ", "Memorial", "white", "memorial", "Matthew 11:20-24"),
    "2026-07-15": ("Memorial of Saint Bonaventure, Bishop and Doctor of the Church", "Lễ nhớ Thánh Bônaventura, giám mục và tiến sĩ Hội Thánh", "Memorial", "white", "memorial", "Matthew 11:25-27"),
    "2026-07-16": ("Thursday of the Fifteenth Week in Ordinary Time", "Thứ Năm Tuần XV Mùa Thường Niên", "Feria", "green", "liturgical_day", "Matthew 11:28-30"),
}
TEXT_FIELDS = (
    ("liturgical", "title"), ("primary", "title"), ("primary", "summary"),
    ("primary", "body"), ("primary", "confidence_note"),
    ("app_hooks", "hero_line"), ("app_hooks", "prayer_prompt"),
)
UNTRANSLATED_WEEKDAY = re.compile(
    r"\b(?:Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday)\b", re.I
)
BOILERPLATE = ("a day of ordinary time to grow in daily faith",
               "on this friday of ordinary time",
               "on this saturday of ordinary time",
               "annual marian days festival gathering",
               "the church invites the faithful to enter deeply into the sacred rhythm")
ART_PLACEHOLDER = "Artwork not selected (editorial placeholder)"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(source, fixture) -> list[str]:
    errors: list[str] = []
    if not isinstance(source, dict) or not isinstance(source.get("entries"), list):
        return ["Source requires an entries array"]
    items = source["entries"]
    expected_dates = list(AUTHORITY)
    got_dates = [e.get("date") for e in items]
    if len(items) != 14 or got_dates != expected_dates:
        errors.append("Source must contain exactly 14 ordered days July 3 through July 16, with no duplicates")
    if fixture.get("total_entries") != len(fixture.get("entries", [])):
        errors.append("Runtime fixture total_entries differs from actual count")
    if len(fixture.get("entries", [])) != 182:
        errors.append("The 2026 normalized fixture must retain 182 total days")
    compiled = fixture.get("entries", [])
    for day, (name_en, name_vi, rank, color, primary_type, gospel) in AUTHORITY.items():
        a = [e for e in items if e.get("date") == day]
        b = [e for e in compiled if e.get("date") == day]
        if len(a) != 1 or len(b) != 1:
            errors.append(f"{day}: source/fixture must each contain exactly one entry, got {len(a)} / {len(b)}")
            continue
        e, f = a[0], b[0]
        if e != f:
            errors.append(f"{day}: source content differs from generated fixture")
        if e.get("id") != f"anno-{day}":
            errors.append(f"{day}: stable native ID mismatch")
        if e.get("weekday") != date.fromisoformat(day).strftime("%A"):
            errors.append(f"{day}: weekday does not match actual Gregorian date")
        lit = e.get("liturgical") or {}
        if (lit.get("title_en"), lit.get("title_vi")) != (name_en, name_vi):
            errors.append(f"{day}: official English/Vietnamese display title mismatch")
        if (lit.get("rank"), lit.get("color")) != (rank, color):
            errors.append(f"{day}: rank/color differs from official USCCB calendar")
        pri = e.get("primary") or {}
        if pri.get("type") != primary_type:
            errors.append(f"{day}: primary.type does not match observance")
        if pri.get("confidence") != "confirmed":
            errors.append(f"{day}: calendar identity must use confirmed confidence")
        if gospel not in pri.get("confidence_note_en", ""):
            errors.append(f"{day}: reading attribution lacks {gospel}")
        for section, stem in TEXT_FIELDS:
            obj = e.get(section) or {}
            en, vi = obj.get(stem + "_en"), obj.get(stem + "_vi")
            if not isinstance(en, str) or not en.strip():
                errors.append(f"{day}: missing {section}.{stem}_en")
            if not isinstance(vi, str) or not vi.strip():
                errors.append(f"{day}: missing {section}.{stem}_vi")
            if (isinstance(en, str) and isinstance(vi, str)
                    and en.strip().casefold() == vi.strip().casefold()):
                errors.append(f"{day}: English copied into {section}.{stem}_vi")
            if isinstance(vi, str) and UNTRANSLATED_WEEKDAY.search(vi):
                errors.append(f"{day}: untranslated English weekday in {section}.{stem}_vi")
        for stem in ("summary_en", "body_en", "hero_line_en"):
            obj = (pri if stem.startswith(("summary", "body")) else e.get("app_hooks", {}))
            if not isinstance(obj, dict):
                errors.append(f"{day}: missing content section for {stem}")
                continue
            value = (obj.get(stem) or "").lower()
            if any(x in value for x in BOILERPLATE):
                errors.append(f"{day}: recycled placeholder/incorrect devotional framing in {stem}")
        sources = e.get("sources", [])
        urls = [s.get("url") for s in sources if isinstance(s, dict)]
        dated_url = f"{USCCB_BASE}{day[5:7]}{day[8:10]}26.cfm"
        if dated_url not in urls or CALENDAR_URL not in urls:
            errors.append(f"{day}: must cite dated USCCB readings and 2026 national calendar")
        if len(set(urls)) != len(urls) or len(urls) < 2:
            errors.append(f"{day}: require at least two distinct source URLs")
        for url in urls:
            parsed = urlsplit(url or "")
            if parsed.scheme != "https" or not parsed.netloc or "example." in parsed.netloc:
                errors.append(f"{day}: invalid/placeholder source URL {url!r}")
        art = e.get("artwork") or {}
        if art.get("status") != "placeholder_only" or art.get("source_url") not in ("", None):
            errors.append(f"{day}: unlicensed/placeholder artwork must never be cleared or have a fake URL")
        if e.get("place") is not None:
            errors.append(f"{day}: invented place must be null until actual location+source verified")
        if "_editorial" in e:
            errors.append(f"{day}: nonshipping editorial scaffold metadata included in runtime")
    # Prevent a few unique summaries being reused between different dates.
    summaries = [(e.get("primary") or {}).get("summary_en") for e in items]
    if len(summaries) != len(set(summaries)):
        errors.append("Duplicate EN daily summaries across the 14-day tranche")
    return errors


def scaffold(day: str, output: Path):
    parsed = date.fromisoformat(day)
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite existing draft: {output}")
    marker = "TODO: author from the dated official calendar and readings"
    obj = {
        "id": f"anno-{day}", "date": day, "weekday": parsed.strftime("%A"),
        "mock_priority": "draft_do_not_ship",
        "liturgical": {"rank": "Feria", "color": "green",
                       "title_en": marker, "title_vi": marker},
        "calendars": {name: marker for name in
                      ("julian", "hebrew", "islamic_umm_al_qura", "coptic", "ethiopian")},
        "primary": {"type": "liturgical_day", "confidence": "contextual",
                    **{f"{key}_{lang}": marker for key in
                       ("title", "summary", "body", "confidence_note") for lang in ("en", "vi")}},
        "place": None,
        "artwork": {"title": ART_PLACEHOLDER, "maker": "Unassigned",
                    "date_label": "Pending license", "source_url": "",
                    "status": "placeholder_only"},
        "sources": [
            {"label": marker, "url": "TODO: precise dated USCCB readings",
             "type": "liturgical_calendar"},
            {"label": marker, "url": CALENDAR_URL,
             "type": "liturgical_calendar"},
        ],
        "app_hooks": {f"{key}_{lang}": marker
                      for key in ("hero_line", "prayer_prompt") for lang in ("en", "vi")},
        "_editorial": {
            "status": "draft_do_not_ship",
            "assets": {"hero_image": None, "license": None, "maker_credit": None,
                       "caption_en": None, "caption_vi": None,
                       "alt_en": None, "alt_vi": None},
            "review_checklist": [
                "Compare exact date/rank/color and optional memorials against official USCCB calendar",
                "Read day-specific lectionary, label scriptural references precisely",
                "Audit all historical names, quantities, quotes, and places against actual sources",
                "Write a date-specific opening, reflection and original devotional prayer",
                "Check English and Vietnamese separately; never copy English as Vietnamese",
                "Keep any geographically unverified place null",
                "Leave all assets placeholder-only until licenses, alt and captions are approved",
                "Have a native VI speaker and Catholic editor review before claiming publication",
                "Check source-to-fixture parity and test VoiceOver/contrast/Dynamic Type before release",
                "Remove _editorial and all TODOs before adding to the shipping source file",
            ],
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"NONSHIPPING draft scaffold: {output}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("audit", help="Check all 14 source dates against shipped fixture and authority")
    new = sub.add_parser("new", help="Scaffold one JSON item in a new file (DRAFT ONLY)")
    new.add_argument("--date", required=True)
    new.add_argument("--output", required=True)
    a = ap.parse_args()
    try:
        if a.cmd == "new":
            scaffold(a.date, Path(a.output))
            return 0
        errors = validate(read(SOURCE), read(FIXTURE))
        for message in errors:
            print("FAIL:", message, file=sys.stderr)
        if errors:
            print(f"REJECT: {len(errors)} failures in 14-day July 2026 tranche", file=sys.stderr)
            return 1
        print("PASS: 14/14 dated USCCB identities, 14/14 source-to-fixture parity, 182 total days")
        print("Human editorial/VI, art rights, URL uptime and native accessibility NOT verified")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
