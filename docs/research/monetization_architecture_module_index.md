# Monetization Architecture — Module Index (Polished Pass)

**Source:** Operator monetization architecture document (`.codewhale/pastes/paste-2026-08-19-074607-2a498568.md`)  
**Purpose:** High-level module index for comparison — NO implementation decisions yet

---

## Three-Layer Foundation (From Source)

| Layer | Description | Revenue Logic | Anno Mapping |
|-------|-------------|---------------|--------------|
| **Layer 1: Free Aggregator** | Official links to others' content (YouTube, parish streams, Vatican feeds) in in-app browser. Free forever. Traffic engine. | Indirect: analytics, audience size, attention for Layer 2/3 | Sprint 1-2: WKWebView aggregator; `BrowserAnalytics` service |
| **Layer 2: Rehosted Free/CC Archive** | Free/CC content collected, organized, searchable. Free to user. Builds authority & engagement. | Indirect: reputation, engagement depth, data for Layer 3 | Sprint 3-4: Content pipeline for Engine B sources |
| **Layer 3: Original Work** | Calendars, pilgrimage routes, artwork, guides — freemium. Sample free, rest paid. Direct revenue. | Direct: subscriptions, product sales, licensing | Sprint 5-6+: Premium tier, StoreKit 2, product catalog |

---

## Module Index

| Module | Description | Core Innovation | Anno Sprint Match | Revenue Type |
|--------|-------------|-----------------|-------------------|--------------|
| **M1: Liturgical Calendar (Freemium)** | Today's date free; full year, PDF print, push alerts, parish sync paid ($8-15/yr) | Annual product cycle; parish bulk license ($75-150/yr) | Sprint 3-4 (calendar engine), Sprint 6 (premium) | Direct Product (A-1) |
| **M2: Pilgrimage Route Guides** | Free sample route; individual guides $10-20; bundle $40-60; custom consult $150-500 | Tiered: free sample → individual → bundle → service | v2 (Map tab), Sprint 6+ (premium) | Direct Product (A-2) |
| **M3: Artwork Multi-Stream** | One asset → digital download ($5-12), POD prints ($20-45), season bundles ($25-40), parish license ($50-100/yr), wallpapers ($3-5), bulletin license ($25-50/yr) | Single asset, 6+ revenue formats, zero inventory via POD | Sprint 1-2 (Design system), Sprint 6+ (catalog) | Direct Product (A-3) |
| **M4: Prayer/Devotional Products** | Vietnamese prayer guide ($8-15 digital, $18-25 print), sacramental prep guides ($10-15 family / $100-200 parish), coloring pages ($5-8), holy cards ($3-5 digital, $8-15 POD) | Fills gaps in VI Catholic resources; parish licensing | v2+ (content expansion) | Direct Product (A-4) |
| **M5: Contextual Affiliate Links** | Embedded in content: pilgrimage→travel, saints→books, rosary→items, seasons→devotional items | Natural moment matching; Amazon, Ignatius, Catholic retailers | Sprint 3+ (content pages) | Affiliate (B-1) |
| **M6: Pilgrimage Tour Referrals** | 3-5% of $3-8K tours; negotiate direct with 206 Tours, Tekton, Unitours, VI-specific operators | High-ticket referral; one booking = month's rent | v2+ (Map tab + routes) | Affiliate (B-2) |
| **M7: In-App Browser Analytics (Aggregate Only)** | Anonymized: content views, peak times, feast engagement, source popularity, device/geo. Quarterly reports to diocese ($200-500/qtr), publishers, tour operators | Privacy-respecting aggregate insights; consulting model | Sprint 1-2 (BrowserAnalytics), Sprint 6+ (reporting) | Indirect (C-1) |
| **M8: Premium App Features (In-App Browser Enabled)** | Free: browse, 5 bookmarks. Premium ($2-4/mo / $20-30/yr): unlimited bookmarks, push for Mass/feasts, offline reading, cross-device resume, custom alerts, ad-free | Feature gating on browser capabilities; low price impulse | Sprint 3-4 (StoreKit 2), Sprint 6 (launch) | Subscription (C-2) |
| **M9: VI Catholic Business Directory** | Free basic listings; enhanced $15-30/mo; featured $50-100/mo; annual sponsor $300-500/yr | "Catholic Yellow Pages" for Westminster/OC; targeted audience | Sprint 6+ (directory section) | Directory (D-1) |
| **M10: Event Promotion** | Free basic calendar; featured/push $25-75/event; newsletter slot $50-100 | Community bulletin board with premium visibility | Sprint 6+ (calendar integration) | Directory (D-2) |
| **M11: Prayer Intention Board (Donation-Linked)** | Free submit; optional $1-5 donation framed as ministry support. Cultural fit: offerings at shrines. | Maps to existing VI Catholic practice; high frequency | Sprint 6+ (Saved/Community tab) | Donations (D-3) |
| **M12: Liturgical Season Sponsorships** | $200-500/season (Advent, Lent, Easter, etc.); tasteful static acknowledgment; 5-6 seasons/yr | Prestige association, not ads; culturally resonant | Sprint 6+ (sponsor dashboard) | Sponsorship (E-1) |
| **M13: Underwriting (Public Radio Model)** | $100-250/mo per underwriter; factual, non-promotional, rotating quarterly | Dignified; NPR/PBS model; 2-4 at a time | Sprint 6+ (underwriter management) | Sponsorship (E-2) |
| **M14: Grants (3 Framings)** | Catholic media (USCCB, KofC, diocese), VI cultural preservation (NEH, CA Humanities), immigrant digital access (CA State Library, IMLS) | Cultural preservation = strongest narrative | v2+ (grant writing) | Grants (F-1) |
| **M15: Diocese of Orange Partnership** | Endorsement, channel sharing, $1-5K/yr stipend, co-application for larger grants | Institutional credibility + distribution | Sprint 4-6 (direct conversation) | Grants/Institutional (F-2) |
| **M16: Calendar Data Licensing** | $500-2K/yr per licensee (Hallow, Laudate, iBreviary, VI outlets) for API access | Your calendar becomes canonical VI Catholic calendar | v2+ (API) | Licensing (G-1) |
| **M17: White-Label Platform** | Setup $1-3K + $100-300/mo for other dioceses (San Jose, Houston, DC, Atlanta, Dallas) | Scale revenue without scaling content workload | v2+ (multi-tenant) | Licensing (G-2) |

---

## Quick Comparison Matrix

| Dimension | M1 Calendar | M2 Pilgrimage | M3 Artwork | M4 Prayer | M5 Affiliate | M6 Tour Referral | M7 Analytics | M8 Premium App | M9 Directory | M10 Events | M11 Prayer Board | M12 Season Sponsor | M13 Underwriting | M14 Grants | M15 Diocese | M16 Calendar API | M17 White-Label |
|-----------|-------------|---------------|------------|-----------|--------------|------------------|--------------|----------------|--------------|------------|------------------|--------------------|------------------|------------|-------------|------------------|-----------------|
| **Ethical Risk** | None | None | None | None | Low | Low | Low* | Low | Low | Low | Medium** | Low | None | None | None | Low | Low |
| **Dev Effort** | Medium | High | Low | Medium | Low | Low | Medium | Medium | Medium | Low | Medium | Low | Low | High | Medium | High | High |
| **Revenue Ceiling** | High | High | Medium | Medium | Medium | **Highest** | Medium | High | Medium | Medium | Medium | Medium | Medium | High | Medium | Medium | **Highest** |
| **Time to First $** | Medium | Slow | Fast | Medium | Fast | Medium | Slow | Medium | Slow | Fast | Fast | Medium | Medium | Slow | Medium | Slow | Slow |
| **Cultural Fit** | Highest | High | Highest | Highest | High | High | Medium | High | **Highest** | High | **Highest** | **Highest** | High | Medium | Highest | Low | Medium |
| **Anno Sprint** | 3-6 | v2+ | 1-2, 6+ | v2+ | 3+ | v2+ | 1-2, 6+ | 3-6 | 6+ | 6+ | 6+ | 6+ | 6+ | v2+ | 4-6 | v2+ | v2+ |

*M7 = aggregate only, never individual data — bright line
**M11 = must frame donation as optional ministry support, never payment for prayer efficacy

---

## Anno-Specific Integration Map

| Anno Feature | Enables Modules |
|--------------|-----------------|
| **WKWebView Aggregator (Today/Calendar)** | M1 (calendar content), M5 (affiliate in content), M7 (analytics), M8 (premium browser features) |
| **Calendar Engine (4-yr, EN/VI, lunar)** | M1 (full calendar), M3 (artwork per day), M16 (API), M17 (white-label) |
| **Map Tab / Pilgrimage Routes (v2)** | M2 (route guides), M6 (tour referrals), M8 (offline maps premium) |
| **Artwork/Design System** | M3 (6 formats), M12/M13 (sponsor artwork sections) |
| **StoreKit 2 / SwiftData** | M1 (calendar sub), M8 (premium tier), M11 (donation IAP) |
| **Vietnamese Localization** | All — cultural specificity = differentiation |
| **Parish Network (16+ in OC)** | M1 (parish license), M9 (directory), M10 (events), M15 (diocese) |
| **Saved/Community Tab** | M11 (prayer board), M8 (saved offline), M3 (saved artwork) |

---

## Revenue Projection (From Source)

| Revenue Source | Month 1-6 | Month 7-12 | Year 2+ |
|---|---|---|---|
| Digital products (M1, M2, M3, M4) | $50-150 | $200-500 | $400-800 |
| App premium (M8) | $0 | $50-150 | $200-600 |
| Affiliate goods (M5) | $20-50 | $75-200 | $150-350 |
| Tour referrals (M6) | $0-90 | $90-400 | $200-600 |
| Ko-fi/donations (M11) | $25-75 | $75-200 | $100-300 |
| Directory (M9) | $0 | $50-150 | $200-500 |
| Season sponsorships (M12) | $0 | $100-300 | $200-500 |
| Underwriting (M13) | $0 | $100-250 | $200-500 |
| Event promotion (M10) | $0 | $25-75 | $75-200 |
| Prayer board donations (M11) | $0 | $50-150 | $150-400 |
| Grants amortized (M14) | $0 | $200-800 | $400-2,000 |
| **Monthly Total** | **$95-365** | **$1,015-3,175** | **$2,075-5,750** |

---

## Launch Sequence (From Source)

| Phase | Timing | Modules Activated |
|-------|--------|-------------------|
| **1** | Week 1 | M11 (Ko-fi) |
| **2** | Week 2-4 | M7 (aggregator + analytics) |
| **3** | Month 1-2 | M1 (calendar freemium) |
| **4** | Month 2-3 | M5 (affiliate programs) |
| **5** | Month 3-4 | M6 (tour operator outreach) |
| **6** | Month 4-6 | M15 (diocese conversation), M14 (grant research) |
| **7** | Month 6-9 | M9 (directory free tier), M12 (Advent sponsor) |
| **8** | Month 9-12 | M8 (premium tier), M11 (prayer board), M13 (underwriters) |
| **9** | Year 2 | M16 (API licensing), M17 (white-label), M14 (larger grants) |

---

## Ethics Test (From Source — Apply to Any New Idea)

1. **Would I be embarrassed to explain this in Vietnamese to an elderly parishioner after Sunday Mass?**
2. **Am I profiting from someone else's sacred content, or my own labor around it?**
3. **If my most vulnerable user (elderly, limited English/income) engaged, would they be better off?**

---

## Next Step

Say a module code (M1-M17) and what you want next — expand, filter, cross-reference with Anno sprints, or delegate. No further work until then.