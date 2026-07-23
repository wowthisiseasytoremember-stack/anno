# Audit: Agent Output v2 (Second Implementation) — Anno Sacred Atlas

**Source:** User-pasted code dump (second batch, post-zip)
**Comparison target:** First agent's zip output (`workspace-019f2b75...`)
**Review date:** 2026-07-04

---

## Overall Grade: 8.5/10

Substantially better than v1. Architecture is cleaner, models are richer, localization is proper `LocalizedStringKey`, and the premium value story is more coherent. This version has a stronger founder-product-engineer feel.

---

## What's Better vs v1

**Localization is now production-grade.** `LocalizedStringKey` enums that map directly to Xcode `.xcstrings`. Not a hand-rolled dictionary. This is the correct approach — can be wired to actual translators via Apple's String Catalog workflow.

**`@Observable` macro.** iOS 17+ native observable, no `@StateObject`/`@ObservedObject` boilerplate. Cleaner, less fragile, fewer re-render bugs.

**SwiftData integration is real.** `JourneySession`, `FieldNote`, `PassportStamp` are actual SwiftData `@Model` classes with relationships and cascade delete. The modelContext is wired at the container level. This is shippable persistence, not a stub.

**Teardrop-shaped pins.** The `TeardropShape` is a genuine design improvement over flat circles — more premium, more map-like, more "sacred atlas." The tradition-specific symbols inside the pin communicate at a glance.

**Paywall has specific counts.** The spec's key requirement: "Better if your mock data uses realistic counts." The `nearbyCountSummary()` returns `(total, today, traditional, disputed)` — this is the conversion mechanic the spec asked for. The `PaywallCardView` uses these specifics rather than vague marketing copy.

**Location simulation for previews.** `LocationService.startSimulating(alongRoute:)` cycles through route stops, updating `currentCoordinate`. This makes Pilgrim Mode demo-able without GPS hardware — important for App Store previews and investor demos.

**EntitlementService is cleaner.** `canBrowseFullAtlas`, `canReadFullDossier`, `canUseConfidenceLayer`, `canStartPilgrimage` — semantic accessors that the spec asked for. `maxFreePins: 3` is explicit and simple.

**Repository is smaller and tighter.** Single `MockSacredRepository.shared` with inline fixtures in the initializer. No 519-line extension. Data is organized and readable.

**Route pack detail is richer.** Estimated km, estimated hours, hero symbol, previewStopCount, traditions array. The detail view shows numbered stops with progress.

**Hero area uses real artwork.** `ArtworkFrame` with artist, period, provenance, source credit. This is the beauty pillar from the spec.

---

## What's Still Weak

**No tests.** Same as v1. Zero test target. The ViewModel logic (`filteredLocations`, `nearbyCountSummary`, `toggle(confidence:)` gating) has no coverage.

**MapKit still uses `.standard(emphasis: .muted)`.** Better than v1's gradient hack, but still not the "dark sacred atlas" look the design board demands. The `pointsOfInterest: .excluding(.all)` is correct. The gold tint on `.tint(AnnoTheme.gold)` is nice. But without custom tile styling, the map won't look like the mockups.

**Single mock repository file.** The `MockSacredRepository` initializer is a monster — every location, event, artwork, source, and route pack is inlined into one `init()`. This works for demo but will become unmaintainable at real scale. File-by-file fixtures or a JSON loader would be better.

**No pagination or clustering.** Still 18 locations. The code claims "2,400+ sacred sites" in the paywall, but the data model and map integration don't support scale. Annotations at 2,400 would crash MapKit.

**Tier naming is still muddy.** `EntitlementTier` has `free < premium < pilgrim` with `Comparable` conformance, which is correct. But the feature split: premium gets full atlas + route packs, pilgrim gets journey tracking. The spec recommended making pilgrim the annual plan's hero. The code has a 3-tier model that maps to 2 actual products. This needs product decision, not code.

**No temporal scrubber.** The spec suggested century/date filtering as a premium feature. Neither v1 nor v2 implements it. It's not in the scope, but it's the missing "wow" feature that would truly justify $69.99/year.

**Vietnamese localization keys documented but no actual Vietnamese strings.** The `L` enum uses `LocalizedStringKey` which is correct, but no `.xcstrings` file or Vietnamese translations are provided. The spec asked for "Vietnamese UI chrome is in scope" structurally. This is structurally ready but empty.

**`Event` is a Foundation type name collision.** `struct SacredEvent` would be better named to avoid confusion with `SwiftUI.Event` or notification events. Minor but real.

---

## Major Architecture Wins

| Aspect | v1 (zip) | v2 (this) |
|--------|---------|-----------|
| Localization | Dictionary | LocalizedStringKey |
| Observable | ObservableObject + @StateObject | @Observable macro |
| Persistence | Separate SwiftData models, no wiring | Wired via modelContainer |
| Map pins | Circles | Teardrop shapes with symbols |
| Premium framing | Generic "unlock" | Specific counts (12/3/2/1) |
| Location | Mock hardcoded LA | Simulated route walking |
| Data | 519-line static extension | Inline in repository init |
| Artwork support | systemImage only | Full provenance display |

---

## If Building From This

1. Add SwiftData seeds for mock data (replace the monster init with JSON fixtures).
2. Add unit tests for `filteredLocations`, `nearbyCountSummary`, entitlement gating.
3. Implement MapKit clustering (`MKClusterAnnotation`) before adding >100 pins.
4. Add temporal scrubber as premium differentiator (centuries filter).
5. Build `.xcstrings` with actual Vietnamese translations (currently placeholder).
6. Decide: single annual tier (pilgrim = premium) or 3-tier with cumulative benefits?
7. Wire real `CLLocationManager` (the simulation mode is for demo only — remove or gate behind a flag for production).
8. Add custom tile styling or accept that the map won't match the "dark sacred atlas" mockups in v1.0.

---

## Summary

This version is significantly closer to a shippable feature. It has the right architecture, the right localization strategy, the right entitlement model, and the right premium framing. The remaining gaps are execution scale (mock data volume, Vietnamese content, test coverage) and the map styling gap (production MapKit can't do the "dark atlas" look without a tile server or significant customization).

The model that produced this had stronger iOS 17+ patterns (`@Observable`, `SwiftData`, `LocalizedStringKey`) than the first. This reads like a **Claude Opus 4** or **GPT-5** output with specific iOS 17+ training data. The architecture decisions (repository protocol, observable state, SwiftData) are better than the first agent's. The product decisions (specific paywall counts, teardrop pins, simulation) show better taste.
