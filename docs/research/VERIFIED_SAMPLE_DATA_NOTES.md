# Verified Sample Data Notes

Updated: 2026-07-03

## Scope

This packet turns the current Anno Catholic-first direction into a mock-app-ready content slice:

- 14 dated entries from 2026-07-03 through 2026-07-16.
- A first-week subset from 2026-07-03 through 2026-07-09.
- English and Vietnamese display copy.
- Engine A calendar conversions copied from `data/calendar_2026_2029.jsonl`.
- Source URLs on every entry.

## Verification Standard

Each entry needs at least:

- One official or liturgical calendar source where available.
- One biography, encyclopedia, shrine, order, or museum source.
- Explicit confidence labels when geography, apparition narratives, commemoration rank, or artwork rights are not fully confirmed.

## Source Families Used

- USCCB daily readings and 2026 calendar.
- Vatican News and Vatican canonization pages.
- CatholicCulture calendar pages.
- New Advent Catholic Encyclopedia.
- Museum records from Met, Prado, Kroller-Muller, and Wikimedia/WGA where appropriate.
- Shrine or site pages for pilgrimage candidates.

## Editorial Risks To Preserve In UI

- July 5 and July 12 are Sundays. The liturgical day should be primary.
- July 7, July 8, and July 10 are better handled as historical/date saints rather than US General Calendar memorials.
- Saint Thomas in Chennai and Our Lady of Mount Carmel's 1251 scapular apparition should be tagged `traditional`, not flattened into `confirmed`.
- Saint Kateri content needs extra representation review before image selection or marketing copy.
- Modern Vatican News images are reference candidates unless rights are cleared.

## Highest-ROE Next Data Work

1. Replace every artwork candidate with a rights-cleared image asset or a deliberate placeholder.
2. Add one short source excerpt summary per source without copying long passages.
3. Add Vietnamese native editorial review notes to each entry.
4. Build a Swift model fixture from `anno_fortnight_2026-07-03_2026-07-16.json`.
