# Engine B — August 2026: Catholic Liturgical Calendar

You are Engine B of Anno. Produce a JSON array containing one structured entry for each day of August 2026 (ordered sequentially from day 1 to the end of the month). Research each day's Roman Rite Catholic liturgical significance (saint, feast, Sunday theme, or feria) based on the General Roman Calendar and the specific liturgical year cycle applicable to 2026, then output a structured entry following the schema below.

## Execution Requirements

- **Dynamic Dates:** Process all dates for August 2026.
- **Determine the Liturgical Context:** Check the calendar cycle for 2026 (e.g., Sunday Cycle A/B/C, Weekday Cycle I/II) to ensure Sunday themes, scriptural references, and movable feasts align accurately.
- **Establish Day Ranks:** Dynamically sort and research the days based on their highest liturgical precedence:
  - Sundays
  - Solemnities & Major Feasts
  - Obligatory Memorials
  - Optional Memorials
  - Ferias (Weekdays)

## Schema (exact — used for every entry)

```json
{
  "id": "anno-2026-08-DD",
  "date": "2026-08-DD",
  "weekday": "Monday/Tuesday/...",
  "mock_priority": "engine_b_v1",
  "liturgical": {
    "rank": "Solemnity | Feast | Memorial | Optional Memorial | Sunday | Feria",
    "color": "white | red | green | purple | rose",
    "title_en": "Full liturgical title in English",
    "title_vi": ""
  },
  "primary": {
    "type": "saint | feast | solemnity | liturgical_day",
    "title_en": "Subject name/title",
    "title_vi": "",
    "summary_en": "2-4 sentence summary of the day's significance",
    "summary_vi": "",
    "body_en": "Content depth varies by rank. Solemnity/Feast/Sunday: 3-5 paragraphs (300-1000 chars). Memorial: 2-3 paragraphs (200-500 chars). Feria: 1-2 paragraphs (100-300 chars on the season/readings).",
    "body_vi": "",
    "confidence": "confirmed",
    "confidence_note_en": "Brief explanation of source confidence",
    "confidence_note_vi": ""
  },
  "place": {
    "name": "Associated location or null",
    "latitude": null or float,
    "longitude": null or float,
    "confidence": "confirmed | traditional | disputed",
    "source_url": "URL for location claim"
  },
  "artwork": {
    "title": "Title of public domain artwork",
    "maker": "Artist name or null",
    "date_label": "Century/year",
    "source_url": "Wikimedia Commons URL or null",
    "status": "placeholder_only"
  },
  "sources": [
    {"label": "Short label", "url": "https://verifiable-url", "type": "encyclopedia | liturgical_calendar | vatican | academic"}
  ],
  "app_hooks": {
    "hero_line_en": "One compelling card header line capturing the day",
    "hero_line_vi": "",
    "prayer_prompt_en": "Brief prayer or reflection prompt",
    "prayer_prompt_vi": ""
  }
}
```

## Scaling Rules (match depth to rank)

| Rank | Body length | Sources | Place | Artwork |
|------|------------|---------|-------|---------|
| Solemnity | 500-1200 chars | 2-3 | Yes | Yes |
| Feast | 400-800 chars | 2-3 | Yes | Yes |
| Sunday | 300-700 chars | 1-2 | No/null | Optional |
| Memorial | 200-500 chars | 1-2 | Optional | Optional |
| Optional Memorial | 150-400 chars | 1 | Optional | Optional/null |
| Feria | 100-300 chars | 0-1 | null | null |

## Prompt Rules

1. **Language:** English only — all Vietnamese (`_vi`) string fields must be set to `""`.
2. **Verification:** Use real, verifiable URLs only (e.g., newadvent.org, catholicculture.org, vatican.va, usccb.org). Do not fabricate historical facts, dates, or source links.
3. **Ferias:** For plain weekdays lacking a major saint, focus the body text on a seasonal or scriptural reflection tied to the day's standard Mass readings.
4. **Coordinates:** Provide real coordinates or null. For saints, traditional burial sites or shrines are acceptable at `traditional` confidence.
5. **Output Format:** Output a single, clean JSON array containing all processed days in ascending order. Do not wrap the JSON in conversational prose.
6. **No calendar conversions:** Do not include calendar conversions (Julian, Hebrew, Islamic, Coptic, Ethiopian) — those are handled separately.
