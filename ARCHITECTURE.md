# Anno — Architecture

**Reconciled:** 2026-10-03  
**Authority:** current architecture for the active v1 target.

## System shape

Anno is a native SwiftUI iOS application fed by deterministic calendar data and structured devotional/pilgrimage resources.

### Engine A — deterministic calendar computation
- no LLM date math
- produces calendar/date context
- validated with Python tests
- sundown/time-sensitive presentation must use appropriate location/time context or a clearly labeled fallback

### Engine B — research/content pipeline
- structured research and source collection
- output is data, not runtime code
- uncertainty/tradition must remain representable
- user-facing narrative should not invent facts beyond the structured source material

### Native app

Generated from `Anno/project.yml`.

Active product surfaces:
- Today
- Calendar
- Map / Pilgrimage
- Settings / sources as supporting surfaces

The current app is fixture/data-driven. Historical duplicate SwiftData models and KJV-derived architectures are excluded from the active target rather than silently treated as canonical.

## Content resources

Primary devotional fixture:
`Anno/Resources/anno_unified_2026.json`

Flagship route manifest:
`Anno/Resources/flagship_routes_v1.json`

SoCal exemplar:
- `Anno/Resources/PilgrimageRoutes/socal_vietnamese_catholic_pilgrimage_la_vang.json`
- `Anno/Resources/socal_la_vang_exemplar_content_v1.json`
- `Anno/Resources/pilgrimage_moments_v1.json`
- `Anno/Resources/socal_la_vang_physical_markers_v1.json`

The SoCal route is seven spiritual stations grouped into five geographic chapters.

## Pilgrimage state

### Route content
Stable route/station identity and devotional content.

### Progress
`PilgrimageProgressStore` persists visited station IDs and completion locally.

### Active session
`PilgrimageSessionStore` tracks the active route, current station, and start time.

Ending an active session does **not** erase progress.

### Location awareness
`PilgrimageLocationService` is optional and chapter-level for the SoCal exemplar.

Manual **I'm Here** always remains available.

Inside Christ Cathedral, GPS is deliberately not asked to distinguish the Shrine, Martyrs Wall, and Marian Gardens. Exact precision belongs to QR/NFC/AR/Vision/manual selection.

## Deep-link contract

Canonical scheme:
`anno://`

Examples:
- `anno://pilgrimage/<route-id>/<station-id>`
- compact field markers: `anno://p/lv/1` through `anno://p/lv/7`

The same link model should be used by ShareLink, QR, NFC, Spotlight/system entry points, future Messages flows, and future beacon/physical-marker handoffs.

Do not create parallel navigation identity systems.

## Apple-native system surfaces

### Active/core code
- SwiftUI
- MapKit
- Core Haptics
- Core Location
- Spotlight
- deep links
- native sharing

### Staged until device/Xcode activation
Kept under `AppleSurfaces/` where appropriate:
- WidgetKit
- Live Activities / Dynamic Island
- Watch
- App Intents
- Vision/VisionKit
- ARKit
- Core NFC
- beacon monitoring
- Image Playground / adaptive glyph
- visionOS concepts

Staged source is not equivalent to shipped capability. Activate one target/capability at a time and validate on real hardware.

## Visual architecture

Shared visual primitives live under `Anno/Design/`.

Important concepts:
- semantic symbols
- semantic surfaces
- motion tokens
- `SacredIntensity`
- feast / solemnity ceremonial treatment
- Reduce Motion-aware transitions
- Core Haptics significance language

Product principle:

**quiet baseline + earned spectacle**

## Localization contract

English remains primary.

Vietnamese:
- is intentionally authored where supported
- may use independent phrasing/line breaks
- requires human Vietnamese Catholic review for the SoCal exemplar before final public claims

## Monetization boundary

Current direction:

**Free + Premium $49.99/year**

Old RevenueCat and mixed monthly/multi-tier code are not active architecture.

If monetization is activated, use a small StoreKit 2 purchase/restore boundary rather than restoring old paywall architecture wholesale.

## Privacy boundary

- location is optional
- no mandatory GPS proof
- no hidden location history
- camera/Vision should prefer on-device processing
- generated imagery requires explicit user intent/input
- motion/sensor data must not become a spiritual score
- do not make unsupported privacy claims in product metadata

## CI / validation

Cheap CI validates:
- Engine A
- Engine B
- normalization / route integrity
- SoCal exemplar alignment
- physical marker identities

Native macOS CI is intentionally manual/opt-in to preserve runner minutes.

Do not weaken strict concurrency or warnings-as-errors merely to make a native build pass.

## Deferred architecture

Historical data and code remain useful reference, but are not active runtime architecture:
- broad sanctuary browser
- 18-route runtime catalog
- spatial audio
- interfaith UI
- old SwiftData import layer
- old Saved/paywall surfaces
- KJV-derived duplicate service/model stack

Archive or reference these deliberately; do not revive them because a stale document mentions them.
