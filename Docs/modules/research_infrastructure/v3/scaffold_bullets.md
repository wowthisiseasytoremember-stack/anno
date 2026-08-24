# Research Infrastructure Module — Scaffold Bullets for Worker Agent

**Source:** `docs/modules/research_infrastructure/v3/anno_mapping.md`  
**For:** Worker agent reference — what to build, minimal structure

---

## Build-Ready Items (scaffold only, not full implementation)

### 1. Validation Gate Script — `tools/validate_engine_b_output.py`
- Python script: validates Engine B JSON output against schema
- Checks:
  - Schema compliance: all required fields, id pattern, rank/color enums, confidence enum
  - Source validation: ≥2 sources, HTTP 200 resolution, no example.com, type↔URL pattern match
  - Content quality: summary 2-4 sentences, body 3+ paragraphs, no placeholder text
  - Confidence consistency: Solemnity/Feast → confirmed; place.confidence matches
  - Bilingual fields: both *_en and *_vi present; VI is genuine Catholic terminology
  - Tier rules: Tier 2 accessed≤90d; Tier 3 notes=program+date; Tier 4 notes="Produced in Vietnam; state context applies" (REJECT if missing)
- CLI: `python validate_engine_b_output.py --fixture batch.json --strict --check-sources`
- Exit codes: 0=pass, 1=revise, 2=reject

### 2. Source Citation Templates — `docs/research/source_citation_templates.md`
- Format v1/citation_templates.md as reference doc
- Per-outlet templates for 13 publishers (Vatican News VI, Radio Vatican VI, VCC OC, VietCatholicNews/TV, 3 parishes, KVNR, VNCR, TGPSG, HDGM Vietnam, Redemptorists VN)
- Include: publisher short name, full citation name, tier, language, medium, example JSON
- Quick reference card table

### 3. Monthly Batch Template — `docs/research/monthly_batch_template.md`
- From v1/monthly_template.md
- Structure: date range, target dates, Engine A output reference, Engine B prompt queue, validation steps, merge checklist, theological review assignments
- Status tracking: pending/generating/validating/merging/reviewed/approved

### 4. Vietnamese Localization Corpus Pipeline
- `data/corpus/vatican_news_vi/` — download last 90 podcast episodes, extract transcripts (Whisper or YouTube captions)
- `data/corpus/vietcatholic_news/` — scrape article titles + metadata (last 180 days)
- `data/corpus/vcc_mass_captions/` — extract YouTube captions from last 30 VCC OC Masses
- `tools/extract_vi_terminology.py` — spaCy + custom Catholic lexicon → terminology database
- `data/localization/vi_terminology.db` — SQLite: term_en, term_vi, domain (liturgical/doctrinal/papal/cultural), source, confidence
- `data/localization/feast_mapping_vi.json` — EN↔VI feast day mapping for Jul 3-16 (priority), then full year

### 5. Engine B Prompt Integration
- Update `docs/research/anno-research-prompt-main.md` with 4-tier Vietnamese source allowlist
- Add citation template references
- Add validation gate requirements
- Add Vietnamese terminology usage guidance

### 6. AnnoEntry.swift Extensions for Engine B
- Add `bodyEn: String?`, `bodyVi: String?` to `PrimaryContent`
- Add `engineBVersion: String?`, `researchTimestamp: String?` to `AnnoEntry`
- Extend `SourceRef` with: `accessed`, `notes`, `publisher`, `language`, `medium`, `type` (extended enum)

### 7. Outreach Contact Tracker — `docs/outreach/vietnamese_media_contacts.csv`
- Columns: outlet, contact_name, role, email, phone, last_contact, status, notes, tier
- Pre-populate: VCC OC, KVNR 1480, VietCatholicNews, Diocese of Orange Chancery, 3 parish offices
- Status: not_contacted, contacted, meeting_scheduled, mou_drafted, partner

### 8. Audio Licensing Tracker — `docs/AUDIO_LICENSING.md`
- Track: RVA stream (zeno.fm — confirmed free embed), Vatican podcast (RSS — free), Radio MHCG (verify), parish streams (Facebook embed — free)
- Note: Vatican MP4 download = NO; YouTube embed = YES

### 9. Vietnamese Calendar Addendum — `docs/VIETNAMESE_CALENDAR_ADDENDUM.md`
- Vietnamese proper calendar: Nov 24 (117 Martyrs), Aug 22 (La Vang), Jan 1 (Mother of God), etc.
- Lunar observances: Tết, ancestor commemorations, Mid-Autumn
- Moveable feast algorithm for Vietnamese context
- Integration with Engine A calendar_engine.py

### 10. July 17-30 Batch Example — `docs/research/batch_july17-30.md`
- From v1/batch_july17-30.md
- 14 Engine B entries with full sources, bilingual content, confidence notes
- Reference for Sprint 3-4 content generation

---

## Dependency Order

```
Validation Gate (1) ← pure Python, no app needed
    ↓
Citation Templates (2) + Monthly Template (3) ← docs
    ↓
Localization Corpus (4) ← parallel, feeds Engine B + calendar_content
    ↓
Engine B Prompt Integration (5) ← uses corpus + templates
    ↓
AnnoEntry Extensions (6) ← Swift, needs Xcode (Sprint 1)
    ↓
Outreach Tracker (7) + Audio Licensing (8) + Calendar Addendum (9) ← data/docs
    ↓
Batch Example (10) ← reference for Sprint 3-4
```

**Zero-code prep (do this week):**
- Download Vatican podcast episodes (90)
- Scrape VietCatholicNews metadata
- Extract VCC YouTube captions
- Contact VCC OC, KVNR, VietCatholicNews, Diocese Chancery (human)
- Write validation script (Python)

---

## Cross-Module Inputs Needed

| Need | From Module |
|------|-------------|
| Calendar date conversions (Engine A) | `calendar_engine.py` (project root) |
| Vietnamese Media source list | `vietnamese_media` v1/hub_source_list_verified.md |
| Calendar content spec (Layer 3) | `calendar_content` v1/calendar_spec_full.md |
| Monetization source allowlist | `monetization` v2/architecture_17_modules.md (M7, M1) |
| Theological review process | `MVP_PLAN_FINAL.md` Sprint 6 |
| Sprint 3-4 content prompts | `CONTENT_SPRINT_1.md`, `CONTENT_SPRINT_2.md` |