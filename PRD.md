# Anno — Product Requirements

**Reconciled:** 2026-10-03  
**Status:** current product authority together with `START_HERE.md` and `ROADMAP.md`.

## Product

Anno is a Catholic-first native iOS devotional and pilgrimage app.

The v1 product should make two behaviors excellent:

1. **Open Anno today** and receive a beautiful, sourced Catholic devotional experience.
2. **Go somewhere sacred** and have the iPhone make the pilgrimage meaningfully better.

The first physically testable pilgrimage exemplar is **Our Lady of La Vang — Orange County**.

## Audience

Primary launch wedge:

- Catholics who want useful daily devotional context.
- Southern California Catholics.
- Vietnamese-diaspora Catholic families and communities in Orange County.

The product should remain approachable to Catholics outside that audience without flattening the Vietnamese-Catholic specificity of the exemplar.

## V1 surfaces

### Today
- date / feast / liturgical rank
- sourced devotional context
- sacred artwork
- prayer
- sources and confidence
- rank-aware visual ceremony

### Calendar
- liturgical calendar browsing
- visibly differentiated Sundays, feasts, and solemnities
- graceful empty/unavailable states
- English-first with intentional Vietnamese treatment

### Map / Pilgrimage
- five flagship route packs
- Orange County / La Vang featured first
- route and station detail
- persistent visit progress
- manual **I'm Here**
- optional location-aware arrival
- native Apple Maps handoff
- completion keepsake and native sharing

## Orange County exemplar

Core geographic chapters:

1. Christ Cathedral / Our Lady of La Vang campus
   - Our Lady of La Vang Shrine
   - 117 Vietnamese Martyrs wall
   - Marian Gardens
2. St. Columban
3. Vietnamese Catholic Center
4. Our Lady of La Vang Catholic Church
5. St. Barbara

Product grammar:

**ARRIVE → LOOK → KNOW → PRAY → CONTINUE**

Narrative arc:

**Refuge → witness → survival → institution-building → living parish → inheritance**

Mary / La Vang is the thread through the route.

## Apple-native product advantage

Anno should not feel like a cross-platform web app wrapped for iPhone.

Use Apple-native capabilities where they improve:

**ARRIVE → SEE → PRAY → REMEMBER → SHARE**

Core/native direction:
- SwiftUI
- MapKit
- Core Haptics
- Core Location
- Spotlight
- App Intents / Shortcuts
- ShareLink / deep links
- WidgetKit / Lock Screen where validated
- ActivityKit / Dynamic Island where validated
- Apple Watch companion where validated
- Vision / VisionKit for sacred-camera experiences
- ARKit where physical-site conditions make it reliable
- QR / NFC, with beacons only at cooperating sites
- Image Playground / adaptive image glyphs for personal keepsakes, capability-gated

Guardrails:
- manual arrival never requires GPS
- no hidden always-on location history
- no spiritual score, XP, leaderboard, or gamified martyrdom
- generated imagery is never presented as historical evidence
- no framework exists merely to check a feature box

## Visual direction

**Quiet baseline + earned spectacle.**

- ordinary days: calm
- feasts: visibly ceremonial
- solemnities: rare, unmistakable spectacle
- major pilgrimage moments: obvious label + hierarchy + color + motion + haptic reinforcement

Design one notch more obvious than a design team would naturally choose when that materially improves comprehension, emotional payoff, or perceived value.

## Content / truth

- Engine A performs deterministic calendar math.
- Research/content may carry confidence and tradition labels.
- Do not turn devotional tradition into unsupported empirical certainty.
- Durable narrative and volatile practical data are separate.
- Mass/confession/tour/hours information should come from current official sources or be clearly marked for re-checking.
- Vietnamese exemplar copy requires human Vietnamese Catholic review before final release claims.

## Localization

- English is the primary product language.
- Vietnamese is a first-class authored surface where present.
- Vietnamese and English do not need literal line-for-line equivalence.
- Do not claim complete or reviewed Vietnamese coverage unless it is actually reviewed.

## Monetization

Current direction:
- **Free**
- **Premium — $49.99/year**

The old monthly/multi-tier/paywall architecture is not current authority.

If Premium ships in v1, build a small intentional StoreKit 2 annual purchase/restore flow. Do not restore old RevenueCat or mixed-tier code by default.

## Explicitly not current v1 authority

Historical assets may remain in the repo, but these are not active product scope merely because files exist:

- 72-sanctuary browsing UI
- broad 18-route runtime catalog
- spatial/geofenced audio product
- interfaith UI layer
- old SwiftData import architecture
- old Saved/spiritual-bouquet mock surface
- RevenueCat provider
- KJV-derived duplicate architecture
- turn-by-turn navigation
- social network / parish leaderboard / group platform

## V1 success

A new user should be able to:

- open Today and understand what matters today
- browse the Calendar without confusion
- discover the featured Orange County pilgrimage
- begin it without coaching
- understand why every stop belongs
- use the route with or without location permission
- experience meaningful Apple-native delight
- complete the route and want to share or recommend it

For current execution status, see `ROADMAP.md`.
