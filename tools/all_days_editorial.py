#!/usr/bin/env python3
"""Offline editorial gate for every 2026 devotional day (PLAN v4 §6).

Fail-closed offline audit of Anno/Resources/anno_unified_2026.json against the
pinned USCCB ground truth (data/liturgical_groundtruth_<year>.json, produced by
tools/parse_usccb_calendar.py). No network, no LLM, no Mac dependency.

  python3 tools/all_days_editorial.py audit --year 2026
  python3 tools/all_days_editorial.py audit --year 2026 --month 2026-08 --fail-on S1,S2
  python3 tools/all_days_editorial.py audit --year 2026 --report-only
  python3 tools/all_days_editorial.py audit --year 2026 --list-unverified
  python3 tools/all_days_editorial.py repair --dry-run --month 2026-08

Exit rules (default): 0 iff every day is conform | editorial_exception, no
exception carries S1/S2 without a non-null approver, 0 unverified ground-truth
rows, and no expired blocked entries. --fail-on S1,S2 overrides: exit 0 iff no
finding at the listed severities in range and no unverified rows in range.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DEFAULT = ROOT / "Anno/Resources/anno_unified_2026.json"
GROUNDTRUTH = "data/liturgical_groundtruth_{year}.json"
EXCEPTIONS = "data/editorial_exceptions_{year}.json"
BUILD = ROOT / "build"
REPORT_MD = "docs/AUDIT_{year}_REMAINING_DAYS.md"

RANKS = {"Solemnity", "Feast", "Sunday", "Memorial", "Optional Memorial",
         "Feria", "Commemoration"}
COLORS = {"green", "white", "purple", "red"}
VI_REQUIRED_DATES = {"2026-08-15", "2026-11-22", "2026-12-08", "2026-12-25"}
CLAIM_FIELDS = [  # (section, key) — SRC-COUNT/SRC-QUALITY apply when non-empty
    ("primary", "summary_en"), ("primary", "summary_vi"),
    ("primary", "body_en"), ("primary", "body_vi"),
    ("primary", "confidence_note_en"), ("primary", "confidence_note_vi"),
    ("app_hooks", "hero_line_en"), ("app_hooks", "hero_line_vi"),
    ("app_hooks", "prayer_prompt_en"), ("app_hooks", "prayer_prompt_vi"),
    ("artwork", "title"), ("artwork", "maker"), ("artwork", "date_label"),
    ("place", "name"),
]
TYPE_FOR_RANK = {
    "Solemnity": {"solemnity"},
    "Feast": {"feast", "saint"},
    "Sunday": {"liturgical_day"},
    "Feria": {"liturgical_day"},
    "Memorial": {"memorial", "saint"},
    "Optional Memorial": {"memorial", "saint"},
    "Commemoration": {"feast", "liturgical_day"},
}
# Domains treated as primary references for automatic quality tagging.
PRIMARY_DOMAINS = {
    "vatican.va", "usccb.org", "bible.usccb.org", "catholicsaints.info",
    "catholicculture.org", "britannica.com", "newadvent.org", "cathen.org",
    "loc.gov", "metmuseum.org", "commons.wikimedia.org", "custodia.org",
    "hdgmvietnam.com",
}
FERIAL_TITLE = re.compile(
    r"\b(weekday|feria|ordinary time|advent|octave of the nativity)\b", re.I)
PLACEHOLDER_PAT = re.compile(r"example\.(?:com|org|net)|placeholder", re.I)
VN_CHARS = set("ưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹđƯẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼẾỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴỶỸĐ")

SEV_OF = {
    "LIT-NAME": "S1", "LIT-RANK": "S1", "LIT-COLOR": "S1",
    "LIT-NAME-AMBIGUOUS": "S1", "ART-CLEARED-PLACEHOLDER": "S1",
    "SRC-COUNT": "S2", "SRC-PLACEHOLDER": "S2", "VI-FFFD": "S2",
    "VI-EMPTY-REQUIRED": "S2", "VI-IN-EN": "S2", "COPYRIGHT-VERBATIM-PROXY": "S2",
    "LIT-COLOR-CASE": "S3", "TYPE-RANK": "S3", "SRC-SAME-DOMAIN": "S3",
    "SRC-QUALITY": "S3",
}
ADVISORY_OF = {"LIT-NAME-WEAK": "advisory", "OPTIONAL-ELEVATED": "advisory"}


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))


# Word ordinals (USCCB PDF style) <-> digit ordinals (fixture style).
_UNITS = {"first": "1", "second": "2", "third": "3", "fourth": "4", "fifth": "5",
          "sixth": "6", "seventh": "7", "eighth": "8", "ninth": "9",
          "tenth": "10", "eleventh": "11", "twelfth": "12", "thirteenth": "13",
          "fourteenth": "14", "fifteenth": "15", "sixteenth": "16",
          "seventeenth": "17", "eighteenth": "18", "nineteenth": "19",
          "twentieth": "20", "thirtieth": "30",
          "fortieth": "40"}
_ORDS = dict(_UNITS)
for _base, _n in (("twenty", 20), ("thirty", 30), ("forty", 40)):
    for _u, _k in list(_UNITS.items())[:9]:
        _ORDS[f"{_base}-{_u}"] = str(_n + int(_k))
        _ORDS[f"{_base} {_u}"] = str(_n + int(_k))


def norm_title(s: str) -> list[str]:
    s = fold(s or "").lower()
    s = re.sub(r"[’'`]", "", s)
    s = re.sub(r"\b(st|dr|mr)\b\.?", "saint", s)
    s = re.sub(r"(\d+)(st|nd|rd|th)\b", r"\1", s)  # 18th -> 18
    for w in sorted(_ORDS, key=len, reverse=True):
        s = re.sub(rf"\b{w}\b", _ORDS[w], s)  # eighteenth -> 18
    toks = re.findall(r"[a-z0-9]+", s)
    # Role words are liturgical labels, not identity: strip from BOTH sides so
    # candidate ⊆ title matching is not broken by "Doctor of the Church" etc.
    return [t for t in toks if t not in _STOP_TOKENS]


_STOP_TOKENS = {"the", "of", "and", "a", "in", "for", "saint", "blessed",
                "priest", "bishop", "virgin", "religious", "doctor", "pope",
                "abbot", "deacon", "martyr", "martyrs", "apostle", "companions",
                "church", "usa"}


def walk_paths(x, base: str = ""):
    """Yield (dotted_path, string) for every string in a nested structure."""
    if isinstance(x, dict):
        for k, v in x.items():
            p = f"{base}.{k}" if base else str(k)
            if isinstance(v, str):
                yield p, v
            else:
                yield from walk_paths(v, p)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from walk_paths(v, f"{base}[{i}]")


def load_gt(year: int) -> dict:
    p = Path(ROOT / GROUNDTRUTH.format(year=year))
    if not p.exists():
        raise SystemExit(f"missing ground truth {p}; run tools/parse_usccb_calendar.py")
    return json.loads(p.read_text(encoding="utf-8"))


def load_exceptions(year: int) -> dict:
    p = Path(ROOT / EXCEPTIONS.format(year=year))
    if not p.exists():
        return {"schema_version": 1, "entries": []}
    return json.loads(p.read_text(encoding="utf-8"))


def source_file_for(date_str: str) -> Path:
    """Source layer owning this date (mirrors normalize_fixture.py's ingest)."""
    d = date.fromisoformat(date_str)
    research = ROOT / "data/research_results"
    if d.month == 7 and d.day <= 16:
        return ROOT / "data/mock/anno_fortnight_2026-07-03_2026-07-16.json"
    if d.month == 8:
        return ROOT / "data/mock/anno_august_2026.json"
    en = research / f"{date_str}_result_en.json"
    raw = research / f"{date_str}_result.json"
    return en if en.exists() else raw


def candidates_for(gt_row: dict) -> list[dict]:
    """Primary celebration + optional memorials, each as a match candidate."""
    ferial_primary = gt_row["kind"] == "ferial" or bool(
        FERIAL_TITLE.search(gt_row["name_core"])) and gt_row["kind"] != "sunday"
    cands = [{
        "kind": gt_row["kind"], "rank": gt_row["rank"], "color": gt_row["color"],
        "name_core": gt_row["name_core"],
        "tokens": [] if ferial_primary else norm_title(gt_row["name_core"]),
        "required": True, "source": "ground_truth",
    }]
    for opt in gt_row.get("optional_memorials", []):
        name = re.sub(r"^[\[\]]+|[\[\]]+$", "", opt).strip()
        name = re.sub(r"^USA:\s*", "", name)
        name = re.sub(r";\s*BVM$", "", name)
        if not name or name.upper() == "BVM":
            continue
        toks = norm_title(name)
        if toks:
            cands.append({
                "kind": "optional", "rank": "Optional Memorial",
                "color": None, "name_core": name, "tokens": toks,
                "required": False, "source": "optional_memorial",
            })
    if any("BVM" in o for o in gt_row.get("optional_memorials", [])):
        # A listed "; BVM" makes a standalone BVM optional memorial a valid display.
        cands.append({
            "kind": "optional", "rank": "Optional Memorial",
            "color": None, "name_core": "Optional Memorial of the Blessed Virgin Mary",
            "tokens": norm_title("Blessed Virgin Mary"),
            "required": False, "source": "optional_memorial_bvm",
        })
    return cands


def match_candidate(title: str, cands: list[dict]) -> tuple[dict | None, bool]:
    """Return (matched candidate, ambiguous?). Date-local token matching."""
    ttoks = set(norm_title(title))
    if not ttoks:
        return None, False
    ferial_like = bool(FERIAL_TITLE.search(title))
    hits = []
    for c in cands:
        ctoks = set(c["tokens"])
        if not ctoks:
            continue  # ferial candidate matches via ferial_like, not tokens
        if ctoks <= ttoks:
            hits.append(c)
    if len(hits) > 1:
        return None, True
    if hits:
        return hits[0], False
    if ferial_like and any(not c["tokens"] for c in cands):
        return next(c for c in cands if not c["tokens"]), False
    if ferial_like:
        return None, False
    return None, False


def walk_strings(x):
    if isinstance(x, dict):
        for k, v in x.items():
            if isinstance(v, str):
                yield k, v
            else:
                yield from walk_strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from walk_strings(v)


def has_vn_chars(s: str) -> bool:
    return any(ch in VN_CHARS for ch in s)


def audit_entry(entry: dict, gt_row: dict, year: int) -> list[dict]:
    f = []
    lit = entry.get("liturgical", {})
    prim = entry.get("primary", {})
    ft_en = lit.get("title_en", "")
    cands = candidates_for(gt_row)
    matched, ambiguous = match_candidate(ft_en, cands)
    if ambiguous:
        f.append({"code": "LIT-NAME-AMBIGUOUS", "detail": f"{ft_en!r} matches multiple candidates"})
        return f
    if matched is None:
        f.append({"code": "LIT-NAME", "detail": f"no candidate matches {ft_en!r}",
                  "expected": gt_row["name_core"], "actual": ft_en})
        exp_rank, exp_color, required = gt_row["rank"], gt_row["color"], True
    else:
        exp_rank, exp_color, required = matched["rank"], matched["color"], matched["required"]
        if not matched["required"] and exp_rank not in {"Solemnity", "Feast"}:
            pass  # optional memorial displayed: tolerated
    fr = lit.get("rank", "")
    if exp_rank == "Feria":
        ok = fr == "Feria" or (matched is not None and not matched["required"]
                               and fr == "Optional Memorial")
    else:
        ok = fr == exp_rank
    if not ok:
        f.append({"code": "LIT-RANK", "expected": exp_rank, "actual": fr})
    # color
    fc = (lit.get("color") or "")
    if matched is not None and not matched["required"]:
        exp_color_eff = "white"  # displayed optional memorial carries its own color
    elif matched is not None:
        exp_color_eff = exp_color or gt_row["color"]
    else:
        exp_color_eff = gt_row["color"]
    if fc and fc.lower() not in COLORS:
        f.append({"code": "LIT-COLOR", "detail": "unknown color", "actual": fc})
    elif fc and exp_color_eff and fc.lower() != exp_color_eff.lower():
        if fc == fc.lower():
            f.append({"code": "LIT-COLOR", "expected": exp_color_eff, "actual": fc})
        else:
            f.append({"code": "LIT-COLOR-CASE", "expected": exp_color_eff, "actual": fc})
    # type vs rank
    ptype = prim.get("type", "")
    allowed = TYPE_FOR_RANK.get(fr or exp_rank, set())
    if ptype and ptype not in allowed:
        f.append({"code": "TYPE-RANK", "expected": sorted(allowed), "actual": ptype})
    art = entry.get("artwork", {})
    # placeholders anywhere (artwork excluded unless cleared: an empty artwork
    # slot is a normal state; cleared-with-placeholder is ART-CLEARED-PLACEHOLDER)
    art_cleared = art.get("status") == "cleared"
    for sec_name, sec in entry.items():
        if sec_name == "artwork" and not art_cleared:
            continue
        for k, v in walk_paths(sec, sec_name):
            if isinstance(v, str) and not k.endswith(".status") and PLACEHOLDER_PAT.search(v):
                f.append({"code": "SRC-PLACEHOLDER", "field": k,
                          "actual": v[:120]})
    if art.get("status") == "cleared" and (not art.get("source_url")
                                           or PLACEHOLDER_PAT.search(art.get("source_url", ""))):
        f.append({"code": "ART-CLEARED-PLACEHOLDER", "actual": art.get("source_url")})
    # sources
    srcs = entry.get("sources", []) or []
    claims_nonempty = any((entry.get(sec) or {}).get(key) for sec, key in CLAIM_FIELDS)
    if claims_nonempty and len(srcs) < 2:
        f.append({"code": "SRC-COUNT", "actual": len(srcs)})
    doms = [urlsplit(s.get("url", "")).netloc.lower() for s in srcs if s.get("url")]
    if len(doms) >= 2 and len(set(doms)) == 1:
        f.append({"code": "SRC-SAME-DOMAIN", "actual": doms})
    if claims_nonempty and srcs and any("quality" not in s and "type" not in s for s in srcs):
        f.append({"code": "SRC-QUALITY", "actual": [s.get("url", "") for s in srcs]})
    # VI integrity (EN fields must not be Vietnamese text; proper nouns with a
    # few Vietnamese diacritics are legitimate — require VN-dominant strings)
    for k, v in walk_paths(entry):
        if isinstance(v, str) and k.endswith("_vi") and "\ufffd" in v:
            f.append({"code": "VI-FFFD", "field": k})
        if isinstance(v, str) and (k.endswith("_en") or k.endswith("_note_en")):
            letters = [c for c in v if c.isalpha()]
            vn = sum(1 for c in letters if c in VN_CHARS)
            if letters and vn / len(letters) > 0.3:
                f.append({"code": "VI-IN-EN", "field": k})
    d_iso = entry.get("date", "")
    if d_iso in VI_REQUIRED_DATES:
        for key in ("title_vi", "summary_vi", "body_vi"):
            vi = prim.get(key, "")
            if not vi.strip():
                f.append({"code": "VI-EMPTY-REQUIRED", "field": f"primary.{key}"})
            elif key == "title_vi" and vi == prim.get("title_en"):
                f.append({"code": "VI-EMPTY-REQUIRED", "field": "primary.title_vi",
                          "detail": "identical to EN (untranslated)"})
    om = re.search(r"\b(\d{1,2})(st|nd|rd|th)\b", ft_en)
    if om:
        n = int(om.group(1))
        correct = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        if om.group(2) != correct:
            f.append({"code": "ORDINAL-SUFFIX", "field": "liturgical.title_en",
                      "actual": ft_en[:80]})
    return f


def audit(year: int, since: date | None, until: date | None,
          fail_on: set[str] | None, report_only: bool, list_unverified: bool,
          as_of: date) -> int:
    gt_doc = load_gt(year)
    gt = {r["date"]: r for r in gt_doc["rows"]}
    fix_path = ROOT / f"Anno/Resources/anno_unified_{year}.json"
    fixture = json.loads(fix_path.read_text(encoding="utf-8"))
    entries = fixture["entries"]
    exceptions = load_exceptions(year)
    by_date = {e["date"]: e.get("id", "") for e in entries}

    def sev_active(code: str) -> bool:
        return SEV_OF.get(code, "advisory") in (fail_on or {"S1", "S2", "S3"})

    days = {}
    counts = Counter()
    for entry in entries:
        d_iso = entry.get("date", "")
        if since and d_iso < since.isoformat():
            continue
        if until and d_iso > until.isoformat():
            continue
        row = gt.get(d_iso)
        if row is None:
            days[d_iso] = {"id": entry.get("id", ""), "status": "unverified",
                           "findings": [{"code": "GT-MISSING", "detail": "no ground truth row"}]}
            counts["unverified"] += 1
            continue
        findings = audit_entry(entry, row, year)
        # S1/S2 block day status; S3 + advisories are recorded but non-blocking
        blocking = [x for x in findings if SEV_OF.get(x["code"], "advisory") in {"S1", "S2"}]
        advisories = [x for x in findings if SEV_OF.get(x["code"], "advisory") == "advisory"]
        exc = [x for x in exceptions.get("entries", []) if x.get("date") == d_iso]
        status = "conform"
        if blocking:
            covered = {(x.get("date"), x.get("code")) for x in exc}
            uncovered = [x for x in blocking if (d_iso, x["code"]) not in covered]
            approved = {x.get("date") for x in exc if x.get("status") == "editorial_exception"
                        and x.get("approver")}
            unresolved = [x for x in uncovered if (d_iso) not in approved]
            if unresolved:
                status = "defect"
            else:
                status = "editorial_exception"
        elif advisories:
            status = "conform"
        days[d_iso] = {"id": entry.get("id", ""), "status": status,
                       "findings": findings}
        counts[status] += 1

    # exceptions hygiene
    blocked_expired = sum(1 for x in exceptions.get("entries", [])
                          if x.get("status") == "blocked" and x.get("expires", "9999") < as_of.isoformat())
    missing_owner = sum(1 for x in exceptions.get("entries", []) if not x.get("owner"))

    summary = {
        "total": len(days), "conform": counts["conform"],
        "defect": counts["defect"], "editorial_exception": counts["editorial_exception"],
        "unverified": counts["unverified"],
        "blocked_expired": blocked_expired, "entries_missing_owner": missing_owner,
        "by_severity": Counter(SEV_OF.get(x["code"], "advisory")
                               for d in days.values() for x in d["findings"]),
    }

    if list_unverified:
        for d_iso in sorted(days):
            if days[d_iso]["status"] == "unverified":
                print(d_iso)
        return 0

    doc = {
        "audit_version": "1.0",
        "ground_truth_version": gt_doc.get("source_sha256", "unknown"),
        "git_sha": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                                  text=True).stdout.strip(),
        "generated_at": f"{date.today().isoformat()}T00:00:00Z",  # sidecar carries the volatile stamp
        "as_of": as_of.isoformat(),
        "fixture": str(fix_path.relative_to(ROOT)),
        "days": days,
        "summary": summary,
    }
    BUILD.mkdir(exist_ok=True)
    out = BUILD / f"audit_{year}.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if not report_only:
        write_report_md(year, doc, exceptions)
    print(f"AUDIT {'PASS' if exit_ok(doc, fail_on) else 'FAIL'} "
          f"{summary['total']} days | conform={summary['conform']} defect={summary['defect']} "
          f"exception={summary['editorial_exception']} unverified={summary['unverified']}")
    if summary["defect"]:
        for d_iso in sorted(days):
            if days[d_iso]["status"] == "defect":
                codes = [(x["code"], x.get("detail", x.get("actual", ""))) for x in days[d_iso]["findings"]]
                print(f"  DEFECT {d_iso}: {codes}")
    return 0 if exit_ok(doc, fail_on) else 1


def exit_ok(doc: dict, fail_on: set[str] | None) -> bool:
    s = doc["summary"]
    if fail_on is not None:
        active = [x for d in doc["days"].values() for x in d["findings"]
                  if SEV_OF.get(x["code"], "advisory") in fail_on]
        return not active and s["unverified"] == 0
    return (s["defect"] == 0 and s["editorial_exception"] == 0
            and s["unverified"] == 0 and s["blocked_expired"] == 0
            and s["entries_missing_owner"] == 0)


def write_report_md(year: int, doc: dict, exceptions: dict) -> None:
    p = Path(ROOT / REPORT_MD.format(year=year))
    p.parent.mkdir(exist_ok=True)
    s = doc["summary"]
    lines = [
        f"# Audit of {year} devotional days", "",
        f"Generated by `tools/all_days_editorial.py` (offline, fail-closed). "
        f"Ground truth: official USCCB calendar "
        f"(`data/liturgical_groundtruth_{year}.json`, sha {doc['ground_truth_version'][:12]}…).", "",
        "| status | count |", "|---|---|",
        f"| conform | {s['conform']} |", f"| defect | {s['defect']} |",
        f"| editorial_exception | {s['editorial_exception']} |",
        f"| unverified | {s['unverified']} |", "",
        "## Findings by day", "",
    ]
    for d_iso in sorted(doc["days"]):
        d = doc["days"][d_iso]
        if d["status"] == "conform" and not d["findings"]:
            continue
        codes = ", ".join(sorted({x["code"] for x in d["findings"]})) or "—"
        lines.append(f"- **{d_iso}** ({d['status']}): {codes}")
    vn = [x for x in exceptions.get("entries", []) if x.get("owner")]
    lines += ["", "## Tóm tắt song ngữ (Vietnamese summary)", "",
              "Các mục còn **defect/editorial_exception** cần người review người Việt xác nhận",
              "trước khi coi là hoàn tất. Danh sách ngày có vấn đề:", ""]
    for d_iso in sorted(doc["days"]):
        if doc["days"][d_iso]["status"] != "conform":
            lines.append(f"- {d_iso}: {doc['days'][d_iso]['status']}")
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--year", type=int, default=2026)
    shared.add_argument("--since", type=str)
    shared.add_argument("--until", type=str)
    shared.add_argument("--month", type=str, help="YYYY-MM (inclusive, whole month)")
    shared.add_argument("--fail-on", type=str, help="e.g. S1,S2 — overrides default exit rule")
    shared.add_argument("--report-only", action="store_true")
    shared.add_argument("--list-unverified", action="store_true")
    shared.add_argument("--as-of", type=str, default=str(date.today()))
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=False)
    sub.add_parser("audit", parents=[shared])
    sub.add_parser("repair", parents=[shared])
    args = ap.parse_args()
    if args.cmd is None:
        args = shared.parse_args()
        args.cmd = "audit"
        args.dry_run = False

    since = until = None
    if args.month:
        y, m = (int(x) for x in args.month.split("-")[:2])
        since = date(y, m, 1)
        until = date(y + (m == 12), 12 if m == 12 else m + 1, 31 if m == 12 else (date(y, m, 28) + timedelta(days=4)).replace(day=1) - timedelta(days=1))
    elif args.since or args.until:
        since = date.fromisoformat(args.since) if args.since else None
        until = date.fromisoformat(args.until) if args.until else None
    fail_on = {s.strip().upper() for s in args.fail_on.split(",")} if args.fail_on else None
    if args.cmd == "repair":
        raise SystemExit("repair apply lands with the A4 batch work; audit --month N gates each batch")
    sys.exit(audit(args.year, since, until, fail_on, args.report_only,
                   args.list_unverified, date.fromisoformat(args.as_of)))


if __name__ == "__main__":
    main()
