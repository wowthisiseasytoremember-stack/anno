# Sacred Atlas — Design Decisions & Open Questions
**Anno · July 2026**

This document resolves discrepancies across 4 implementation options into a single build direction. It captures every divergence found, states the decision, and flags any remaining open question.

---

## 1. Entitlement Model

| Detail | Value |
|--------|-------|
| **Options** | Opt1: 2-tier (`free`, `premium`) · Opt2/3/4: 3-tier (`free`, `premium`, `pilgrim`) |
| **Decision** | **3-tier** (`free`/`premium`/`pilgrim`) from Opt4's `EntitlementTier` — semantic accessors (`canAccessFullAtlas`, `canStartPilgrimage`, etc.) provide clean gating without inline tier comparisons |
| **Rationale** | The product bible at `ARCHITECTURE.md` already prescribes 3-tier monetization: Free = today's entry, Premium = archive/art/sources, Pilgrim = route packs/offline. Opt4's semantic accessors are the cleanest gating pattern. |
| **Source files** | Opt4 lines 318-350 (enum + semantic gates) |
| **⚠ Open** | None — resolved |

---

## 2. Model Naming: `Confidence` vs `ConfidenceLabel`

| Detail | Value |
|--------|-------|
| **Options** | Opt1/4 use `ConfidenceLabel` · Opt2/3 use `Confidence` |
| **Decision** | **`ConfidenceLabel`** (Opt4's naming) |
| **Rationale** | Prevents collision with Foundation's `Confidence` (e.g. `ConfidenceInterval`). Opt4 also adds localized key bindings (`L10nKey`) — import that pattern. |
| **Source files** | Opt4 lines 154-161 |
| **⚠ Open** | None — resolved |

---

## 3. Map Pin Component

| Detail | Value |
|--------|-------|
| **Options** | Opt2/3: Custom bezier `TeardropShape` + `SacredPinView` · Opt1/4: `SacredPinView` only |
| **Decision** | **`SacredPinView`** (Opt4's approach). Drop `TeardropShape`. |
| **Rationale** | `SacredPinView` already includes tradition-color fill, category icon overlay, today ring (gold stroke), selection state, lock overlay — the exact colorblind-safe icon pattern required by `FEATURES.md` (P0 item #4). TeardropShape adds bezier complexity with zero semantic gain. Opt4's component is complete and correct. |
| **Source files** | Opt4 `SacredPinView` (lines 1922-1964) |
| **⚠ Open** | Verify all category symbols are unicode / SF Symbols (`+`, `✝`, `☦`, `✡`, `☪`, `∞`) to maintain colorblind safety |

---

## 4. SwiftData Schema — `@Attribute(.unique)` on IDs

| Detail | Value |
|--------|-------|
| **Options** | Opt2/3: `@Attribute(.unique) var id: UUID = UUID()` · Opt1/4: `var id: UUID = UUID()` without attribute |
| **Decision** | **Include `@Attribute(.unique)`** on `Journey.id` and `Visit.id` |
| **Rationale** | Prevents duplicate records from corrupting the store. Zero performance cost for UUIDs. Opt4 omitted it, but the plan recommends re-adding it and it's a one-line fix. |
| **Source files** | Opt3 lines 332-340 (Journey), 360-375 (Visit) |
| **⚠ Open** | None — resolved |

---

## 5. SwiftData Schema — Model Names & Relationships

| Detail | Value |
|--------|-------|
| **Options** | Opt2/3: `JourneySession`, `PassportStamp`, `FieldNote` · Opt4: `Journey`, `Visit`, `FieldNote` |
| **Decision** | **Opt4's naming** (`Journey` → `Visit` → `FieldNote` with bidirectional cascades) |
| **Rationale** | Cleaner, shorter, more semantic. `Visit` replaces `PassportStamp` (a stamp IS a visit). The cascade relationships from Opt4 are production-grade: `Journey → [Visit]`, `Journey → [FieldNote]`. |
| **Source files** | Opt4 lines 11240-11320 |
| **⚠ Open** | None — resolved |

---

## 6. Stamp Sigil Generation

| Detail | Value |
|--------|-------|
| **Options** | Opt3 only: sigil code in `Visit.init()` — `SIGIL-{random}-{PLA}` · Others: none |
| **Decision** | **Include** sigil generation in `Visit.init()` |
| **Rationale** | Distinctive UX touch with zero runtime cost. The sigil makes each stamp feel unique from the first visit. Seed from `locationID.prefix(3).uppercased()` + random range. |
| **Source files** | Opt3 `Visit` init (~line 365-375) |
| **⚠ Open** | None — resolved |

---

## 7. Localization Approach

| Detail | Value |
|--------|-------|
| **Options** | Opt1: hardcoded strings · Opt2/3: `LocalizedStringKey` via `L` enum · Opt4: same `L` pattern + Vietnamese fallback |
| **Decision** | **Opt4's `L` enum** (all strings as `LocalizedStringKey`), wired to `Localizable.xcstrings` |
| **Rationale** | Consistent with the project's existing architecture: "Vietnamese localization must be a first-class data shape." Xcode String Catalogs are the specified tool. |
| **Source files** | Opt4 `L.swift` (lines 11327-11542) |
| **⚠ Open** | The SurfaceBook has a `Localizable.xcstrings` file at `~/Documents/` — verify its contents cover the Sacred Atlas keys |

---

## 8. Proximity Detection ("On This Ground")

| Detail | Value |
|--------|-------|
| **Options** | Opt1: 6 refs · Opt2: 2 refs · Opt3: 9 refs · Opt4: **30 refs** |
| **Decision** | **Use Opt4's implementation** — it's the most developed with `OnThisGroundCard`, proximity evaluation in `JourneyViewModel`, and `AnnoLocationManager` with simulation hooks |
| **Rationale** | The plan's recommendation was correct in principle (import from Monolithic V2), but Opt4 independently developed a richer version. Use Opt4 as-is. |
| **Source files** | Opt4 `OnThisGroundCard` (lines 2089-2153), `JourneyViewModel.evaluateProximity` (~line 1780), `AnnoLocationManager` (line 1447) |
| **⚠ Open** | 100m threshold — hardcoded in Opt4. Should be configurable per route pack or user setting? Defer to v2. |

---

## 9. Progress Visualization

| Detail | Value |
|--------|-------|
| **Options** | Opt2/3: `ProgressRing` (trim-based circular gauge) · Opt4: `JourneyProgressView` |
| **Decision** | **Both** — `ProgressRing` as a visual component embedded inside `JourneyProgressView` |
| **Rationale** | Opt4's `JourneyProgressView` (lines 2297-2342) provides the layout shell; `ProgressRing` provides the visual core. They're complementary, not competing. |
| **Source files** | Opt3 `ProgressRing` (~line 350), Opt4 `JourneyProgressView` (line 2297) |
| **⚠ Open** | None — resolved |

---

## 10. SafariView / Source Citation

| Detail | Value |
|--------|-------|
| **Options** | Opt3 only: `SafariView` (SFSafariViewController wrapper) · Others: none |
| **Decision** | **Import** `SafariView` from Opt3 |
| **Rationale** | The architecture mandates "Source sheet" for every fact. SafariView provides the in-app browser for source URL citations without leaving the app. |
| **Source files** | Opt3 `SafariView` (~line 2400-2420) |
| **⚠ Open** | None — resolved |

---

## 11. PreviewHarness

| Detail | Value |
|--------|-------|
| **Options** | Opt2/3: `PreviewHarness` with tier-switching · Opt1/4: none |
| **Decision** | **Import** `PreviewHarness` from Opt3 |
| **Rationale** | Tier-dependent UI requires visual verification at each level. Having a preview toggle between free/premium/pilgrim is a concrete QA tool, not just polish. |
| **Source files** | Opt3 `PreviewHarness` (~line 2581-2620) |
| **⚠ Open** | Adapt to Opt4's 3-tier enum (Opt3 uses the same 3-tier model, so this should be straightforward) |

---

## 12. Pilgrim Passport View

| Detail | Value |
|--------|-------|
| **Options** | Opt3: `PilgrimPassportView` with stamps grid · Opt4: sheet reference only, no implementation |
| **Decision** | **Extract** `PilgrimPassportView` from Opt3 and **adapt** to Opt4's architecture |
| **Rationale** | Opt4's `SacredAtlasView` references `.sheet(isPresented: $viewModel.showPassport) { PilgrimPassportView() }` but the view body lives only in Opt3. Extract stamps grid, journey records, field notes sections. |
| **Source files** | Opt3 `PilgrimPassportView` (~line 1500-1650) |
| **⚠ Open** | Adapt uses of Opt3's `JourneySession` to Opt4's `Journey`. Adapt SwiftData queries from inline to ViewModel. |

---

## 13. Pilgrim Mode View

| Detail | Value |
|--------|-------|
| **Options** | Opt1: `PilgrimModeView` with basic HUD · Opt2/3: `Pilgrim Views` section · Opt4: `PilgrimModeView` sheet reference |
| **Decision** | **Extract** the Pilgrim Mode HUD from Opt3 and **adapt** to Opt4's `JourneyViewModel` |
| **Rationale** | Same as Passport — Opt4 references the sheet but doesn't implement the view body. Opt3 has the complete active-pilgrim HUD with progress, next stop, current site, field notes entry. |
| **Source files** | Opt3 `Pilgrim views` section (~line 1665-1936) |
| **⚠ Open** | Same adaptation issue as Passport — Opt3's models need mapping to Opt4's schema |

---

## 14. RoutePacks View

| Detail | Value |
|--------|-------|
| **Options** | Opt2/3: `RoutePackListView` + `RoutePackDetailView` · Opt4: sheet reference, no implementation |
| **Decision** | **Extract** from Opt3 and **adapt** to Opt4's `RoutePack`/`RouteStop` models |
| **Rationale** | Same pattern — Opt4 has the models but not the views |
| **Source files** | Opt3 `Route Packs` section (~line 1463-1664) |
| **⚠ Open** | Same model adaptation |

---

## 15. Monolithic vs Modular File Structure

| Detail | Value |
|--------|-------|
| **Options** | Opt1/4: multi-file · Opt2/3: single monolithic file |
| **Decision** | **Multi-file** (Opt4's folder structure from the plan's §5.2) |
| **Rationale** | The plan's §5.2 folder layout is definitive. 9 files under `Features/SacredAtlas/` with clear separation. |
| **Source files** | Plan doc §5.2 |
| **⚠ Open** | None — resolved. Follow the plan's folder structure exactly. |

---

## 16. `PilgrimageService` — Separate Service vs Inline in ViewModel

| Detail | Value |
|--------|-------|
| **Options** | Opt4: `PilgrimageService` as a separate `@Observable` class · Opt3: inline in `JourneyViewModel` |
| **Decision** | **Opt4's `PilgrimageService`** (separate service) |
| **Rationale** | Cleaner separation of concerns. `SacredAtlasViewModel` uses it to check visit status; `JourneyViewModel` uses it to record visits. Single responsibility. |
| **Source files** | Opt4 `PilgrimageService` (~line 1522-1590) |
| **⚠ Open** | None — resolved |

---

## Summary of Open Questions (remaining ⚠)

| # | Question | Impact | Resolution Needed |
|---|----------|--------|-------------------|
| 1 | Do the `Localizable.xcstrings` on the SurfaceBook cover Sacred Atlas keys? | Blocker for localization | Retrieve & audit the file |
| 2 | Should the 100m proximity threshold be configurable? | Nice-to-have, defer | Tag as v2 |
| 3 | Extract & adapt PilgrimModeView from Opt3 → Opt4 architecture | Must-do | Coding task |
| 4 | Extract & adapt PilgrimPassportView from Opt3 → Opt4 architecture | Must-do | Coding task |
| 5 | Extract & adapt RoutePacks views from Opt3 → Opt4 architecture | Must-do | Coding task |
| 6 | Verify all category symbols are colorblind-safe Unicode/SF Symbols | Must-do | Review Opt4's category icon mapping |

All other divergences are resolved above with a clear direction and source stakes.

---

## Build Order (Recommended)

1. **Foundation**: Extract Opt4's 9 files into the plan's §5.2 folder structure
2. **Schema fixes**: Add `@Attribute(.unique)` to `Journey.id` + `Visit.id`
3. **Components**: Import `ProgressRing`, `SafariView`, `PreviewHarness` from Opt3
4. **Sigils**: Add stamp code generation to `Visit.init()`
5. **Missing views**: Extract & adapt PilgrimModeView, PilgrimPassportView, RoutePacks from Opt3
6. **Localization**: Wire `L` keys to `Localizable.xcstrings`
7. **Verification**: Build + PreviewHarness at each tier level
