# Vietnamese Catholic Media Hub Monetization — Expanded Module Breakdown (Polish Pass)

**Source:** Operator research dump (third paste, 2026-08-19)  
**Purpose:** High-level module index for comparison — NO implementation decisions yet

---

## Module Index

| Module | Description | Core Innovation | Anno Relevance |
|--------|-------------|-----------------|----------------|
| **M1: In-App Browser as Asset** | WebView wrapper with persistent bottom bar (Save, Share, Prayer List, Reminders), cross-source watch history/resume, push notifications (free: 3/day, premium: unlimited) | Directory + analytics without rehosting; cross-platform resume = killer feature | Native iOS WKWebView + SwiftData for history; UserNotifications framework |
| **M2: Freemium Gating Refined** | Rolling window (today + 3 days free), feast-day free bursts (Tết, La Vang Aug 22, Martyrs Nov 24), preview + paid full (map thumb free → hi-res PDF paid) | Feels generous, monetizes depth, feast bursts drive signup surges | Calendar engine + date logic; StoreKit 2 subscription |
| **M3: Three-Tier Membership** | Free (Giáo dân), Supporter $3-5/mo (Ân nhân), Patron $15-25/mo (Đại ân nhân) — physical annual calendar mail-out for Patron | Physical premium makes 5x price feel worth it; culturally native calendar tradition | StoreKit 2 tiers; fulfillment for physical calendar |
| **M4: Physical Goods** | Annual liturgical wall calendar (lunar + solar), printed pilgrimage guidebooks (POD), holy/novena cards, art prints, sacramentals (rosaries via partner) | B2B parish bulk + B2C Tết gift market; POD = no inventory risk | Design assets; Printful/Printify/Lulu integration; parish wholesale |
| **M5: B2B / Institutional** | Parish licensing (embed calendar, bulk premium codes), Diocesan licensing (VCC endorsement), Religious order sponsorships, Catholic school licensing | $200-500/yr per institution scales faster than $3/mo individuals | Enterprise StoreKit / Apple Business Manager; diocesan relationships |
| **M6: Bulletin-Style Sponsorships** | Manually curated slots (funeral homes, restaurants, tax, immigration, dental, insurance), feast-day sponsorship ("presents today's feast"), section sponsorship (Archive) | Culturally native model — Little Saigon businesses expect this; not "ads" | Admin dashboard for sponsor management; non-programmatic |
| **M7: Affiliate — Expanded** | VI pilgrimage tour operators (5-10% of $2.5-5K tours), Knights of Columbus insurance, Catholic dating apps, VI Catholic publishers, online VI courses | High-ticket referrals (one tour = month's rent); mission-aligned | Web/Deep links; revenue tracking |
| **M8: Devotional Donations** | Annual fund drive (public radio model), memorial/intention offerings (centuries-old practice), digital candle/vigil lights | Non-classless, culturally resonant, recurring habit | StoreKit 2 consumable IAPs; intention submission flow |
| **M9: Grants (Free Money)** | Google Ad Grants ($10k/mo ads), OSV Institute, Catholic Extension, KofC, Lilly/GHR/Koch, VI community foundations | Requires nonprofit/fiscal sponsor; unlocks massive acquisition leverage | 501c3 or fiscal sponsor; grant writing |
| **M10: Ethical Data Insights** | Aggregate reports ("State of VI Catholic Media"), diocesan/religious order consulting ($75-150/hr), NEVER sell individual data | Authority positioning + revenue; bright line at individual data | Analytics pipeline; aggregate export; privacy policy |

---

## Quick Comparison Matrix

| Dimension | M1 Browser | M2 Gating | M3 Tiers | M4 Physical | M5 B2B | M6 Sponsors | M7 Affiliate | M8 Donations | M9 Grants | M10 Data |
|-----------|-----------|-----------|----------|-------------|--------|-------------|--------------|--------------|-----------|----------|
| **Ethical Risk** | None | Low | Low | None | Low | Low | Low | None | None | Medium* |
| **Dev Effort** | Medium | Medium | Medium | Low (POD) | High | Low | Low | Low | High | Medium |
| **Revenue Ceiling** | Medium (sticky) | High | High | Medium | **Highest** | Medium | High | Medium | High (lump) | Medium |
| **Time to First $** | Medium | Medium | Fast | Medium | Slow | Fast | Medium | Fast | Slow | Medium |
| **Cultural Fit** | High | High | High | **Highest** | High | **Highest** | High | **Highest** | Medium | Low |
| **Anno Sprint Match** | Sprint 1-2 | Sprint 3-4 | Sprint 6+ | Sprint 6+ | v2+ | Sprint 6+ | v2+ | Sprint 6+ | v2+ | v2+ |

*M10 = bright line: aggregate only, never individual

---

## Anno-Specific Integration Map

| Anno Feature | Monetization Modules Enabled |
|--------------|------------------------------|
| **WKWebView aggregator (Today/Calendar tabs)** | M1 (bottom bar, history, notifications) |
| **Calendar engine (4-year, EN/VI, lunar)** | M2 (rolling window), M4 (annual calendar), M5 (parish license) |
| **Map tab (pilgrimage routes v2)** | M1 (resume), M3 (Patron guides), M4 (guidebooks), M7 (tour affiliates) |
| **Artwork/Design system** | M3 (Supporter downloads), M4 (prints, cards), M6 (section sponsor) |
| **StoreKit 2 / SwiftData** | M2 (subscriptions), M3 (tiers), M8 (consumables) |
| **Vietnamese localization** | All — cultural specificity = differentiation |
| **Parish network (16+ in OC)** | M5 (B2B), M6 (bulletin sponsors), M4 (wholesale) |

---

## Suggested Build Order (from source)

1. **Sprint 1-2:** Free aggregator + WKWebView + tip jar (Ko-fi) + 1 pilgrimage affiliate (M1, M3, M7)
2. **Sprint 3-4:** Memorial/intention offerings + physical calendar preorder (M8, M4) — first real revenue
3. **Sprint 5-6:** Premium tier (Supporter/Patron) with maps/guides/artwork + cross-source resume (M3, M2)
4. **Sprint 6+:** 2-3 local Little Saigon sponsor slots (M6) — fills rent gap
5. **Post-launch:** Pitch VCC + Diocese for endorsement/licensing (M5)
6. **v2:** Nonprofit/fiscal sponsor → Google Ad Grants + grants (M9)
7. **v2+:** Scale to San Jose, Houston, DC-Metro, Atlanta, Dallas (M5 expansion)

---

## Ethics Test (from source — apply to any new idea)

1. **Would I be embarrassed to explain this to a priest or my grandmother?**
2. **Am I profiting from someone else's sacred content, or my own labor around it?**
3. **If my most vulnerable user (elderly, limited English/income) engaged, would they be better off?**

---

## Next Step

Say a module code (M1–M10) and what you want next — expand, filter, cross-reference with Anno sprints, or delegate. No further work until then.