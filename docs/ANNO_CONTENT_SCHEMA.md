# Anno Content Schema

Updated: 2026-07-03

## Purpose

This schema describes the mock content shape used by `data/mock/anno_fortnight_2026-07-03_2026-07-16.json`. It is intentionally close to SwiftUI app needs: one dated entry can power the Today screen, calendar list, map pin, source sheet, Vietnamese toggle, and premium art/audio gates.

## Top-Level Fixture

```json
{
  "schema_version": "anno.mock.v1",
  "generated_on": "2026-07-03",
  "source_window": {},
  "editorial_policy": {},
  "entries": []
}
```

## Entry

Required fields:

| Field | Type | Use |
|---|---:|---|
| `id` | string | Stable app/content identifier |
| `date` | `YYYY-MM-DD` | Gregorian date key |
| `weekday` | string | English weekday display/fallback |
| `mock_priority` | string | `week_real_data` or `fortnight_extension` |
| `liturgical` | object | Rank, color, bilingual liturgical title |
| `calendars` | object | Engine A calendar conversions |
| `primary` | object | Main saint/day/history content |
| `place` | object/null | Sacred site or null when no fixed site is verified |
| `artwork` | object | Provenance candidate, not necessarily a licensed asset |
| `sources` | array | Source URLs and types |
| `app_hooks` | object | Short bilingual lines for UI surfaces |

## Confidence Contract

Use confidence in the UI, not only the data model:

- `confirmed`: liturgical rank, canonization, museum record, shrine identity, or well-sourced historical fact.
- `traditional`: devotional tradition, apparition narrative, traditional tomb/martyrdom site, or approximate Gospel geography.
- `disputed`: conflicting claims or insufficient evidence. Avoid for v1 mocks unless the uncertainty is valuable.
- `contextual`: useful map anchor but not the exact place of the event.

## Swift Model Mapping

Suggested native types:

```swift
struct AnnoFixture: Codable {
    let schemaVersion: String
    let generatedOn: String
    let entries: [AnnoEntry]
}

struct AnnoEntry: Codable, Identifiable {
    let id: String
    let date: String
    let weekday: String
    let mockPriority: String
    let liturgical: LiturgicalInfo
    let calendars: CalendarConversions
    let primary: PrimaryContent
    let place: SacredPlace?
    let artwork: ArtworkCandidate
    let sources: [SourceRef]
    let appHooks: AppHooks
}
```

Swift should decode snake_case with `JSONDecoder.keyDecodingStrategy = .convertFromSnakeCase`.

## Rendering Rules

- Today screen title: `primary.title_*`.
- Liturgical chip: `liturgical.rank` + `liturgical.title_*`.
- Confidence pill: `primary.confidence`.
- Map tab: include entries where `place != null`.
- Source sheet: group `sources` by `type`.
- Vietnamese mode: use `*_vi` fields first; fall back to English only when a field is missing.
- Premium gates: gate high-res artwork and audio, not basic daily text or source transparency.

## Do Not Flatten

Do not merge `confidence_note_*` into the summary. The note belongs in a source/confidence sheet, because it is exactly the kind of scholarly honesty that differentiates Anno from generic devotional apps.
