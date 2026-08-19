# Monetization Module (M1-M17) → Anno Features Mapping

**Source:** `monetization` module (v1-v3: architecture_17_modules.md, sprint_mapping.md, roe_decomposition.md, calendar_spec_grant_decomposition.md)  
**Target:** Anno MVP (`MVP_PLAN_FINAL.md`, `AnnoEntry.swift`, `AGENTS.md`, `CLAUDE.md`)  
**Date:** 2026-08-19

---

## Executive Summary

The monetization architecture defines **17 modules (M1-M17)** across 7 revenue categories (A-G). Anno's current MVP sprints (1-6) only unlock a subset. **7 modules are "build-ready" in design** (M1, M3, M6, M8, M12, M13, M14, M15) but **only 3 can execute without the app running** (M5, M11-Ko-fi, M14, M15). The rest need Sprint 1 (macOS/Xcode) or v2 Map tab.

---

## Module-by-Module Mapping to Anno MVP

| Module | Anno Sprint Dependency | Current Anno Status | Gap / Extension Needed |
|--------|------------------------|---------------------|------------------------|
| **M1: Liturgical Calendar (Freemium)** | Sprint 3-4 (content), Sprint 6 (premium gate) | Calendar engine works; Today/Calendar UI exists; **Paywall deleted** | Add 7-layer content (calendar_content module); re-add paywall at Layer 3; StoreKit 2 subscription for premium |
| **M2: Pilgrimage Route Guides** | v2+ (Map tab deleted) | Map folder deleted in Sprint 1 | **Blocked** — needs MapKit integration, route data model, v2 scope |
| **M3: Artwork Multi-Stream** | Sprint 1-2 (design system), Sprint 6+ (catalog) | `ArtworkCandidate` exists; `Design/AnnoTheme.swift` exists | Add 6-format pipeline (digital, POD, bundle, parish license, wallpaper, bulletin); `ArtworkCandidate` needs `downloadUrl`, `purchaseUrl`, `price` |
| **M4: Prayer/Devotional Products** | v2+ (content expansion) | Not in MVP | **Blocked** — needs content pipeline; could be PDF exports from calendar_content Layer 4/6 |
| **M5: Contextual Affiliate Links** | Sprint 3+ (content pages) | Content pages exist (TodayView) | Add affiliate link injection in content render; Amazon/Ignatius/TAN/Catholic Company programs |
| **M6: Pilgrimage Tour Referrals** | v2+ (Map tab + routes) | Map deleted | **Blocked** — needs M2 first; outreach email + 1-pager ready (from ROE doc) |
| **M7: Browser Analytics (Aggregate)** | Sprint 1-2 (WKWebView), Sprint 6+ (reporting) | `NotificationService`, `SearchHistory` exist | Build `BrowserAnalytics` service: schema, aggregation, quarterly reports; privacy-first (no PII) |
| **M8: Premium App Features** | Sprint 3-4 (StoreKit 2), Sprint 6 (launch) | Paywall folder deleted; StoreKit 2 not wired | **Re-add** subscription IAP; gate: unlimited bookmarks, push (Mass/feasts), offline, custom alerts; "$1/mo" framing |
| **M9: VI Business Directory** | Sprint 6+ (Saved/Community tab) | `Saved/SavedView.swift` exists (Spiritual Bouquet) | Add directory section; parish data from `vietnamese_media` M3; enhanced/featured tiers |
| **M10: Event Promotion** | Sprint 6+ (Calendar + push) | Calendar tab exists; no push | Add event model; featured/push pricing; newsletter slot |
| **M11: Prayer Intention Board** | Sprint 5-6 (SwiftData bookmarks) | `Bookmark.swift` + `BookmarkActions.swift` being fixed in Sprint 1 | Extend bookmarks → community intentions; consumable IAP for $1-5 donations; cultural framing |
| **M12: Liturgical Season Sponsorships** | Sprint 6+ (TestFlight + users) | Not in MVP | Sponsor dashboard; static acknowledgment in content; 5-6 seasons/yr; $200-500/season |
| **M13: Underwriting (NPR Model)** | Sprint 6+ (TestFlight + users) | Not in MVP | Underwriter management; rotating quarterly; $100-250/mo; factual non-promotional |
| **M14: Grants (3 Framings)** | v2+ (grant writing) | **No app needed** | CCC draft ready (calendar_content); customize brackets; VCC letter needed; multi-grant reuse |
| **M15: Diocese Partnership** | Sprint 4-6 (direct conversation) | **No app needed** | VCC OC warm intro → gift → wait protocol; endorsement unlocks M1, M9, M12, M14 |
| **M16: Calendar Data Licensing** | v2+ (API + proven dataset) | Calendar engine works (Python) | Public API; accuracy proof; licensees: Hallow, Laudate, iBreviary, VI outlets |
| **M17: White-Label Platform** | v2+ (multi-tenant) | Single-tenant SwiftUI | Multi-tenant architecture; setup $1-3K + $100-300/mo; target: San Jose, Houston, DC, Atlanta, Dallas |

---

## Anno MVP Sprint Coverage vs. Monetization Modules

| Sprint | Anno Deliverable | Monetization Modules Enabled |
|--------|------------------|------------------------------|
| **1: Xcode + Clean Build** | App compiles, runs | M7 (browser analytics foundation), M3 (design system), M8 (StoreKit 2 setup) |
| **2: Week Fixture + Empty States** | 7 real days visible | M1 (calendar content preview), M5 (affiliate in content) |
| **3: Content Batch 1 (Jul 3-9)** | 7 saint feast entries | M1 (Layer 3 content), M3 (artwork per day), M5 (affiliate links in bios) |
| **4: Content Batch 2 (Jul 10-16)** | 7 more entries | M1, M3, M5 continued |
| **5: Wire Content + Bookmarks** | SwiftData persistence, merge script | M8 (bookmark gating), M11 (intention board foundation) |
| **6: Polish + Ship (TestFlight)** | App in TestFlight | M8 (premium launch), M9 (directory MVP), M10 (events), M11 (prayer board), M12/M13 (sponsor pitch with real users) |

---

## What's Build-Ready NOW (No macOS, No App Running)

| Module | Deliverable | Source Doc | Status |
|--------|-------------|------------|--------|
| **M5** | Affiliate program applications (Amazon, Ignatius, TAN, Catholic Company) | sprint_mapping.md | Apply today — 1-3 day approval |
| **M11 (Ko-fi)** | Ko-fi page + link | sprint_mapping.md | 5 min setup |
| **M14** | Grant LOI / CCC application draft | calendar_spec_grant_decomposition.md | Draft exists — customize brackets |
| **M15** | Diocese conversation (VCC OC) | sprint_mapping.md, roe_decomposition.md | Email today — warm intro protocol |
| **M3 (assets)** | Artwork creation (10-20 pieces) | sprint_mapping.md | Design work; upload to POD later |
| **M4 (content)** | Prayer guide / sacramental prep writing | sprint_mapping.md | Pure writing; PDF export later |
| **M6 (outreach)** | Tour operator email + 1-pager | roe_decomposition.md | Deliverable ready — send when ready |
| **M12/M13** | Sponsor/underwriter prospectus (bilingual) | calendar_spec_grant_decomposition.md | Structure defined — fill specifics |

---

## Critical Dependencies (Monetization → Anno Features)

| Monetization Need | Anno Feature Required | Sprint |
|-------------------|----------------------|--------|
| M1: Full calendar premium | 7-layer content (calendar_content), paywall at Layer 3, StoreKit 2 | 3-6 |
| M1: Parish bulk sales | Calendar dataset (460 entries), print export (JSON→InDesign) | v2 parallel |
| M3: Artwork commerce | `ArtworkCandidate` extensions, POD integration, design system | 1-2, 6+ |
| M5: Affiliate links | Content render injection point | 3+ |
| M7: Analytics | WKWebView aggregator, `BrowserAnalytics` service, privacy schema | 1-2 |
| M8: Premium tier | StoreKit 2 subscription, feature gates, push notifications | 3-6 |
| M9: Directory | Parish data (vietnamese_media M3), Community tab UI | 6+ |
| M11: Prayer board | SwiftData consumable IAP, community UI | 5-6 |
| M12/M13: Sponsors | Traffic proof, sponsor dashboard, static content injection | 6+ |
| M14: Grants | VCC letter, demo app (TestFlight), metrics | 6+ |
| M15: Diocese | VCC endorsement → unlocks parish access | 4-6 |
| M16: API | Public API, rate limiting, authentication, canonical calendar proof | v2+ |

---

## Revenue Projection Reality Check (Architecture vs. MVP Timeline)

| Architecture Year 1 (Month 7-12) | MVP Reality (TestFlight ~Month 2-3) |
|----------------------------------|--------------------------------------|
| M1 digital: $200-500 | **Month 3-6**: $0-50 (TestFlight → App Store review lag) |
| M3 artwork: $0 (directory not started) | **Month 3-6**: $0-100 (POD needs asset library first) |
| M5 affiliate: $75-200 | **Month 3-6**: $20-50 (needs content volume) |
| M7 analytics: $0 | **Month 3-6**: $0 (needs quarterly data) |
| M8 premium: $50-150 | **Month 3-6**: $0-50 (StoreKit 2 + review) |
| **Total Month 7-12: $1,015-3,175** | **Realistic Month 3-6: $20-250** |

**Key insight:** Architecture assumes app in market Month 1. Real MVP: TestFlight Month 2-3, App Store Month 3-4, organic growth Month 4-6. Revenue ramp is 2-3 months behind architecture.

---

## Recommended Sequence for Anno (Aligned with MVP_PLAN_FINAL.md)

| Phase | Work | Monetization Modules | Sprint |
|-------|------|---------------------|--------|
| **Pre-MVP (This Week)** | Ko-fi + Affiliate apps + Grant LOI + Diocese email + Artwork creation + Prayer guide writing | M5, M11-Ko-fi, M14, M15, M3-assets, M4-content | — |
| **MVP Sprint 1-2** | Xcode build, WKWebView aggregator, BrowserAnalytics schema | M7, M3-design, M8-StoreKit setup | 1-2 |
| **MVP Sprint 3-4** | Content batches (phone), Layer 3 bios, artwork per day | M1-content, M3-assets, M5-links | 3-4 |
| **MVP Sprint 5** | Merge script, SwiftData bookmarks (title+date) | M8-bookmark gate, M11-foundation | 5 |
| **MVP Sprint 6** | TestFlight, premium tier launch, sponsor outreach | M8-launch, M9-MVP, M10, M11-board, M12/M13-pitch | 6 |
| **Post-MVP v2** | Map tab, pilgrimage routes, API, white-label | M2, M6, M16, M17 | v2+ |

---

## Cross-Module Dependencies (from calendar_spec_grant_decomposition.md)

| Dependency | Modules Involved | Anno Integration Point |
|------------|------------------|------------------------|
| Calendar data → App + Print + API | M1, M3, M8, M16, M17 | Single dataset (AnnoEntry.swift) feeds 5 revenue streams |
| Artwork → Calendar + Store + Wallpaper | M3, M1, M8 | Daily artwork in Layer 2 = passive marketing for M3 |
| Parish sales → Directory → Sponsors | M1, M9, M12 | Parish relationships (M15) unlock directory + sponsorship |
| VCC endorsement → Grants + Sales + Credibility | M15, M14, M1 | Single relationship cascades to 3 revenue channels |
| Content calendar → Sponsors + Affiliates | M5, M6, M12 | 52-week map aligns content to revenue moments |

---

## Summary: Build-Ready Design vs. Execution Blocked by App

| **Design Complete (can scaffold)** | **Needs App Running (Sprint 1-6)** | **Needs v2+ (Map/Multi-tenant)** |
|-----------------------------------|-----------------------------------|----------------------------------|
| M1: 7-layer spec, parish packet, pricing model | M1: Premium gate, StoreKit 2, push | M2: Pilgrimage routes (MapKit) |
| M3: 6 formats, gift tier, print specs | M3: POD integration, catalog UI | M6: Tour referrals (needs M2) |
| M6: Outreach email + 1-pager | M5: Affiliate injection in content | M16: API licensing (needs proven data) |
| M7: Analytics schema + aggregation logic | M7: WKWebView event capture | M17: White-label (multi-tenant) |
| M8: Paywall UX, "$1/mo" framing, feature list | M8: Subscription IAP, feature gates | |
| M12/M13: Prospectus structure + content calendar | M12/M13: Sponsor dashboard, traffic proof | |
| M14: CCC draft (customize brackets) | M14: VCC letter, demo metrics | |
| M15: Protocol + tier list + warm intro | M15: VCC meeting → endorsement | |
| M5/M11-Ko-fi/M14/M15: **Zero code, execute today** | M9/M10/M11: Directory, events, prayer board | |

---

## Immediate Action Items (This Week, No macOS)

1. **Set up Ko-fi** (M11) — 5 minutes
2. **Apply to 3 affiliate programs** (M5) — Amazon Associates, Ignatius Press, Catholic Company — 30 minutes
3. **Customize CCC grant draft** (M14) — replace brackets, attach VCC letter when secured — 1 hour
4. **Email VCC OC communications director** (M15) — request meeting, bring sample calendar — 10 minutes
5. **Create 10 artwork pieces** (M3 assets) — La Vang, Vietnamese Martyrs, seasonal — design time
6. **Write prayer guide outline** (M4 content) — Vietnamese prayer book structure — writing time
7. **Run Content Sprints 3-4 on phone** — 7 days each — unblocks M1 content
8. **Write `tools/merge_content.py`** (ichabod) — enables Sprint 5

---

## Decision: Which Module to "Prototype" First?

**None require code prototyping on ichabod except M7 (BrowserAnalytics).** All others are either:
- **Preparation** (assets, applications, writing, outreach) — do this week
- **App-dependent** (M1, M3, M8, M9, M10, M11, M12, M13) — need Sprint 1-6
- **v2-dependent** (M2, M6, M16, M17) — need Map tab + scale

If you want a code prototype on ichabod: **M7 BrowserAnalytics service** (Python/Node, schema + aggregation + quarterly report generator). Everything else is either preparation or blocked on macOS/app.