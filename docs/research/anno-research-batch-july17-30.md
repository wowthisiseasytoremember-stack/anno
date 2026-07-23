# Engine B — Batch Research Wrapper

**Purpose:** Generate multiple dates in sequence using the main research prompt.
**Usage:** Replace the date list below. Fire each date as a separate agent delegation with the main prompt as context.

## Batch: July 17-30, 2026

One entry per date. Each entry follows the `anno.mock.v1` schema from the main research prompt.

| # | Date | Weekday | Notes |
|---|------|---------|-------|
| 1 | 2026-07-17 | Friday | |
| 2 | 2026-07-18 | Saturday | |
| 3 | 2026-07-19 | Sunday | Liturgical anchor — Sunday is primary |
| 4 | 2026-07-20 | Monday | |
| 5 | 2026-07-21 | Tuesday | |
| 6 | 2026-07-22 | Wednesday | |
| 7 | 2026-07-23 | Thursday | |
| 8 | 2026-07-24 | Friday | |
| 9 | 2026-07-25 | Saturday | Feast of St. James the Apostle |
| 10 | 2026-07-26 | Sunday | Liturgical anchor |
| 11 | 2026-07-27 | Monday | |
| 12 | 2026-07-28 | Tuesday | |
| 13 | 2026-07-29 | Wednesday | Feast of Sts. Martha, Mary, and Lazarus |
| 14 | 2026-07-30 | Thursday | |

## Known Fixed Feasts in This Window

| Date | Feast | Rank | Source |
|------|-------|------|--------|
| Jul 22 | St. Mary Magdalene | Feast | https://www.catholicculture.org/culture/liturgicalyear/calendar/day.cfm?date=2026-07-22 |
| Jul 25 | St. James the Apostle | Feast | https://www.catholicculture.org/culture/liturgicalyear/calendar/day.cfm?date=2026-07-25 |
| Jul 26 | Sts. Joachim and Anne | Memorial | https://www.catholicculture.org/culture/liturgicalyear/calendar/day.cfm?date=2026-07-26 |
| Jul 29 | Sts. Martha, Mary, and Lazarus | Memorial | https://www.catholicculture.org/culture/liturgicalyear/calendar/day.cfm?date=2026-07-29 |
| Jul 30 | St. Peter Chrysologus | Optional Memorial | https://www.catholicculture.org/culture/liturgicalyear/calendar/day.cfm?date=2026-07-30 |
| Jul 31 | St. Ignatius of Loyola | Memorial | https://www.catholicculture.org/culture/liturgicalyear/calendar/day.cfm?date=2026-07-31 |

## Delegation Pattern

For each date, fire a subagent with:
1. The main research prompt as context (at `/tmp/anno-research-prompt-main.md`)
2. Goal: "Generate the anno.mock.v1 JSON for {{ DATE }} following the prompt rules exactly."
3. Verify: The returned JSON has all required fields, non-empty sources, and valid confidence labels.

## Output Accumulation

Collect each returned JSON into a single fixture file:
```json
{
  "schema_version": "anno.mock.v1",
  "generated_on": "2026-07-10",
  "entries": [
    ... collected entries here
  ]
}
```
