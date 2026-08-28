# Anno — Mac-Free Build Plan (S3/S4 Infrastructure)

**Status:** Post-MMR v6 (all critical findings folded — FINAL EXECUTION PLAN)
**Date:** 2026-08-28
**Branch:** visual-polish
**Author:** GCU No Trouble At All

---

## Goal

Build every artifact needed for TestFlight release **on Linux** — so the next macOS session is a single `fastlane beta_deploy` command that produces a valid TestFlight build.

> **Clarification:** This plan builds *artifacts* (Fastfile, docs, Swift files, workflow YAML) on Linux. The GitHub Actions release workflow **requires macOS runners** and cannot run on Linux. The Linux value is artifact authoring, not CI execution.

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

### 1. Documentation First — Schema for Everything (MMR Fix: Phase 1)
| File | Purpose |
|------|---------|
| `docs/SECRETS.md` | **Exact mapping table:** Fastfile placeholder → GitHub Secret name → Source (ASC / Match / RevenueCat). Include note: "GitHub auto-masks secrets in logs; avoid `echo $SECRET`." |
| `docs/MATCH_SETUP.md` | Mac playbook: exact `fastlane match` commands (brew install → init → appstore → push → verify `readonly: true` works) |
| `docs/RELEASE_CHECKLIST.md` | 30-min Mac session: match init → secrets verify → vi signoff → `fastlane beta_deploy` |
| `docs/VIETNAMESE_REVIEW_SIGNOFF.md` | **Enforced gate** — tracks: reviewer name, date, `vi_review_complete: true`. Release checklist: "Verify this file exists with `vi_review_complete: true` before `beta_deploy`." |

### 2. Fastlane (Default `readonly: true` + Split Lanes — MMR Critical Fix)
| File | Purpose |
|------|---------|
| `fastlane/Fastfile` | **Three lanes:**<br>• `beta_validate` — `match(type: "appstore", readonly: true)` + `gym` (build only, **no pilot**)<br>• `beta_deploy` — `match(type: "appstore", readonly: true)` + `gym` + `pilot(skip_submission: true, skip_waiting_for_build_processing: true)` (upload to TestFlight, **no App Store review trigger**)<br>• `match_appstore` / `match_development` — **guarded by `ENV['MATCH_WRITE'] == '1'`** (write only on Mac, explicit opt-in) |
| `fastlane/Appfile` | App identifier, team ID, Apple ID |
| `fastlane/Matchfile` | `git_url`, `type("appstore")`, `readonly(true)` |
| `fastlane/Gemfile` | `gem "fastlane", "~> 2.225"` — **version pinned** (MMR finding) |
| `fastlane/Gemfile.lock` | **Committed** — ensures deterministic CI bundle install |

**Secrets referenced as placeholders (exact names for SECRETS.md):**
- `MATCH_GIT_URL` — git remote for match repo
- `MATCH_PASSWORD` — match repo encryption password
- `APP_STORE_CONNECT_API_KEY_KEY_ID` — ASC API key ID
- `APP_STORE_CONNECT_API_KEY_ISSUER_ID` — ASC API issuer ID
- `APP_STORE_CONNECT_API_KEY_CONTENT` — raw .p8 file content (NOT base64)
- `FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD` — for `pilot` upload
- `REVENUECAT_API_KEY` — (if using server-side webhooks; SDK public key goes in app bundle)

### 3. RevenueCat Protocol + MockStore (Complete + Linux-Testable — MMR Critical Fix)
| File | Purpose |
|------|---------|
| `Anno/Services/StoreKitProvider.swift` | **Protocol** —<br>`func getOfferings() async throws -> [Offering]`<br>`func getCustomerInfo() async throws -> CustomerInfo`<br>`func purchase(_ package: Package) async throws`<br>`func restorePurchases() async throws` |
| `Anno/Services/StoreService.swift` | **Logic-only service** — no SwiftUI deps. Conforms to `StoreKitProvider`. Injects `StoreKitProvider`. Used by `StoreViewModel`. |
| `Anno/Services/RevenueCatProvider.swift` | Production impl — wraps `Purchases` SDK, conforms to `StoreKitProvider` |
| `Anno/Services/MockStoreProvider.swift` | **Test impl** — in-memory entitlement state, deterministic success/failure, simulates async state transitions, used by Linux `swift test` |
| `Anno/Services/EntitlementManager.swift` | Reads `CustomerInfo.entitlements.active["premium"]?.isActive` — pure Swift, testable on Linux |
| `Anno/ViewModels/StoreViewModel.swift` | **SwiftUI deps here** (`@Observable`, etc.) — injects `StoreService`. **NOT tested on Linux.** |
| `AnnoTests/StoreKitProviderTests.swift` | Tests `StoreService` + `EntitlementManager` + `MockStoreProvider` — **Linux-compatible target** |

**Products (RevenueCat Dashboard → App Store Connect):**
- `anno.subscription.yearly` — $19.99/yr (intro: 7-day free trial)
- `anno.subscription.monthly` — $2.99/mo

**Entitlement:** `premium` (attached to both products)

**Verification command (runs on Linux):**
```bash
swift test --filter StoreKitProviderTests
```

### 4. GitHub Actions — Release Workflow (Tag-Gated + Safety Order — MMR Critical Fix)
| File | Purpose |
|------|---------|
| `.github/workflows/ios-release.yml` | **Single job `release`** on `macos-latest` (90 min timeout) |

**Tag gating (ORDER MATTERS — MMR Fix):**
```yaml
# 1. Dry-run FIRST (most specific)
- if: github.ref == 'refs/tags/v*-dryrun'
  run: fastlane beta_validate
# 2. Semver deploy SECOND
- if: github.ref == 'refs/tags/v[0-9]+.[0-9]+.[0-9]+'
  run: fastlane beta_deploy
```

**Job: release** (sequential steps):
```yaml
- checkout
- xcodegen generate
- actions/cache: ~/Library/Developer/Xcode/DerivedData + SPM cache
- bundle install (fastlane/Gemfile)
- fastlane beta_validate  # dry-run tags
- fastlane beta_deploy    # semver tags
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

**Default `readonly: true` in all deployment lanes** — write only with `MATCH_WRITE=1`.

### 5. CI/CD — Update Existing Build Workflow + macOS Integration Test
| File | Change |
|------|--------|
| `.github/workflows/ios-build.yml` | Add `validate` **step** in existing job: `xcodegen generate` → `xcodegen validate` → `xcodebuild -analyze` |
| `.github/workflows/ios-release.yml` | Add **separate `test:storekit` job** on `macos-latest`: `swift test --filter StoreKitProviderTests` + RevenueCat SDK integration smoke test (runs on semver tags only) |

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
| First `fastlane beta_deploy` execution | `docs/RELEASE_CHECKLIST.md` |
| TestFlight internal testing | (post-MVP) |

---

## Execution Order (Schema First, Then Parallel)

```
PHASE 1 — SCHEMA & DOCUMENTATION (Unblocks Everything)
├── docs/SECRETS.md            ← exact mapping table (Fastfile placeholder → GitHub Secret → Source)
├── docs/MATCH_SETUP.md        ← exact shell commands
├── docs/RELEASE_CHECKLIST.md  ← 30-min walkthrough + vi signoff gate
└── docs/VIETNAMESE_REVIEW_SIGNOFF.md ← reviewer, date, vi_review_complete: true

PHASE 2 — PARALLEL ARTIFACT AUTHORSHIP (Linux)
├── fastlane/Fastfile          ← beta_validate, beta_deploy (readonly default), guarded write lanes
├── fastlane/Appfile
├── fastlane/Matchfile
├── fastlane/Gemfile           ← "gem \"fastlane\", \"~> 2.225\""
├── fastlane/Gemfile.lock      ← commit this
├── StoreKitProvider.swift     ← protocol (with getOfferings)
├── StoreService.swift         ← logic-only, no SwiftUI
├── RevenueCatProvider.swift   ← production
├── MockStoreProvider.swift    ← test impl (async state transitions)
├── EntitlementManager.swift   ← pure Swift
├── StoreViewModel.swift       ← SwiftUI deps, injects StoreService
├── StoreKitProviderTests.swift ← swift test --filter StoreKitProviderTests
├── .github/workflows/ios-release.yml (single job, tag gating ORDER: dryrun first, cache, concurrency, pilot config)
└── Update ios-build.yml validate step (generate → validate → analyze)

PHASE 3 — METADATA
├── fastlane/metadata/en-US/
└── fastlane/metadata/vi/README.md

PHASE 4 — VERIFICATION (Executable)
├── [Linux] swift test --filter StoreKitProviderTests → MUST PASS
├── [CI] git tag v0.0.0-dryrun && git push origin v0.0.0-dryrun
│   └── Verify: ios-release.yml starts, runs beta_validate, match readonly + gym succeed (no upload)
├── [CI] Confirm: NO TestFlight build created from dry-run
├── [CI] git tag v1.0.0 && git push origin v1.0.0
│   └── Verify: ios-release.yml starts, runs beta_deploy, test:storekit job runs, TestFlight build uploaded
└── [Mac] Run RELEASE_CHECKLIST.md → fastlane beta_deploy (if CI skipped)
```

---

## Acceptance Criteria (Executable)

| Phase | Verification Command | Expected Result |
|-------|---------------------|-----------------|
| Schema | `ls docs/SECRETS.md docs/MATCH_SETUP.md` | Both exist |
| Fastlane | `cd fastlane && bundle exec fastlane --version` | `fastlane 2.225.x` |
| Gemfile.lock | `git ls-files fastlane/Gemfile.lock` | Tracked |
| StoreKit tests | `swift test --filter StoreKitProviderTests` | All pass on Linux |
| ios-release.yml (dry-run) | `git tag v0.0.0-dryrun && git push origin v0.0.0-dryrun` | Workflow triggers, `beta_validate` runs, match readonly + gym succeed, **no pilot upload** |
| ios-release.yml (deploy) | `git tag v1.0.0 && git push origin v1.0.0` | Workflow triggers, `beta_deploy` runs, `test:storekit` job runs, TestFlight build uploaded |
| SECRETS.md | `grep -c "MATCH_GIT_URL\|APP_STORE_CONNECT_API_KEY_KEY_ID\|MATCH_PASSWORD" docs/SECRETS.md` | ≥ 6 mappings |
| VI signoff | `cat docs/VIETNAMESE_REVIEW_SIGNOFF.md | grep "vi_review_complete: true"` | Returns line |
| Tag safety | Push `v1.0.0-dryrun` → verify `beta_validate` runs, NOT `beta_deploy` | Correct lane |

---

## Estimated Effort

| Phase | Items | Est. Time |
|-------|-------|-----------|
| Schema + docs | 1 | 45 min |
| Parallel artifact authorship | 2 | 4 hrs |
| Metadata | 3 | 45 min |
| Verification (dry-run + Mac) | 4 | 1 hr |
| **Total** | | **~6.5 hrs** |

All doable on ichabod (Linux). Mac session = `MATCH_SETUP.md` → verify `VIETNAMESE_REVIEW_SIGNOFF.md` → `fastlane beta_deploy`.