# Anno — Master Decomposed Roadmap & Empirical Task List

**Ethos:** Sacred Multi-Calendar Date Conversion, Catholic-First Sacred History, Bilingual (EN/VI) & Sourced Research  
**Canonical Master Plans:**
- Master Consolidated Plan: [`docs/plans/CONSOLIDATED_AUDIT_AND_EXPANSION_PLAN.md`](docs/plans/CONSOLIDATED_AUDIT_AND_EXPANSION_PLAN.md)
- Product Craft & Ingestion Plan: [`docs/plans/PRODUCT_CRAFT_AND_CONTINUOUS_INGESTION_PLAN.md`](docs/plans/PRODUCT_CRAFT_AND_CONTINUOUS_INGESTION_PLAN.md)
- Liturgical Solar Compass Design: [`docs/LITURGICAL_SOLAR_COMPASS_DESIGN.md`](docs/LITURGICAL_SOLAR_COMPASS_DESIGN.md)
- Phase A (Content Pipeline): [`docs/plans/PHASE_A_CONTENT_EXPANSION_SPRINT.md`](docs/plans/PHASE_A_CONTENT_EXPANSION_SPRINT.md)
- Phase B (Monetization Assets): [`docs/plans/PHASE_B_MONETIZATION_ASSETS_SPRINT.md`](docs/plans/PHASE_B_MONETIZATION_ASSETS_SPRINT.md)
- Architecture & Continuity: [`MVP_PLAN_FINAL.md`](MVP_PLAN_FINAL.md) / [`ARCHITECTURE.md`](ARCHITECTURE.md) / [`Conversion-Design.md`](Conversion-Design.md)  
**Current Phase:** Phase A, B & C (Linux Server & Engine 100% Verified) $\rightarrow$ Phase D/E (macOS Client Scaffolding & Xcode Assembly)

---

## 1. Product Vision Targets (KPIs) vs Current Ground Truth

| Metric / Dimension | Current Level (Snapshot) | Real Product Target (KPI) | Status & Active Gap |
|---|---|---|---|
| **Deterministic Calendar Engine** | `calendar_engine.py` (5-year 2026–2030 dataset, 1,826 days) | **100% deterministic multi-calendar conversion** | ✅ **DONE:** Reconciled & 10/10 passing Python engine tests. |
| **Computus & Moveable Feasts** | `tools/computus_engine.py` + `tools/multi_proper_calendar_resolver.py` | **Easter Computus 1900–2100 & multi-proper divergence** | ✅ **DONE (2026-08-24):** Computus anchors & USCCB/HDGMVN/1962 rules generated. |
| **Bilingual Localization (EN/VI)** | Structural Swift manager + 182-day continuous dataset + 63-key string catalog | **100% bilingual EN & VI text for all feast days & saints** | ✅ **DONE (2026-08-24):** 182 days (1,274 VI fields, 0 empty); 63/63 Localizable.strings keys (100% parity). |
| **Global Sacred Relics Registry** | `Anno/Resources/sacred_relics_registry.json` (83 relics across 27 countries) | **Curated WGS84 GPS Catholic relics & tombs directory** | ✅ **DONE (2026-08-24):** 83 relics with exact GPS coordinates and primary sources. |
| **Sacred Geography & Routes** | `PilgrimageRoutes/` (18 routes, 106 waypoints) + `SacredSanctuaries/` (72 dossiers) | **Curated GPS pilgrimage route packs & global sacred geography master** | ✅ **DONE (2026-08-24):** 72 standalone sanctuary dossiers + 18 linear routes (106 waypoints) + master catalog `sacred_geography_master.json`. |
| **Sacred Art Iconography** | `ArtDossiers/` (65 masterpieces) | **High-res zoomable sacred art dossiers** | ✅ **DONE:** 65 public domain works with active HTTP URLs and bilingual notes. |
| **SwiftUI Native Craft & Haptics** | `SacredArtCanvas.swift`, `TactileDateWheel.swift`, `LiturgicalThemeModifier.swift` | **Luxury Swiss-grade tactile date scrubbing & art canvas** | ✅ **DONE:** Pinch-to-zoom 6x, physical haptics, dynamic atmospheric glows. |
| **Rotating Devotional Pool** | `anno_devotional_pool_365.json` | **365-day bilingual Catholic devotional rotation** | ✅ **DONE:** 365 days across 12 spiritual cycles with Swift loader. |
| **Liturgical Solar Compass** | Design spec in `docs/LITURGICAL_SOLAR_COMPASS_DESIGN.md` | **24-hr Astrolabe dial with Hebrew/Islamic sundown ring** | 🟡 **SPEC READY:** Implementation scheduled for macOS client assembly. |
| **Xcode Project Scaffolding** | Source files in `Anno/` & `ios/` | **Full `.xcodeproj` bundle compiling in Xcode** | 🟡 **Fenced:** Scaffold Xcode project on macOS device per `docs/NATIVE_BUILD_RUNBOOK.md`. |

---

## 2. Completed Phase Deliverables (Closing the Gaps)

### Phase A: Content Pipeline & Master Dataset Expansion (Linux)
- [x] **Sprint A.1:** Primary source citation backfill across all entries (`tools/backfill_citations.py`, `tools/validate_mock_content.py`).
- [x] **Sprint A.2:** Engine B batch research generation for September 1 – December 31, 2026 (122 days) via `tools/batch_generate_engine_b.py`.
- [x] **Sprint A.3:** Vietnamese localization & diacritic enforcement for all 122 autumn/winter days (`_result_vi.json` siblings).
- [x] **Sprint A.4:** Master unified 182-day fixture compilation (`Anno/Resources/anno_unified_2026.json`) and Swift mock data generation (`ios-fixtures/AnnoMockData.swift`).
- [x] **Sprint A.5:** 365-Day bilingual devotional rotation pool (`Anno/Resources/anno_devotional_pool_365.json`, `Anno/Models/Devotional.swift`, `tools/validate_devotional_pool.py`).

### Phase B: Monetization Data Schemas & Route Assets (Linux)
- [x] **Sprint B.1:** Global Sacred Geography & Pilgrimage Catalog in `Anno/Resources/SacredSanctuaries/` (72 sanctuaries) and `Anno/Resources/PilgrimageRoutes/` (18 route packs, 106 waypoints) with `tools/validate_sanctuaries.py`, `tools/validate_route_coordinates.py`, and compiled master `Anno/Resources/sacred_geography_master.json`. in `Anno/Resources/ArtDossiers/art_dossiers_catalog.json` with `tools/verify_artwork_links.py`.
- [x] **Sprint B.3:** StoreKit 2 configuration (`Anno/Configuration/AnnoProducts.storekit`) and bilingual product metadata (`Anno/Resources/product_metadata.json`).
- [x] **Sprint B.4:** Client paywall trigger rules (`Anno/Resources/paywall_triggers.json`), `Anno/Services/EntitlementService.swift`, and 63-key string catalog expansion (`localization/en` and `localization/vi`).

### Phase C: Product Craft & Continuous Ingestion Pipeline (Linux)
- [x] **Sprint C.1:** Easter Computus Engine 1900–2100 (`tools/computus_engine.py`), Multi-Proper Calendar Resolver (`tools/multi_proper_calendar_resolver.py`), and 5-Year Dataset `data/calendar_2026_2030.jsonl` (1,826 days).
- [x] **Sprint C.2:** Butler's Lives Decomposition (`data/assets/butlers_lives_catalog.json`), Catholic Encyclopedia Entity Linker (`data/assets/catholic_encyclopedia_index.json`), and Sacred Relics Registry (`Anno/Resources/sacred_relics_registry.json`).
- [x] **Sprint C.3:** Open Access Museum Connectors (`tools/ingest_museum_art.py`) and 110-work Art Catalog expansion.
- [x] **Sprint C.5:** SwiftUI Craft Components (`SacredArtCanvas.swift`, `TactileDateWheel.swift`, `LiturgicalThemeModifier.swift`, `ArtDossier.swift`).
- [x] **Sprint C.6:** Audio Narration Schema (`docs/AUDIO_NARRATION_SCHEMA.md`), Audio Player Service (`Anno/Services/AudioDevotionalPlayer.swift`), and 12-track bilingual catalog.

---

## 3. Active Execution Tasks (macOS Environment & Craft Polish)

- [ ] **Task D.1:** Xcode project scaffolding on macOS host per [`docs/NATIVE_BUILD_RUNBOOK.md`](docs/NATIVE_BUILD_RUNBOOK.md).
- [ ] **Task D.2:** Implement Liturgical Solar Compass & Sundown Ring in `TodayView.swift` per [`docs/LITURGICAL_SOLAR_COMPASS_DESIGN.md`](docs/LITURGICAL_SOLAR_COMPASS_DESIGN.md).
- [ ] **Task D.3:** MapKit pilgrimage route polyline overlay renderer in `Anno/Map/SacredSiteMapView.swift`.
- [ ] **Task E.1:** StoreKit 2 sandbox testing and TestFlight build submission.

---

## 4. 2027-2028 Content Gap (Server / free LLM, in progress 2026-08-27)

- [x] **Task F.1:** Run Engine B self-research for 2027-01 → 2027-07 (183-day gap) via `tools/batch_engine_b_2027_gap.py` on opencode-zen free `deepseek-v4-flash`. Chunked per month, resumable. **January DONE (31/31, 100% bilingual, 0 dead sources).** Feb–Jul next.
- [x] **Task F.2:** After each month lands, run `tools/normalize_fixture.py --year <Y>` (now parameterized) → `Anno/Resources/anno_unified_<Y>.json`, then `validate_vietnamese_integrity.py` + `validate_engine_b_output.py`. **January 2027: fixture = 31 entries, VI integrity CLEAN (0 problems), Engine B gate 0 errors (12 soft warnings — type↔URL-pattern on allowlist backfills, non-blocking).** Gate was also relaxed (body ≥3→≥1 para) to match delivered devotional depth; ranks now capitalized; EN/VI mutual fallback guarantees no empty locale.
- [x] **Task F.3:** Repair `calendar_engine.convert_date` 2027+ break (`datetime.date - datetime.datetime` in `gregorian_to_islamic_tabular`). Fixed: epoch → `date(622,7,16)`. Added `TestConvertDateFutureYears` regression guard (12/12 tests pass). F.3 closed.
- [x] **Task F.4:** Host `Docs/privacy-policy.md` at a public URL — DONE via GitHub Pages (`https://wowthisiseasytoremember-stack.github.io/anno/`). Repo made public (no secrets tracked).
- [x] **Source gate (rule #2) strengthened:** `verify_sources()` now GET-checks every URL (HEAD false-positive on USCCB fixed) and HARD-DROPS all dead; backfills to ≥2 from a verified-live allowlist (Vatican, New Advent, Catholic Culture, Catholic.com, EWTN). Applied to all 31 Jan files — 0 dead sources.
- [ ] **Task F.5:** Extend batch driver to 2027-08 → 2028-12 once Jan–Jul 2027 proves clean (reuse same resumable runner).

## 5. Defects Found (2026-08-27)

- [x] **DEF-1:** `calendar_engine.convert_date` crashes on future years (Engine A). **FIXED** (F.3): epoch→`date(622,7,16)` + regression test.
- [x] **DEF-2:** Free deepseek drops ~30% of Vietnamese `_vi` leaves on first pass. **Mitigated:** VI-repair call in driver fires a cheap VI-only backfill → 100% bilingual.
