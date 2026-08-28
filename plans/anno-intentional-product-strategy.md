# Anno — Intentional Product Strategy

**Status:** Standalone (post-MMR extraction)
**Date:** 2026-08-28
**Branch:** visual-polish
**Author:** GCU No Trouble At All

---

## Purpose

Separated from infrastructure plan per MMR: **"Move 'Intentional Product Strategy' to a separate document. Do not implement until TestFlight is live."**

This doc captures the product vision so it's not lost — implementation happens *after* S4 (TestFlight).

---

## The Core Insight

**Every Catholic app has the same content** (readings, saints, prayers). The *content* is a commodity. What makes Anno worth $20/yr is **how the content meets the user in their actual day**.

---

## Intentional Touches (Retention → Conversion)

| Touch | Standard App | Anno Intentional |
|-------|--------------|------------------|
| **Morning open** | Static "Reading of the Day" | **Context-aware greeting**: "Good morning, [name]. Today is the Memorial of St. Monica — patron of mothers. Your 7-day streak is alive." |
| **Missed a day** | Nothing / generic streak break | **Grace note**: "You missed yesterday. That's okay — God's mercy is new every morning. Want to catch up with a 2-min reflection?" |
| **Sunday** | Same UI, just "Sunday" label | **Sunday distinct mode**: Full-screen art, longer reflection, "Prepare for Mass" checklist (readings, intentions, fast status) |
| **Feast days** | Small badge | **Feast celebration**: Custom hero image, patronage explanation, "How to celebrate today" (food, tradition, prayer) |
| **Lent/Advent** | Color change (purple) | **Seasonal journey**: Daily micro-practice (fast, give, pray), progress visual, "Why this season matters" audio intro (Day 1) |
| **Language switch** | Toggle EN/VI | **Bilingual woven**: VI isn't a toggle — it's *interleaved*. "Chào buổi sáng. Today is St. Joseph the Worker..." — serves bilingual households naturally |
| **Widget** | Static verse | **Living widget**: Updates with liturgical color, feast icon, one-tap "Open to pray" |
| **Complications** | None | **Watch complication**: Liturgical color ring + feast initial — glance = orientation |

---

## Monetization Architecture (Conversion → Revenue)

### 1. Freemium Boundary (The "Aha!" Moment)

| Free (Forever) | Premium ($19.99/yr) |
|----------------|---------------------|
| Today's readings (EN) | **Full bilingual** (EN + VI interleaved) |
| Today's saint (summary) | **Full saint story** (3-5 paragraphs + patronage + art) |
| Basic calendar view | **Liturgical year navigation** (seasons, octaves, ember days) |
| 1 widget (static) | **All widgets + complications + dynamic** |
| Push: daily reading | **Push: contextual** (feast alert, Lent practice, Sunday prep) |
| | **Audio reflections** (90-sec, human voice, EN + VI) |
| | **Offline sync** (30 days cached) |
| | **Export/Share** (prayer cards, beautiful images) |
| | **Patron saint tracker** (your saints, their feast alerts) |

**Boundary logic:** Free user hits the "Want the full story?" / "Want this in Vietnamese too?" / "Want audio?" moment *during* their natural flow — not a paywall screen.

### 2. Conversion Triggers (Built into Flow)

| Trigger | Timing | Message |
|---------|--------|---------|
| **Streak milestone** | Day 7, 30, 100 | "30 days of daily prayer. That's a habit. Unlock audio reflections to go deeper." |
| **Feast day open** | On feast tap | "This saint has a beautiful story. Premium unlocks the full 3-min read." |
| **Language toggle** | 2nd VI view | "You're reading in Vietnamese. Premium keeps both languages woven together." |
| **Season start** | Ash Wed / 1st Advent | "Lent begins tomorrow. Premium gives you the daily journey — micro-practices, audio, progress." |
| **Share attempt** | Tap share on free | "Create a beautiful prayer card with art. Premium unlocks export." |

### 3. Subscription Psychology

- **Annual only at launch** ($19.99) — no monthly churn, higher LTV, simpler messaging ("$1.66/month for daily grace")
- **7-day free trial** — Apple handles, no code needed
- **No "Pro" / "Plus" tiers** — one price, everything. Simplicity = trust.
- **Family Sharing enabled** — one sub = whole household (critical for Catholic families)

### 4. Retention Mechanics (Post-Subscribe)

| Mechanic | Purpose |
|----------|---------|
| **Streak repair** | 1 free "grace repair" per quarter — reduces churn from guilt |
| **Seasonal re-engagement** | Push: "Lent starts in 3 days. Your journey awaits." |
| **Patron saint anniversary** | "It's your confirmation saint's feast! Here's a special reflection." |
| **Annual renewal nudge** | Day 330: "Your year of daily prayer is almost complete. Renew to keep the streak." |
| **Content freshness** | New saint art / audio each season — "What's new this Advent?" |

---

## Acquisition (Zero-Cost, High-Intent)

| Channel | Asset | Hook |
|---------|-------|------|
| **App Store Search** | Keywords: "Catholic daily readings bilingual", "Vietnamese Catholic app", "liturgical calendar 2026" | EN+VI is a *differentiator* — almost no apps do it well |
| **Parish bulletins** | QR code + one-pager | "Daily readings in English & Vietnamese — free for your parishioners" |
| **Catholic creator collabs** | Guest audio reflection | "Fr. Mike / Sr. Miriam / [your network] records one Advent reflection" |
| **Reddit / Discord** | r/Catholicism, r/VietnameseCatholics | "Built this for my mom who wanted both languages. Free tier is generous." |
| **SEO / Web** | `anno.app` landing page | "The only bilingual daily devotional with liturgical intelligence" |

---

## Metrics That Matter (Instrument from Day 1)

| Metric | Target | Tool |
|--------|--------|------|
| **D1 Retention** | >40% | Mixpanel / Amplitude (free tier) |
| **D7 Retention** | >25% | |
| **Trial → Paid** | >15% | App Store Connect |
| **Paid → Renewal (Y1)** | >60% | |
| **Premium feature adoption** | >50% of subs use audio/widgets | Custom events |
| **VI language usage** | >30% of sessions | |
| **Share/export rate** | >5% of premium sessions | |

---

## Data Model Extensions (Add to SwiftData Now — Zero Cost)

These enable the intentional layer later. Add to `Anno/Models/` now:

```swift
// UserProfile.swift
@Model
final class UserProfile {
    var name: String = ""
    var languagePreference: Language = .english  // .english, .vietnamese, .interleaved
    var patronSaintIDs: [String] = []  // e.g. ["joseph", "monica", "therese"]
    var notificationConsent: Bool = false
    var notificationTypes: Set<NotificationType> = []
    var createdAt: Date = Date()
    var lastActiveAt: Date = Date()
}

// Streak.swift
@Model
final class Streak {
    var current: Int = 0
    var longest: Int = 0
    var lastCompletedDate: Date?
    var lastRepairDate: Date?
    var repairsUsedThisQuarter: Int = 0
}

// SeasonalProgress.swift
@Model
final class SeasonalProgress {
    var season: LiturgicalSeason  // .advent, .christmas, .lent, .easter, .ordinary
    var year: Int
    var day: Int = 0
    var practicesCompleted: Set<String> = []  // e.g. "lent-day-5-fast"
    var startedAt: Date?
    var completedAt: Date?
}

// FeatureFlags.swift
@Model
final class FeatureFlags {
    var audioEnabled: Bool = false
    var viEnabled: Bool = false
    var widgetsEnabled: Bool = false
    var complicationsEnabled: Bool = false
    var exportEnabled: Bool = false
    var updatedAt: Date = Date()
}
```

---

## RevenueCat Entitlement Mapping

| RevenueCat Entitlement | Unlocks |
|------------------------|---------|
| `premium` | All premium features (bilingual, full saints, audio, widgets, export, offline, patron tracker) |

**Offering:** `anno_premium_annual` → `anno.subscription.yearly` (App Store Connect)
**Intro:** 7-day free trial (configured in RevenueCat dashboard)

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| VI localization quality | Flag clearly as "draft — native review needed"; recruit 1-2 VI beta testers from parish network |
| Audio reflection production | Start with 12 (one per month) — record yourself or AI voice (kokoro) with human review; expand if retention warrants |
| Catholic niche = small TAM | TAM = 70M US Catholics + 7M VI Catholics + global. Niche = loyal, high LTV, low CAC. Own the bilingual lane. |
| Apple rejects "religious" subscription | StoreKit 2 + RevenueCat is standard; many Catholic apps (Hallow, Laudate, iBreviary) use subscriptions. Follow their metadata patterns. |
| Content liability (wrong feast/reading) | Calendar engine is deterministic + USCCB-verified. Add disclaimer: "Check your local parish bulletin." |

---

## Implementation Phasing (Post-TestFlight)

| Phase | Features | Est. Effort |
|-------|----------|-------------|
| **P1: Onboarding + Paywall** | First-run flow, trial upsell, RevenueCat paywall UI | 1-2 weeks |
| **P2: Bilingual Weaving + Full Saints** | Interleaved EN/VI, expanded saint content, patron tracker | 2-3 weeks |
| **P3: Audio + Widgets** | 12 monthly audio reflections (EN+VI), dynamic widgets, watch complications | 2-3 weeks |
| **P4: Seasonal Journeys** | Lent/Advent micro-practices, progress visuals, seasonal audio intros | 2 weeks |
| **P5: Push + Retention** | Contextual push (feast, streak, season), streak repair, renewal nudge | 1-2 weeks |
| **P6: Polish + Share** | Prayer card export, beautiful share images, offline sync | 1 week |

**Total post-TestFlight: ~10-13 weeks to full intentional product**

---

## Connection to Infrastructure Plan

The infrastructure plan (`anno-mac-free-build-plan.md`) delivers:
- TestFlight build with RevenueCat configured
- SwiftData models extended with UserProfile, Streak, SeasonalProgress, FeatureFlags
- App Store Connect metadata (EN only for MVP)

This strategy doc then drives the *next* sprint cycles. No conflict — clean separation.