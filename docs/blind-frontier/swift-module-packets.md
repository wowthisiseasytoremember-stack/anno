# Blind Frontier Swift Module Packets

Updated: 2026-07-03

These packets are for blind agents that cannot inspect this repository. Each agent must return complete Swift files, preview/mock data, and integration notes. Do not ask agents to modify repo paths.

## Shared Contract For All Swift Modules

Allowed imports: `SwiftUI`, `Foundation`, `MapKit` only when map behavior is requested, `WidgetKit` only for widgets, `ActivityKit` only for Live Activity concepts.

Use these model stubs exactly in previews if needed:

```swift
struct AnnoEntry: Identifiable, Hashable {
    let id: String
    let date: String
    let weekday: String
    let liturgical: LiturgicalInfo
    let calendars: CalendarConversions
    let primary: PrimaryContent
    let place: SacredPlace?
    let artwork: ArtworkCandidate
    let sources: [SourceRef]
    let appHooks: AppHooks
}
struct LiturgicalInfo: Hashable { let rank: String; let color: String; let titleEn: String; let titleVi: String }
struct CalendarConversions: Hashable { let julian: String; let hebrew: String; let islamicUmmAlQura: String; let coptic: String; let ethiopian: String }
struct PrimaryContent: Hashable { let titleEn: String; let titleVi: String; let summaryEn: String; let summaryVi: String; let confidence: ConfidenceLevel; let confidenceNoteEn: String; let confidenceNoteVi: String }
struct SacredPlace: Hashable { let name: String; let latitude: Double; let longitude: Double; let confidence: ConfidenceLevel; let sourceUrl: String }
struct ArtworkCandidate: Hashable { let title: String; let maker: String; let dateLabel: String; let sourceUrl: String; let status: String }
struct SourceRef: Identifiable, Hashable { var id: String { url }; let label: String; let url: String; let type: String }
struct AppHooks: Hashable { let heroLineEn: String; let heroLineVi: String; let prayerPromptEn: String; let prayerPromptVi: String }
enum ConfidenceLevel: String, Hashable { case confirmed, traditional, disputed, contextual }
enum LanguageMode: String, CaseIterable, Identifiable { case english = "EN"; case vietnamese = "VI"; var id: String { rawValue } }
```

Design constraints: dark first, background `#13110E`, surface `#1F1B16`, accent `#C9A84C`, text `#EDE7DA`, secondary text `#9B9085`, divider `#2E2A24`. Use one accent color per screen. Body text must wrap and must not use fixed-height containers.

## Packet 1: Pilgrimage Map Module

Return files:

- `SacredSiteMapView.swift`
- `SacredSiteListView.swift`
- `SacredSiteDetailView.swift`

Entry point: `SacredSiteMapView(entries: [AnnoEntry], language: LanguageMode)`.

Requirements: MapKit pins only for `place != nil`; list fallback always present; pin detail shows entry title, place name, coordinates, place confidence, source URL, Apple Maps deep link, and a route teaser UI. Traditional/contextual places must not look as certain as confirmed places. Include previews with six sample pins and one no-place entry excluded.

## Packet 2: Source Confidence Module

Return files:

- `SourceSheet.swift`
- `SourceGroupView.swift`
- `SourceRow.swift`
- `ConfidenceExplanationView.swift`

Entry point: `SourceSheet(entry: AnnoEntry, language: LanguageMode)`.

Requirements: Group `sources` by `type`; show label, URL, type, confidence note, and open-link affordance. Include visual treatment for `confirmed`, `traditional`, `disputed`, and `contextual`. Source transparency must not be premium gated.

## Packet 3: Art Lightbox Module

Return files:

- `ArtLightboxView.swift`
- `ArtworkAttributionRow.swift`
- `ArtworkRightsBadge.swift`

Entry point: `ArtLightboxView(entry: AnnoEntry, language: LanguageMode)`.

Requirements: Placeholder-first gallery; no remote loading; attribution rows for title, maker, date, source URL; visible states for cleared, candidate pending clearance, reference-only, and placeholder-only. The UI must not imply uncleared art is bundled.

## Packet 4: Calendar Browser Module

Return files:

- `CalendarBrowserView.swift`
- `CalendarEntryRow.swift`
- `MonthGridView.swift`
- `WeekStripView.swift`

Entry point: `CalendarBrowserView(entries: [AnnoEntry], selectedID: Binding<String>, language: LanguageMode)`.

Requirements: Week and month modes; date selection; Sunday/liturgical anchor treatment; confidence visible in rows; July 5 renders as Fourteenth Sunday in Ordinary Time, not primarily a saint memorial.

## Packet 5: Paywall Stub Module

Return files:

- `ArchivePaywallView.swift`
- `ProductCopy.swift`
- `BenefitRow.swift`

Entry point: `ArchivePaywallView(language: LanguageMode)`.

Requirements: Static only, no StoreKit. Sell archive, art, audio, maps, saved collections, and expanded sources. Include restore/terms/privacy placeholders. Prohibit guilt copy, fake scarcity, spiritual-anxiety triggers, ads, Grace Tokens, and paid prayer outcomes.

## Packet 6: WidgetKit Concept Module

Return files:

- `AnnoTodayWidget.swift`
- `AnnoWidgetEntry.swift`
- `AnnoWidgetProvider.swift`

Entry point: Widget extension files only.

Requirements: Static fixture-style data; Today title, date, confidence, and short hero line; EN/VI structure noted but no shared app group required. Include target/capability notes and mark any needed Xcode setup explicitly.

## Packet 7: Live Activity / Alerts Concept Module

Return files only if feasible:

- `AnnoDailyActivityAttributes.swift`
- `AnnoDailyActivityView.swift`
- `DailyReminderNotificationPrototype.swift`

Requirements: Prototype files only; no project wiring. Use ActivityKit only for a time-bound daily reflection concept if technically coherent. Otherwise return local notification prototype and explain why Live Activity is not appropriate for a static daily entry.
