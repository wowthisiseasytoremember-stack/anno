# Research Infrastructure Module → Anno Features Mapping

**Source:** `research_infrastructure` module (v1-v3: engine_b_prompt.md, citation_templates.md, validation_gate.md, media_landscape_with_sprints.md)  
**Target:** Anno MVP (`MVP_PLAN_FINAL.md`, `AnnoEntry.swift`, `AGENTS.md`, `CLAUDE.md`, `tools/validate_engine_b_output.py`)  
**Date:** 2026-08-19

---

## Executive Summary

The research_infrastructure module provides the **Engine B pipeline**: daily historical research prompt with 4-tier source allowlist, per-outlet citation templates, validation gate script requirements, and monthly batch workflow. This is the **content generation engine** that feeds:
- `AnnoEntry.primary` (body, summary, confidence)
- `AnnoEntry.sources` (validated citations)
- `AnnoEntry.app_hooks` (hero_line, prayer_prompt)
- `AnnoEntry.place` (sacred site coordinates)
- `AnnoEntry.artwork` (public domain artwork candidates)
- `calendar_content` Layer 3 (Depth) saint bios/feast context
- Vietnamese localization corpus for structural VI content

---

## Engine B Prompt → AnnoEntry Field Mapping

| Engine B Output Field | AnnoEntry.swift Field | Notes |
|----------------------|----------------------|-------|
| `id` | `id` | Pattern: `anno-YYYY-MM-DD` |
| `date` / `weekday` | `date` / `weekday` | Direct mapping |
| `mock_priority` | (not in model) | Internal tracking; `engine_b_v1` |
| `liturgical.rank` | `liturgical.rank` | Enum: Solemnity, Feast, Memorial, Optional Memorial, Feria, Sunday |
| `liturgical.color` | `liturgical.color` | Enum: white, red, green, purple, rose, gold, verdigris |
| `liturgical.title_en/vi` | `liturgical.titleEn/Vi` | Direct mapping |
| `calendars.*` | `calendars.*` | Julian, Hebrew, Islamic, Coptic, Ethiopian (Engine A) |
| `primary.type` | `primary.type` | saint, liturgical_day, historical_event, feast, solemnity |
| `primary.title_en/vi` | `primary.titleEn/Vi` | Direct mapping |
| `primary.summary_en/vi` | `primary.summaryEn/Vi` | 2-4 sentences |
| `primary.body_en/vi` | **NEW: `primary.bodyEn/Vi`** | 3-5 paragraphs — extends AnnoEntry |
| `primary.confidence` | `primary.confidence` | Enum: confirmed, traditional, disputed, contextual |
| `primary.confidence_note_en/vi` | `primary.confidenceNoteEn/Vi` | Direct mapping |
| `place` | `place` | SacredPlace struct (name, lat, lng, confidence, source_url) |
| `artwork` | `artwork` | ArtworkCandidate (title, maker, date_label, source_url, status) |
| `sources` | `sources` | SourceRef array (label, url, type) |
| `app_hooks.hero_line_en/vi` | `appHooks.heroLineEn/Vi` | Direct mapping |
| `app_hooks.prayer_prompt_en/vi` | `appHooks.prayerPromptEn/Vi` | Direct mapping |

---

## Required AnnoEntry.swift Extensions (from Engine B)

```swift
// ADD to PrimaryContent
let bodyEn: String?      // 3-5 paragraph researched article
let bodyVi: String?      // Vietnamese translation with Catholic terminology

// ADD to AnnoEntry (optional, populated by Engine B)
let engineBVersion: String?  // "engine_b_v1" — tracks pipeline version
let researchTimestamp: String? // ISO8601 when Engine B ran
```

---

## Source Allowlist (4 Tiers) → Anno Integration

| Tier | Publishers | Validation Rule | Anno Use |
|------|------------|-----------------|----------|
| **1** | Vatican News VI, Radio Vatican VI, VCC OC | No additional validation | Primary: universal feasts, papal docs, canonizations, diocesan calendar |
| **2** | VietCatholicNews/TV, Parish livestreams (3 confirmed) | `accessed` date within 90 days | Secondary: Vietnamese cultural context, La Vang, martyrs, local feasts |
| **3** | KVNR 1480, VNCR 106.3 | Explicit `notes` with program + broadcast date | Tertiary: broadcast placement, radio archive |
| **4** | TGPSG, HDGM Vietnam, Redemptorists Vietnam | **Require** "Produced in Vietnam; state context applies" in notes | Reference only with badge; liturgical practice reference |

---

## Citation Templates → Anno SourceRef Enhancement

| Current SourceRef | Extended for Vietnamese Media |
|-------------------|-------------------------------|
| `label` | Keep |
| `url` | Keep |
| `type` | Extend enum: `liturgical_calendar`, `vatican`, `encyclopedia`, `academic`, `news`, `devotional`, `vietnamese_diocesan`, `vietnamese_diaspora`, `vietnamese_radio`, `vietnam_produced` |

```swift
// EXTEND SourceRef
enum SourceType: String, Codable {
    case liturgicalCalendar = "liturgical_calendar"
    case vatican = "vatican"
    case encyclopedia = "encyclopedia"
    case academic = "academic"
    case news = "news"
    case devotional = "devotional"
    case vietnameseDiocesan = "vietnamese_diocesan"
    case vietnameseDiaspora = "vietnamese_diaspora"
    case vietnameseRadio = "vietnamese_radio"
    case vietnamProduced = "vietnam_produced"
}

struct SourceRef: Codable, Identifiable, Hashable {
    var id: String { url }
    let label: String
    let url: String
    let type: SourceType
    let accessed: String?        // YYYY-MM-DD (required for Tier 2)
    let notes: String?           // Required for Tier 3/4
    let publisher: String?       // Full publisher name for citation display
    let language: String?        // "vi" | "en"
    let medium: String?          // "video" | "audio" | "text" | "livestream"
}
```

---

## Validation Gate → Anno Sprint Integration

| Validation Check | Anno Integration Point | Sprint |
|------------------|------------------------|--------|
| Schema compliance | `tools/validate_mock_content.py` runs on batch output | Sprint 5 (merge) |
| Source URL resolution (HTTP 200) | Pre-merge check; fail fast on dead links | Sprint 5 |
| Minimum 2 sources, 3 preferred | Enforced in validation script | Sprint 5 |
| No example.com URLs | Enforced | Sprint 5 |
| Source type ↔ URL pattern matching | USCCB → liturgical_calendar, Vatican.va → vatican, etc. | Sprint 5 |
| Content quality (summary 2-4 sentences, body 3+ paragraphs) | Rejects placeholder "A day of ordinary time..." | Sprint 5 |
| Confidence consistency (Solemnity/Feast → confirmed) | Auto-check | Sprint 5 |
| Bilingual fields present (EN + VI) | Enforced; VI must be genuine Vietnamese Catholic terminology | Sprint 5 |
| Tier 2: accessed within 90 days | Check `accessed` field | Sprint 5 |
| Tier 3: notes with program + date | Check `notes` field | Sprint 5 |
| Tier 4: "Produced in Vietnam; state context applies" | **Reject if missing** | Sprint 5 |

---

## Monthly Batch Workflow → Anno Content Sprints

| Batch Phase | Anno Sprint | Output |
|-------------|-------------|--------|
| **Engine A** (calendar_engine.py) | Pre-Sprint 1 | 4-year date conversions + movable feasts |
| **Engine B Prompt** (per date) | Sprint 3-4 (phone) | 14 AnnoEntry JSON (Jul 3-16) |
| **Validation Gate** | Sprint 5 (merge) | Validated `anno_week_current.json` |
| **Normalization** (normalize_fixture.py) | Sprint 5 | `Anno/Resources/anno_unified_2026.json` |
| **Theological Review** (human) | Sprint 6 | Sign-off on 3-5 entries |

---

## Vietnamese Localization Corpus → Anno Structural VI

| Corpus Source | Extraction | Anno Use |
|---------------|------------|----------|
| Vatican News VI podcast transcripts | Download 90 episodes → Whisper/transcript | Liturgical, doctrinal, papal terminology |
| VCC OC Mass captions | YouTube captions last 30 Masses | Diocesan liturgical terminology, homiletic style |
| VietCatholicNews articles | Scrape 180 days metadata | Cultural context, La Vang, martyrs terminology |
| **Terminology pipeline** | spaCy + custom Catholic lexicon | `data/localization/vi_terminology.db` |
| **Feast mapping EN↔VI** | From corpus + official calendar | `data/localization/feast_mapping_vi.json` |

---

## Sprint Dependencies (from media_landscape_with_sprints.md)

| Sprint | Research Infra Tasks | Anno Dependency |
|--------|---------------------|-----------------|
| **Corpus Build (parallel, no macOS)** | Download Vatican transcripts, scrape VietCatholicNews, extract VCC captions, build terminology pipeline, generate feast mapping, document citation templates | Feeds Engine B, Layer C localization, calendar_content Layer 6 |
| **Outreach Validation (human)** | Contact VCC OC, KVNR media kit, VietCatholicNews media kit, Diocese calendar, survey 3 parish streams | Feeds M15 (diocese), M12/M13 (sponsors), M9 (directory) |
| **Sprint 1-2 (macOS)** | Build `BrowserAnalytics` with source schema, implement YouTube embed + audio player in WKWebView | M7 Analytics, M1/M5 Layer 5 |
| **Sprint 3-4 (phone content)** | Use feast mapping for Jul 3-16 content generation; cite sources per citation templates | calendar_content Layer 3, Engine B |
| **Sprint 5-6** | Wire source database to app; parish directory UI; sponsor outreach with traffic data | M8, M9, M12, M13 |

---

## File Inventory for Anno Project

| Artifact | Path | Status |
|----------|------|--------|
| Engine B main prompt | `docs/research/anno-research-prompt-main.md` | ✅ Exists (v1/engine_b_prompt.md) |
| Source citation templates | `docs/research/source_citation_templates.md` | ⏳ TODO (from v1/citation_templates.md) |
| Validation gate script | `tools/validate_engine_b_output.py` | ⏳ TODO (spec in v1/validation_gate.md) |
| Vietnamese terminology database | `data/localization/vi_terminology.db` | ⏳ TODO |
| Feast day EN↔VI mapping | `data/localization/feast_mapping_vi.json` | ⏳ TODO |
| Audio licensing tracker | `docs/AUDIO_LICENSING.md` | ⏳ TODO |
| Vietnamese calendar addendum | `docs/VIETNAMESE_CALENDAR_ADDENDUM.md` | ⏳ TODO |
| Outreach contact tracker | `docs/outreach/vietnamese_media_contacts.csv` | ⏳ TODO |
| Monthly batch template | `docs/research/monthly_batch_template.md` | ⏳ TODO (from v1/monthly_template.md) |
| July 17-30 batch example | `docs/research/batch_july17-30.md` | ⏳ TODO (from v1/batch_july17-30.md) |

---

## Cross-Module Dependencies

| Research Infra Provides | Consumed By Module |
|------------------------|-------------------|
| Engine B research output (AnnoEntry JSON) | `calendar_content` Layer 3 (Depth) |
| Source allowlist + citation templates | `vietnamese_media` M1-M10 ingestion |
| Validation gate script | `monetization` M7 (analytics), Sprint 5 merge |
| Vietnamese terminology corpus | `calendar_content` Layer 6 (Culture), Layer C |
| Feast mapping EN↔VI | `calendar_content` (all layers), `monetization` M1 |
| Monthly batch workflow | `calendar_content` production tracker (460 entries) |
| VCC OC source (Tier 1) | `monetization` M15 (Diocese partnership) |
| Parish livestream sources (Tier 2/3) | `monetization` M9 (Directory), `calendar_content` Layer 5 |
| VietCatholicNews (Tier 2) | `monetization` M5 (affiliate), M10 (events) |

---

## Summary: What's Ready vs. What Needs Build

| **Ready (specs complete, can scaffold)** | **Needs Implementation** |
|------------------------------------------|--------------------------|
| Engine B prompt (v1/engine_b_prompt.md) | `tools/validate_engine_b_output.py` (Python) |
| Citation templates (v1/citation_templates.md) | `docs/research/source_citation_templates.md` (formatted) |
| Validation gate spec (v1/validation_gate.md) | `tools/validate_mock_content.py` enhancements |
| Monthly batch template (v1/monthly_template.md) | `docs/research/monthly_batch_template.md` |
| Source allowlist (4 tiers) | Engine B prompt integration + validation rules |
| Vietnamese localization corpus plan | `tools/extract_vi_terminology.py`, corpus download scripts |
| Feast mapping table spec | `data/localization/feast_mapping_vi.json` generation |
| Outreach contact tracker spec | `docs/outreach/vietnamese_media_contacts.csv` |

---

## Immediate Action Items (This Week, No macOS)

1. **Write `tools/validate_engine_b_output.py`** — implement all validation checks from v1/validation_gate.md
2. **Format `docs/research/source_citation_templates.md`** — from v1/citation_templates.md
3. **Create `docs/research/monthly_batch_template.md`** — from v1/monthly_template.md
4. **Download Vatican News VI podcast transcripts (90 days)** — `data/corpus/vatican_news_vi/`
5. **Scrape VietCatholicNews metadata (180 days)** — `data/corpus/vietcatholic_news/`
6. **Extract VCC OC YouTube captions (30 Masses)** — `data/corpus/vcc_mass_captions/`
7. **Build feast mapping table** — `data/localization/feast_mapping_vi.json` for Jul 3-16
8. **Contact VCC OC for partnership** — human task (M15)