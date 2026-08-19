# Vietnamese Catholic Media Hub Monetization — Module Breakdown

**Source:** Operator research dump (`.codewhale/pastes/paste-2026-08-19-073637-b25348ad.md`)  
**Purpose:** High-level module index for comparison — NO implementation decisions yet

---

## Module Index

| Module | Description | Core Principle | Anno Relevance |
|--------|-------------|----------------|----------------|
| **M1: Affiliate Marketing** | Catholic retailers, pilgrimage tours, Amazon Associates, travel booking | Commission on things audience already buys; no content restriction | App Store metadata could link; website companion; pilgrimage routes in v2 |
| **M2: Own Digital Products** | Liturgical calendar (PDF/print), pilgrimage route guides, artwork prints, devotional ebooks | Sell what you created — highest margin, most dignified | Calendar = Sprint 6 deliverable; pilgrimage = Map tab v2; artwork = Design assets |
| **M3: Patronage/Membership** | Ko-fi, Patreon/Memberful tiers — free core, paid extras | "Support the hub" not "paywall content" | Supporter tier could fund ongoing content; parish partner tier for bulk |
| **M4: Ethical Sponsorship** | Mission-aligned sponsors only; fully disclosed; non-interruptive | Sponsorship around content, not paywalling content | Diocesan partnership; pilgrimage tour operators; local VI Catholic businesses |
| **M5: Grants/Institutional** | Catholic foundations (CCF OC, Knights of Columbus), NEH, OC Community Foundation | Frame as community resource + cultural preservation | Nonprofit path; grant writing for sustainability |
| **M6: Anti-Patterns (Avoid)** | Generic ad networks, paywalls on aggregated content, aggressive capture, data selling, theologically conflicting sponsors | Bright-line "what destroys trust" | Guardrails for any monetization decision |

---

## Quick Comparison Matrix

| Dimension | M1 Affiliate | M2 Own Products | M3 Patronage | M4 Sponsorship | M5 Grants | M6 Avoid |
|-----------|-------------|-----------------|--------------|----------------|-----------|----------|
| **Ethical Risk** | Low | None | Low | Medium (disclosure) | None | High |
| **Implementation Effort** | Low | Medium | Low | Medium | High | N/A |
| **Revenue Ceiling** | Medium | High | Medium | Medium | High (lump sum) | N/A |
| **Time to First $** | Fast | Medium | Fast | Medium | Slow | N/A |
| **Audience Alignment** | High (buys anyway) | High (fills gap) | High (cultural fit) | Medium (vetting) | N/A | N/A |
| **Anno Integration Point** | Pilgrimage routes, books | Calendar, art, guides | Supporter perks | Diocese, local biz | Nonprofit setup | Policy doc |
| **Legal/IP Complexity** | Low | You own IP | Low | Contracts | 501c3 filing | N/A |

---

## Anno-Specific Integration Notes

| Anno Asset | Monetization Module Match |
|------------|---------------------------|
| **Liturgical calendar (EN/VI)** | M2 — Primary product (PDF + print-on-demand + parish license) |
| **Pilgrimage routes (Map tab v2)** | M1 (affiliate tours) + M2 (route guides) + M4 (tour operator sponsors) |
| **Artwork/Design assets** | M2 — Prints, digital downloads, parish licensing |
| **Daily devotional content** | M3 — Supporter tier early access; M2 — compiled ebooks |
| **Vietnamese localization** | All modules — cultural specificity is the differentiator |
| **App Store presence** | M3 — "Supporter" IAP (StoreKit 2) for ad-free/early access; M2 — paid content packs |

---

## Suggested Sequence (from source)

1. **Immediate:** Ko-fi (M3) — zero overhead, culturally appropriate
2. **Sprint 6 / Launch:** Digital calendar (M2) — seasonal, original IP, natural launch moment
3. **Post-launch:** Pilgrimage tour affiliates (M1) — high value per referral
4. **Parallel:** Diocese of Orange / Catholic Foundation grants (M5) — community resource framing
5. **v2:** Membership tier (M3), sponsorships (M4), expanded product line (M2)

---

## Next Step

Say a module code (M1–M6) and what you want next — expand, filter, cross-reference with Anno roadmap, or delegate. No further work until then.