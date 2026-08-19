# Anno — Master Decomposed Roadmap & Empirical Task List

**Ethos:** Sacred Multi-Calendar Date Conversion, Catholic-First Sacred History, Bilingual (EN/VI) & Sourced Research  
**Canonical Continuity Tracker:** `MVP_PLAN_FINAL.md` / `ARCHITECTURE.md`  
**Current Phase:** Phase 3 (Single Loop) / Phase 4 (Prove Loop Gating)

---

## 1. Product Vision Targets (KPIs) vs Current Ground Truth

| Metric / Dimension | Current Level (Snapshot) | Real Product Target (KPI) | Status & Active Gap |
|---|---|---|---|
| **Deterministic Calendar Engine** | `calendar_engine.py` (Gregorian, Hebrew, Hijri) | **100% deterministic multi-calendar conversion** | ✅ **DONE:** Reconciled & passing Python engine tests. |
| **Bilingual Localization (EN/VI)** | Structural Swift manager + bilingual EN/VI content (fortnight + Engine B + August Bilingual) | **100% bilingual EN & VI text for all feast days & saints** | ✅ **DONE (2026-08-19):** August 217/217 `*_vi`; Engine B 14/14 `*_vi`; fortnight already filled. |
| **Engine B Source Gate** | `validate_engine_b_output.py` script | **100% strict LLM citation validation before use** | ✅ **DONE:** Gate script built & tested. |
| **Swift Fixture Exporter** | `export_swift_fixture.py` script | **Automated 4-year calendar JSONL -> Swift export** | ✅ **DONE:** Fixture exporter functional. |
| **Xcode Project Scaffolding** | Source files in `Anno/` & `ios/` | **Full `.xcodeproj` bundle compiling in Xcode** | 🟡 **Gap:** Scaffold Xcode project on macOS device. |
| **SwiftUI Native Screen Views** | 4 primary view components implemented | **4 complete screens (Today, Calendar, Map, Saved)** | 🟡 **Gap:** MapKit sacred-geography pins CUT from MVP (v2) — see Task 3. Other 3 screens scaffolded. |

---

## 2. The 3-Layer Engine Architecture

- [x] **Engine A (Deterministic Calendar Conversion):** Pure Python math (pyluach, hijri-converter, convertdate) converting Gregorian $\leftrightarrow$ Hebrew $\leftrightarrow$ Hijri without LLM hallucination.
- [x] **Engine B Output Gate (Sourced Historical Research):** Validates LLM research output and primary source citations before ingestion (`tools/validate_engine_b_output.py`).
- [x] **Layer C (Devotional Content Framing):** Renders inspirational devotional framing over verified historical facts.

---

## 3. Screen Specifications (4 Main Screens)

- [x] **Screen A (Today View):** `TodayView.swift` (daily feast card, multi-calendar date display, saint biography, prayer).
- [x] **Screen B (Calendar Converter & Grid):** `CalendarView.swift` (Gregorian/Hebrew/Hijri dual calendar picker and conversion table).
- [ ] **Screen C (Sacred Geography Map):** `MapView.swift` (MapKit view pinning historical saint birthplaces, apparition sites, and monastic shrines).
- [x] **Screen D (Saved Reflections & Bookmarks):** `SavedView.swift` (bookmarked feast days, custom prayers, and reading history).

---

## 4. Active Execution Tasks (Closing the Gaps)

- [x] **Task 1: Complete August Vietnamese Mock Data:** 217 `*_vi` fields filled in `data/mock/anno_august_2026.json` (2026-08-19); source folded from part1-3 slices.
- [x] **Task 1b: Engine B 07-17→07-30 Vietnamese:** all 14 dates have `*_vi` (49 + 49 fields) via `_result_vi.json` siblings.
- [ ] **Task 2: Xcode Project Scaffolding:** Mac-only — see `docs/NATIVE_BUILD_RUNBOOK.md`. Cannot run on ichabod.
- [ ] **Task 3: MapKit Sacred Geography Integration:** CUT from MVP scope (per MMR review); v2 backlog.
- [ ] **Task 4: StoreKit 2 & String Catalogs Setup:** StoreKit CUT from MVP (v2); String Catalogs import `localization/{en,vi}` on Mac.
- [ ] **Task 5: Mac Build Sweep:** Mac-only — see runbook.
- [x] **Task 6: Normalize 3 content tracks** into `Anno/Resources/anno_unified_2026.json` (59 entries); `export_swift_fixture.py` re-pointed; `AnnoMockData.swift` regenerated.
- [ ] **Task 7: Add sources to fortnight/August fixtures** (45/59 entries have <2 sources) OR relax `validate_mock_content.py`. Server-doable.
