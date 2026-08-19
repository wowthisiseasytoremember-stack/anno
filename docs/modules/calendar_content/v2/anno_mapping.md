# Calendar Content Module → Anno Features Mapping

**Source:** `calendar_content` module (v1/v2 specs)  
**Target:** Anno MVP (`MVP_PLAN_FINAL.md`, `AnnoEntry.swift`, `AGENTS.md`)  
**Date:** 2026-08-19

---

## Current Anno Data Model (`AnnoEntry.swift`) Coverage

| AnnoEntry Field | Type | Calendar Spec Layer | Status |
|-----------------|------|---------------------|--------|
| `id` | String | — | ✅ Exists |
| `date` / `weekday` | String | Layer 1 (Glance) | ✅ Exists |
| `liturgical` (rank, color, titleEn, titleVi) | LiturgicalInfo | Layers 1, 2, 3 | ✅ Exists — **needs lunar/zodiac** |
| `calendars` (julian, hebrew, islamic, coptic, ethiopian) | CalendarConversions | Layer 1 (Glance) | ✅ Exists — **needs Vietnamese lunar** |
| `primary` (type, titleEn/Vi, summaryEn/Vi, confidence) | PrimaryContent | Layer 3 (Depth) | ✅ Exists — **needs reflection, readings, history** |
| `place` (SacredPlace) | SacredPlace? | Layer 5 (Connection) / Layer 6 (Culture) | ✅ Exists — **needs parish directory integration** |
| `artwork` (ArtworkCandidate) | ArtworkCandidate | Layer 2 (Open) / Layer 5 (Connection) | ✅ Exists — **needs daily showcase + download/buy** |
| `sources` ([SourceRef]) | [SourceRef] | All layers | ✅ Exists |
| `appHooks` (heroLineEn/Vi, prayerPromptEn/Vi) | AppHooks | Layer 4 (Practice) | ✅ Exists — **needs actionable practice + additional devotions** |

---

## Mapping: Calendar Spec 7 Layers → Anno MVP Features

| Spec Layer | Free/Paid | Anno MVP Feature | Gap / Extension Needed |
|------------|-----------|------------------|------------------------|
| **1. The Glance** | Free | Today tab header / Lock screen widget / Push notification | **Add**: Vietnamese lunar date + zodiac year; liturgical color as visual tint; rank badge (Lễ Trọng/Lễ Kính/Lễ Nhớ) |
| **2. The Open** | Free | TodayView (artwork, date, feast, color, verse, Mass link, "See more") | **Add**: Daily artwork showcase (passive marketing for M3); "See more" → paywall at Layer 3 |
| **3. The Depth** | Paid | TodayView expanded / Detail sheet | **NEW**: Saint bio/feast context (150-250 words bilingual), historical dates, full reading citations — **extends `PrimaryContent`** |
| **4. The Practice** | Paid | — | **NEW**: Prayer + actionable practice + additional devotions (rosary decade, Vietnamese martyrs prayer) — **extends `AppHooks`** |
| **5. The Connection** | Paid | — | **NEW**: Mass stream links (from vietnamese_media M1/M3), readings links, artwork download/buy (M3), pilgrimage links (M2), hymn suggestions — **new `Connections` struct** |
| **6. The Culture** | Paid | — | **NEW**: Vietnamese Catholic cultural note (parish spotlight, history, diaspora resonance) — **new `CultureNote` struct** |
| **7. The Arc** | Paid | — | **NEW**: Liturgical narrative (season context, yesterday→today→tomorrow, solstice connections) — **new `ArcNote` struct** |

---

## Mapping: Physical Production Standards → Anno/M3 (Artwork Multi-Stream)

| Print Spec | Anno Module | Status |
|------------|-------------|--------|
| 11×14/17 matte, Wire-O binding, writing space | M3 (Artwork Multi-Stream) | **New product format** — not in app; separate POD workflow |
| Front matter: letter, movable feasts table, Ordo summary, martyrs list | M1 (Calendar) | **Export format** — JSON → InDesign/LaTeX template |
| Back matter: common prayers (Kinh Mân Côi), parish directory with QR, blank family record pages | M1 + M9 (Directory) | **New export** — combines calendar data + parish directory |
| Cover: commissioned La Vang/Vietnamese Martyrs art | M3 | **New artwork commission** — not stock |

---

## Mapping: Paywall UX → Anno M8 (Premium App Features)

| Spec Element | Anno M8 Current | Extension |
|--------------|-----------------|-----------|
| Free = Layers 1-2 only | "Free: browse, 5 bookmarks" | **Redefine free tier**: Layers 1-2 (Glance + Open) beautiful enough for daily habit |
| Paid = Layers 3-7 | "Premium: unlimited, push, offline..." | **Paywall at Layer 3** with "$1/month" framing, "sứ vụ" language, dignity-preserving |
| Push notifications | Listed in M8 | **Layer 5 triggers**: Mass start times + feast day reminders |

---

## Mapping: Content Production Calendar → Anno Sprints (MVP_PLAN_FINAL.md)

| Spec Content Type | Count | Anno Sprint | Feasibility |
|-------------------|-------|-------------|-------------|
| Fixed feast days (Layer 3) | ~180 | Sprint 3-4 (phone) + Sprint 5 (merge) | ✅ **Layer 3 only** — agent can draft bios |
| Moveable feasts (Layer 3) | ~25 | Sprint 3-4 | ✅ **Layer 3 only** — algorithmic dates + agent draft |
| Ordinary Time weekdays (Layer 3) | ~160 | Sprint 3-4 | ✅ **Layer 3 only** — 3-year lectionary cycle |
| Culture notes (Layer 6) | ~52 | **Not in MVP** | ❌ **Human only** — v2 backlog |
| Arc notes (Layer 7) | ~40 | **Not in MVP** | ❌ **Human only** — v2 backlog |
| **Year 1 Total** | **~460** | | **MVP ships 14 days (Sprints 3-4); full 460 is post-MVP** |

---

## Key Mismatches / Decisions Needed

| Issue | Calendar Spec | Anno MVP | Decision Needed |
|-------|---------------|----------|-----------------|
| **Lunar calendar** | Core feature (dual solar+lunar+zodiac) | Not in `CalendarConversions` | Add `vietnameseLunar` + `zodiacYear` to `CalendarConversions` |
| **Reading citations** | Full VN liturgical format (Bài đọc I, Đáp ca, etc.) | Not in model | Add `readings` field to `PrimaryContent` or new `LiturgicalReadings` struct |
| **Rank taxonomy** | Lễ Trọng / Lễ Kính / Lễ Nhớ / Feria | `LiturgicalInfo.rank` is free string | Define enum: `solemnity`, `feast`, `memorial`, `optionalMemorial`, `feria` |
| **Paywall location** | At Layer 3 (Depth) | Not implemented (Paywall folder deleted) | **Sprint 6+**: Re-add paywall gate at Layer 3 expansion |
| **Parish directory integration** | Layer 5 (Mass links) + Layer 6 (parish spotlight) | Not in MVP (Map tab deleted) | **M9 Directory** needed for Layer 5/6 — v2 |
| **Artwork commerce** | Layer 5 (download free sample, buy high-res) | `ArtworkCandidate` has URL only | Add `downloadUrl`, `purchaseUrl`, `price` to `ArtworkCandidate` (M3) |

---

## Proposed AnnoEntry.swift Extensions (Minimal, Additive)

```swift
// ADD to CalendarConversions
let vietnameseLunar: String?      // "Mùng 5 tháng 10 âm lịch"
let zodiacYear: String?           // "Năm Đinh Mùi"

// ADD to PrimaryContent  
let readings: LiturgicalReadings? // Bilingual VN citation format
let historicalContext: String?    // "117 vị, tử đạo 1745–1862, phong thánh 19/6/1988"
let reflectionEn: String?         // Layer 3: 150-250 word reflection
let reflectionVi: String?

// NEW structs for Layers 4-7 (only populated for paid tier)
struct DevotionalPractice: Codable, Hashable {
    let prayerEn: String
    let prayerVi: String
    let actionEn: String          // Concrete practice
    let actionVi: String
    let additionalDevotionsEn: String?
    let additionalDevotionsVi: String?
}

struct Connections: Codable, Hashable {
    let massStreams: [MassStream]     // From vietnamese_media M1/M3
    let readingsUrl: String?
    let artworkDownloadUrl: String?   // Free sample
    let artworkPurchaseUrl: String?   // High-res
    let artworkPrice: Double?
    let pilgrimageLinks: [PilgrimageLink]  // M2
    let hymnSuggestions: [HymnSuggestion]
}

struct CultureNote: Codable, Hashable {
    let noteEn: String
    let noteVi: String
    let relatedParishId: String?      // Links to M9 Directory
}

struct ArcNote: Codable, Hashable {
    let contextEn: String
    let contextVi: String
    let tomorrowPreviewEn: String
    let tomorrowPreviewVi: String
}

// ADD to AnnoEntry (all optional — nil for free tier)
let practice: DevotionalPractice?
let connections: Connections?
let culture: CultureNote?
let arc: ArcNote?
```

---

## Integration with Other Modules

| Calendar Spec Needs | Provided By Module |
|---------------------|-------------------|
| Vietnamese Mass stream URLs (Layer 5) | `vietnamese_media` M1 (34 YouTube) + M3 (8 parish livestreams) |
| Parish directory for Layer 6 spotlights | `vietnamese_media` M3 + `monetization` M9 (Directory) |
| Artwork assets for Layer 2/5 | `monetization` M3 (Artwork Multi-Stream) |
| Pilgrimage routes for Layer 5 | `monetization` M2 (Pilgrimage Route Guides) |
| Source citations for Layer 3 bios | `research_infrastructure` (Engine B output) |
| Grant funding for content production | `monetization` M14 (CCC draft ready) |
| Parish B2B sales for print calendar | `monetization` M1 (Parish bulk license) + M15 (Diocese partnership) |

---

## Recommended Sequence for Anno

| Phase | Work | Module | Sprint |
|-------|------|--------|--------|
| **1. Data Model Extension** | Add lunar, readings, rank enum, optional paid layers to `AnnoEntry.swift` | calendar_content → Anno | Sprint 1 (macOS) |
| **2. Moveable Feast Calculator** | Algorithm for Easter-dependent dates (Vietnamese proper calendar) | calendar_content | Sprint 1-2 (Python) |
| **3. Content Pipeline** | Scaffold DB schema + production tracker (460 rows) | calendar_content | Sprint 2 |
| **4. Layer 3 Content (MVP scope)** | Generate 14 days of Layer 3 bios (Sprints 3-4 phone prompts) | calendar_content + research_infrastructure | Sprint 3-4 |
| **5. Merge + Validate** | `tools/merge_content.py` combines batches → `anno_week_current.json` | calendar_content | Sprint 5 |
| **6. Free Tier Polish** | Layers 1-2 beautiful, "See more" → paywall placeholder | calendar_content + M8 | Sprint 6 |
| **7. Paid Layers (Post-MVP)** | Layers 3-7 implementation, paywall, IAP | M8 + calendar_content | v2 |
| **8. Print Calendar Export** | JSON → InDesign/LaTeX → POD | M1 + M3 | v2 (parallel track) |
| **9. Parish Sales** | B2B packet → VCC/OC parishes | M1 + M15 | v2 (parallel track) |

---

## Summary: What's Build-Ready Now vs. What Waits

| **Build-Ready (can scaffold immediately)** | **Needs App Infrastructure / v2** |
|--------------------------------------------|-----------------------------------|
| • `AnnoEntry.swift` extensions (lunar, readings, rank enum, optional paid layers) | • Layers 4-7 UI (Practice, Connection, Culture, Arc) |
| • Moveable feast calculator (Python) | • Paywall gate at Layer 3 |
| • Content production tracker (460-row Kanban) | • Parish directory (M9) for Layer 5/6 |
| • Layer 3 draft generation prompts (phone-deliverable) | • Artwork commerce (M3) download/buy flow |
| • Grant application (CCC draft → customize brackets) | • Print calendar export pipeline |
| • Parish B2B sales packet (6 docs → hand-edit register) | • Full 460-entry Year 1 content production |
| • Sponsor/underwriter prospectus (bilingual) | • VCC endorsement letter (prerequisite for grants/sales) |