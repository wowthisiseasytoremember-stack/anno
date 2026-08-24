# Monetization Module — Versioned Index

**Purpose:** All 17 revenue modules (M1-M17) with specs, launch sequence, and cross-references.

---

## Versioned Files

| Version | File | Description |
|---------|------|-------------|
| **v1** | `architecture_polished_pass.md` | Full architecture doc (paste-2026-08-19-074607) — 3-layer foundation, 17 modules A-G, revenue projection, launch sequence |
| **v1** | `roe_ranking_doc.md` | ROE ranking doc (paste-2026-08-19-074908) — ranked assets, deliverables, decision framework |
| **v1** | `basic_index.md` | First decomposition: 6 modules (M1-M6: affiliate, own products, patronage, sponsorship, grants, avoid) |
| **v1** | `expanded_index.md` | Second decomposition: 10 modules (M1-M10: browser, gating, tiers, physical, B2B, sponsors, affiliate+, donations, grants, data) |
| **v2** | `architecture_17_modules.md` | Synthesized 17-module index with comparison matrix, Anno integration map, revenue projection, launch sequence, ethics test |
| **v2** | `decomposition_vs_prior.md` | Cross-ref: what's new (7 modules), expanded (6), merged/split (4) vs v1 indexes |
| **v2** | `sprint_mapping.md` | Each module mapped to Anno sprints — actionable now vs needs app vs needs v2 |
| **v3** | `roe_decomposition.md` | ROE doc decomposed against 17-module architecture — ranking, new actionable items, calendar spec additions |
| **v3** | `calendar_spec_grant_decomposition.md` | Calendar spec + grant draft decomposed — M1, M3, M8, M12, M13, M14, M15 now build-ready |

---

## Module Quick Reference (M1-M17)

| Code | Module | Sprint | Build-Ready? | Key v3 Additions |
|------|--------|--------|--------------|------------------|
| **M1** | Liturgical Calendar (Freemium) | 3-6 | 🟢 **Yes** | Full spec in calendar_content/ |
| **M2** | Pilgrimage Route Guides | v2+ | 🟡 Content-ready | — |
| **M3** | Artwork Multi-Stream | 1-2, 6+ | 🟢 **Yes** | Daily showcase + print specs + gift tier |
| **M4** | Prayer/Devotional Products | v2+ | 🟡 Content-ready | — |
| **M5** | Contextual Affiliate Links | 3+ | 🟡 When content exists | Content calendar alignment |
| **M6** | Pilgrimage Tour Referrals | v2+ | 🟢 **Outreach ready** | Email + 1-pager in ROE doc |
| **M7** | Browser Analytics (Aggregate) | 1-2, 6+ | 🟡 Needs app | Consulting model, specific buyers |
| **M8** | Premium App Features | 3-6 | 🟢 **Paywall UX done** | 7-layer split, "$1/mo" framing |
| **M9** | VI Business Directory | 6+ | 🟡 Needs app | Parish list + protocol |
| **M10** | Event Promotion | 6+ | 🟡 Needs app | Content calendar |
| **M11** | Prayer Intention Board | 6+ | 🟡 Needs app | Layer 4/6 integration |
| **M12** | Liturgical Season Sponsorships | 6+ | 🟢 **Prospectus ready** | 52-week content calendar |
| **M13** | Underwriting (NPR Model) | 6+ | 🟢 **Prospectus ready** | Same as M12 |
| **M14** | Grants (3 Framings) | v2+ | 🟢 **CCC draft ready** | Full narrative + VCC letter strategy |
| **M15** | Diocese Partnership | 4-6 | 🟢 **Protocol ready** | Warm intro → gift → wait → they ask |
| **M16** | Calendar Data Licensing | v2+ | 🟡 Needs dataset | Moat validated |
| **M17** | White-Label Platform | v2+ | 🟡 Needs v2 | Calendar infrastructure |

---

## Entry Points for Workers

| Task | Worker Type | Input Files |
|------|-------------|-------------|
| Build browser analytics service (M7) | `deepseek-worker` | v2/architecture_17_modules.md (M7), v3/calendar_spec_grant_decomposition.md (Layer 5) |
| Scaffold sponsor/underwriter CRM | `deepseek-worker` | v2/architecture_17_modules.md (M12/M13), v3/roe_decomposition.md (prospectus) |
| Build affiliate link tracker | `yolo-worker` | v1/architecture_polished_pass.md (B-1 table), v2/sprint_mapping.md |
| Grant application boilerplate generator | `yolo-worker` | v3/calendar_spec_grant_decomposition.md (CCC draft) |