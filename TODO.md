# Anno — Master Decomposed Roadmap & Empirical Task List

**Ethos:** Sacred Multi-Calendar Date Conversion, Catholic-First Sacred History, Bilingual (EN/VI) & Sourced Research  
**Canonical Continuity Tracker:** `MVP_PLAN_FINAL.md` / `ARCHITECTURE.md`  
**Current Phase:** Phase 3 (Single Loop) / Phase 4 (Prove Loop Gating)

---

## 1. Product Vision Targets (KPIs) vs Current Ground Truth

| Metric / Dimension | Current Level (Snapshot) | Real Product Target (KPI) | Status & Active Gap |
|---|---|---|---|
| **Deterministic Calendar Engine** | `calendar_engine.py` (Gregorian, Hebrew, Hijri) | **100% deterministic multi-calendar conversion** | ✅ **DONE:** Reconciled & passing Python engine tests. |
| **Bilingual Localization (EN/VI)** | Structural Swift manager + partial EN mock data | **100% bilingual EN & VI text for all feast days & saints** | 🟡 **Gap:** Resolve missing Vietnamese translations in August 2026 mock data. |
| **Engine B Source Gate** | `validate_engine_b_output.py` script | **100% strict LLM citation validation before use** | ✅ **DONE:** Gate script built & tested. |
| **Swift Fixture Exporter** | `export_swift_fixture.py` script | **Automated 4-year calendar JSONL -> Swift export** | ✅ **DONE:** Fixture exporter functional. |
| **Xcode Project Scaffolding** | Source files in `Anno/` & `ios/` | **Full `.xcodeproj` bundle compiling in Xcode** | 🟡 **Gap:** Scaffold Xcode project on macOS device. |
| **SwiftUI Native Screen Views** | 4 primary view components implemented | **4 complete screens (Today, Calendar, Map, Saved)** | 🟡 **Gap:** Complete MapKit saint geographic pin integration in `MapView.swift`. |

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

- [ ] **Task 1: Complete August Vietnamese Mock Data:** Translate remaining missing Vietnamese strings in `AnnoMockData.swift` and August JSON datasets.
- [ ] **Task 2: Xcode Project Scaffolding:** Open project on macOS, generate `.xcodeproj`, and configure bundle target (`com.anno.app`).
- [ ] **Task 3: MapKit Sacred Geography Integration:** Wire geographic lat/lon coordinates into `MapView.swift` for interactive shrine exploration.
- [ ] **Task 4: StoreKit 2 & String Catalogs Setup:** Configure StoreKit 2 subscription tiers and Xcode String Catalogs for `vi.lproj`.
- [ ] **Task 5: Mac Build Sweep:** Execute batch build and test sweep on MacBook Pro.
