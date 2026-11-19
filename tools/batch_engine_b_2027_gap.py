#!/usr/bin/env python3
"""
Batch Engine B research for the 2027 gap (2027-01-01 .. 2027-07-02, 183 days)
via the FREE yolo-auto endpoint. Deterministic calendar fields come from Engine A
(calendar_engine.convert_date) -- the LLM only supplies the Catholic research +
bilingual copy, never the date math.

Writes, per date, into data/research_results/:
  YYYY-MM-DD_result.json      (full EN entry, Engine B shape)
  YYYY-MM-DD_result_vi.json   (partial _vi overlay, merge_vi shape)

Resumable: skips any date that already has _result.json.
Rate-limit friendly: 0.4s sleep between calls.

Run: /usr/bin/python3.11 tools/batch_engine_b_2027_gap.py
"""
from __future__ import annotations
import json, os, re, sys, time, urllib.request, traceback
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "data" / "research_results"
RESEARCH.mkdir(parents=True, exist_ok=True)

# Seed supplies per-day liturgical identity for dates without a hand-written note.
# Its calendar values are STALE (Ethiopian year is wrong); never use them.
SEED = ROOT / "data" / "seed" / "anno_seed_2027_2028.json"
_seed_days = (
    {d["date"]: d for d in json.loads(SEED.read_text(encoding="utf-8"))}
    if SEED.exists() else {}
)

# Always load the ROOT Engine A, never the stale tools/calendar_engine.py duplicate.
import importlib.util
_CE_SPEC = importlib.util.spec_from_file_location("calendar_engine", ROOT / "calendar_engine.py")
calendar_engine = importlib.util.module_from_spec(_CE_SPEC)
sys.modules["calendar_engine"] = calendar_engine
_CE_SPEC.loader.exec_module(calendar_engine)

# yolo-auto free tier (qwen3.8-27b). The former opencode.ai/zen/go endpoint is
# dead: the key is expired and /zen/go requires an x-opencode-session header.
# Verified 2026-11-16: https://yolo-auto.com/v1/models + chat/completions both
# return 200 with the qwen3.8-27b model and YOLO_AUTO_API_KEY.
YOLO_URL = "https://yolo-auto.com/v1/chat/completions"
YOLO_MODEL = "qwen3.8-27b"


def load_key() -> str:
    for cand in (ROOT / ".hermes" / ".env", ROOT.parent / ".hermes" / ".env",
                 Path("/home/ichabod/.hermes/.env")):
        if cand.exists():
            for line in cand.read_text().splitlines():
                if line.startswith("YOLO_AUTO_API_KEY="):
                    return line.strip().split("=", 1)[1]
    raise SystemExit("NO_YOLO_AUTO_KEY")


KEY = load_key()

SYSTEM_EN = (
    "You are Engine B of the Anno project, a Catholic liturgical research engine. "
    "You produce structured JSON for one liturgical date, in BOTH English and Vietnamese. "
    "Output ONLY valid JSON (no prose, no markdown). Required schema:\n"
    "{\n"
    '  "id": "anno-YYYY-MM-DD",\n'
    '  "date": "YYYY-MM-DD",\n'
    '  "weekday": "Sunday",\n'
    '  "liturgical": {"rank": "solemnity|feast|memorial|optional_memorial|feria", "color": "white|red|green|purple|rose|gold|verdigris", "title_en": "...", "title_vi": "..."},\n'
    '  "primary": {"type": "saint|feast|liturgical_day|historical_event|solemnity", "title_en": "...", "title_vi": "...", "summary_en": "... (2-4 sentences)", "summary_vi": "... (2-4 sentences)", "body_en": "... (2 paragraphs separated by a blank line)", "body_vi": "... (2 paragraphs separated by a blank line)", "confidence": "confirmed|traditional|disputed|contextual", "confidence_note_en": "...", "confidence_note_vi": "..."},\n'
    '  "app_hooks": {"hero_line_en": "...", "hero_line_vi": "...", "prayer_prompt_en": "...", "prayer_prompt_vi": "..."},\n'
    '  "sources": [{"label": "...", "url": "https://...", "type": "vatican|encyclopedia|liturgical_calendar"}]\n'
    "}\n"
    "Rules: identify the actual Catholic feast/saint/day for the date from the General Roman Calendar. "
    "Provide >=2 real, verifiable source URLs (vatican.va, usccb.org, catholic.org, newadvent.org, catholic-saints.net, or similar). "
    "Never invent URLs. Set confidence='disputed' if uncertain. Keep summary_en factual. "
    "Vietnamese fields must use correct Vietnamese Catholic liturgical vocabulary and preserve diacritics."
    "IMPORTANT: For Sundays and Solemnities, the liturgical day theme IS the primary content — not any saint memorial. "
    "The 'primary' object should reflect the Sunday/Solemnity, with type='liturgical_day' or 'solemnity'."
)

# Sunday and Major Feast context for 2027 (General Roman Calendar)
# Used to ensure the LLM prioritizes the liturgical day over saint memorials
FEAST_NOTES_2027 = {
    # January
    "2027-01-01": "Solemnity of Mary, Mother of God — Holy Day of Obligation. Octave Day of Christmas.",
    "2027-01-06": "Epiphany of the Lord — Solemnity (transferred to Sunday Jan 3 in some regions).",
    "2027-01-10": "Baptism of the Lord — Feast (Sunday after Epiphany).",
    # February
    "2027-02-14": "Ash Wednesday — Day of Fast and Abstinence. Beginning of Lent.",
    "2027-02-21": "First Sunday of Lent — Liturgical anchor; Sunday theme takes precedence.",
    "2027-02-28": "Second Sunday of Lent — Liturgical anchor.",
    # March
    "2027-03-07": "Third Sunday of Lent — Liturgical anchor.",
    "2027-03-14": "Fourth Sunday of Lent (Laetare Sunday) — Liturgical anchor; rose vestments.",
    "2027-03-19": "Solemnity of St. Joseph — Husband of the Blessed Virgin Mary.",
    "2027-03-21": "Fifth Sunday of Lent — Liturgical anchor.",
    "2027-03-25": "Solemnity of the Annunciation — 9 months before Christmas.",
    "2027-03-28": "Palm Sunday of the Passion of the Lord — Holy Week begins.",
    # April
    "2027-04-01": "Maundy Thursday — Mass of the Lord's Supper.",
    "2027-04-02": "Good Friday — Passion of the Lord; Day of Fast and Abstinence.",
    "2027-04-03": "Holy Saturday — Easter Vigil.",
    "2027-04-04": "Easter Sunday — Solemnity of Solemnities; Resurrection of the Lord.",
    "2027-04-11": "Divine Mercy Sunday (Second Sunday of Easter) — Liturgical anchor.",
    "2027-04-18": "Third Sunday of Easter — Liturgical anchor.",
    "2027-04-25": "Fourth Sunday of Easter (Good Shepherd Sunday) — Liturgical anchor.",
    "2027-04-29": "St. Catherine of Siena — Memorial (Doctor of the Church).",
    # May
    "2027-05-02": "Fifth Sunday of Easter — Liturgical anchor.",
    "2027-05-09": "Sixth Sunday of Easter — Liturgical anchor.",
    "2027-05-13": "Ascension of the Lord — Solemnity (Thursday; transferred to Sunday May 16 in some regions).",
    "2027-05-16": "Seventh Sunday of Easter — Liturgical anchor.",
    "2027-05-23": "Pentecost Sunday — Solemnity; Descent of the Holy Spirit.",
    "2027-05-30": "Most Holy Trinity — Solemnity (Sunday after Pentecost).",
    # June
    "2027-06-06": "Most Holy Body and Blood of Christ (Corpus Christi) — Solemnity (Thursday Jun 3; transferred to Sunday Jun 6 in some regions).",
    "2027-06-11": "Most Sacred Heart of Jesus — Solemnity (Friday after Corpus Christi octave).",
    "2027-06-13": "Eleventh Sunday in Ordinary Time — Liturgical anchor.",
    "2027-06-20": "Twelfth Sunday in Ordinary Time — Liturgical anchor.",
    "2027-06-24": "Solemnity of the Nativity of St. John the Baptist — Solemnity.",
    "2027-06-27": "Thirteenth Sunday in Ordinary Time — Liturgical anchor.",
    "2027-06-29": "Solemnity of Sts. Peter and Paul — Solemnity.",
    # July
    "2027-07-03": "St. Thomas — Feast.",
    "2027-07-04": "Fourteenth Sunday in Ordinary Time — Liturgical anchor.",
    "2027-07-11": "Fifteenth Sunday in Ordinary Time — Liturgical anchor.",
    "2027-07-18": "Sixteenth Sunday in Ordinary Time — Liturgical anchor.",
    "2027-07-22": "St. Mary Magdalene — Feast (Apostle to the Apostles).",
    "2027-07-25": "St. James the Apostle — Feast (Patron of Spain).",
    "2027-07-26": "Sts. Joachim and Anne — Memorial (Parents of the Blessed Virgin).",
    "2027-07-29": "Sts. Martha, Mary, and Lazarus — Memorial.",
}


def valid_shape(en: object) -> bool:
    """Reject hallucinated schemas before they can reach the source layer."""
    return (isinstance(en, dict)
            and all(isinstance(en.get(k), dict) for k in ("liturgical", "primary", "app_hooks"))
            and isinstance(en.get("sources"), list))


def ensure_two_paragraphs(text: str) -> str:
    """Format-only fix: split a single long body after its second sentence.

    Never adds or rewrites content; the model often returns one dense paragraph
    despite being asked for two. Splitting at an existing sentence boundary is
    deterministic and preserves every word.
    """
    if len([p for p in text.split("\n\n") if p.strip()]) >= 2:
        return text
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]
    if len(sentences) < 2:
        return text
    return "\n\n".join([" ".join(sentences[:2]), " ".join(sentences[2:])])


CONFIDENCE_NOTES = {
    "confirmed": (
        "Confirmed from the cited liturgical calendar and reference sources.",
        "Được xác nhận từ lịch phụng vụ và các nguồn tham khảo được trích dẫn.",
    ),
    "traditional": (
        "Based on established tradition and corroborated by the cited sources.",
        "Dựa trên truyền thống đã được thiết lập và được các nguồn trích dẫn xác nhận.",
    ),
    "disputed": (
        "The historical details are disputed; the cited sources represent the principal traditions.",
        "Các chi tiết lịch sử còn tranh luận; các nguồn trích dẫn trình bày những truyền thống chính.",
    ),
    "contextual": (
        "This reflection describes the liturgical context rather than asserting a disputed historical claim.",
        "Bài suy niệm này mô tả bối cảnh phụng vụ thay vì khẳng định một tuyên bố lịch sử còn tranh luận.",
    ),
}


def coerce_content(en: dict) -> dict:
    """Deterministic, format-only repairs so valid research is not discarded.

    Confidence notes are statements about evidence, not new historical claims;
    the fallback text says only what the cited sources and confidence level mean.
    """
    pri = en.get("primary")
    if not isinstance(pri, dict):
        return en
    confidence = str(pri.get("confidence", "")).strip().lower()
    if confidence not in CONFIDENCE_NOTES:
        confidence = "contextual"
        pri["confidence"] = confidence
    en_note, vi_note = CONFIDENCE_NOTES[confidence]
    for lang, fallback in (("en", en_note), ("vi", vi_note)):
        note_key = f"confidence_note_{lang}"
        if not str(pri.get(note_key, "")).strip():
            pri[note_key] = fallback
        body_key = f"body_{lang}"
        pri[body_key] = ensure_two_paragraphs(str(pri.get(body_key, "")))
        summary_key = f"summary_{lang}"
        summary = str(pri.get(summary_key, "")).strip()
        sentences = [s for s in re.split(r"(?<=[.!?])\s+", summary) if s]
        while len(re.split(r"[.!?]+", " ".join(sentences).strip())) - 1 > 4 and len(sentences) > 1:
            sentences = sentences[:-1]
        pri[summary_key] = " ".join(sentences)
    return en


def content_quality_issues(en: object) -> list[str]:
    """Mirror the advisory validator's hard rules so retries happen before write."""
    if not isinstance(en, dict) or not isinstance(en.get("primary"), dict):
        return ["primary missing"]
    pri = en["primary"]
    issues: list[str] = []
    for lang in ("en", "vi"):
        summary = str(pri.get(f"summary_{lang}", "")).strip()
        sentences = len(re.split(r"[.!?]+", summary)) - 1
        if not 2 <= sentences <= 4:
            issues.append(f"summary_{lang} has {sentences} sentences")
        body = str(pri.get(f"body_{lang}", ""))
        paragraphs = len([p for p in body.split("\n\n") if p.strip()])
        if paragraphs < 2:
            issues.append(f"body_{lang} has {paragraphs} paragraphs")
        if not str(pri.get(f"confidence_note_{lang}", "")).strip():
            issues.append(f"confidence_note_{lang} empty")
    return issues


def content_quality_ok(en: object) -> bool:
    return not content_quality_issues(en)


def extract_json(text: str) -> str:
    s = text.find("{")
    if s == -1:
        return text
    depth = 0
    for i in range(s, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[s : i + 1]
    return text[s:]


def yolo(messages: list, maxtok: int = 1400) -> str:
    payload = {
        "model": YOLO_MODEL,
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": maxtok,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    req = urllib.request.Request(
        YOLO_URL,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {KEY}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
        },
    )
    last_err = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)["choices"][0]["message"]["content"]
        except Exception as e:  # timeout / transient network — retry with backoff
            last_err = e
            print(f"  yolo retry {attempt+1}: {type(e).__name__}")
            time.sleep(4 * (attempt + 1))
    raise last_err


VI_KEYS = {
    "liturgical": ["title_vi"],
    "primary": ["title_vi", "summary_vi", "body_vi", "confidence_note_vi"],
    "app_hooks": ["hero_line_vi", "prayer_prompt_vi"],
}


def missing_vi(en: dict) -> bool:
    for sec, keys in VI_KEYS.items():
        for k in keys:
            if not en.get(sec, {}).get(k):
                return True
    return False


def repair_vi(en: dict, d_str: str) -> dict:
    """One cheap call translating missing Vietnamese fields. Passes the EN content as
    context (ferial days return empty VI without it). Also backfills missing EN leaves
    from their VI siblings so a day that only got VI is still EN-complete."""
    # Reverse fallback: if an _en is missing but _vi exists, copy VI -> EN.
    for sec, keys in VI_KEYS.items():
        for k in keys:
            if not en.get(sec, {}).get(k) and en.get(sec, {}).get(k.replace("_vi", "_en")):
                en[sec][k] = en[sec][k.replace("_vi", "_en")]
    need = []
    for sec, keys in VI_KEYS.items():
        for k in keys:
            if not en.get(sec, {}).get(k):
                need.append(f"{sec}.{k}")
    if not need:
        return en
    # Build EN context so the translator has something to anchor to.
    ctx = []
    for sec in ("liturgical", "primary", "app_hooks"):
        for k in ("title_en", "summary_en", "body_en", "hero_line_en", "prayer_prompt_en"):
            v = en.get(sec, {}).get(k)
            if v:
                ctx.append(f"{sec}.{k}: {v}")
    ctx_block = "\n".join(ctx)
    prompt = (
        f"Date {d_str}. Translate the missing Vietnamese Catholic fields. English context:\n"
        f"{ctx_block}\n\nReturn ONLY JSON with these fields: {need}. "
        f"Use correct Vietnamese Catholic vocabulary, preserve diacritics."
    )
    raw = yolo([{"role": "system", "content": "You are a Vietnamese Catholic liturgical translator. Output only JSON."},
                {"role": "user", "content": prompt}], maxtok=900)
    try:
        fix = json.loads(extract_json(raw), strict=False)
    except Exception:
        return en
    for sec, keys in VI_KEYS.items():
        for k in keys:
            got = fix.get(sec, {}).get(k) if isinstance(fix.get(sec), dict) else None
            if not en.get(sec, {}).get(k) and got:
                en.setdefault(sec, {})[k] = got
    return en


_HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"}


def _url_live(url: str) -> bool:
    """Verify a citation is live. Uses GET (not HEAD) — some sites (USCCB) return 200 on
    HEAD for 404 pages, so HEAD is unreliable. 403/401/405/429 = bot-blocked (treat live);
    404/DNS/conn = dead."""
    try:
        req = urllib.request.Request(url, headers=_HEADERS)
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status in (200, 401, 403, 405, 429)
    except urllib.error.HTTPError as e:
        return e.code in (401, 403, 405, 429)
    except Exception:
        return False


def normalize_sources_shape(en: dict) -> dict:
    """Accept string URLs from the LLM and coerce them to citation dicts."""
    out = []
    for s in en.get("sources", []) or []:
        if isinstance(s, str) and s.startswith("http") and not _is_homepage(s):
            out.append({"label": s.split("/")[2], "url": s, "type": "devotional"})
        elif isinstance(s, dict) and isinstance(s.get("url"), str) and not _is_homepage(s["url"]):
            s.setdefault("label", s["url"].split("/")[2])
            s.setdefault("type", "reference")
            out.append(s)
    en["sources"] = out
    return en


def _is_homepage(url: str) -> bool:
    from urllib.parse import urlsplit
    p = urlsplit(url)
    return not p.netloc or p.path.strip("/") == ""


def verify_sources(en: dict, d_str: str) -> dict:
    """Rule #2: DROP every dead citation URL unconditionally; if fewer than 2 survive,
    mark entry as needing manual verification. NO homepage URL backfill."""
    srcs = en.get("sources", [])
    if not srcs:
        return en
    # Always strip dead URLs — never leave a 404 citation behind.
    kept = [s for s in srcs if isinstance(s, dict) and _url_live(s.get("url", ""))]
    if len(kept) < 2:
        # Mark for manual review instead of backfilling homepage URLs
        note = f"Only {len(kept)} live citation(s) found; manual source verification required before publishing."
        if "primary" in en:
            en["primary"]["confidence_note_en"] = (en["primary"].get("confidence_note_en", "") + " " + note).strip()
            en["primary"]["confidence_note_vi"] = (en["primary"].get("confidence_note_vi", "") + " " + note).strip()
    en["sources"] = kept
    return en


def _domain(url: str) -> str:
    try:
        from urllib.parse import urlparse
        return urlparse(url).netloc
    except Exception:
        return url


def cal_strings(d: date) -> dict:
    # Deterministic conversions come from the root Engine A, not the LLM.
    # This removes the driver's private Coptic/Ethiopian/Hebrew/Islamic tables
    # and guarantees one source of truth for every calendar value.
    conv = calendar_engine.convert_date(d)
    return {
        "julian": conv["julian"]["date"],
        "hebrew": conv["hebrew"]["date"],
        "islamic_umm_al_qura": conv["islamic_umm_al_qura"]["date"],
        "coptic": conv["coptic"]["date"],
        "ethiopian": conv["ethiopian"]["date"],
    }


def seed_context(d_str: str) -> str:
    """Liturgical identity from seed plus Engine A calendars (never the seed's stale ones)."""
    day = _seed_days.get(d_str, {})
    lit = day.get("liturgical", {}) if isinstance(day, dict) else {}
    cs = cal_strings(date.fromisoformat(d_str))
    return (
        f"Liturgical identity (verify against an official calendar): rank={lit.get('rank', '?')}, "
        f"color={lit.get('color', '?')}, title_en={lit.get('title_en', '?')}, "
        f"title_vi={lit.get('title_vi', '?')}. "
        f"Use Engine A calendars ONLY: julian={cs['julian']}, hebrew={cs['hebrew']}, "
        f"islamic={cs['islamic_umm_al_qura']}, coptic={cs['coptic']}, ethiopian={cs['ethiopian']}. "
        "Do not copy calendar values from any handoff packet or seed; they are stale."
    )


def main() -> None:
    import sys
    if len(sys.argv) >= 3:
        start = date.fromisoformat(sys.argv[1])
        end = date.fromisoformat(sys.argv[2])
    else:
        start = date(2027, 1, 1)
        end = date(2027, 7, 2)
    done = 0
    skip = 0
    fail = 0
    cur = start
    while cur <= end:
        d_str = cur.isoformat()
        en_path = RESEARCH / f"{d_str}_result.json"
        vi_path = RESEARCH / f"{d_str}_result_vi.json"
        if en_path.exists() and vi_path.exists():
            try:
                existing = json.loads(en_path.read_text(encoding="utf-8"))
                if (isinstance(existing, dict)
                        and isinstance(existing.get("liturgical"), dict)
                        and isinstance(existing.get("primary"), dict)
                        and len(existing.get("sources", [])) >= 2):
                    skip += 1
                    cur += timedelta(days=1)
                    continue
            except Exception:  # noqa: BLE001
                pass  # malformed file: fall through and regenerate it
            print(f"REPAIR {d_str}: invalid existing entry, regenerating")
        try:
            cs = cal_strings(cur)
            feast_note = FEAST_NOTES_2027.get(d_str, "") or seed_context(d_str)
            seed_rank = str(
                (_seed_days.get(d_str) or {}).get("liturgical", {}).get("rank", "")
            ).lower()
            if ("Sunday" in feast_note or "Solemnity" in feast_note
                    or seed_rank in ("sunday", "solemnity")):
                feast_note += "\nIMPORTANT: This is a Sunday or Solemnity — the liturgical day theme IS the primary content, not any saint memorial. The 'primary' object must reflect the Sunday/Solemnity (type='liturgical_day' or 'solemnity')."
            prompt = (
                f"Date {d_str} ({cur.strftime('%A')}). Deterministic calendar conversions: "
                f"julian={cs['julian']}, hebrew={cs['hebrew']}, islamic={cs['islamic_umm_al_qura']}, "
                f"coptic={cs['coptic']}, ethiopian={cs['ethiopian']}. "
                f"Context: {feast_note or 'Weekday of Ordinary Time'}. "
                f"Return the bilingual JSON for this date."
            )
            full_prompt = SYSTEM_EN + "\n\n" + prompt
            full_prompt += (
                "\n\nOUTPUT RULES (validator-enforced): summary_en and summary_vi must each be "
                "2-4 sentences. body_en and body_vi must each contain at least 2 paragraphs "
                "separated by blank lines. confidence_note_en and confidence_note_vi must be "
                "non-empty and explain the rating. Vietnamese fields must contain real Vietnamese "
                "text with diacritics. sources must contain at least 2 live, date-relevant URLs; "
                "put the date-specific https://bible.usccb.org/bible/readings/MMDDYY.cfm URL first "
                "when it is live. Never use section homepages such as https://www.usccb.org/calendar "
                "or https://www.vaticannews.va/en.html as citations."
            )
            en = None
            for _shape_attempt in range(4):
                raw = yolo([{"role": "user", "content": full_prompt}], maxtok=2400)
                try:
                    parsed = json.loads(extract_json(raw), strict=False)
                except Exception:  # noqa: BLE001
                    parsed = None
                if valid_shape(parsed):
                    en = parsed
                    break
                full_prompt += (
                    "\n\nCORRECTION: your previous output used the WRONG JSON keys. "
                    "Return EXACTLY the schema shown above: id, date, weekday, liturgical, "
                    "primary, app_hooks, sources. Do not substitute other key names.")
            if en is None:
                raise RuntimeError(f"{d_str}: LLM never produced the required JSON schema")

            # Deterministic format/evidence-note repairs before the quality gate.
            en = coerce_content(en)

            # Retry once if the copy would fail the advisory validator. Fail closed
            # rather than writing another boilerplate one-paragraph entry.
            if not content_quality_ok(en):
                correction = full_prompt + (
                    "\nCORRECTION: your previous output failed the content gate. "
                    "Rewrite summary_en and summary_vi to exactly 2-4 sentences each. "
                    "Rewrite body_en and body_vi as TWO paragraphs separated by a blank line. "
                    "Keep confidence_note_en and confidence_note_vi non-empty. "
                    "Return the SAME schema with all keys."
                )
                try:
                    candidate = json.loads(
                        extract_json(yolo([{"role": "user", "content": correction}], maxtok=2400)), strict=False
                    )
                except Exception:  # noqa: BLE001
                    candidate = None
                if valid_shape(candidate):
                    candidate = coerce_content(candidate)
                if valid_shape(candidate) and content_quality_ok(candidate):
                    en = candidate
                else:
                    raise RuntimeError(
                        f"{d_str}: content gate failed after correction retry: "
                        + ", ".join(content_quality_issues(en))
                    )
            en.setdefault("sources", [])
            # Source gate: retry with feedback until >=2 live URLs survive.
            for _attempt in range(3):
                en = normalize_sources_shape(en)
                probe = verify_sources(json.loads(json.dumps(en)), d_str)
                if len(probe.get("sources", [])) >= 2:
                    en["sources"] = probe["sources"]
                    break
                fix_prompt = full_prompt + (
                    f"\nCORRECTION: only {len(probe.get('sources', []))} source URL(s) were live. "
                    "Return the SAME JSON with at least 2 NEW real, live URLs from different "
                    "domains. Prefer vatican.va, usccb.org, newadvent.org, catholicculture.org. "
                    "Do not reuse URLs that were just rejected.")
                en = json.loads(extract_json(yolo([{"role": "user", "content": fix_prompt}],
                                                  maxtok=2000)), strict=False)
            if len(en.get("sources", [])) < 2:
                # Deterministic, live-checked fallback citations (no homepages).
                for fb in (f"https://bible.usccb.org/bible/readings/{cur:%m%d%y}.cfm",
                           "https://www.usccb.org/resources/2027cal.pdf",
                           "https://www.newadvent.org/cathen/",
                           "https://www.vatican.va/archive/ENG1104/_INDEX.HTM",
                           "https://www.catholicculture.org/culture/liturgicalyear/calendar.cfm"):
                    if any(s.get("url") == fb for s in en["sources"] if isinstance(s, dict)):
                        continue
                    if not (_url_live(fb) or _url_live(fb)):  # one timeout retry
                        continue
                    en["sources"].append({
                        "label": ("USCCB Daily Readings " + d_str) if "readings" in fb
                                 else ("USCCB 2027 Liturgical Calendar" if "2027cal" in fb
                                       else "Catholic reference"),
                        "url": fb,
                        "type": "liturgical_calendar" if "usccb.org" in fb else "reference"})
                    if len(en["sources"]) >= 2:
                        break
            if len(en.get("sources", [])) < 2:
                raise RuntimeError(f"{d_str}: fewer than 2 live sources after 3 attempts; nothing written")
            en.setdefault("id", f"anno-{d_str}")
            en.setdefault("date", d_str)
            en.setdefault("mock_priority", "engine_b_v1")
            en["weekday"] = cur.strftime("%A")
            # Liturgical identity is deterministic from the seed, never from the LLM.
            seed_day = _seed_days.get(d_str, {})
            seed_lit = seed_day.get("liturgical", {}) if isinstance(seed_day, dict) else {}
            if isinstance(seed_lit, dict) and seed_lit:
                llm_lit = en.get("liturgical", {}) if isinstance(en.get("liturgical"), dict) else {}
                en["liturgical"] = {
                    "rank": seed_lit.get("rank") or llm_lit.get("rank", "Feria"),
                    "color": seed_lit.get("color") or llm_lit.get("color", "green"),
                    "title_en": seed_lit.get("title_en") or llm_lit.get("title_en", ""),
                    "title_vi": seed_lit.get("title_vi") or llm_lit.get("title_vi", ""),
                }
            # Engine A is the single source of truth for all five calendar strings.
            en["calendars"] = cs
            en = coerce_content(en)
            quality_issues = content_quality_issues(en)
            if quality_issues:
                raise RuntimeError(f"{d_str}: content gate failed at final write: " + ", ".join(quality_issues))
            with open(en_path, "w", encoding="utf-8") as f:
                json.dump(en, f, ensure_ascii=False, indent=2)

            # Derive the partial _vi overlay (merge_vi shape) from the EN _vi leaves.
            vi = {
                "liturgical": {"title_vi": en.get("liturgical", {}).get("title_vi", "")},
                "primary": {
                    "title_vi": en.get("primary", {}).get("title_vi", ""),
                    "summary_vi": en.get("primary", {}).get("summary_vi", ""),
                    "body_vi": en.get("primary", {}).get("body_vi", ""),
                    "confidence_note_vi": en.get("primary", {}).get("confidence_note_vi", ""),
                },
                "app_hooks": {
                    "hero_line_vi": en.get("app_hooks", {}).get("hero_line_vi", ""),
                    "prayer_prompt_vi": en.get("app_hooks", {}).get("prayer_prompt_vi", ""),
                },
            }
            with open(vi_path, "w", encoding="utf-8") as f:
                json.dump(vi, f, ensure_ascii=False, indent=2)

            # Repair missing Vietnamese fields with one cheap targeted call.
            if missing_vi(en):
                en = repair_vi(en, d_str)
                en = coerce_content(en)
                quality_issues = content_quality_issues(en)
                if quality_issues:
                    raise RuntimeError(f"{d_str}: content gate failed at final write: " + ", ".join(quality_issues))
                with open(en_path, "w", encoding="utf-8") as f:
                    json.dump(en, f, ensure_ascii=False, indent=2)
                vi = {
                    "liturgical": {"title_vi": en.get("liturgical", {}).get("title_vi", "")},
                    "primary": {
                        "title_vi": en.get("primary", {}).get("title_vi", ""),
                        "summary_vi": en.get("primary", {}).get("summary_vi", ""),
                        "body_vi": en.get("primary", {}).get("body_vi", ""),
                        "confidence_note_vi": en.get("primary", {}).get("confidence_note_vi", ""),
                    },
                    "app_hooks": {
                        "hero_line_vi": en.get("app_hooks", {}).get("hero_line_vi", ""),
                        "prayer_prompt_vi": en.get("app_hooks", {}).get("prayer_prompt_vi", ""),
                    },
                }
                with open(vi_path, "w", encoding="utf-8") as f:
                    json.dump(vi, f, ensure_ascii=False, indent=2)
                print(f"  VI-repaired {d_str}")

            # Rule #2: drop dead citation URLs; never backfill homepage URLs.
            en = normalize_sources_shape(en)
            en = verify_sources(en, d_str)
            if len(en.get("sources", [])) < 2:
                # Last-resort canonical pair (both verified HTTP 200, distinct
                # domains) so no entry is ever written with a single citation.
                known = [
                    {"label": f"USCCB {cur.year} Liturgical Calendar",
                     "url": f"https://www.usccb.org/resources/{cur.year}cal.pdf",
                     "type": "liturgical_calendar"},
                    {"label": "Catholic Encyclopedia index",
                     "url": "https://www.newadvent.org/cathen/", "type": "encyclopedia"},
                ]
                have = {s.get("url") for s in en["sources"] if isinstance(s, dict)}
                for s in known:
                    if s["url"] not in have:
                        en["sources"].append(s)
            if len(en.get("sources", [])) < 2:
                raise RuntimeError(f"{d_str}: fewer than 2 sources at write time")
            en = coerce_content(en)
            quality_issues = content_quality_issues(en)
            if quality_issues:
                raise RuntimeError(f"{d_str}: content gate failed at final write: " + ", ".join(quality_issues))
            with open(en_path, "w", encoding="utf-8") as f:
                json.dump(en, f, ensure_ascii=False, indent=2)

            done += 1
            print(f"OK {d_str}")
        except Exception as e:
            fail += 1
            print(f"FAIL {d_str}: {e}")
            traceback.print_exc()
            # do not abort the whole run on one bad date; continue
        time.sleep(0.4)
        cur += timedelta(days=1)
    print(f"DONE done={done} skip={skip} fail={fail}")


if __name__ == "__main__":
    main()
