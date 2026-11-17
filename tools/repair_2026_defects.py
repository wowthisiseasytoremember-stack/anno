#!/usr/bin/env python3
"""Repair defective 2026 devotional days at the SOURCE layer (PLAN v4 A4).

Never writes to the fixture. Identity (title/rank/color/primary.type) comes
ONLY from the pinned USCCB ground truth (the hashed official PDF). The LLM
(yolo-auto) writes English narrative + source URLs; every URL is checked live
before it is written. The day's official readings citation from the PDF is
included in the prompt so the narrative is specific, not generic filler.

Vietnamese policy (honours the "no machine translation" rule):
  * week-number-only fixes: mechanically correct the number in existing VI
    strings (and untranslated English weekday names), nothing else;
  * days whose celebration changed: clear *_vi so the EN-primary fixture falls
    back to English (v1 scope: VI is for the 8 major feasts only);
  * the 4 required feast dates are never touched by this tool.

Dry run first:
    python3 tools/repair_2026_defects.py --month 2026-09 --dry-run
Apply a month, then gate:
    python3 tools/repair_2026_defects.py --month 2026-09
    python3 tools/normalize_fixture.py --year 2026
    python3 tools/all_days_editorial.py audit --year 2026 --month 2026-09 --fail-on S1,S2
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
from all_days_editorial import audit, load_gt, match_candidate, norm_title  # noqa: E402

GT_PATH = ROOT / "data/liturgical_groundtruth_2026.json"
RESEARCH = ROOT / "data/research_results"
AUGUST = ROOT / "data/mock/anno_august_2026.json"
FORTNIGHT = ROOT / "data/mock/anno_fortnight_2026-07-03_2026-07-16.json"
YOLO_URL = "https://yolo-auto.com/v1/chat/completions"
YOLO_MODEL = "qwen3.8-27b"

TYPE_FOR = {"Solemnity": "solemnity", "Feast": "feast", "Memorial": "memorial",
            "Optional Memorial": "saint", "Commemoration": "liturgical_day",
            "Sunday": "liturgical_day", "Feria": "liturgical_day"}
ORD_MAP = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
           "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10,
           "eleventh": 11, "twelfth": 12, "thirteenth": 13, "fourteenth": 14,
           "fifteenth": 15, "sixteenth": 16, "seventeenth": 17,
           "eighteenth": 18, "nineteenth": 19, "twentieth": 20,
           "thirtieth": 30, "fortieth": 40}
for _b, _n in (("twenty", 20), ("thirty", 30)):
    for _u, _k in list(ORD_MAP.items())[:9]:
        ORD_MAP[f"{_b}-{_u}"] = _n + _k
VI_WEEKDAYS = {"Sunday": "Chủ Nhật", "Monday": "Thứ Hai", "Tuesday": "Thứ Ba",
               "Wednesday": "Thứ Tư", "Thursday": "Thứ Năm", "Friday": "Thứ Sáu",
               "Saturday": "Thứ Bảy"}


def api_key() -> str:
    for p in (Path("/home/ichabod/.hermes/.env"), ROOT.parent / ".hermes/.env"):
        if p.exists():
            for line in p.read_text().splitlines():
                if line.startswith("YOLO_AUTO_API_KEY="):
                    return line.strip().split("=", 1)[1]
    raise SystemExit("missing YOLO_AUTO_API_KEY")


KEY = api_key()


def yolo(prompt: str, maxtok: int = 1800) -> str:
    payload = {"model": YOLO_MODEL,
               "messages": [{"role": "user", "content": prompt}],
               "temperature": 0.25, "max_tokens": maxtok,
               "chat_template_kwargs": {"enable_thinking": False}}
    req = urllib.request.Request(
        YOLO_URL, data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json",
                 "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"})
    last = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=150) as r:
                body = json.loads(r.read().decode())
                return body["choices"][0]["message"].get("content") or ""
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"yolo failed: {last}")


def extract_json(text: str) -> str:
    s = text.find("{")
    if s < 0:
        raise ValueError("no JSON object in LLM output")
    depth = 0
    for i in range(s, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[s:i + 1]
    raise ValueError("unterminated JSON in LLM output")


def url_live(url: str) -> bool:
    if not url.startswith("https://"):
        return False
    if re.search(r"example\.(com|org|net)|placeholder|fake|invalid", url, re.I):
        return False
    req = urllib.request.Request(url, method="GET", headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status < 400
    except urllib.error.HTTPError as e:
        return e.code in (401, 403, 405, 429)  # bot-challenged but reachable
    except Exception:  # noqa: BLE001
        return False


def suffix(n: int) -> str:
    if 10 <= n % 100 <= 20:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def ordinal_from(title: str) -> int | None:
    toks = norm_title(title)
    if toks and toks[0].isdigit():
        return int(toks[0])
    m = re.search(r"\b(" + "|".join(sorted(ORD_MAP, key=len, reverse=True)) + r")\b",
                  title.lower())
    return ORD_MAP[m.group(1)] if m else None


def week_number(gt: dict, d: str) -> int | None:
    """OT/Advent week number for a date, derived from the PDF's Sunday titles."""
    dte = date.fromisoformat(d)
    cur = dte
    while cur.weekday() != 6:
        cur -= timedelta(days=1)
    sunday = gt.get(cur.isoformat())
    if sunday is None:
        return None
    if sunday["kind"] == "sunday" and "Ordinary Time" in sunday["title_en"]:
        return ordinal_from(sunday["title_en"])
    if "King of the Universe" in sunday["title_en"]:
        return 34
    if "Advent" in sunday["title_en"]:
        return ordinal_from(sunday["title_en"])
    return None


def canonical_identity(gt_row: dict, existing: dict, gt: dict) -> dict:
    """Return pinned identity + display policy for one date."""
    kind, rank = gt_row["kind"], gt_row["rank"]
    if kind == "ferial":
        cands = [c for c in (existing.get("liturgical", {}).get("title_en", ""),)]
        # Match the existing title against optional memorials of this day.
        opts = []
        for o in gt_row.get("optional_memorials", []):
            name = re.sub(r"^[\[\]]+|[\[\]]+$", "", o).strip()
            name = re.sub(r"^USA:\s*", "", name)
            name = re.sub(r";\s*BVM$", "", name)
            if name and name.upper() != "BVM":
                opts.append({"tokens": norm_title(name), "name_core": name,
                             "rank": "Optional Memorial", "color": None,
                             "required": False, "kind": "optional"})
        match, _ = match_candidate(existing.get("liturgical", {}).get("title_en", ""), opts)
        if match is not None:
            color = "red" if re.search(r"martyr", match["name_core"], re.I) else "white"
            return {"title_en": existing["liturgical"]["title_en"], "rank": "Optional Memorial",
                    "color": color, "type": "saint", "numeric_vi": False,
                    "identity_change": True, "kind": "optional"}
        n = week_number(gt, gt_row["date"])
        if n and "Octave" not in gt_row["title_en"]:
            if "Advent" in " ".join(o for o in [gt_row["title_en"]] + [str(gt.get((date.fromisoformat(gt_row["date"]) - timedelta(days=1)).isoformat(), {}).get("title_en", ""))]) or date.fromisoformat(gt_row["date"]).month == 12 and date.fromisoformat(gt_row["date"]).day < 25:
                word = {1: "First", 2: "Second", 3: "Third", 4: "Fourth"}.get(n, str(n))
                title = f"{gt_row['weekday']} of the {word} Week of Advent"
            else:
                title = (f"{gt_row['weekday']} of the {n}{suffix(n)} Week "
                         "in Ordinary Time")
        else:
            title = gt_row["title_en"]
        return {"title_en": title, "rank": "Feria", "color": gt_row["color"],
                "type": "liturgical_day", "numeric_vi": True,
                "identity_change": False, "kind": "ferial"}
    numeric = kind in {"sunday", "ferial"}
    return {"title_en": gt_row["title_en"], "rank": rank, "color": gt_row["color"],
            "type": TYPE_FOR.get(rank, "liturgical_day"), "numeric_vi": numeric,
            "identity_change": not numeric, "kind": kind}


def build_prompt(d: str, gt_row: dict, ident: dict) -> str:
    readings = gt_row.get("readings") or "not printed in the USCCB daily calendar"
    opts = "; ".join(gt_row.get("optional_memorials", [])) or "none"
    return f"""You are Engine B of Anno, a Catholic liturgical research engine. Write the ENGLISH narrative for ONE liturgical day. Output ONLY one valid JSON object (no prose, no markdown fences).

AUTHORITATIVE IDENTITY — from the official USCCB 2026 Liturgical Calendar PDF. DO NOT contradict, change, or second-guess it. This day is:
  date: {d} ({gt_row['weekday']})
  display title: {ident['title_en']}
  rank: {ident['rank']}   color: {ident['color']}
  official readings citation: {readings}
  optional memorials printed for this day: {opts}

Return exactly this shape:
{{
  "primary": {{"type": "{ident['type']}", "title_en": "{ident['title_en']}", "summary_en": "... (2-4 factual sentences, 140+ chars)", "body_en": "... (specific 1-2 paragraphs, 400+ chars)", "confidence": "confirmed|traditional|disputed", "confidence_note_en": "..."}},
  "app_hooks": {{"hero_line_en": "...", "prayer_prompt_en": "..."}},
  "artwork": {{"title": "title of a real public-domain artwork", "maker": "artist", "date_label": "c. 1500", "source_url": "https://commons.wikimedia.org/wiki/File:...", "status": "public_domain"}},
  "place": {{"name": "relevant place, city, country"}},
  "sources": [{{"label": "...", "url": "https://...", "type": "vatican|encyclopedia|liturgical_calendar|museum|reference"}}]
}}

RULES:
- The narrative MUST be specifically about {ident['title_en']} — name the saint/feast/Sunday in the first sentence. Generic filler about "the liturgical year" is REJECTED.
- Facts must be well-established. If uncertain, set confidence='disputed' and say what is uncertain in confidence_note_en. Never invent facts, quotes, or URLs.
- Provide AT LEAST 2 real, reachable source URLs from at least 2 different domains. Prefer vatican.va, usccb.org, bible.usccb.org, newadvent.org, catholicsaints.info, catholicculture.org, britannica.com, loc.gov, metmuseum.org, commons.wikimedia.org. All source URLs are checked with HTTP GET before being saved.
- The artwork source_url must be a real Wikimedia Commons file page URL; if you cannot be certain one exists, use {{"title": null, "maker": null, "date_label": null, "source_url": null, "status": "placeholder_only"}} instead of inventing a URL.
- Include the day's official readings citation where it helps (e.g. "The liturgy pairs ... with {readings}").
- Do NOT write Vietnamese fields — only the English fields in the shape above."""


def validate(obj: dict, ident: dict) -> list[str]:
    errs = []
    if not isinstance(obj, dict):
        return ["not a dict"]
    p = obj.get("primary") or {}
    for k in ("summary_en", "body_en", "title_en", "confidence_note_en"):
        if not isinstance(p.get(k), str) or not p[k].strip():
            errs.append(f"primary.{k} missing")
    if len(p.get("body_en") or "") < 350:
        errs.append("body_en too short")
    if len(p.get("summary_en") or "") < 120:
        errs.append("summary_en too short")
    if p.get("confidence") not in {"confirmed", "traditional", "disputed"}:
        errs.append("bad confidence")
    if p.get("title_en") != ident["title_en"]:
        errs.append("LLM changed the pinned title")
    ident_tokens = [t for t in norm_title(ident["title_en"])
                    if t not in {"sunday", "week", "ordinary", "time", "advent", "feria",
                                 "1", "2", "3", "4", "5", "6", "7", "8", "9"}]
    body = (p.get("body_en") or "").lower()
    need = [t for t in ident_tokens if not t.isdigit()][:2]
    if need and not any(t in body for t in need):
        errs.append(f"body does not name the celebration ({need})")
    hooks = obj.get("app_hooks") or {}
    for k in ("hero_line_en", "prayer_prompt_en"):
        if not isinstance(hooks.get(k), str) or not hooks[k].strip():
            errs.append(f"app_hooks.{k} missing")
    srcs = obj.get("sources") or []
    if len(srcs) < 2:
        errs.append("fewer than 2 sources")
    urls = [s.get("url", "") for s in srcs if isinstance(s, dict)]
    domains = {re.sub(r"^www\.", "", u.split("/")[2]) for u in urls
               if u.startswith("https://") and len(u.split("/")) > 2}
    if len(domains) < 2:
        errs.append("fewer than 2 distinct source domains")
    for s in srcs:
        if not isinstance(s, dict) or not s.get("label") or not s.get("type"):
            errs.append("source missing label/type")
    for v in [p.get("summary_en", ""), p.get("body_en", ""),
              p.get("confidence_note_en", ""), hooks.get("hero_line_en", ""),
              hooks.get("prayer_prompt_en", "")]:
        if isinstance(v, str) and re.search(r"placeholder|example\.com|lorem ipsum", v, re.I):
            errs.append("placeholder text in narrative")
    return errs


def vi_overlay_for(existing: dict, ident: dict, d: str, gt: dict) -> dict:
    over = json.loads(json.dumps(existing.get("_vi_overlay") or {}))
    if ident["identity_change"]:
        over.update({"liturgical": {"title_vi": ""},
                     "primary": {"title_vi": "", "summary_vi": "", "body_vi": "",
                                 "confidence_note_vi": ""},
                     "app_hooks": {"hero_line_vi": "", "prayer_prompt_vi": ""}})
        return over

    def fix(s):
        if not isinstance(s, str) or not s:
            return s
        n = week_number(gt, d)
        if n:
            s = re.sub(r"(tuần\s+)\d+", rf"\g<1>{n}", s)
            s = re.sub(r"(Chúa Nhật\s+(?:tuần\s+)?)\d+", rf"\g<1>{n}", s)
        for en, vi in VI_WEEKDAYS.items():
            s = s.replace(f"Ngày {en}", f"Ngày {vi}")
        return s

    for sec in ("liturgical", "primary", "app_hooks"):
        if isinstance(over.get(sec), dict):
            for k, v in list(over[sec].items()):
                if k.endswith("_vi"):
                    over[sec][k] = fix(v)
    return over


def locate(d: str) -> tuple[str, object, dict | None]:
    """Return (kind, container, vi_path) for a date's source layer."""
    p_en = RESEARCH / f"{d}_result_en.json"
    p_raw = RESEARCH / f"{d}_result.json"
    p_vi = RESEARCH / f"{d}_result_vi.json"
    if p_en.exists():
        return "research", p_en, p_vi
    if p_raw.exists():
        return "research", p_raw, p_vi
    m = date.fromisoformat(d).month
    if m == 8:
        return "august", AUGUST, None
    if m == 7:
        return "fortnight", FORTNIGHT, None
    raise SystemExit(f"no source layer for {d}")


def load_entry(kind: str, container, d: str) -> tuple[dict, list | None, int | None]:
    if kind == "research":
        return json.loads(container.read_text(encoding="utf-8")), None, None
    arr = json.loads(container.read_text(encoding="utf-8"))
    for i, e in enumerate(arr):
        if e.get("date") == d:
            return e, arr, i
    raise SystemExit(f"entry {d} not in {container}")


def write_entry(kind: str, container, arr, idx, entry, d, over, vi_path):
    if kind == "research":
        container.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")
        if vi_path:
            vi_path.write_text(json.dumps(over, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
    else:
        arr[idx] = entry
        container.write_text(json.dumps(arr, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")


def compose(existing: dict, ident: dict, llm: dict, over: dict, d: str, gt_row: dict) -> dict:
    e = json.loads(json.dumps(existing))
    e["id"] = f"anno-{d}"
    e["date"] = d
    e["weekday"] = gt_row["weekday"]
    e["liturgical"] = {"rank": ident["rank"], "color": ident["color"],
                       "title_en": ident["title_en"],
                       "title_vi": (over.get("liturgical") or {}).get("title_vi", "")}
    p = e.setdefault("primary", {})
    p.update({"type": ident["type"],
              "title_en": ident["title_en"],
              "title_vi": (over.get("primary") or {}).get("title_vi", ""),
              "summary_en": llm["primary"]["summary_en"],
              "summary_vi": (over.get("primary") or {}).get("summary_vi", ""),
              "body_en": llm["primary"]["body_en"],
              "body_vi": (over.get("primary") or {}).get("body_vi", ""),
              "confidence": llm["primary"]["confidence"],
              "confidence_note_en": llm["primary"]["confidence_note_en"],
              "confidence_note_vi": (over.get("primary") or {}).get("confidence_note_vi", "")})
    hooks = e.setdefault("app_hooks", {})
    ov = over.get("app_hooks") or {}
    hooks["hero_line_en"] = llm["app_hooks"]["hero_line_en"]
    hooks["hero_line_vi"] = ov.get("hero_line_vi", "")
    hooks["prayer_prompt_en"] = llm["app_hooks"]["prayer_prompt_en"]
    hooks["prayer_prompt_vi"] = ov.get("prayer_prompt_vi", "")
    e["artwork"] = llm.get("artwork") or {"title": None, "maker": None, "date_label": None,
                                          "source_url": None, "status": "placeholder_only"}
    e["place"] = llm.get("place")
    e["sources"] = llm["sources"]
    return e


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", help="YYYY-MM")
    ap.add_argument("--dates", help="comma-separated YYYY-MM-DD")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    gt_doc = load_gt(2026)
    gt = {r["date"]: r for r in gt_doc["rows"]}
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        audit(2026, None, None, None, True, False, date.today())  # refresh build/audit_2026.json
    audit_doc = json.loads((ROOT / "build/audit_2026.json").read_text(encoding="utf-8"))
    defects = {d for d, v in audit_doc["days"].items() if v["status"] == "defect"}
    if args.month:
        defects = {d for d in defects if d.startswith(args.month)}
    if args.dates:
        want = set(args.dates.split(","))
        defects &= want
    dates = sorted(defects)
    if args.limit:
        dates = dates[:args.limit]
    if args.list or args.dry_run:
        for d in dates:
            row = gt[d]
            print(f"{d} | {row['kind']:13} | {row['title_en'][:62]}")
        print(f"TOTAL {len(dates)} defect days")
        return  # --list AND --dry-run are read-only

    fx = json.loads((ROOT / "Anno/Resources/anno_unified_2026.json").read_text(encoding="utf-8"))
    fixture = {e["date"]: e for e in fx["entries"]}
    ok = fail = 0
    for d in dates:
        row, existing = gt[d], fixture[d]
        kind, container, vi_path = locate(d)
        entry, arr, idx = load_entry(kind, container, d)
        vi_raw = json.loads(vi_path.read_text(encoding="utf-8")) if vi_path and vi_path.exists() else {}
        existing = dict(existing)
        existing["_vi_overlay"] = vi_raw if vi_path else {
            "liturgical": {"title_vi": entry.get("liturgical", {}).get("title_vi", "")},
            "primary": {k: entry.get("primary", {}).get(k, "") for k in
                        ("title_vi", "summary_vi", "body_vi", "confidence_note_vi")},
            "app_hooks": {k: entry.get("app_hooks", {}).get(k, "") for k in
                          ("hero_line_vi", "prayer_prompt_vi")},
        }
        ident = canonical_identity(row, existing, gt)
        prompt = build_prompt(d, row, ident)
        llm, errs = None, []
        for attempt in range(3):
            try:
                raw = yolo(prompt if attempt == 0 else
                           prompt + "\n\nPREVIOUS ATTEMPT FAILED: " + "; ".join(errs[:5]) +
                           "\nReturn a corrected JSON object. Use only URLs you are confident are live "
                           "(prefer vatican.va, usccb.org, newadvent.org, catholicculture.org). "
                           "Do not include an artwork URL unless it is a real Commons file page.")
                candidate = json.loads(extract_json(raw))
                errs = validate(candidate, ident)
                if errs:
                    continue
                # Drop dead URLs (repo pipeline convention); require 2 live ones.
                live = [s for s in candidate["sources"]
                        if isinstance(s, dict) and url_live(s.get("url", ""))]
                if len(live) < 2:
                    errs = [f"only {len(live)} live source URLs after HTTP check"]
                    continue
                seen_domains = set()
                distinct = []
                for s in live:
                    dom = re.sub(r"^www\.", "", s["url"].split("/")[2])
                    if dom not in seen_domains:
                        distinct.append(s)
                        seen_domains.add(dom)
                if len(distinct) < 2:
                    # Deterministic second source: the official USCCB daily
                    # readings page for this date (live-checked, date-pinned).
                    dte = date.fromisoformat(d)
                    fallback = f"https://bible.usccb.org/bible/readings/{dte:%m%d%y}.cfm"
                    fdom = re.sub(r"^www\.", "", fallback.split("/")[2])
                    if url_live(fallback) and all(
                            re.sub(r"^www\.", "", s["url"].split("/")[2]) != fdom
                            for s in distinct):
                        distinct.append({"label": f"USCCB Daily Readings {d}",
                                         "url": fallback, "type": "liturgical_calendar"})
                if len(distinct) < 2:
                    errs = ["fewer than 2 distinct live source domains"]
                    continue
                candidate["sources"] = distinct
                art = candidate.get("artwork") or {}
                if art.get("status") == "public_domain":
                    au = art.get("source_url") or ""
                    if "commons.wikimedia.org/wiki/File:" not in au or not url_live(au):
                        candidate["artwork"] = {"title": None, "maker": None,
                                                "date_label": None, "source_url": None,
                                                "status": "placeholder_only"}
                llm = candidate
                break
            except Exception as e:  # noqa: BLE001
                errs = [str(e)[:200]]
        if llm is None:
            print(f"FAIL {d}: {'; '.join(errs[:3])}", flush=True)
            fail += 1
            continue
        over = vi_overlay_for(existing, ident, d, gt)
        new_entry = compose(entry, ident, llm, over, d, row)
        write_entry(kind, container, arr, idx, new_entry, d, over, vi_path)
        print(f"OK   {d}: {ident['rank']:17} | {ident['title_en'][:55]}", flush=True)
        ok += 1
        time.sleep(0.4)
    print(f"REPAIR SUMMARY: ok={ok} fail={fail} total={len(dates)}")


if __name__ == "__main__":
    main()
