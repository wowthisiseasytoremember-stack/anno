# Monetization Architecture — Decomposition Against Existing Indexes

**Source:** `.codewhale/pastes/paste-2026-08-19-074607-2a498568.md` (new)  
**Against:**
- `monetization_module_index.md` (M1-M6 — basics)
- `monetization_expanded_module_index.md` (M1-M10 — polish pass)
- `vietnamese_media_module_index.md` (M1-M10 — media sources, not monetization)

---

## Module Cross-Reference

| New Module | Matches Existing | Notes |
|------------|------------------|-------|
| **M1: Liturgical Calendar (Freemium)** | `expanded:M2` (Freemium Gating), `basic:M2` (Own Products) | More detailed: annual pricing, parish bulk, PDF print, push alerts |
| **M2: Pilgrimage Route Guides** | `expanded:M4` (Physical Goods - guidebooks), `basic:M1` (Affiliate tours) | Adds tiered: free sample → individual → bundle → custom consult |
| **M3: Artwork Multi-Stream** | `expanded:M3` (Tiers - Patron physical), `basic:M2` (Own Products) | **Major expansion:** 6 formats from one asset (digital, POD, bundles, parish license, wallpapers, bulletin license) |
| **M4: Prayer/Devotional Products** | — | **New:** prayer guide, sacramental prep, coloring pages, holy cards — all VI-specific gaps |
| **M5: Contextual Affiliate Links** | `expanded:M7` (Affiliate Expanded), `basic:M1` (Affiliate) | Adds specific content→affiliate mapping table |
| **M6: Pilgrimage Tour Referrals** | `expanded:M7` (Affiliate - high-ticket), `basic:M1` | Dedicated section: 3-5% of $3-8K tours; direct operator negotiation |
| **M7: Browser Analytics (Aggregate)** | `expanded:M1` (In-App Browser as Asset), `expanded:M10` (Ethical Data) | **Refined:** consulting model (not data sale); diocese/publishers/tour operators as buyers |
| **M8: Premium App Features** | `expanded:M2` (Freemium Gating), `expanded:M3` (Tiers) | Feature table tied to browser capabilities; $2-4/mo price point |
| **M9: VI Business Directory** | — | **New:** "Catholic Yellow Pages" for Westminster/OC; free basic + enhanced tiers |
| **M10: Event Promotion** | — | **New:** Community calendar with featured/push tiers |
| **M11: Prayer Intention Board** | `expanded:M8` (Devotional Donations) | **Refined:** cultural framing (offerings at shrines); optional $1-5; high frequency |
| **M12: Liturgical Season Sponsorships** | `expanded:M6` (Bulletin Sponsors) | **Refined:** per-season ($200-500), prestige not ads, static acknowledgment |
| **M13: Underwriting** | `expanded:M6` (related) | **New model:** NPR/PBS style factual acknowledgments; $100-250/mo |
| **M14: Grants (3 Framings)** | `expanded:M9` (Grants), `basic:M5` | **Expanded:** 3 distinct framings (Catholic media, VI cultural preservation, immigrant digital access) |
| **M15: Diocese Partnership** | `expanded:M5` (B2B/Institutional) | **Specific:** VCC OC direct conversation; 4 concrete outcomes |
| **M16: Calendar Data Licensing** | `expanded:M5` (B2B licensing) | **Specific:** API to Hallow/Laudate/iBreviary; $500-2K/yr |
| **M17: White-Label Platform** | `expanded:M5` (B2B scaling) | **Specific:** Multi-tenant for San Jose, Houston, DC, Atlanta, Dallas |

---

## What's **New** in Architecture Doc (Not in Either Existing Index)

| Module | Why It's New |
|--------|--------------|
| **M4: Prayer/Devotional Products** | Entire category missing — VI prayer guide, sacramental prep, coloring, holy cards |
| **M9: Business Directory** | Community directory model — not in either index |
| **M10: Event Promotion** | Community calendar monetization — not in either index |
| **M13: Underwriting** | NPR/PBS model distinct from sponsorship — not in either index |
| **M15: Diocese Partnership** | Concrete conversation strategy with 4 outcomes — `expanded:M5` only had "pitch VCC" |
| **M16: Calendar Data Licensing** | Specific licensees (Hallow, Laudate, iBreviary) and pricing — `expanded:M5` was generic |
| **M17: White-Label** | Specific target dioceses and pricing — `expanded:M5` was generic "scale to other cities" |

---

## What's **Expanded Significantly** vs. Existing Indexes

| Module | Basic Index | Expanded Index | Architecture Doc Adds |
|--------|-------------|----------------|----------------------|
| **M3: Artwork** | "Artwork prints" (one line) | "Physical Goods" includes prints | **6 revenue formats from one asset**, POD zero-inventory, bulletin license ($25-50/yr) |
| **M6: Tour Referrals** | "Pilgrimage tour affiliates" | "VI pilgrimage tour operators" | **Direct operator negotiation**, 3-5% of $3-8K, group departure organizer model (10-15%) |
| **M7: Analytics** | Browser + analytics | Browser + cross-source resume | **Consulting model** (not data sale), specific buyers (diocese, publishers, tour ops), ethical guardrails |
| **M11: Prayer Board** | "Donations: memorial/intention" | "Devotional Donations: digital candle/vigil" | **Cultural framing** (offerings at shrines), $1-5 optional, frequency math ($600/mo at 20/day) |
| **M12: Sponsorships** | "Bulletin-style sponsors" | "Bulletin-Style Sponsorships" | **Per liturgical season** ($200-500), prestige association, not programmatic |
| **M14: Grants** | "Grants: Google Ad Grants, OSV, etc." | "Grants: Google Ad Grants, OSV, KofC, Lilly" | **3 framings** with specific sources per framing; cultural preservation = strongest |

---

## What's **In Existing Indexes But Not in Architecture Doc**

| Existing Module | In Basic? | In Expanded? | Status |
|-----------------|-----------|--------------|--------|
| `basic:M3` Patronage/Membership (Ko-fi, Patreon tiers) | ✅ | — | **Merged into M11 (Ko-fi) + M8 (Premium tiers)** — not separate |
| `basic:M4` Ethical Sponsorship (mission-aligned) | ✅ | — | **Split into M12 (season) + M13 (underwriting)** — more specific |
| `expanded:M1` In-App Browser (bottom bar, history, resume) | — | ✅ | **Split into M7 (analytics) + M8 (premium features)** — separated concerns |
| `expanded:M5` B2B/Institutional (parish, diocesan, school licensing) | — | ✅ | **Split into M1 (parish calendar license) + M15 (diocese) + M16 (API) + M17 (white-label)** |
| `expanded:M10` Ethical Data Insights (aggregate reports, consulting) | — | ✅ | **→ M7** (analytics consulting) — same concept |

---

## Vietnamese Media Index — No Monetization Overlap

The `vietnamese_media_module_index.md` is **source classification** (M1-M10: streaming, radio, parish, official, diaspora, etc.), not monetization. It feeds Engine B source allowlist.

**Connection point:** Architecture doc's M7 (analytics) tracks which media sources (from VI media index) get most engagement → informs M5/M6 affiliate priorities and M12/M13 sponsor pitches.

---

## Summary: Net Module Count

| Index | Modules | Notes |
|-------|---------|-------|
| Basic (`monetization_module_index.md`) | 6 (M1-M6) | High-level categories |
| Expanded (`monetization_expanded_module_index.md`) | 10 (M1-M10) | Sprint-mapped, product-focused |
| **Architecture Doc (new)** | **17 (M1-M17)** | **Most granular; revenue-modeled; launch-sequenced** |

**Architecture doc = supersedes both for monetization planning.** It decomposes the expanded index's M1-M10 into 17 specific revenue streams with pricing, timing, and dependencies.

---

## Ready for Next Comparison

When you send the next doc, I'll diff it against this 17-module architecture baseline.