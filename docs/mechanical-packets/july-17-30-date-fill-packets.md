# July 17-30 Date Fill Packets

Updated: 2026-07-03

Use one packet per date. Each packet returns exactly one `anno.mock.v1` entry JSON object and a short `open_questions` array.

Shared constraints: Catholic-first; no unsourced factual claims; English and Vietnamese content fields; at least two sources, three preferred; confidence must be `confirmed`, `traditional`, or `disputed`; place may be `null`; artwork may be `placeholder_only` if rights are unclear.

Dates:

- 2026-07-17 Friday: return `anno-2026-07-17-{slug}`
- 2026-07-18 Saturday: return `anno-2026-07-18-{slug}`
- 2026-07-19 Sunday: return `anno-2026-07-19-{slug}` and treat Sunday as the liturgical anchor
- 2026-07-20 Monday: return `anno-2026-07-20-{slug}`
- 2026-07-21 Tuesday: return `anno-2026-07-21-{slug}`
- 2026-07-22 Wednesday: return `anno-2026-07-22-{slug}`
- 2026-07-23 Thursday: return `anno-2026-07-23-{slug}`
- 2026-07-24 Friday: return `anno-2026-07-24-{slug}`
- 2026-07-25 Saturday: return `anno-2026-07-25-{slug}`
- 2026-07-26 Sunday: return `anno-2026-07-26-{slug}` and treat Sunday as the liturgical anchor
- 2026-07-27 Monday: return `anno-2026-07-27-{slug}`
- 2026-07-28 Tuesday: return `anno-2026-07-28-{slug}`
- 2026-07-29 Wednesday: return `anno-2026-07-29-{slug}`
- 2026-07-30 Thursday: return `anno-2026-07-30-{slug}`

Output shape:

```json
{
  "entry": {},
  "open_questions": []
}
```
