# Native iOS Build Tasks

Updated: 2026-07-03

This breaks Anno into agent-safe implementation slices. Each task has a bounded write scope so separate agents can work without trampling each other.

## Build Principle

Start with a local-data native shell before backend, auth, analytics, or subscriptions. The first success condition is simple: the app launches, decodes the verified fixture, displays the July 3-9 week in English and Vietnamese, shows confidence/source notes, and places map pins for entries with verified places.

## Task 1: Project Scaffold

Owner scope:

- `Anno.xcodeproj`
- `Anno/AnnoApp.swift`
- `Anno/RootView.swift`
- `Anno/Assets.xcassets`

Requirements:

- Create a SwiftUI iOS app named `Anno`.
- Minimum target: current stable iOS target chosen by Xcode defaults.
- Dark appearance first.
- No networking, accounts, analytics, or StoreKit yet.
- Root view has tab shell: Today, Calendar, Map, Saved.

Acceptance:

- App builds in Xcode.
- First screen is the usable Today tab, not a marketing page.

## Task 2: Data Models And Fixture Loading

Owner scope:

- `Anno/Models/AnnoEntry.swift`
- `Anno/Services/FixtureStore.swift`
- `Anno/Resources/anno_fortnight_2026-07-03_2026-07-16.json`
- `Anno/Resources/anno_week_2026-07-03_2026-07-09.json`

Inputs:

- `data/mock/anno_fortnight_2026-07-03_2026-07-16.json`
- `data/mock/anno_week_2026-07-03_2026-07-09.json`
- `docs/ANNO_CONTENT_SCHEMA.md`

Requirements:

- Decode with `JSONDecoder.keyDecodingStrategy = .convertFromSnakeCase`.
- Preserve optional `place`.
- Preserve `confidence` and `confidence_note_*`.
- Expose `weekEntries` in the order from `entry_ids`.

Acceptance:

- Unit test proves 14 fortnight entries and 7 week entries decode.
- July 3 title is Saint Thomas in EN and VI.

## Task 3: Localization Bridge

Owner scope:

- `Anno/Localization/LanguageMode.swift`
- `Anno/Localization/LocalizedEntryText.swift`
- `Anno/Resources/Localizable.xcstrings`

Inputs:

- `data/localization/vi_terms.json`
- `localization/vi/Localizable.strings`

Requirements:

- Add EN/VI toggle.
- Use `*_vi` content fields when Vietnamese mode is selected.
- Text must wrap without clipping.
- Keep proper names readable; do not auto-translate source URLs or artwork titles unless data provides translated copy.

Acceptance:

- July 6 renders Vietnamese title, hero line, summary, prayer prompt, and confidence note.
- Long Vietnamese text does not clip on iPhone SE width.

## Task 4: Today Screen

Owner scope:

- `Anno/Today/TodayView.swift`
- `Anno/Today/ArtworkCandidateView.swift`
- `Anno/Today/ConfidenceBadge.swift`
- `Anno/Today/CalendarConversionGrid.swift`

Requirements:

- Use Anno brand palette from `docs/BRAND_VISUAL_ADDENDUM.md`.
- Use one accent color per screen; Today defaults to gold.
- Show date, title, hero line, liturgical card, artwork candidate placeholder, confidence badge, summary, place row, prayer prompt, source-confidence note, and calendar conversions.
- Preserve traditional/contextual/confirmed differences visibly.

Acceptance:

- Matches the information hierarchy in `visuals/anno-real-week-mock.html`.
- No fixed-height body text.

## Task 5: Calendar Week Screen

Owner scope:

- `Anno/Calendar/WeekCalendarView.swift`
- `Anno/Calendar/EntryListRow.swift`

Requirements:

- Show the verified July 3-9 week.
- Selecting a day updates the Today detail.
- Sunday entries are visually distinguished as liturgical anchors.
- Confidence labels visible in rows.

Acceptance:

- All seven week entries selectable.
- July 5 shows as Fourteenth Sunday in Ordinary Time, not primarily as a saint memorial.

## Task 6: Map Screen

Owner scope:

- `Anno/Map/SacredSiteMapView.swift`
- `Anno/Map/SacredSiteListView.swift`

Requirements:

- Use MapKit.
- Add pins only for entries where `place != nil`.
- Pin detail shows entry title, place name, coordinates, and place confidence.
- If MapKit preview is unavailable, a list fallback must still show coordinates.

Acceptance:

- Week map has six pins; July 5 is excluded because it has no fixed place.
- Traditional/contextual pins are not styled as confirmed.

## Task 7: Source Sheet

Owner scope:

- `Anno/Sources/SourceSheet.swift`
- `Anno/Sources/SourceRow.swift`

Requirements:

- Show source label, type, URL, and open-in-browser affordance.
- Show primary confidence note.
- Group sources by type when possible.

Acceptance:

- July 3 shows USCCB, Vatican News, and CatholicCulture.
- Source transparency is available without premium gating.

## Task 8: Paywall Stub

Owner scope:

- `Anno/Paywall/ArchivePaywallView.swift`
- `Anno/Paywall/ProductCopy.swift`

Inputs:

- `docs/MONETIZATION_PAYWALL_SYSTEM.md`
- `docs/PRIVACY_MONETIZATION_TRUST_SPEC.md`

Requirements:

- Static paywall only; no StoreKit integration in this task.
- Copy sells archive, art, maps, audio, and saved collections.
- Include restore/terms/privacy placeholders.
- No guilt copy, fake scarcity, Grace Tokens, ads, or spiritual-anxiety triggers.

Acceptance:

- Paywall can be presented from archive/map/save attempts.
- Today content remains accessible without paywall.

## Task 9: Preview And Snapshot Pack

Owner scope:

- `Anno/Preview Content/`
- `docs/IOS_PREVIEW_CHECKLIST.md`

Requirements:

- Add SwiftUI previews for EN and VI.
- Include small-screen and large-screen preview notes.
- Capture screenshots for Today EN, Today VI, Week, Map, and Source Sheet.

Acceptance:

- Screenshots prove text is not clipped and source/confidence surfaces are visible.

## Agent Assignment Notes

- Do not let any task introduce networking unless explicitly asked.
- Do not rename Anno.
- Do not introduce custom fonts before an accessibility audit.
- Do not remove confidence labels to make UI simpler.
- Do not turn the app into a landing page.
- Preserve the data model; if a field feels inconvenient, adapt the view, not the truth.
