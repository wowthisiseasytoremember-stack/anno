# Audit: Agent Output — Anno Pilgrimage Map Feature

**Source:** `workspace-019f2b75-22c2-76ae-bc48-35bdc67e5aef.zip`
**Authoring prompt:** "Frontier Agent Prompt: Build Anno's Premium Pilgrimage Map Feature"
**Format:** Swift Package Manager module (32 files, 155KB)
**Review date:** 2026-07-04

---

## Overall Grade: 7/10

Impressive structure, thin content, mixed taste. The architecture is a sound production scaffold. The mock data, map integration, and test coverage are not ready for production.

---

## What's Genuinely Good

**Architecture.** Repository protocol → ViewModel → Views is the right shape. SwiftData models alongside in-memory state is a realistic production seam. 32 files in a logical folder tree — well-organized.

**EntitlementPolicy.** `canOpenLocation()`, `canUsePilgrimMode` — simple, testable, no StoreKit leak. Three-tier model (free/premium/pilgrim) matches the spec.

**Localization is structurally sound.** `AnnoLocalizer` with 80+ key-value pairs covering all UI chrome. Vietnamese + English. No hardcoded strings in views. Production-ready for localization QA.

**SacredAtlasTheme is tasteful.** Ink (#1A140E), deepUmber (#21170E), parchment (#F0E0C2), antiqueGold (#C89235), oxblood (#6B1210). The `parchmentCard()` and `sacredGlass()` view modifiers are clean and reusable.

**Mock data is thoughtful.** Sources have confidence-specific reliability notes ("Official Roman liturgical reference; not a site archaeology source"). Events link to medieval/renaissance artwork with provenance. Multi-calendar notations on events. LA-area mock sites let the "Near You" flow work in previews.

**Privacy is baked in.** Privacy header in Pilgrim Mode, local-only disclaimer, no account assumption, location permission only on demand.

---

## What's Weak or Wrong

**MapKit integration is naive.** Standard `.mapStyle` with `.pointsOfInterest: .excludingAll` — MapKit doesn't let you theme beyond light/dark. The `mapMoodOverlay` (overlapping gradients + `.blendMode(.multiply)`) is a visual hack that also tints UI elements. A custom tile service or `.imagery` with darkened overlay is needed for the "dark sacred atlas" look.

**Mock data file is monolithic.** `MockSacredAtlasData.swift` is a 519-line extension with all locations, events, artworks, sources, route packs as static arrays in one file. Should be at least 3 files. The repository protocol means swapping is possible, but the mock IS the reference implementation and it's one massive file.

**Zero tests.** No test target in Package.swift. `SacredAtlasViewModel` has 358 lines of business logic (filtering, entitlement gating, journey state machine) with zero unit tests. The spec asked for "testable business logic."

**Tier boundary is muddy.** ImplementationNote recommends making pilgrim the annual tier's hero feature, but the code treats `premium` and `pilgrim` as separate exclusives. A `.premium` user cannot use pilgrim mode. Tiers should be cumulative or there should be a single annual tier.

**Mock data is too thin for the $69.99 story.** ~20 locations, ~15 events, ~5 route packs. The spec asked for a feature justifying $69.99/year. The mock is enough for a UI demo but doesn't prove the scale story. No pagination, region bucketing, or lazy loading is modeled.

**Map pins don't cluster.** MapKit's built-in `Annotation` system works for 20 pins. At 200+ it's unusably slow. Clustering isn't implemented. The spec didn't explicitly require it, but claiming production readiness for a "sacred atlas" with hundreds or thousands of sites requires it.

**Localization is a dictionary, not .strings files.** Xcode localization workflows require `.xcstrings`. The dictionary approach is a stub that would need replacement before shipping.

**Preview matrix is thin.** ImplementationNote claims previews for free/premium/pilgrim tiers, no-location-permission, active journey, Vietnamese UI — but `SacredAtlasPreviewMatrix.swift` and the `DemoApp` don't deliver this. One-off preview fixtures exist but aren't organized into the matrix the spec asked for.

**Map is centered on Los Angeles.** The mock LA locations make sense for preview, but the app's core value is Rome/Jerusalem/Santiago. A Rome-centered default would sell the product better in demo mode.

---

## Model Attribution

The codebase reads like an **o1-pro or Claude Opus** output — structurally competent, clean SwiftUI patterns, but with the characteristic thinness of a one-pass generation. The mocking strategy (static arrays, no SwiftData seeds) and the MapKit-naive dark overlay are hallmarks of an LLM that has read SwiftUI docs but hasn't shipped MapKit in production.

---

## If Building From This

1. Accept the architecture and folder structure as-is.
2. Replace mock data with real Anno data sources.
3. Replace MapKit annotations with `MKMapView` delegate clustering before adding >50 pins.
4. Replace the gradient overlay with either `.imagery` map + dark `MapPolyline`/`MapOverlay`, or custom tile server.
5. Add unit tests for `SacredAtlasViewModel.filteredLocations`, `isLocked`, and journey state transitions.
6. Replace `AnnoLocalizer` dictionary with Xcode `.xcstrings` files.
7. Add production `CLLocationManager` wrapper (mock returns hardcoded LA coordinate).
8. Merge premium/pilgrim into cumulative tiers.
9. Re-center default map region on Rome.
10. Implement pin clustering before claiming real data readiness.
