## Localization Design Rules

- No visible UI chrome text may be baked into raster images.
- All buttons, tabs, chips, badges, sheet titles, settings labels, empty states, and paywall copy must come from localization keys.
- Event narratives, prayers, artwork metadata, and source titles remain English-only in v0.
- All date strings must use locale-aware formatting.
- Components should size to English strings as the max-width baseline.
- Vietnamese diacritics must render cleanly using system fonts.
- Runtime language switching must update visible UI without app restart.
- If a Vietnamese key is nil, fall back to English silently. Never show a blank label.
- Dynamic Type must be tested at every size step with all Vietnamese strings. No truncation.
