# Anno — Mac-Free Build Plan (S3/S4 Infrastructure)

**Status:** Post-MMR v5 (all critical findings folded — final execution plan)
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

### 1. Fastlane (Placeholders First + Split Lanes — MMR Critical Fix)
| File | Purpose |
|------|---------|
| `fastlane/Fastfile` | **Three lanes:**<br>• `beta_validate` — `match(type: "appstore", readonly: true)` + `gym` (build only, **no pilot**)<br>• `beta_deploy` — `match(type: "appstore", readonly: true)` + `gym` + `pilot` (upload to TestFlight)<br>• `match_appstore` / `match_development` — **guarded by `ensure_env(env: 'CI')`** (write only on Mac) |
| `fastlane/Appfile` | App identifier, team ID, Apple ID |
| `fastlane/Matchfile` | `git_url`, `type("appstore")`, `readonly(true)` |
| `fastlane/Gemfile` | `gem "fastlane", "~> 2.225"` — **version pinned** (MMR finding)<br>**Commit `fastlane/Gemfile.lock`** to repo |
| `fastlane/Gemfile.lock` | Committed — ensures deterministic CI bundle install |

**Secrets referenced as placeholders (exact names for SECRETS.md):**
- `MATCH_GIT_URL` — git remote for match repo
- `MATCH_PASSWORD` — match repo encryption password
- `APP_STORE_CONNECT_API_KEY_KEY_ID` — ASC API key ID
- `APP_STORE_CONNECT_API_KEY_ISSUER_ID` — ASC API issuer ID
- `APP_STORE_CONNECT_API_KEY_CONTENT` — raw .p8 file content (NOT base64)
- `FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD` — for `pilot` upload
- `REVENUECAT_API_KEY` — (if using server-side webhooks; SDK public key goes in app bundle)

### 2. RevenueCat Protocol + MockStore (Testable on Linux — MMR Critical Fix)
| File | Purpose |
|------|---------|
| `Anno/Services/StoreKitProvider.swift` | **Protocol** — `func getCustomerInfo() async throws -> CustomerInfo`, `func purchase(_ package: Package) async throws`, `func restorePurchases() async throws` |
| `Anno/Services/RevenueCatProvider.swift` | Production impl — wraps `Purchases` SDK, conforms to `StoreKitProvider` |
| `Anno/Services/MockStoreProvider.swift` | **Test impl** — in-memory entitlement state, deterministic success/failure, used by Linux `swift test` |
| `Anno/Services/EntitlementManager.swift` | Reads `CustomerInfo.entitlements.active["premium"]?.isActive` — pure Swift, testable on Linux |
| `Anno/ViewModels/StoreViewModel.swift` | UI-facing: packages, purchase, restore, error handling — injects `StoreKitProvider` |
| `AnnoTests/StoreKitProviderTests.swift` | Tests `EntitlementManager` + `StoreViewModel` with `MockStoreProvider` |

**Products (RevenueCat Dashboard → App Store Connect):**
- `anno.subscription.yearly` — $19.99/yr (intro: 7-day free trial)
- `anno.subscription.monthly` — $2.99/mo

**Entitlement:** `premium` (attached to both products)

**Verification command (runs on Linux):**
```bash
swift test --filter StoreKitProviderTests
```

### 3. GitHub Actions — Release Workflow (Tag-Gated — MMR Critical Fix)
| File | Purpose |
|------|---------|
| `.github/workflows/ios-release.yml` | **Single job `release`** on `macos-latest` (90 min timeout) |

**Tag gating:**
- `v*-dryrun` tags → run `beta_validate` lane (match + gym, no upload)
- `v[0-9]+.[0-9]+.[0-9]+` semver tags → run `beta_deploy` lane (full upload)

**Job: release** (sequential steps):
```yaml
- checkout
- xcodegen generate
- actions/cache: ~/Library/Developer/Xcode/DerivedData + SPM cache
- bundle install (fastlane/Gemfile)
- if: github.ref matches 'v*-dryrun' → fastlane beta_validate
- if: github.ref matches 'v[0-9]+.[0-9]+.[0-9]+' → fastlane beta_deploy
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

**No pre-flight match step** — `fastlane beta_validate` / `beta_deploy` handle it.

### 4. CI/CD — Update Existing Build Workflow
| File | Change |
|------|--------|
| `.github/workflows/ios-build.yml` | Add `validate` **step** in existing job: `xcodegen generate` → `xcodegen validate` → `xcodebuild -analyze` (MMR: ordering dependency) |

### 5. Documentation (After Fastlane Placeholders)
| File | Purpose |
|------|---------|
| `docs/SECRETS.md` | **Exact mapping table:** Fastfile placeholder → GitHub Secret name → Source (ASC / Match / RevenueCat). Include note: "GitHub auto-masks secrets in logs; avoid `echo $SECRET`." |
| `docs/MATCH_SETUP.md` | Mac playbook: exact `fastlane match` commands (brew install → init → appstore → push → verify `readonly: true` works) |
| `docs/RELEASE_CHECKLIST.md` | 30-min Mac session: match init → secrets verify → `fastlane beta_deploy` |
| `docs/VIETNAMESE_REVIEW_SIGNOFF.md` | **Enforced gate** — tracks: reviewer name, date, `vi_review_complete: true` (MMR finding). Release checklist: "Verify this file exists with `vi_review_complete: true` before `beta_deploy`." |

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

## Execution Order (Parallel Where Possible)

```
PHASE 1 — PARALLEL ARTIFACT AUTHORSHIP (Unblocks Everything)
├── fastlane/Fastfile          ← beta_validate, beta_deploy, guarded write lanes
├── fastlane/Appfile
├── fastlane/Matchfile
├── fastlane/Gemfile           ← "gem \"fastlane\", \"~> 2.225\""
├── fastlane/Gemfile.lock      ← commit this
├── StoreKitProvider.swift     ← protocol
├── RevenueCatProvider.swift   ← production
├── MockStoreProvider.swift    ← test impl
├── EntitlementManager.swift   ← pure Swift
├── StoreViewModel.swift       ← injects StoreKitProvider
├── StoreKitProviderTests.swift ← swift test --filter StoreKitProviderTests
├── .github/workflows/ios-release.yml (single job, tag gating, cache, concurrency)
└── Update ios-build.yml validate step (generate → validate → analyze)

PHASE 2 — DOCUMENTATION (Maps to Placeholders)
├── docs/SECRETS.md            ← exact mapping table
├── docs/MATCH_SETUP.md        ← exact shell commands
├── docs/RELEASE_CHECKLIST.md  ← 30-min walkthrough + vi signoff gate
└── docs/VIETNAMESE_REVIEW_SIGNOFF.md ← reviewer, date, vi_review_complete: true

PHASE 3 — METADATA
├── fastlane/metadata/en-US/
└── fastlane/metadata/vi/README.md

PHASE 4 — VERIFICATION (Executable — MMR Fix)
├── [Linux] swift test --filter StoreKitProviderTests → MUST PASS
├── [CI] git tag v0.0.0-dryrun && git push origin v0.0.0-dryrun
│   └── Verify: ios-release.yml starts, runs beta_validate, match readonly + gym succeed (no upload)
├── [CI] Confirm: NO TestFlight build created from dry-run
└── [Mac] Run RELEASE_CHECKLIST.md → fastlane beta_deploy on semver tag (e.g., v1.0.0)
```

---

## Acceptance Criteria (Executable — MMR Fix)

| Phase | Verification Command | Expected Result |
|-------|---------------------|-----------------|
| Fastlane | `cd fastlane && bundle exec fastlane --version` | `fastlane 2.225.x` |
| Gemfile.lock | `git ls-files fastlane/Gemfile.lock` | Tracked |
| StoreKit tests | `swift test --filter StoreKitProviderTests` | All pass on Linux |
| ios-release.yml (dry-run) | `git tag v0.0.0-dryrun && git push origin v0.0.0-dryrun` | Workflow triggers, `beta_validate` runs, match readonly + gym succeed, **no pilot upload** |
| ios-release.yml (deploy) | `git tag v1.0.0 && git push origin v1.0.0` | Workflow triggers, `beta_deploy` runs, TestFlight build uploaded |
| SECRETS.md | `grep -c "MATCH_GIT_URL\|APP_STORE_CONNECT_API_KEY_KEY_ID\|MATCH_PASSWORD" docs/SECRETS.md` | ≥ 6 mappings |
| VI signoff | `cat docs/VIETNAMESE_REVIEW_SIGNOFF.md | grep "vi_review_complete: true"` | Returns line |

---

## Estimated Effort

| Phase | Items | Est. Time |
|-------|-------|-----------|
| Parallel artifact authorship | 1 | 4 hrs |
| Documentation | 2 | 30 min |
| Metadata | 3 | 45 min |
| Verification (dry-run + Mac) | 4 | 1 hr |
| **Total** | | **~6 hrs** |

All doable on ichabod (Linux). Mac session = `MATCH_SETUP.md` → verify `VIETNAMESE_REVIEW_SIGNOFF.md` → `fastlane beta_deploy`.