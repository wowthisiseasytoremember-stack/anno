# Anno — Mac-Free Build Plan (S3/S4 Infrastructure)

**Status:** Post-MMR v4 (all critical findings folded)
**Date:** 2026-08-28
**Branch:** visual-polish
**Author:** GCU No Trouble At All

---

## Goal

Build every artifact needed for TestFlight release **on Linux** — so the next macOS session is a single `fastlane beta` command that produces a valid TestFlight build.

> **Clarification (MMR):** This plan builds *artifacts* (Fastfile, docs, Swift files, workflow YAML) on Linux. The GitHub Actions release workflow **requires macOS runners** and cannot run on Linux. The Linux value is artifact authoring, not CI execution.

**Target:** Anno iOS app (Catholic daily devotional, EN/VI, StoreKit 2 subscription via RevenueCat)

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

**Architecture:** Single Xcode project (no SPM split).

---

## What We Build on Linux

### 1. Fastlane (Placeholders First — MMR Order Fix)
| File | Purpose |
|------|---------|
| `fastlane/Fastfile` | **Primary lane:** `beta` (TestFlight, `match(type: "appstore", readonly: true)`). **Write lanes:** `match_appstore`, `match_development` — **guarded by `ensure_env(env: 'CI')`**. **Remove** redundant `match` pre-flight steps — `fastlane beta` handles match internally (MMR finding). |
| `fastlane/Appfile` | App identifier, team ID, Apple ID |
| `fastlane/Matchfile` | `git_url`, `type("appstore")`, `readonly(true)` |
| `fastlane/Gemfile` | **Only `gem "fastlane"`** — match is in core, no plugins needed (MMR finding) |

**Secrets referenced as placeholders (exact names for SECRETS.md):**
- `MATCH_GIT_URL` — git remote for match repo
- `MATCH_PASSWORD` — match repo encryption password
- `APP_STORE_CONNECT_API_KEY_KEY_ID` — ASC API key ID
- `APP_STORE_CONNECT_API_KEY_ISSUER_ID` — ASC API issuer ID
- `APP_STORE_CONNECT_API_KEY_CONTENT` — raw .p8 file content (NOT base64)
- `FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD` — for `pilot` upload
- `REVENUECAT_API_KEY` — (if using server-side webhooks; SDK public key goes in app bundle)

### 2. Documentation (After Fastlane Placeholders)
| File | Purpose |
|------|---------|
| `docs/SECRETS.md` | **Exact mapping table:** Fastfile placeholder → GitHub Secret name → Source (ASC / Match / RevenueCat). Include note: "GitHub auto-masks secrets in logs; avoid `echo $SECRET`." |
| `docs/MATCH_SETUP.md` | Mac playbook: exact `fastlane match` commands (brew install → init → appstore → push → verify `readonly: true` works) |
| `docs/RELEASE_CHECKLIST.md` | 30-min Mac session: match init → secrets verify → `fastlane beta` |

### 3. GitHub Actions — Release Workflow (Single Job — MMR Critical Fix)
| File | Purpose |
|------|---------|
| `.github/workflows/ios-release.yml` | **Single job `release`** on `macos-latest` (90 min timeout) |

**Job: release** (sequential steps, no artifact passing):
```yaml
- checkout
- xcodegen generate
- actions/cache: ~/Library/Developer/Xcode/DerivedData + SPM cache
- bundle install (fastlane/Gemfile)
- fastlane beta  # runs gym (build) + pilot (upload) + match (readonly) internally
```

**Concurrency:** `group: release, cancel-in-progress: true`

**Env vars (standard fastlane — MMR Finding):**
```yaml
APP_STORE_CONNECT_API_KEY_KEY_ID
APP_STORE_CONNECT_API_KEY_ISSUER_ID
APP_STORE_CONNECT_API_KEY_CONTENT  # raw .p8
MATCH_GIT_URL
MATCH_PASSWORD
FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD
REVENUECAT_API_KEY  # if webhooks used
```

**No pre-flight match step** — `fastlane beta` handles it (MMR finding).

### 4. StoreKit 2 — RevenueCat with Protocol/Mock (MMR Critical Fix)
| Decision | Rationale |
|----------|-----------|
| **RevenueCat SDK** | Cross-platform, handles grace period / billing retry / family sharing server-side, dashboard for product config |
| **Protocol + MockStore** | Enables `swift test` on Linux — CI regression testing for subscription logic |

**Files:**
| File | Purpose |
|------|---------|
| `Anno/Services/StoreKitProvider.swift` | **Protocol** — `func getCustomerInfo() async throws -> CustomerInfo`, `func purchase(_ package: Package) async throws`, `func restorePurchases() async throws` |
| `Anno/Services/RevenueCatProvider.swift` | Production impl — wraps `Purchases` SDK, conforms to `StoreKitProvider` |
| `Anno/Services/MockStoreProvider.swift` | **Test impl** — in-memory entitlement state, deterministic success/failure, used by Linux `swift test` |
| `Anno/Services/EntitlementManager.swift` | Reads `CustomerInfo.entitlements.active["premium"]?.isActive` — pure Swift, testable on Linux |
| `Anno/ViewModels/StoreViewModel.swift` | UI-facing: packages, purchase, restore, error handling — injects `StoreKitProvider` |

**Products (RevenueCat Dashboard → App Store Connect):**
- `anno.subscription.yearly` — $19.99/yr (intro: 7-day free trial)
- `anno.subscription.monthly` — $2.99/mo

**Entitlement:** `premium` (attached to both products)

**Test target:** `AnnoTests/StoreKitProviderTests.swift` — tests `EntitlementManager` + `StoreViewModel` with `MockStoreProvider`

### 5. CI/CD — Update Existing Build Workflow
| File | Change |
|------|--------|
| `.github/workflows/ios-build.yml` | Add `validate` **step** (not separate job) in existing job: `xcodegen generate` → `xcodegen validate` → `xcodebuild -analyze` (MMR: ordering dependency) |

### 6. App Store Connect Metadata (Minimal Viable)
| File | Purpose |
|------|---------|
| `fastlane/metadata/en-US/description.txt` | 4000 char |
| `fastlane/metadata/en-US/keywords.txt` | 100 char |
| `fastlane/metadata/en-US/release_notes.txt` | "Initial release" |
| `fastlane/metadata/en-US/support_url.txt` | |
| `fastlane/metadata/en-US/marketing_url.txt` | |
| `fastlane/metadata/vi/README.md` | **"DO NOT SUBMIT — needs native Vietnamese speaker review before TestFlight"** |

**Skip for now:** Design tokens, widgets, audio, push, onboarding paywall — all post-TestFlight (see `plans/anno-intentional-product-strategy.md`)

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

## Execution Order (Clean, Unblocked)

```
PHASE 1 — FASTLANE PLACEHOLDERS (Unblocks Everything)
├── fastlane/Fastfile          ← beta lane (readonly match), write lanes guarded, NO pre-flight match
├── fastlane/Appfile
├── fastlane/Matchfile
└── fastlane/Gemfile           ← ONLY "gem \"fastlane\""

PHASE 2 — REVENUECAT PROTOCOL + MOCK (Testable on Linux)
├── StoreKitProvider.swift     ← protocol
├── RevenueCatProvider.swift   ← production
├── MockStoreProvider.swift    ← test impl
├── EntitlementManager.swift   ← pure Swift
├── StoreViewModel.swift       ← injects StoreKitProvider
└── StoreKitProviderTests.swift ← swift test on Linux

PHASE 3 — CI/CD RELEASE WORKFLOW (Single Job)
├── .github/workflows/ios-release.yml (single release job, cache, concurrency)
└── Update ios-build.yml validate step (xcodegen generate → validate → analyze)

PHASE 4 — DOCUMENTATION (Maps to Placeholders)
├── docs/SECRETS.md            ← exact secret ↔ placeholder mapping table
├── docs/MATCH_SETUP.md        ← exact shell commands
└── docs/RELEASE_CHECKLIST.md  ← 30-min walkthrough

PHASE 5 — METADATA
├── fastlane/metadata/en-US/
└── fastlane/metadata/vi/README.md

PHASE 6 — VERIFICATION
├── Tag dry-run (v0.0.0-dryrun) → confirm match readonly + build + deploy
└── Commit, push, CI green
```

---

## Acceptance Criteria

- [ ] `fastlane/Fastfile` has `beta` lane with `match(type: "appstore", readonly: true)` + write lanes guarded by `ensure_env(env: 'CI')` + no pre-flight match step
- [ ] `fastlane/Gemfile` has **only** `gem "fastlane"`
- [ ] `docs/SECRETS.md` exact mapping table (Fastfile placeholder → GitHub Secret name → Source)
- [ ] `docs/MATCH_SETUP.md` exact `fastlane match` commands + verify readonly step
- [ ] `docs/RELEASE_CHECKLIST.md` walkable in <30 min
- [ ] `ios-release.yml`: **single `release` job**, caching (DerivedData + SPM), 90min, concurrency group, no artifact passing
- [ ] `StoreKitProvider.swift` + `RevenueCatProvider.swift` + `MockStoreProvider.swift` + `EntitlementManager.swift` + `StoreViewModel.swift` implemented
- [ ] `StoreKitProviderTests.swift` passes on Linux (`swift test`)
- [ ] `ios-build.yml` validate: `xcodegen generate` → `xcodegen validate` → `xcodebuild -analyze` (sequential steps in same job)
- [ ] `fastlane/metadata/en-US/` populated, `vi/` has placeholder README
- [ ] Dry-run tag passes end-to-end

---

## Estimated Effort

| Phase | Items | Est. Time |
|-------|-------|-----------|
| Fastlane placeholders | 1 | 45 min |
| RevenueCat protocol + mock + tests | 2 | 2.5 hrs |
| CI/CD release workflow (single job + cache) | 3 | 1 hr |
| Documentation | 4 | 30 min |
| Metadata | 5 | 45 min |
| Verification (dry-run) | 6 | 30 min |
| **Total** | | **~6 hrs** |

All doable on ichabod (Linux). Mac session = `MATCH_SETUP.md` → `fastlane beta`.