# Calendar Content Module — Scaffold Bullets for Worker Agent

**Source:** `docs/modules/calendar_content/v2/anno_mapping.md`  
**For:** Worker agent reference — what to build, minimal structure

---

## Build-Ready Items (scaffold only, not full implementation)

### 1. AnnoEntry.swift Extensions
- Add Vietnamese lunar date + zodiac year to `CalendarConversions`
- Add `readings`, `historicalContext`, `reflectionEn`, `reflectionVi` to `PrimaryContent`
- Define `LiturgicalRank` enum (solemnity, feast, memorial, optionalMemorial, feria) — replace free-string rank
- Define `LiturgicalReadings` struct (VN format: reading1, psalm, reading2, gospel)
- Define `DevotionalPractice` (prayer + actionable practice + additional devotions, bilingual)
- Define `Connections` (massStreams, readingsUrl, artwork download/buy, pilgrimageLinks, hymnSuggestions)
- Define `CultureNote` (bilingual note + relatedParishId)
- Define `ArcNote` (season context + tomorrow preview, bilingual)
- Add optional `practice`, `connections`, `culture`, `arc` to `AnnoEntry` (nil = free tier)

### 2. Moveable Feast Calculator (Python)
- Easter Computus algorithm (Gregorian)
- Derive all moveable feasts: Ash Wed → Christ the King
- Add Vietnamese proper calendar fixed dates (Nov 24 Martyrs, Aug 22 La Vang, etc.)
- Lunar calendar conversion (Tết, Mid-Autumn) via `lunarcalendar` or `vietnamese-lunar` pip
- CLI: `python moveable_feasts.py --year 2026 --output data/moveable_2026.json`
- Output JSON: date → { feastNameEn, feastNameVi, rank, color, isMoveable }

### 3. Content Production Tracker (460-row Kanban)
- Columns: entry_id, date, feast_name_en, feast_name_vi, rank, layer3_status, layer3_assignee, layer3_due, layer4_status, layer6_status, layer7_status, artwork_status, notes
- ~180 fixed feasts (General Roman Calendar + Vietnamese proper)
- ~25 moveable feasts (from calculator above)
- ~160 Ordinary Time weekdays (3-year lectionary A/B/C)
- ~52 culture notes (weekly rotation)
- ~40 arc notes (seasonal transitions)
- Status values: not_started, drafting, review, approved, blocked

### 4. Layer 3 Phone-Deliverable Prompts (Sprints 3-4)
- Update `CONTENT_SPRINT_1.md` and `CONTENT_SPRINT_2.md` with Layer 3 spec:
  - 150-250 word bilingual saint bio / feast context
  - Historical context line (dates, canonization)
  - Full VN reading citations (Bài đọc I, Đáp ca, Bài đọc II, Tin Mừng)
  - Confidence level + source citations
- Add validation checklist (word count, bilingual, VN format, confidence, sources)
- Create `CONTENT_SPRINT_TEMPLATE.md` for future weekly batches

### 5. Grant / Parish B2B / Sponsor Docs (customize brackets, hand-edit Vietnamese register)
- **CCC Grant Application** → `docs/grants/ccc_application.md` (fill all brackets, attach VCC letter)
- **Parish B2B Packet (6 docs)** → `docs/business/parish_packet/`:
  1. Introduction letter (Vietnamese, formal, no ask)
  2. Product sheet (bilingual, pricing tiers, co-branding)
  3. Parish council presentation outline (10 slides)
  4. Internal FAQ (objection responses)
  5. Target parish list (16 OC parishes, tiered)
  6. Sample calendar bookmark note (which page to highlight)
- **Sponsor/Underwriter Prospectus** → `docs/business/sponsor_prospectus_bilingual.md` (1 page, tiered pricing, 52-week alignment)
- **All Vietnamese copy**: human edit only — formal register (kính thưa, con xin phép, lòng kính trọng)

---

## Dependency Order

```
Moveable Feast Calculator (2)
    ↓
Content Tracker (3) ← needs moveable dates
    ↓
Layer 3 Prompts (4) ← needs tracker dates/feasts
    ↓
AnnoEntry Extensions (1) ← parallel, needed for Sprint 5 merge
```

Grant/Parish/Sponsor docs (5) — independent, start after VCC endorsement

---

## Cross-Module Inputs Needed

| Need | From Module |
|------|-------------|
| Vietnamese Mass stream URLs | `vietnamese_media` M1 (34 YouTube) + M3 (8 parish livestreams) |
| Parish directory data | `vietnamese_media` M3 + `monetization` M9 |
| Artwork assets | `monetization` M3 |
| Pilgrimage routes | `monetization` M2 |
| Source citations for bios | `research_infrastructure` (Engine B output) |