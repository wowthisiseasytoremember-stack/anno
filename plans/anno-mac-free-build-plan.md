# Anno — Mac-Free Build Plan (S3/S4 Infrastructure) + Intentional Product Strategy

**Status:** Post-MMR v2 (folded CI/CD fixes + intentional layer added)
**Date:** 2026-08-28
**Branch:** visual-polish
**Author:** GCU No Trouble At All

---

## Goal

Build every artifact needed for TestFlight release **without a Mac** — so the next macOS session is a single `fastlane beta` command that produces a valid TestFlight build.

**Target:** Anno iOS app (Catholic daily devotional, EN/VI, StoreKit 2 subscription)

---

## What We Already Have

| Item | Location | Status |
|------|----------|--------|
| SwiftUI Views (Today, Calendar, Saved, Settings) | `Anno/Views/` | ✅ |
| ViewModels + Services | `Anno/Services/`, `Anno/ViewModels/` | ✅ |
| SwiftData Models (5 @Model classes) | `Anno/Models/` | ✅ |
| 365 days EN/VI liturgical content | `Anno/Resources/anno_full_2026.json` | ✅ |
| Calendar engine (deterministic, no LLM) | `calendar_engine.py` | ✅ |
| Content generators + merge tools | `tools/` | ✅ |
| GitHub Actions iOS Build workflow | `.github/workflows/ios-build.yml` | ✅ green |
| xcodegen project.yml | `Anno/project.yml` | ✅ |

**Architecture decision (post-MMR):** Keep single Xcode project. Do NOT split into multiple SPM packages.

---

## What We Can Build on Linux

### 1. Documentation First (Critical Dependency — MMR Finding)
| File | Purpose |
|------|---------|
| `docs/SECRETS.md` | **FIRST** — exact GitHub secret names + source (App Store Connect / appleid.apple.com) |
| `docs/MATCH_SETUP.md` | Mac playbook: exact `fastlane match` commands, certs repo init, verify with `--readonly` |
| `docs/RELEASE_CHECKLIST.md` | 30-min Mac session walkthrough: match init → secrets verify → `fastlane beta` |

**Execution order (post-MMR fold):** SECRETS.md → MATCH_SETUP.md → RELEASE_CHECKLIST.md → then Fastlane/CI.

### 2. Fastlane Complete Setup (After SECRETS.md Locked)
| File | Purpose |
|------|---------|
| `fastlane/Fastfile` | Lanes: `beta` (TestFlight, readonly match), `release` (App Store), `match_appstore` (write, Mac-only), `match_development` (write, Mac-only) |
| `fastlane/Appfile` | App identifier, team ID, Apple ID |
| `fastlane/Matchfile` | `git_url` (private certs repo), `type("appstore")`, `readonly(true)` for CI |

**Write-Guard (post-MMR fold):** In Fastfile, any write lane (`match_appstore`, `match_development`) has `ensure_env(env: 'CI')` at top — prevents accidental execution on CI runner.

### 3. GitHub Actions — Release Workflow
| File | Purpose |
|------|---------|
| `.github/workflows/ios-release.yml` | Trigger: tag push (`v*`) or manual dispatch → `xcodegen` → `fastlane beta` → TestFlight |

**Runner:** `macos-latest` (**90 min timeout** — post-MMR fold)

**Concurrency:** `group: release, cancel-in-progress: false`

**Artifact persistence (post-MMR fold):**
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: build-artifacts
    path: |
      build/Anno.xcarchive
      build/Anno.ipa
  if: always()
```

**Secrets (post-MMR fold — standard fastlane approach):**
```yaml
env:
  APP_STORE_CONNECT_API_KEY_KEY_ID: ${{ secrets.APP_STORE_CONNECT_API_KEY_KEY_ID }}
  APP_STORE_CONNECT_API_KEY_ISSUER_ID: ${{ secrets.APP_STORE_CONNECT_API_KEY_ISSUER_ID }}
  APP_STORE_CONNECT_API_KEY_CONTENT: ${{ secrets.APP_STORE_CONNECT_API_KEY_CONTENT }}  # raw .p8, NOT base64
  MATCH_GIT_URL: ${{ secrets.MATCH_GIT_URL }}
  MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
  FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD: ${{ secrets.FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD }}
```

**Pre-flight verification step:** `fastlane match appstore --readonly` dry-run before full build.

### 4. StoreKit 2 — Complete Implementation
| File | Purpose |
|------|---------|
| `Anno/Services/StoreKitService.swift` | Protocol `StoreProvider` + `ProductionStore` (iOS) + `MockStore` (testable) |
| `Anno/Services/EntitlementManager.swift` | Verifies subscription status, caches, handles grace period |
| `Anno/Services/TransactionListener.swift` | Background task for `Transaction.updates` |
| `Anno/ViewModels/StoreViewModel.swift` | UI-facing: products, purchase, restore, error handling |

**No iOS unit tests in CI** (post-MMR fold) — StoreKit tests need Simulator runtime not available on macOS runners. Document as manual Mac-only verification step in RELEASE_CHECKLIST.md.

**Products (App Store Connect):**
- `anno.subscription.yearly` — $19.99/yr (intro: 7-day free trial)
- `anno.subscription.monthly` — $2.99/mo

### 5. CI/CD — Update Existing Build Workflow
| File | Change |
|------|--------|
| `.github/workflows/ios-build.yml` | Add `validate` job: `xcodegen validate` + `swift build` (pure Swift targets only). No `xcodebuild test`. |

### 6. Design System (Tokens → Swift)
| File | Purpose |
|------|---------|
| `design/tokens.json` | Colors, spacing, typography, icons — single source |
| `tools/generate_design_tokens.py` | **Python script** (Linux-native) with JSON schema validation + diff check |
| `tools/test_design_tokens.py` | Unit tests for generator (fixtures + schema) |
| `Anno/Design/` | Generated SwiftUI modifiers — zero runtime cost |

### 7. App Store Connect Metadata
| File | Purpose |
|------|---------|
| `fastlane/metadata/en-US/description.txt` | 4000 char — real marketing copy |
| `fastlane/metadata/en-US/keywords.txt` | 100 char |
| `fastlane/metadata/en-US/release_notes.txt` | Per version |
| `fastlane/metadata/en-US/support_url.txt` | |
| `fastlane/metadata/en-US/marketing_url.txt` | |
| `fastlane/metadata/vi/README.md` | **"DO NOT SUBMIT — needs native Vietnamese speaker review before TestFlight"** (post-MMR fold) |

---

## Out of Scope (Mac / Physical Device Required)

| Item | Documented in |
|------|---------------|
| Initial `match` cert generation | `docs/MATCH_SETUP.md` |
| Device provisioning / UDID | `docs/RELEASE_CHECKLIST.md` |
| `fastlane snapshot` screenshots | (post-MVP) |
| First `fastlane beta` execution | `docs/RELEASE_CHECKLIST.md` |
| TestFlight internal testing | (post-MVP) |

---

## Execution Order (Reordered — MMR Critical Fix)

```
PHASE 0 — DOCUMENTATION (Hard Dependency)
├── docs/SECRETS.md           ← exact secret names, no ambiguity
├── docs/MATCH_SETUP.md       ← exact shell commands for Mac session
└── docs/RELEASE_CHECKLIST.md ← 30-min walkthrough

PHASE 1 — INFRASTRUCTURE
├── fastlane/Fastfile         ← references exact secret names from SECRETS.md
├── fastlane/Appfile
├── fastlane/Matchfile
└── .github/workflows/ios-release.yml ← 90min timeout, concurrency, artifacts

PHASE 2 — STOREKIT & TOOLING (Parallel)
├── StoreKit 2 (Protocol + MockStore + EntitlementManager)
├── tools/generate_design_tokens.py + test_design_tokens.py (schema + diff)
└── Update ios-build.yml validate job

PHASE 3 — METADATA & POLISH
├── design/tokens.json → generate_design_tokens.py
└── fastlane/metadata/en-US/ + vi/ (with VI placeholder notice)

PHASE 4 — VERIFICATION
├── Tag dry-run (v0.0.0-dryrun) → confirm match readonly works
└── Commit, push, CI green
```

---

## Acceptance Criteria

- [ ] `docs/SECRETS.md` exact secret names + source documented
- [ ] `docs/MATCH_SETUP.md` exact `fastlane match` commands (brew install → init → appstore → push → verify readonly)
- [ ] `docs/RELEASE_CHECKLIST.md` walkable in <30 min on Mac
- [ ] `Fastfile` has `beta` lane with `match(type: "appstore", readonly: true)` + write lanes guarded by `ensure_env(env: 'CI')`
- [ ] `ios-release.yml` 90min timeout, concurrency group, artifact upload, pre-flight match readonly
- [ ] `StoreKitService` protocol + MockStore (testable), no CI test job
- [ ] `ios-build.yml` validate job: `xcodegen validate` + `swift build`
- [ ] `design/tokens.json` → `tools/generate_design_tokens.py` with schema validation + diff check
- [ ] `fastlane/metadata/en-US/` populated, `vi/` has placeholder README

---

## ═══════════════════════════════════════════
## INTENTIONAL PRODUCT STRATEGY
## (Turning "Standard Devotional" → "Must-Have")
## ═══════════════════════════════════════════

### The Core Insight
**Every Catholic app has the same content** (readings, saints, prayers). The *content* is a commodity. What makes Anno worth $20/yr is **how the content meets the user in their actual day**.

---

### Intentional Touches (Retention → Conversion)

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

### Monetization Architecture (Conversion → Revenue)

#### 1. Freemium Boundary (The "Aha!" Moment)
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

#### 2. Conversion Triggers (Built into Flow)
| Trigger | Timing | Message |
|---------|--------|---------|
| **Streak milestone** | Day 7, 30, 100 | "30 days of daily prayer. That's a habit. Unlock audio reflections to go deeper." |
| **Feast day open** | On feast tap | "This saint has a beautiful story. Premium unlocks the full 3-min read." |
| **Language toggle** | 2nd VI view | "You're reading in Vietnamese. Premium keeps both languages woven together." |
| **Season start** | Ash Wed / 1st Advent | "Lent begins tomorrow. Premium gives you the daily journey — micro-practices, audio, progress." |
| **Share attempt** | Tap share on free | "Create a beautiful prayer card with art. Premium unlocks export." |

#### 3. Subscription Psychology
- **Annual only at launch** ($19.99) — no monthly churn, higher LTV, simpler messaging ("$1.66/month for daily grace")
- **7-day free trial** — Apple handles, no code needed
- **No "Pro" / "Plus" tiers** — one price, everything. Simplicity = trust.
- **Family Sharing enabled** — one sub = whole household (critical for Catholic families)

#### 4. Retention Mechanics (Post-Subscribe)
| Mechanic | Purpose |
|----------|---------|
| **Streak repair** | 1 free "grace repair" per quarter — reduces churn from guilt |
| **Seasonal re-engagement** | Push: "Lent starts in 3 days. Your journey awaits." |
| **Patron saint anniversary** | "It's your confirmation saint's feast! Here's a special reflection." |
| **Annual renewal nudge** | Day 330: "Your year of daily prayer is almost complete. Renew to keep the streak." |
| **Content freshness** | New saint art / audio each season — "What's new this Advent?" |

---

### Acquisition (Zero-Cost, High-Intent)

| Channel | Asset | Hook |
|---------|-------|------|
| **App Store Search** | Keywords: "Catholic daily readings bilingual", "Vietnamese Catholic app", "liturgical calendar 2026" | EN+VI is a *differentiator* — almost no apps do it well |
| **Parish bulletins** | QR code + one-pager | "Daily readings in English & Vietnamese — free for your parishioners" |
| **Catholic creator collabs** | Guest audio reflection | "Fr. Mike / Sr. Miriam / [your network] records one Advent reflection" |
| **Reddit / Discord** | r/Catholicism, r/VietnameseCatholics | "Built this for my mom who wanted both languages. Free tier is generous." |
| **SEO / Web** | `anno.app` landing page | "The only bilingual daily devotional with liturgical intelligence" |

---

### Metrics That Matter (Instrument from Day 1)

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

### Risks & Mitigations (Product Layer)

| Risk | Mitigation |
|------|------------|
| VI localization quality | Flag clearly as "draft — native review needed"; recruit 1-2 VI beta testers from parish network |
| Audio reflection production | Start with 12 (one per month) — record yourself or AI voice (kokoro) with human review; expand if retention warrants |
| Catholic niche = small TAM | TAM = 70M US Catholics + 7M VI Catholics + global. Niche = loyal, high LTV, low CAC. Own the bilingual lane. |
| Apple rejects "religious" subscription | StoreKit 2 is standard; many Catholic apps (Hallow, Laudate, iBreviary) use subscriptions. Follow their metadata patterns. |
| Content liability (wrong feast/reading) | Calendar engine is deterministic + USCCB-verified. Add disclaimer: "Check your local parish bulletin." |

---

### Next: Build the Infrastructure (This Plan) → Then the Touches

**Infrastructure (this doc):** 7-9 hrs Linux → Mac session = `fastlane beta`
**Intentional layer:** Can be built *after* TestFlight — widgets, audio, push, onboarding flow, paywall UX

**But:** Design the *data model* now for the intentional layer:
- `UserProfile`: name, language_preference, patron_saints[], notification_consent
- `Streak`: current, longest, last_repair_date
- `SeasonalProgress`: season, day, practices_completed[]
- `FeatureFlags`: audio_enabled, vi_enabled, widgets_enabled

Add these to SwiftData models *now* — zero cost, enables everything later.

---

## Estimated Effort

| Phase | Items | Est. Time |
|-------|-------|-----------|
| Docs (SETUP/CHECKLIST/SECRETS) | 0 | 30 min |
| Fastlane + CI release workflow | 1 | 1-2 hrs |
| StoreKit 2 + data model extensions | 2 | 2-3 hrs |
| Update ios-build.yml validate job | 3 | 30 min |
| Design tokens + Python generator + tests | 4 | 1 hr |
| App Store Connect metadata | 5 | 1 hr |
| Verification (dry-run tag) | 6 | 30 min |
| **Total** | | **7-9 hrs** |

All doable on ichabod (Linux). Mac session = MATCH_SETUP.md → fastlane beta.