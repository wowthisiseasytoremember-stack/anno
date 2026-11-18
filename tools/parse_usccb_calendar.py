#!/usr/bin/env python3
"""Parse the official USCCB Liturgical Calendar PDF into pinned ground truth.

Source of truth: "Liturgical Calendar for the Dioceses of the United States of
America" published by the USCCB Secretariat of Divine Worship. The PDF already
resolves every precedence/supersession question (the USCCB did that work), so
the ground truth for a year is simply the parsed official calendar — not a
resolver we re-implement.

  1. Fetch (or reuse the cached) calendar PDF:
       python3 tools/parse_usccb_calendar.py --fetch --year 2026
  2. Convert with pdftotext -layout and parse:
       python3 tools/parse_usccb_calendar.py --year 2026

Output: data/liturgical_groundtruth_<year>.json with one row per date, each
carrying title/kind/rank/color/optional memorials, celebration_id,
disambiguation_tokens, and provenance (source url + pdf sha256).

Fail-closed: unparseable day lines or a wrong row count raise; nothing is
written on failure.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "build" / "usccb_cache"
OUT_DIR = ROOT / "data"

CAL_URL = "https://www.usccb.org/resources/{year}cal.pdf"
MONTHS = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
          "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]
WEEKDAYS = {"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4, "SAT": 5, "SUN": 6}
RANK_WORDS = {"Solemnity": "Solemnity", "Feast": "Feast", "Memorial": "Memorial",
              "Optional Memorial": "Optional Memorial", "Commemoration": "Commemoration"}
COLORS = {"red", "white", "green", "violet", "rose", "black", "pink"}
COLOR_PAT = r"(?:red|white|green|violet|rose|black|pink)"
# Latin-Additional characters are NOT NFD-decomposable (e.g. d-with-stroke);
# fold them with an explicit map before slugifying.
FOLD = {"đ": "d", "Đ": "D", "ū": "u", "Ū": "U", "ā": "a", "ē": "e", "ī": "i",
        "ō": "o", "œ": "oe", "æ": "ae", "ł": "l", "ß": "ss"}
DROP_TOKENS = {"saint", "st", "blessed", "of", "the", "and", "or", "a", "in",
               "priest", "bishop", "virgin", "religious", "doctor", "pope",
               "abbot", "deacon", "empress", "queen", "king", "companions",
               "church", "usa", "usa:"}
KEEP_TOKENS = {"apostle", "evangelist", "baptist", "martyr", "archangel"}


def fold(s: str) -> str:
    out = []
    for ch in s:
        if ch in FOLD:
            out.append(FOLD[ch])
        elif unicodedata.combining(ch):
            out.append(unicodedata.normalize("NFD", ch)[0])
        else:
            out.append(ch)
    return "".join(out)


def slugify(s: str) -> str:
    s = fold(s).lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return re.sub(r"_+", "_", s)[:80]


def name_tokens(title: str) -> list[str]:
    toks = []
    for raw in fold(title).lower().replace("-", " ").split():
        if raw in DROP_TOKENS:
            continue
        toks.append(raw.strip(".,;:"))
    return [t for t in toks if t]


def tokens_for_match(title: str) -> list[str]:
    """Identity tokens for title matching: keep role words that disambiguate
    same-named saints (John, James), drop the rest."""
    return [t for t in name_tokens(title) if t in KEEP_TOKENS or len(t) > 3]


def day_line_re() -> re.Pattern:
    return re.compile(r"^\s{0,10}(\d{1,2})\s+(MON|TUE|WED|THU|FRI|SAT|SUN)\b\s*(.*)$",
                      re.IGNORECASE)


def color_part_re() -> re.Pattern:
    return re.compile(
        rf"(({COLOR_PAT})(?:\s*(?:/|or)\s*({COLOR_PAT}))*)\s*$")


def title_case_upper(s: str) -> str:
    small = {"in", "of", "the", "and", "or", "a", "within", "for"}
    words = []
    for i, w in enumerate(s.lower().split()):
        words.append(w if (w in small and i > 0) else w.capitalize())
    return " ".join(words)


def rank_from_line(line: str) -> str | None:
    for word, rank in RANK_WORDS.items():
        if line.strip().lower().startswith(word.lower()):
            return rank
    return None


# Official readings citation: "Am 5:14-15, 21-24/Mt 8:28-34 (379) Pss Prop"
READINGS_RE = re.compile(
    r"^[A-Z][A-Za-z]{0,14}\s+[\d:]+[a-z]?(?:[,\-–][\s\w:]+)*"
    r"(?:/[A-Z][A-Za-z]{0,14}\s+[\d:]+[a-z]?(?:[,\-–][\s\w:]+)*)+")


def clean_readings(parts: list[str]) -> str:
    """Join citation lines, dropping Lectionary page numbers and psalm labels."""
    out = []
    for p in parts:
        s = re.sub(r"\s*\(\d+\)\s*", " ", p)
        s = re.sub(r"\s+Pss(?:alter)?\s+[IVXLC]+\s*$", "", s)
        s = re.sub(r"\s+", " ", s).strip()
        if s:
            out.append(s)
    return " / ".join(out)


def parse_months(txt_path: Path, year: int, start: date, end: date) -> dict:
    """Parse the layout text into {date_iso: row} for dates in [start, end]."""
    lines = txt_path.read_text(encoding="utf-8").splitlines()
    pat = day_line_re()
    cur_month = None
    cur_year = None
    rows: dict[str, dict] = {}
    errors: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^\s*([A-Z]+)\s+(\d{4})\s*$", line)
        if m and m.group(1) in MONTHS:
            cur_month, cur_year = m.group(1), int(m.group(2))
            i += 1
            continue
        if cur_year == year:  # all 12 months of the target civil year
            dm = pat.match(line)
            if dm:
                day = int(dm.group(1))
                weekday_token = dm.group(2)
                rest = dm.group(3).rstrip()
                d = date(cur_year, MONTHS.index(cur_month) + 1, day)
                if not (start <= d <= end):
                    i += 1
                    continue
                if WEEKDAYS[weekday_token.upper()] != d.weekday():
                    errors.append(f"{d}: weekday token {weekday_token} != calendar {d.strftime('%a')}")
                cm = color_part_re().search(rest)
                if cm:
                    colors_raw = re.split(r"\s*(?:/|or)\s*", cm.group(1).strip())
                    title_raw = rest[: cm.start()].strip()
                else:
                    colors_raw, title_raw = [], rest
                # Collect continuation lines until the next day line / month header.
                rank = None
                opt_memorials: list[str] = []
                bracket_buf: list[str] | None = None
                title_parts = [title_raw] if title_raw else []
                readings_parts: list[str] = []
                holyday = False
                j = i + 1
                while j < len(lines):
                    nxt = lines[j]
                    if pat.match(nxt) or re.match(r"^\s*([A-Z]+)\s+\d{4}\s*$", nxt):
                        break
                    if "APPENDIX" in nxt or "APÉNDICE" in nxt:
                        break  # end of the English calendar; appendix follows
                    if re.match(r"^\s*\d+\s*$", nxt):
                        j += 1
                        continue
                    if nxt.strip().startswith("["):
                        if "]" in nxt:
                            opt_memorials.append(nxt.strip())
                        else:
                            bracket_buf = [nxt.strip()]
                    elif bracket_buf is not None:
                        if "]" in nxt:
                            bracket_buf.append(nxt.strip())
                            opt_memorials.append(" ".join(bracket_buf))
                            bracket_buf = None
                        else:
                            bracket_buf.append(nxt.strip())
                    elif rank is None and rank_from_line(nxt):
                        rank = rank_from_line(nxt)
                        if "Holyday of Obligation" in nxt:
                            holyday = True
                    elif not re.search(r"\d", nxt):
                        # Pure-word line: legitimate title continuation (readings
                        # citations always contain digits). Never collect rank
                        # keywords or page noise as title.
                        stripped = nxt.strip()
                        if stripped and not rank_from_line(stripped) \
                                and not re.match(r"^(Pss|Psalter)\b", stripped):
                            title_parts.append(stripped)
                    elif READINGS_RE.match(nxt.strip()):
                        # Official readings citation line for this day.
                        readings_parts.append(nxt.strip())
                    j += 1
                title = " ".join(title_parts)
                title = re.sub(r"\s+", " ", title).strip()
                title = re.sub(r"\s*\((?:Thirty|Second|Third|Fourth|First|Fifth|Sixth|Seventh)[^)]*Week[^)]*\)\s*",
                               " ", title, flags=re.I).strip()
                title = re.sub(r"^USA:\s*", "", title)
                title = re.sub(r"(?<=[a-zA-Z])(\d{1,2})$", r"", title.strip())  # PDF footnote markers
                if title.isupper():
                    title = title_case_upper(title)
                rows[d.isoformat()] = {
                    "date": d.isoformat(),
                    "weekday": d.strftime("%A"),
                    "title_en": title,
                    "rank": rank,
                    "kind": None,  # filled below
                    "color_raw": colors_raw,
                    "optional_memorials": opt_memorials,
                    "readings": clean_readings(readings_parts),
                    "holyday_of_obligation": holyday,
                }
                i = j
                continue
        i += 1
    if errors:
        raise SystemExit("PARSE ERRORS:\n" + "\n".join(errors))
    return rows


def classify(rows: dict[str, dict]) -> None:
    """Fill kind/color from rank + PDF colors, and generate ids/tokens."""
    ferial_pat = re.compile(
        r"\b(weekday|day within the octave|octave of the nativity|lenten weekday|"
        r"easter weekday|within the octave of easter|after ash wednesday|"
        r"of holy week)\b", re.I)
    for d_iso, row in rows.items():
        rank, colors = row["rank"], row["color_raw"]
        primary = (colors or ["green"])[0]
        t = row["title_en"]
        if rank == "Solemnity":
            row["kind"], row["rank"] = "solemnity", "Solemnity"
        elif rank == "Feast":
            row["kind"], row["rank"] = "feast", "Feast"
        elif rank == "Memorial":
            row["kind"], row["rank"] = "memorial", "Memorial"
        elif "sunday" in t.lower():
            row["kind"], row["rank"] = "sunday", "Sunday"
        elif ferial_pat.search(t):
            row["kind"], row["rank"] = "ferial", "Feria"
        elif rank == "Commemoration" or (rank is None):
            # Rank-less named day in the official calendar: only All Souls today.
            row["kind"], row["rank"] = "commemoration", "Commemoration"
        else:
            row["kind"], row["rank"] = "ferial", "Feria"
        row["color"] = {"violet": "purple"}.get(primary, primary)
        # name_core: identity name = title minus parentheticals and role words
        core = re.sub(r"\([^)]*\)", "", t).strip()
        row["name_core"] = re.sub(r"\s+", " ", core).strip(" ,;")
        row["celebration_id"] = slugify(row["name_core"]) or f"ferial_{d_iso}"
        row["disambiguation_tokens"] = tokens_for_match(row["name_core"])


def validate(rows: dict[str, dict], start: date, end: date) -> None:
    d = start
    missing = []
    while d <= end:
        if d.isoformat() not in rows:
            missing.append(d.isoformat())
        d += timedelta(days=1)
    extra = set(rows) - {d.isoformat() for d in
                         (start + timedelta(n) for n in range((end - start).days + 1))}
    problems = []
    if missing:
        problems.append(f"missing dates: {missing}")
    if extra:
        problems.append(f"unexpected dates: {sorted(extra)}")
    for d_iso, row in rows.items():
        if not row["title_en"]:
            problems.append(f"{d_iso}: empty title")
        if row["color"] not in {"green", "white", "purple", "red"}:
            problems.append(f"{d_iso}: bad color {row['color']!r}")
        if not row["kind"]:
            problems.append(f"{d_iso}: unclassified kind")
    if problems:
        raise SystemExit("VALIDATION FAILED:\n" + "\n".join(problems))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, default=2026)
    ap.add_argument("--fetch", action="store_true", help="download the calendar PDF")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    year = args.year
    pdf = CACHE / f"{year}cal.pdf"
    txt = CACHE / f"{year}cal.txt"
    CACHE.mkdir(parents=True, exist_ok=True)
    if args.fetch and not pdf.exists():
        subprocess.run(["curl", "-sL", "--max-time", "60", "-A",
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                        CAL_URL.format(year=year), "-o", str(pdf)], check=True)
    if not pdf.exists():
        raise SystemExit(f"missing {pdf}; run with --fetch")
    if not txt.exists():
        subprocess.run(["pdftotext", "-layout", str(pdf), str(txt)], check=True)

    sha = subprocess.run(["sha256sum", str(pdf)], capture_output=True, text=True).stdout.split()[0]
    # The PDF spans Nov(prev year)–Dec(year). Pin the civil-year Jan 1–Dec 31.
    start, end = date(year, 1, 1), date(year, 12, 31)
    rows = parse_months(txt, year, start, end)
    classify(rows)
    validate(rows, start, end)

    out_path = args.out or (OUT_DIR / f"liturgical_groundtruth_{year}.json")
    doc = {
        "schema_version": "1.0",
        "source_url": CAL_URL.format(year=year),
        "source_sha256": sha,
        "generated_by": "tools/parse_usccb_calendar.py",
        "authority": "USCCB Secretariat of Divine Worship — official liturgical calendar",
        "color_note": ("violet maps to fixture 'purple'; multi-colors keep the primary "
                       "(first listed). 'violet or white or black' (All Souls) pins violet->purple."),
        "rows": [rows[k] for k in sorted(rows)],
    }
    out_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    kinds: dict[str, int] = {}
    for r in doc["rows"]:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    print(f"Wrote {out_path.relative_to(ROOT)}: {len(doc['rows'])} rows {kinds}")
    print(f"source sha256: {sha}")


if __name__ == "__main__":
    main()
