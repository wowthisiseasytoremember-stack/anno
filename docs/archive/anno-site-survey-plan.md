# Anno Project — Execution Sequence (v2, MMR-Ingested)

**Date:** 2026-07-10
**Context:** Native SwiftUI iOS sacred-history app. Catholic-first, Vietnamese-ready. Working name: Anno.

---

## Current State (What's True)

**On disk at ~/Projects/Anno/:**
- All docs: AGENTS.md, ARCHITECTURE.md, ROADMAP.md, STATE.md, FEATURES.md, ANNO_CONTENT_SCHEMA.md, NATIVE_IOS_BUILD_TASKS.md, IOS_PREVIEW_CHECKLIST.md, CATHOLIC_IOS_PRODUCT_BIBLE.md, SACRED_ATLAS_COMPLETION_PLAN.md, FROM_KJV_SPRINT_20260710.md, CLONE_FROM_KJV.md, AGENT_HANDOFF.md
- ~40 SwiftUI source files — TodayView, Calendar, Map, Saved, Paywall, Models, Components, Services, Utilities, Design, Settings, Sources
- Full 4-year dataset (2.8MB, Jan 2026–Dec 2029) at `Anno/Resources/anno_full_2026_2029.json` — schema-compatible but currently generic placeholder content ("Feria in Ordinary Time" for most weekdays, no real saint/feast content)
- `anno_week_current.json` broken — references Jan 1-7 IDs instead of Jul 3-9
- `calendar_engine.py` exists (2 copies: root + tools/) but not reconciled from infrastructure bundle
- All 13 KJV clone files confirmed present on disk
- Vietnamese UI terms and Localizable.strings exist
- Mechanical packets defined for: Swift QA, July 17-30 date fill, translation review, artwork clearance

**Key blockers:**
1. **No Xcode project file** — code can't compile or preview
2. **Content is placeholder** — full dataset exists but entries are generic ("Feria in Ordinary Time" placeholders with empty sources[])
3. **Engine B research pipeline not started** — no real Catholic content generation
4. **No widget target** — "Today in Sacred History" widget identified as low-effort, high-visibility

## Prioritization

| Priority | Sprint | What |
|----------|--------|------|
| **P0** | A | Unblock compilation — Xcode project, data models, fixture fix |
| **P0** | A | Widget target in scaffold (even if content ships later) |
| **P1** | B | Privacy compliance — Anno-specific PrivacyInfo.xcprivacy, privacy policy |
| **P1** | B | Widget content implementation |
| **P1** | C | Engine B research pipeline + content generation |
| **P2** | D | Architecture — Calendar engine reconciliation, confidence badges, Engine A wire |
| **P2** | E | Sacred Atlas (Opt4 base + Opt3 UX) |
| **P3** | F | App Store submission prep — assets, screenshots, TestFlight, metadata, CI/CD |

---

## Sprint A: Unblock Compilation

**Goal:** App launches, decodes fixtures, shows a Today screen and tabs.

| # | Task | Detail | Verifies |
|---|------|--------|----------|
| A1 | Create Xcode project | Task 1 from NATIVE_IOS_BUILD_TASKS.md. Xcode 16+ file-system-synchronized groups. Add widget target as stub (even if content ships later). Dark appearance default. | Build succeeds |
| A2 | Wire data models + fixtures | Task 2 from NATIVE_IOS_BUILD_TASKS.md. AnnoEntry, FixtureStore, Resources. Snake_case decoder. | Unit test: 14 fortnight + 7 week entries decode. Jul 3 title correct. |
| A3 | Fix week_current.json | Point to Jul 3-9 entries from full dataset. Verify all 7 entry IDs exist with matching schema version. Validate JSONDecoder can decode them. | App loads Jul 3-9 week. |
| A4 | Localization smoke test | Run app with Vietnamese locale. Assert all critical UI strings non-empty. Add English fallback for missing *_vi fields. | No blank labels in VI mode. |
| A5 | Vietnamese UI verification | IOS_PREVIEW_CHECKLIST items: Today EN/VI at SE width, Calendar, Map, Source sheet. | Screenshots captured per checklist. |
| A6 | Add loading states | Shimmer/skeleton loading for initial fixture fetch (even with local data). prevents-reduced-motion respected. | Smooth first-launch impression. |
| A7 | Run validation tools | `validate_anno_local_build.py`, `validate_localization.py`, `validate_mock_content.py` | All pass. |

**Risk mitigation:**
- Xcode scaffold with sync groups → verify all source files auto-register with a build
- Schema version check before fixture fix → if dates missing, generate via mechanical packet pipeline
- Missing VI fallback → English default, logged for later translation

---

## Sprint B: Compliance + Widget

**Goal:** Submission-ready privacy posture. Widget target content implemented.

| # | Task | Detail | Verifies |
|---|------|--------|----------|
| B1 | PrivacyInfo.xcprivacy | Create Anno-specific privacy manifest (not a KJV copy). Declare: no tracking, no data collection. StoreKit purchase data is Apple-managed; location (Sprint E) needs purpose string. | Apple privacy manifest format valid. |
| B2 | Privacy policy | Write zero-collection privacy policy for hosting. Adapt from KJV template — add StoreKit disclosure. Include restore/terms links. | Can be linked from App Store. |
| B3 | Widget content | Implement "Today in Sacred History" widget. TimelineProvider with date-based rotation from the full dataset. .systemSmall/.systemMedium sizes. containerBackground(.clear, for: .widget). | Widget shows today's entry. |
| B4 | App icon | Generate programmatic app icon (PIL + asset catalog JSON). 1024pt + all required sizes. | App icon displays on device. |

**Risk mitigation:**
- PrivacyInfo.xcprivacy must be accurate — audit actual data flows. MapKit location permission added separately when Sacred Atlas lands.
- Widget target already in project scaffold (A1) — this sprint implements the content.

---

## Sprint C: Engine B — Catholic Research Pipeline

**Goal:** Production research pipeline that generates real Catholic content for the full liturgical year.

| # | Task | Detail | Verifies |
|---|------|--------|----------|
| C1 | Research prompt v1 | Write the daily Catholic saint/feast research prompt. Self-contained, specifies output schema (confirmed/traditional/disputed), source requirements, bilingual fields. | Pilot run on Jul 17 produces correct schema. |
| C2 | Pilot generation | Generate Jul 17-30 (14 days) using the prompt. Cross-ref against authoritative Catholic sources (USCCB, Vatican, CatholicCulture). | Manual review: sources match, confidence correct, no hallucinated saints. |
| C3 | Source validation gate | Script that checks each entry against known Catholic reference databases. Flags entries where confidence conflicts with known calendars. | Gate catches a known test discrepancy. |
| C4 | Full year generation | Generate 365 entries for Catholic liturgical year (2026). Batch process — research agent per date. Sources populated, confidence assigned, VI fields follow English pattern. | All 365 dates populated. |
| C5 | Fill backlog dates | Generate Jul 17-30 entries (14 days) per mechanical packets if pilot reveals prompt issues. | Each packet returns valid anno.mock.v1 JSON. |
| C6 | Content validation | Run validate_mock_content.py on the full generated set. Check: bilingual fields, calendar conversions, source coverage, no placeholder text in primary fields. | All validators pass. |

**Risk mitigation:**
- Pilot 14 days first before committing to 365 — validates prompt quality early
- Maintain backup of existing placeholder dataset in case generation pipeline fails
- Use parallel agents for date batch generation (14 dates per batch)
- Source validation gate prevents hallucinated saints/feasts

---

## Sprint D: Architecture — Engine A + UI Wiring

**Goal:** Calendar conversion engine reconciled and wired. Confidence badges live.

| # | Task | Detail | Verifies |
|---|------|--------|----------|
| D1 | Engine A reconciliation | Import calendar_engine.py + JSONL from archived infrastructure bundle (`/home/ichabod/07_Backups/Anno_infrastructure_archive_2026-08-19/Anno/interfaith/`). Diff against existing project copies. Schema version check. | Engine produces same output as original. |
| D2 | Calendar conversion wire | Wire Engine A output into TodayView calendar conversion grid. Show Julian, Hebrew, Islamic, Coptic, Ethiopian conversions for each date. | Jul 3 shows correct conversions. |
| D3 | Confidence badges | Implement confirmed/traditional/disputed pills in TodayView. Distinct visual styling per confidence level. Tooltip showing confidence_note. | Each confidence level visually distinct. |
| D4 | Map view refinement | Verify MapKit integration. Pins only where `place != null`. List fallback for simulator. | Week has 6 pins (Jul 5 excluded as no fixed place). |
| D5 | Source sheet verification | Verify SourceSheet displays correctly with populated sources from Engine B output. Group by type. | Jul 3 shows USCCB, Vatican News, CatholicCulture. |
| D6 | Environment validation | Run all three validation tools. Verify Engine B entries decode without errors when bundled into app resources. | Full app launches with real content. |
| D7 | App Store compliance prep | Age rating, permissions review, accessibility audit (VoiceOver, Dynamic Type). | Checklist complete. |

**Risk mitigation:**
- Engine A reconciliation: if schema drift found → migration script, don't force-merge
- Map view: if MapKit preview unavailable, list fallback is already in SacredSiteListView.swift
- Build verification after every D task prevents cascade failures

---

## Sprint E: Sacred Atlas

**Goal:** Sacred pilgrimage map + pilgrim mode.

| # | Task | Detail | Verifies |
|---|------|--------|----------|
| E1 | Opt4 base implementation | Per SACRED_ATLAS_COMPLETION_PLAN.md §5.2 folder layout. SacredAtlasViewModel, SacradAtlasRepository, SwiftData models. | Map shows locations with pins. |
| E2 | Opt3 UX enhancements | Layer "On This Ground" proximity banner (100m), SafariServices sheet, custom pins. | Proximity banner triggers in test. |
| E3 | Pilgrim mode | PilgrimModeView, PilgrimPassportView, RoutePacks. Journey tracking with SwiftData. | Passport stamps accumulate. |
| E4 | StoreKit 2 scaffolding | Subscription tiers: free/premium/premium+pilgrim. Paywall from existing ArchivePaywallView. Restore/terms/privacy. | Static paywall displays correctly. |
| E5 | Final integration sweep | Full app walkthrough: today → calendar → map → saved → paywall. VI toggle at every screen. | No blank screens, no unlocalized UI. |

**Risk mitigation:**
- Opt3 UX enhancements can be deferred to v1.1 if Opt4 base is complex
- Location permissions added in this sprint, not earlier
- StoreKit 2 is scaffolding only — subscription products set up in App Store Connect

---

## Sprint F: App Store Submission

**Goal:** Ship.

| # | Task | Detail | Verifies |
|---|------|--------|----------|
| F1 | App Store metadata | Name, subtitle, description, keywords, support URL, marketing URL. EN + VI. | App Store Connect drafts. |
| F2 | Screenshots | Capture all required device sizes per IOS_PREVIEW_CHECKLIST. EN + VI. | 6 screenshots × 2 languages × required sizes. |
| F3 | TestFlight build | Archive, upload, distribute to internal testers. 7-day beta test. | Crash-free session rate >99%. |
| F4 | CI/CD (optional) | GitHub Actions for build validation on each push. | PRs automatically build. |
| F5 | Final compliance sweep | PrivacyInfo.xcprivacy, age rating, content rights, export compliance. | No warnings during App Store review. |
| F6 | Submit | Archive → App Store Connect → Submit for Review. | App is live. |

---

## Architecture Diagram (What Gets Built)

```
Anno/
├── AnnoApp.swift + RootView.swift  ← Tab nav: Today/Calendar/Map/Saved
├── AnnoWidget/                      ← "Today in Sacred History" (Sprint A target, B impl)
├── Today/                           ← TodayView, ConfidenceBadge, CalendarConversionGrid
├── Calendar/                        ← MonthCalendarView, EntryListRow
├── Map/                             ← SacredSiteMapView, SacredSiteListView, Pilgrim mode
├── Saved/                           ← SavedView
├── Paywall/                         ← ArchivePaywallView, ProductCopy
├── Sources/                         ← SourceSheet, SourceRow
├── Models/                          ← AnnoEntry, Bookmark + SwiftData (Journey, Visit, FieldNote)
├── Services/                        ← FixtureStore, AnnoDevotionalLoader, DevotionalProvider,
│                                      BookmarkActions, NotificationService, SearchHistory
├── Components/                      ← GlassCard, ShareCard, ShareableImage, VerseActionBar
├── Design/                          ← AnnoTheme, Typography
├── Localization/                    ← LanguageMode, LocalizedEntryText, Localizable.xcstrings
├── Utilities/                       ← Haptics
├── Settings/                        ← SettingsView
├── Resources/                       ← anno_full_2026_2029.json (real content, post-Sprint C)
├── data/                            ← mock/, localization/, assets/ (artwork clearance queue)
├── docs/                            ← All canonical planning docs
├── tools/                           ← Validation and generation utilities
└── Features/SacredAtlas/            ← Atlas + pilgrim mode (Sprint E)
    ├── Models/  (AtlasModels, Journey.swift, Visit.swift, FieldNote.swift)
    ├── ViewModels/  (SacredAtlasViewModel, JourneyViewModel)
    ├── Services/  (AnnoLocationManager, EntitlementService)
    ├── Views/  (SacredAtlasView, LocationDetailView, PilgrimModeView, PilgrimPassportView)
    └── Infrastructure/  (AnnoTheme, L.swift, MockSacredAtlasRepository)
```

## Verification Gates

Every sprint ends with a verification run:
```
python3 tools/validate_anno_local_build.py
python3 tools/validate_localization.py --localization-dir localization
python3 tools/validate_mock_content.py
```

Plus iOS-specific per IOS_PREVIEW_CHECKLIST.md.

## Changelog

- 2026-07-10 v2 — MMR-ingested: Added explicit A6 loading states, A4 localization smoke test, B3 widget content, C1-C6 content pipeline with pilot-first approach, D4-D7 verification, E StoreKit scaffolding, F submission sprint. Source validation gate added. Widget target moved to Sprint A. Verified all 13 KJV files on disk (MMR false positive corrected).
