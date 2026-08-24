# Calendar Content Module — Versioned Index

**Purpose:** All specs, schemas, and production assets for the Vietnamese Catholic liturgical calendar (core product M1).

---

## Versioned Files

| Version | File | Description |
|---------|------|-------------|
| **v1** | `calendar_spec_full.md` | Full calendar spec + grant draft (paste-2026-08-19-075412) — 7-layer architecture, physical production, editorial standards, paywall UX, production calendar |
| **v1** | `roe_calendar_sections.md` | ROE ranking doc calendar-relevant sections (paste-2026-08-19-074908) — B2B parish focus, dataset spec, pricing model |
| **v2** | `decomposition.md` | Cross-ref against monetization architecture — what's new, expanded, build-ready modules, content workload, agent-vs-human split |
| **v3** | *(future)* | Database schema, moveable feast calculator, production tracker CSV, Layer 3 draft bios |

---

## Module Quick Reference (from spec)

| Layer | Name | Free/Paid | Content |
|-------|------|-----------|---------|
| **1** | The Glance | Free | Lock screen / notification: date, feast, color, 1 verse |
| **2** | The Open | Free | App open screen: artwork, date, feast, color, verse, Mass link, "See more" |
| **3** | The Depth | Paid | Saint bio / feast context (150-250 words bilingual) |
| **4** | The Practice | Paid | Prayer + actionable practice + additional devotions |
| **5** | The Connection | Paid | Mass streams, readings, artwork download/buy, pilgrimage links, hymns |
| **6** | The Culture | Paid | VI Catholic cultural note (parish, history, diaspora resonance) |
| **7** | The Arc | Paid | Liturgical narrative: where today sits in season story |

---

## Production Workload

| Content Type | Count | Reusable | Agent Can Draft? |
|--------------|-------|----------|------------------|
| Fixed feast days | ~180 | Annual | Layer 3 only |
| Moveable feasts | ~25 | 3-year cycle | Layer 3 only |
| Ordinary Time weekdays | ~160 | 3-year cycle | Layer 3 only |
| Culture notes (L6) | ~52 | Evergreen | **No** — human only |
| Arc notes (L7) | ~40 | Seasonal | **No** — human only |
| **Year 1 Total** | **~460** | | |
| **Year 2+** | **~30-50** | | |

---

## Entry Points for Workers

| Task | Worker Type | Input Files |
|------|-------------|-------------|
| Scaffold DB schema + moveable feast calculator | `deepseek-worker` | v1/calendar_spec_full.md (layers), v2/decomposition.md (workload) |
| Generate Layer 3 first-draft bios (180 fixed) | `deepseek-worker` | v1/calendar_spec_full.md (Layer 3 examples), AnnoEntry.swift |
| Build production tracker CSV (460 rows) | `yolo-worker` | v2/decomposition.md (production calendar table) |
| Extract moveable feast algorithm | `deepseek-worker` | v1/calendar_spec_full.md (algorithm notes) |