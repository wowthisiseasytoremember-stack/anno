# Monetization → Anno Sprint Mapping

**Purpose:** Exact cross-reference between monetization modules and Anno's current MVP sprints. Shows what's actionable **now** (no macOS) vs. what requires the app to run.

---

## Current Anno Sprint Status (from MVP_PLAN_FINAL.md)

| Sprint | Days | Status | Blockers |
|--------|------|--------|----------|
| **1: Xcode Project + Clean Build** | 1 | 🟡 **BLOCKED** | Requires macOS (Xcode) — ichabod cannot run |
| **2: Week Fixture + Empty States** | 0.5 | 🟡 Waiting | Depends on Sprint 1 |
| **3: Content Batch 1 (Jul 3-9)** | 1 | ✅ **READY** | Phone-deliverable — can run today |
| **4: Content Batch 2 (Jul 10-16)** | 1 | ✅ **READY** | Phone-deliverable — can run today |
| **5: Wire Content + Bookmarks** | 1 | 🟡 Waiting | Needs merge script + content from 3-4 |
| **6: Polish + Ship (TestFlight)** | 2 | 🟡 Waiting | Needs Sprints 1-5 |

---

## Monetization Modules by Sprint Dependency

### ✅ **Actionable NOW (No macOS, No App Required)**

| Module | Why It's Ready | What You Can Do Today |
|--------|----------------|-----------------------|
| **M11: Ko-fi / Donations** | Zero code; just a link | Set up Ko-fi page; add link to any web presence |
| **M14: Grant Research** | Pure research/writing | Identify 5-10 targets; draft one LOI |
| **M15: Diocese Conversation** | Relationship building | Email/meet VCC OC communications director |
| **M5: Affiliate Program Applications** | Amazon Associates, Ignatius, TAN, Catholic Company | Apply (takes 1-3 days approval); no app needed |
| **M3: Artwork Asset Creation** | Design work; POD integration later | Create 10-20 pieces; upload to Printful/Printify |
| **M4: Prayer/Devotional Writing** | Pure content | Write Vietnamese prayer guide, sacramental prep, coloring pages |

### 🟡 **Needs Sprint 1-2 (App Compiles, Runs on Simulator)**

| Module | Sprint Dependency | What Unlocks It |
|--------|-------------------|-----------------|
| **M1: Liturgical Calendar (Freemium)** | Sprint 1 (app runs) + Sprint 3-4 (content) | Calendar engine already works; need app to display + StoreKit 2 |
| **M7: In-App Browser Analytics** | Sprint 1 (WKWebView aggregator) | BrowserAnalytics service + aggregate reporting |
| **M8: Premium App Features** | Sprint 1 + Sprint 3 (StoreKit 2 setup) | Subscription infrastructure in app |

### 🟠 **Needs Sprint 5-6 (Real Content + Bookmarks + Polish)**

| Module | Sprint Dependency | What Unlocks It |
|--------|-------------------|-----------------|
| **M9: Business Directory** | Sprint 6 (Saved/Community tab exists) | Directory section in app; parish outreach |
| **M10: Event Promotion** | Sprint 6 (Calendar tab + push) | Calendar integration + push notifications |
| **M11: Prayer Intention Board (In-App)** | Sprint 5 (SwiftData bookmarks) + Sprint 6 | Community tab + consumable IAP for donations |
| **M12: Liturgical Season Sponsorships** | Sprint 6 (app in TestFlight, real users) | Sponsor dashboard + traffic to show |
| **M13: Underwriting** | Sprint 6 (app in TestFlight, real users) | Same as M12 |

### 🔴 **Needs v2+ (Map Tab, Scale, Multi-Tenant)**

| Module | Sprint Dependency | What Unlocks It |
|--------|-------------------|-----------------|
| **M2: Pilgrimage Route Guides** | v2 (Map tab restored) | MapKit integration + route data |
| **M6: Pilgrimage Tour Referrals** | v2 (Map tab + routes live) | Routes in app + tour operator partnerships |
| **M16: Calendar Data Licensing** | v2+ (API + canonical calendar) | Public API + proof of accuracy |
| **M17: White-Label Platform** | v2+ (multi-tenant architecture) | Significant engineering investment |

---

## Recommended Immediate Sequence (Next 2 Weeks)

| Week | Focus | Modules Advanced | Owner |
|------|-------|------------------|-------|
| **This Week** | Content Sprints 3-4 | — | You (iPhone) |
| **This Week** | Write `tools/merge_content.py` | Enables Sprint 5 | Me (ichabod) |
| **This Week** | Enrich `Bookmark.swift` (title + date) | Enables Sprint 5.4 | Me (ichabod) |
| **This Week** | Set up Ko-fi (M11) | Immediate revenue path | You (5 min) |
| **This Week** | Apply to 3 affiliate programs (M5) | Revenue path when content exists | You (30 min) |
| **This Week** | Draft 1 grant LOI (M14) | Long-term funding | You (1 hr) |
| **This Week** | Email VCC OC for meeting (M15) | Institutional path | You (10 min) |
| **Next Week** | Run merged content validation | Unblocks Sprint 5 | Me (ichabod) |
| **Next Week** | Create 10 artwork pieces (M3) | Asset library for M3/M12 | You (design time) |
| **Next Week** | Write prayer guide outline (M4) | Product for v2 | You (writing time) |

---

## What This Means for Your Question

**"Which monetization module to prototype first?"**

**Answer: None yet.** The modules that could be prototyped (M1, M3, M8) all need the app running. The modules that need no app (M5, M11, M14, M15, M3-creation, M4-writing) are **preparation work**, not prototypes.

**Prototype ≠ Preparation.** A prototype is code you can test. Preparation is assets you create.

---

## If You Insist on a Prototype Target

The **only module you can prototype code for on ichabod** is:

| Module | Prototype Scope | What You'd Build |
|--------|-----------------|------------------|
| **M7: BrowserAnalytics** | Python/Node service that ingests anonymized browser events, outputs aggregate reports | `tools/browser_analytics.py` — schema, aggregation logic, quarterly report generator. Test with mock data. |

Everything else either:
- Needs Swift/StoreKit (M1, M8, M11-in-app)
- Needs MapKit (M2, M6)
- Needs real users/traffic (M9, M10, M12, M13)
- Needs API infrastructure (M16, M17)

---

## Decision Matrix

| If You Want To... | Do This |
|-------------------|---------|
| **Make progress on Anno MVP** | Run Content Sprints 3-4 on phone → I'll write merge script → Sprint 5 ready |
| **Build monetization assets** | Ko-fi + affiliate apps + grant LOI + diocese email + artwork creation + prayer guide writing |
| **Prototype monetization code** | Build `tools/browser_analytics.py` (M7) — only ichabod-doable prototype |
| **Validate monetization assumptions** | Run MMR on the monetization architecture doc (goal-first + red-team) |

---

**My recommendation:** Content Sprints 3-4 + merge script this week. Monetization preparation in parallel. Prototype M7 only if you have spare engineering cycles after Sprint 5 is unblocked.