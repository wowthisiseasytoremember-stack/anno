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


## High-priority 2026 feast editorial contract (2026-11-06)

**Scope:** the four mandatory bilingual dates inside the Jul 3–Dec 31 normalized fixture: **Aug 15 (Assumption), Nov 22 (Christ the King), Dec 8 (Immaculate Conception), Dec 25 (Christmas)**. The four other designated 2026 feasts fall outside this fixture window.

- A native `AnnoEntry` combines liturgical identity, sourced primary devotional text, one optional sacred place, artwork candidate metadata, source references, and app hooks.
- **Canonical edit locations:** August source array `data/mock/anno_august_2026.json`; September–December research input `data/research_results/YYYY-MM-DD_result.json`; and any matching `_result_vi.json` language overlay.
- **Generated app fixture:** `Anno/Resources/anno_unified_2026.json`. Modify upstream first and regenerate; never make a fixture-only edit.
- Required feast dates must carry rank `Solemnity`, color `white`, correctly dated names, direct USCCB references, meaningful EN/VI summaries and hooks, and no EN fallback masquerading as VI translation.
- Source URLs and primary claims do not prove image rights. A `placeholder_only` artwork is **not** an approved asset. Keep art/title metadata and citation UI accessible, not hidden in a decoration.
- Liturgical rank/date is a documented fact; apparition narratives and traditional locations are not presented as empirically proven. Human Catholic theology and Vietnamese language sign-off remain required.
- Not a Snowfall/web editorial stack: the native UX owns VoiceOver, Dynamic Type, contrast, and preview performance.

### Single-file starter / offline checks

```bash
python3 tools/major_feast_editorial.py new --date 2027-01-06 --output /tmp/feast.json
python3 tools/normalize_fixture.py --year 2026
python3 tools/major_feast_editorial.py audit
python3 -m unittest discover -s tools -p 'test_major_feast_editorial.py' -v
```

The starter creates one **non-shipping** native-shape JSON record with `TODO` source-backed sections, artwork/license/alt slots and an editorial checklist under `_editorial`; clear all TODOs and remove `_editorial` before integration. It refuses to overwrite files. The `audit` and tests are stdlib Python, don't fetch URLs and run on Linux. They check authority dates, EN/VI presence and differences, official links, and upstream-to-fixture parity, but do not claim to have human-reviewed every historical sentence.

The full per-entry findings, claims requiring human review, and authority URLs are in `docs/MAJOR_FEAST_2026_EDITORIAL_AUDIT.md`.
