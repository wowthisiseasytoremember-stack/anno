# Calendar Content Module — Scaffold TODOs for Worker Agent

**Source:** `docs/modules/calendar_content/v2/anno_mapping.md`  
**For:** Worker agent (deepseek-worker / yolo-worker)  
**Scope:** Build-ready items only — scaffold structure, not full implementation

---

## Scaffold TODO List

### 1. AnnoEntry.swift Extensions
**File:** `Anno/Models/AnnoEntry.swift` (macOS/Xcode required)
- [ ] Add `vietnameseLunar: String?` and `zodiacYear: String?` to `CalendarConversions`
- [ ] Add `readings: LiturgicalReadings?`, `historicalContext: String?`, `reflectionEn: String?`, `reflectionVi: String?` to `PrimaryContent`
- [ ] Define `LiturgicalRank` enum: `solemnity`, `feast`, `memorial`, `optionalMemorial`, `feria` → replace `LiturgicalInfo.rank: String`
- [ ] Define `LiturgicalReadings` struct (VN citation format: reading1, psalm, reading2, gospel)
- [ ] Define `DevotionalPractice` struct (prayerEn/Vi, actionEn/Vi, additionalDevotionsEn/Vi)
- [ ] Define `Connections` struct (massStreams, readingsUrl, artworkDownloadUrl, artworkPurchaseUrl, artworkPrice, pilgrimageLinks, hymnSuggestions)
- [ ] Define `CultureNote` struct (noteEn, noteVi, relatedParishId)
- [ ] Define `ArcNote` struct (contextEn, contextVi, tomorrowPreviewEn, tomorrowPreviewVi)
- [ ] Add optional `practice`, `connections`, `culture`, `arc` fields to `AnnoEntry`
- [ ] All new fields optional (nil = free tier)

**Acceptance:** `Cmd+B` zero errors; JSON decode/encode works with nil paid fields

---

### 2. Moveable Feast Calculator (Python)
**File:** `tools/moveable_feasts.py` (pure Python, no LLM)
- [ ] Implement Easter date algorithm (Computus) for Gregorian calendar
- [ ] Derive: Ash Wednesday, Palm Sunday, Holy Thursday, Good Friday, Easter Vigil, Easter Sunday, Divine Mercy Sunday, Ascension, Pentecost, Corpus Christi, Sacred Heart, Christ the King
- [ ] Add Vietnamese proper calendar fixed dates: Nov 24 (Vietnamese Martyrs), Aug 22 (Đức Mẹ La Vang), Jan 1 (Mẹ Maria), etc.
- [ ] Add lunar calendar conversion (Tết, Mid-Autumn, etc.) — use `lunarcalendar` or `vietnamese-lunar` pip package
- [ ] Output: JSON mapping `YYYY-MM-DD` → `{ feastNameEn, feastNameVi, rank, color, isMoveable }`
- [ ] CLI: `python moveable_feasts.py --year 2026 --output data/moveable_2026.json`

**Acceptance:** Runs on ichabod (Linux); output validates against known 2026 dates

---

### 3. Content Production Tracker (460-row Kanban)
**File:** `data/production_tracker.csv` (or Notion/Airtable export)
- [ ] Columns: `entry_id`, `date`, `feast_name_en`, `feast_name_vi`, `rank`, `layer3_status`, `layer3_assignee`, `layer3_due`, `layer4_status`, `layer6_status`, `layer7_status`, `artwork_status`, `notes`
- [ ] Rows: ~180 fixed feasts + ~25 moveable + ~160 ordinary time + ~52 culture + ~40 arc = ~460
- [ ] Pre-populate fixed feasts from General Roman Calendar + Vietnamese proper calendar
- [ ] Pre-populate moveable feasts from Tool #2 output
- [ ] Pre-populate Ordinary Time weekdays (3-year lectionary cycle A/B/C)
- [ ] Status values: `not_started`, `drafting`, `review`, `approved`, `blocked`
- [ ] Filter views: by layer, by status, by assignee, by due date

**Acceptance:** CSV opens in spreadsheet; 460 rows; filters work

---

### 4. Layer 3 Phone-Deliverable Prompts (Sprints 3-4)
**Files:** `CONTENT_SPRINT_1.md`, `CONTENT_SPRINT_2.md` (already exist — extend them)
- [ ] Update `CONTENT_SPRINT_1.md` prompt: add Layer 3 spec (150-250 word bilingual bio, historical context, reading citations)
- [ ] Update `CONTENT_SPRINT_2.md` prompt: same
- [ ] Add validation checklist: word count, bilingual, VN citation format, confidence level, source citations
- [ ] Add output format: matches `PrimaryContent` + new Layer 3 fields
- [ ] Create `CONTENT_SPRINT_TEMPLATE.md` for future batches (Jul 17-23, Jul 24-30, etc.)

**Acceptance:** Prompt run on phone produces valid JSON for 7 days; passes `tools/validate_mock_content.py`

---

### 5. Grant/Parish/Sponsor Docs — Customize Brackets, Hand-Edit Register
**Files:** (create in `docs/business/` or `docs/grants/`)
- [ ] **Grant Application (CCC)**: Copy `calendar_content/v1/calendar_spec_full.md` CCC draft → `docs/grants/ccc_application.md` → replace all `[BRACKETS]` with real info
- [ ] **Parish B2B Packet (6 docs)**: Create `docs/business/parish_packet/`
  - `01_introduction_letter_vi.md` — formal Vietnamese, no ask
  - `02_product_sheet_bilingual.md` — pricing tiers, co-branding
  - `03_council_presentation_outline.md` — 10 slides
  - `04_faq_internal.md` — objection responses
  - `05_target_parish_list.md` — 16 OC parishes tiered
  - `06_sample_calendar_note.md` — which page to bookmark
- [ ] **Sponsor/Underwriter Prospectus**: `docs/business/sponsor_prospectus_bilingual.md` — 1 page, tiered pricing, 52-week content calendar alignment
- [ ] **All Vietnamese copy**: Hand-edit for formal register (kính thưa, con xin phép, lòng kính trọng) — **do not delegate to AI**

**Acceptance:** Docs exist with real info (not brackets); Vietnamese register verified by native speaker

---

## Worker Dispatch Notes

| Task | Worker Type | Input Files | Output Location |
|------|-------------|-------------|-----------------|
| 1. AnnoEntry extensions | `deepseek-worker` (macOS) | `AnnoEntry.swift`, `anno_mapping.md` | `Anno/Models/AnnoEntry.swift` |
| 2. Moveable feast calculator | `deepseek-worker` | `anno_mapping.md`, `calendar_spec_full.md` | `tools/moveable_feasts.py` |
| 3. Production tracker | `yolo-worker` | `decomposition.md` (production calendar table) | `data/production_tracker.csv` |
| 4. Layer 3 prompts | `deepseek-worker` | `CONTENT_SPRINT_1.md`, `anno_mapping.md` | `CONTENT_SPRINT_1.md`, `CONTENT_SPRINT_2.md`, `CONTENT_SPRINT_TEMPLATE.md` |
| 5. Business docs | **Human only** (register) | `calendar_spec_full.md`, `roe_calendar_sections.md` | `docs/grants/`, `docs/business/` |

---

## Dependencies Between Tasks

```
Moveable Feast Calculator (2)
        ↓
Production Tracker (3) ← needs moveable dates
        ↓
Layer 3 Prompts (4) ← needs tracker dates/feasts
        ↓
AnnoEntry Extensions (1) ← can start in parallel, needed for Sprint 5 merge
```

**Grant/Parish/Sponsor docs (5)** — independent, can start anytime after VCC endorsement secured

---

## Definition of Done (Per Task)

| Task | Done When |
|------|-----------|
| 1. AnnoEntry extensions | Swift compiles; JSON round-trip works; nil paid fields decode |
| 2. Moveable feast calc | Runs on Linux; 2026 output matches USCCB calendar; JSON valid |
| 3. Production tracker | 460 rows; all fixed/moveable/ordinary dates present; CSV readable |
| 4. Layer 3 prompts | Phone test produces 7 valid entries; validator passes |
| 5. Business docs | No brackets remain; Vietnamese register verified; PDFs export cleanly |