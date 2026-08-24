# Anno — Master Decomposed Roadmap & Empirical Task List

**Ethos:** Sacred Multi-Calendar Date Conversion, Catholic-First Sacred History, Bilingual (EN/VI) & Sourced Research  
**Canonical Master Plans:**
- Master Consolidated Plan: [`docs/plans/CONSOLIDATED_AUDIT_AND_EXPANSION_PLAN.md`](docs/plans/CONSOLIDATED_AUDIT_AND_EXPANSION_PLAN.md)
- Phase A (Content Pipeline): [`docs/plans/PHASE_A_CONTENT_EXPANSION_SPRINT.md`](docs/plans/PHASE_A_CONTENT_EXPANSION_SPRINT.md)
- Phase B (Monetization Assets): [`docs/plans/PHASE_B_MONETIZATION_ASSETS_SPRINT.md`](docs/plans/PHASE_B_MONETIZATION_ASSETS_SPRINT.md)
- Architecture & Continuity: [`MVP_PLAN_FINAL.md`](MVP_PLAN_FINAL.md) / [`ARCHITECTURE.md`](ARCHITECTURE.md) / [`Conversion-Design.md`](Conversion-Design.md)  
**Current Phase:** Phase A & Phase B (100% Complete & Verified on Linux) $\rightarrow$ Phase C/D (macOS Client Scaffolding)

---

## 1. Product Vision Targets (KPIs) vs Current Ground Truth

| Metric / Dimension | Current Level (Snapshot) | Real Product Target (KPI) | Status & Active Gap |
|---|---|---|---|
| **Deterministic Calendar Engine** | `calendar_engine.py` (Gregorian, Hebrew, Hijri) | **100% deterministic multi-calendar conversion** | ✅ **DONE:** Reconciled & passing Python engine tests. |
| **Bilingual Localization (EN/VI)** | Structural Swift manager + 182-day continuous dataset + 63-key string catalog | **100% bilingual EN & VI text for all feast days & saints** | ✅ **DONE (2026-08-24):** 182 days (1,274 VI fields, 0 empty); 63/63 Localizable.strings keys (100% parity). |
| **Engine B Source Gate & Citations** | `validate_mock_content.py` + `validate_engine_b_output.py` | **100% strict LLM citation validation before use** | ✅ **DONE:** All 182 entries pass with $\ge 2$ verified primary/academic sources. |
| **Swift Fixture Exporter** | `export_swift_fixture.py` script | **Automated 4-year calendar JSONL -> Swift export** | ✅ **DONE:** 182-day Swift mock dataset compiled into `AnnoMockData.swift`. |
| **Monetization & StoreKit 2** | `AnnoProducts.storekit` + `EntitlementService.swift` | **Full 4-tier funnel with Day Pass & Pilgrimage Subscriptions** | ✅ **DONE:** StoreKit config, paywall triggers, and entitlement service built. |
| **Sacred Geography & Routes** | `PilgrimageRoutes/` (4 routes, 21 waypoints) | **Curated GPS pilgrimage route packs** | ✅ **DONE:** Rome, Holy Land, European Marian, and Vietnam shrines complete. |
| **Sacred Art Iconography** | `ArtDossiers/` (65 masterpieces) | **High-res zoomable sacred art dossiers** | ✅ **DONE:** 65 public domain works with active HTTP URLs and bilingual notes. |
| **Rotating Devotional Pool** | `anno_devotional_pool_365.json` | **365-day bilingual Catholic devotional rotation** | ✅ **DONE:** 365 days across 12 spiritual cycles with Swift loader. |
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
- [x] **Sprint B.1:** 4 Pilgrimage route packs in `Anno/Resources/PilgrimageRoutes/` (Rome Seven Churches, Holy Land Way of the Cross, European Marian Shrines, Vietnam Sacred Shrines) with `tools/validate_route_coordinates.py`.
- [x] **Sprint B.2:** 65 High-resolution sacred art dossiers in `Anno/Resources/ArtDossiers/art_dossiers_catalog.json` with `tools/verify_artwork_links.py`.
- [x] **Sprint B.3:** StoreKit 2 configuration (`Anno/Configuration/AnnoProducts.storekit`) and bilingual product metadata (`Anno/Resources/product_metadata.json`).
- [x] **Sprint B.4:** Client paywall trigger rules (`Anno/Resources/paywall_triggers.json`), `Anno/Services/EntitlementService.swift`, and 63-key string catalog expansion (`localization/en` and `localization/vi`).

---

## 3. Active Execution Tasks (macOS Environment)

- [ ] **Task C.1:** Xcode project scaffolding on macOS host per [`docs/NATIVE_BUILD_RUNBOOK.md`](docs/NATIVE_BUILD_RUNBOOK.md).
- [ ] **Task C.2:** MapKit pilgrimage route polyline overlay renderer in `Anno/Map/SacredSiteMapView.swift`.
- [ ] **Task D.1:** StoreKit 2 sandbox testing and TestFlight build submission.
