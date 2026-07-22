# AGENT C — QA REPORT · Pilot batch 2026-11-23 → 2026-11-29

**Gate result: PASS** (after repairs below). Final file: `PILOT_FINAL_2026-11-23_2026-11-29.json` (7 entries, JSON-validated, schema-complete).

---

## 1. SCHEMA REPAIR — what was missing, what was added

Agent B's structural report was accurate. Every entry (7/7) was missing the same four primary fields:

| Field | Status before | Fix |
|---|---|---|
| `primary.summary_en` | missing 7/7 | composed from body/dossier, 1–2 sentences each |
| `primary.summary_vi` | missing 7/7 | composed natively in Agent B's register |
| `primary.confidence_note_en` | missing 7/7 | written from each entry's confidence profile |
| `primary.confidence_note_vi` | missing 7/7 | native Vietnamese composition |
| `liturgical.rank` / `title_en` / `title_vi` | missing 7/7 | added (rank slugs: optional_memorial / memorial / weekday_civic_observance / weekday_devotional / weekday / sunday) |
| `app_hooks.hero_line_*` / `prayer_prompt_*` | in `primary` only | mirrored into `app_hooks` per contract |
| `mock_priority` (top-level) | missing 7/7 | added: 11/24 = `flagship`, 11/26 & 11/29 = `high`, rest `standard` |

`vi_notes` + `audio_script` (script_en/script_vi) were present and well-formed in all 7 entries. Fixture envelope (`schema_version`, `generated_on`, `source_window`, `editorial_policy`, `entries`) intact. All keys snake_case. **PASS.**

## 2. URL REALITY CHECK

28 unique URLs curl-checked (HTTP status), failures retried with browser UA and via fetch service.

| URL | Result | Action |
|---|---|---|
| newadvent.org/cathen/04012c.htm (Clement I — the correct `c` page, not the composer trap) | 200 ✓ | keep |
| newadvent.org/cathen/03445a.htm (Catherine) | 200 ✓ | keep |
| bible.usccb.org readings ×8 (112326, 112426, 112526, 112626-Thanksgiving, 112726, 112826, 112926, 112722) | 200 ×2, then 403 ×6 | **keep** — 403 is USCCB bot-blocking of curl, not a dead page; two fetched 200 in the same run, pattern verified by Agent A live-fetch and by 2025 same-cycle page via search. The no-`.cfm` Thanksgiving URL form is correct. |
| catholicworldreport.com (Miguel Pro) | 200 ✓ | keep |
| ewtnnews.com (Andrew Dũng-Lạc) | 200 ✓ | keep |
| causesanti.va (Martiri del Vietnam) | 200 ✓ | keep |
| **cbcvietnam.org/martyrs-under-nguyen-dynasty-persecution-faith/** | **unreachable (000)** | **REPLACED** with `https://www.cbcvietnam.org/martyr-saints-of-vietnam/` — verified live; it is the CBCV hub carrying that article, and independently confirms the June 19, 1988 canonization date. |
| ccel.org cathen14.pdf (Vénard letter) | 200 ✓ | keep |
| museothyssen.org (Caravaggio Catherine) | 200 ✓ | keep |
| plimoth.org | 200 ✓ | keep |
| chapellenotredamedelamedaillemiraculeuse.com | 200 ✓ | keep |
| vaticanstate.va (St James of the Marches) | 200 ✓ | keep |
| franciscanmedia.org (St James) | 200 ✓ | keep |
| whc.unesco.org/en/list/1433 (Church of the Nativity) | 200 ✓ | keep |
| commons.wikimedia.org ×7 artwork files | 200 ✓ all | keep — note 11/24 filename has source-side typo `Matyrdom_of_Saint_Pierre_Borie_1838_Vietnam.jpg`, but it resolves to the correct file |

CatholicCulture: **0 occurrences** — correctly dropped upstream. No `example.com`, no invented New Advent IDs. **PASS** (1 replacement).

## 3. FACT ARBITRATION — verdicts

| # | Question | Verdict | Evidence |
|---|---|---|---|
| a | 117 Martyrs canonization: June 19 vs July 19, 1988 | **June 19, 1988.** July 19 is a secondary-source error (EWTN snippet). | CBCV (fetched live), Catholic Times/CNA, Cardiff West Catholics, multiple parish sources all give June 19, 1988. Date inserted into body_en/body_vi/summaries/audio script. |
| b | Bl. Andrew Phú Yên's death: July 26 vs 27, 1644 | **July 26, 1644 primary**, July 27 acknowledged. | Vatican News (2025, via diocesan bulletin): executed 26 July 1644; his feast is July 26. New Catholic Encyclopedia Jubilee vol. gives 27 July. Bodies now read "July 26, 1644 (some sources give July 27)" / "ngày 26 tháng 7 năm 1644 (có tài liệu ghi ngày 27)"; confidence notes record the discrepancy. |
| c | Christ Cathedral altar relic of St. Andrew Dũng-Lạc | **Stays OUT.** Unverifiable against rcbo.org (only a kids.kiddle.co summary seen). Confirmed absent from both EN and VI bodies; `vi_notes.local_resonance_flags` documents the deliberate omission. The La Vang Shrine mention (rcbo.org-sourced) remains. |
| d | Advent I Year A citations (Is 2:1-5 / Rom 13:11-14 / Mt 24:37-44) | **Verified correct.** | USCCB same-cycle page (2025-11-30) and 2022 cycle page both confirm; dossier's Ps 80 anomaly noted as a page-composition artifact, not a citation error. |

## 4. VI QUALITY GATE

Read all `*_vi` fields in full. Overall: native, reverent, parish-editor register; diacritics clean; terminology consistent (Lễ nhớ tùy chọn, Mùa Thường Niên, Đức Mẹ, Thánh lễ, Chân phước, tiên khởi tử đạo, Kinh Vực Sâu). No MT fingerprints found. Fixes applied:

1. `vua Trajanô` → `hoàng đế Trajanô` (11/23) — register: Roman emperors are *hoàng đế*, not *vua*.
2. `vua Maximinusô` → `hoàng đế Maximinô` (11/25) — same fix + standard Vietnamese form of the name.
3. `Sách Xán` → `Sách Tiến sĩ (Sirach)` (11/26) — "Xán" is not the Catholic Vietnamese book name; CGKPV tradition uses **Sách Tiến sĩ** (Ecclesiasticus).
4. Sirach 50:22-24 citation (EN+VI) — marked as adapted/diễn ý so quotation marks don't impersonate an official rendering.
5. Vénard letter (VI) — added "theo bản diễn dịch" so the «…» block is honestly a careful rendering, not a claimed official CGKPV-equivalent text. EN quotes the verified Catholic Encyclopedia text and is untouched.
6. `đám chứng nhân` → `đoàn chứng nhân` (11/24) — register elevation.

Scripture fragments (Is 2:5, Mt 24:42, Lc 17:17 in VI) sit within normal homiletic-paraphrase distance of CGKPV wording and are woven into prose; left as-is. **PASS.**

## 5. CONFIDENCE HONESTY

All 7 entries were already honest: Catherine's Acts = traditional (with the 1969/2002 calendar history stated); Clement's anchor = traditional; Miraculous Medal = traditional-with-documentation; La Vang appears only as a verified shrine fact (no apparition claims asserted); canonization-grade material = confirmed. The new `confidence_note_*` fields now make this explicit per entry. **PASS.**

---

## REMAINING RISKS (carried to production)

1. **USCCB curl-403**: pages are live for browsers but hostile to scripted fetch; production pipeline should verify USCCB URLs via a rendering fetch or accept pattern-validation + one live spot-check per batch.
2. **Islamic calendar column** is tabular-civil (±1 day vs Umm al-Qura) — flagged in `computation_note`; acceptable for devotional use, not for religious ruling.
3. **Andrew Phú Yên date discrepancy** is disclosed in-text; if the app ever shows a single-date field for him, use July 26 (feast day / Vatican News).
4. **Artwork subject verification** was URL-level (200 + filename/title match); a human should eyeball the 7 Commons files before the pilot ships visually.
5. `place.source_url` for 11/24 reuses the EWTN article (execution site at Ô Cầu Giấy is approximate in coords) — acceptable at `contextual` confidence.
