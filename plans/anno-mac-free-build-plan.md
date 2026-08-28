# Anno — Mac-Free Build Plan (S3/S4 Infrastructure)

**Status:** Post-MMR v3 (clean, focused)
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

**Architecture:** Single Xcode project (no SPM split).

---

## What We Build on Linux

### 1. Fastlane (Placeholders First — MMR Order Fix)
| File | Purpose |
|------|---------|
| `fastlane/Fastfile` | Lanes: `beta` (TestFlight, readonly match), `release` (App Store), `match_appstore` (write, Mac-only), `match_development` (write, Mac-only) — **write lanes guarded by `ensure_env(env: 'CI')`** |
| `fastlane/Appfile` | App identifier, team ID, Apple ID |
| `fastlane/Matchfile` | `git_url`, `type("appstore")`, `readonly(true)` |
| `fastlane/Gemfile` | Fastlane + plugins (prevents 'missing gem' on fresh runners) — **MMR finding** |

**Secrets referenced as placeholders:** `MATCH_GIT_URL`, `MATCH_PASSWORD`, `APP_STORE_CONNECT_API_KEY_KEY_ID`, `APP_STORE_CONNECT_API_KEY_ISSUER_ID`, `APP_STORE_CONNECT_API_KEY_CONTENT` (raw .p8), `FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD`

### 2. Documentation (After Fastlane Placeholders)
| File | Purpose |
|------|---------|
| `docs/SECRETS.md` | Exact GitHub secret names + source (maps to Fastfile placeholders) |
| `docs/MATCH_SETUP.md` | Mac playbook: exact `fastlane match` commands (brew install → init → appstore → push → verify readonly) |
| `docs/RELEASE_CHECKLIST.md` | 30-min Mac session: match init → secrets verify → `fastlane beta` |

### 3. GitHub Actions — Release Workflow (Split Jobs — MMR Finding)
| File | Purpose |
|------|---------|
| `.github/workflows/ios-release.yml` | **Two jobs**: `build` (heavy) + `deploy` (fastlane) |

**Job: build** (`macos-latest`, 60 min timeout)
- Checkout + `actions/cache` for `~/Library/Developer/Xcode/DerivedData` + SPM cache
- `xcodegen generate`
- `xcodebuild build-for-testing -scheme Anno -destination 'generic/platform=iOS' -archivePath build/Anno.xcarchive`
- Upload `.xcarchive` as artifact

**Job: deploy** (`macos-latest`, 30 min timeout, needs: build)
- Download `.xcarchive` artifact
- `fastlane beta` (uses `match readonly`, uploads to TestFlight)
- **Pre-flight:** `fastlane match appstore --readonly --verbose` before build step

**Concurrency:** `group: release, cancel-in-progress: true`

**Env vars (standard fastlane — MMR Finding):**
```yaml
APP_STORE_CONNECT_API_KEY_KEY_ID
APP_STORE_CONNECT_API_KEY_ISSUER_ID
APP_STORE_CONNECT_API_KEY_CONTENT  # raw .p8, NOT base64
MATCH_GIT_URL
MATCH_PASSWORD
FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD
```

### 4. StoreKit 2 — Use RevenueCat (MMR Finding)
| Decision | Rationale |
|----------|-----------|
| **RevenueCat SDK** | Cross-platform, handles grace period / billing retry / family sharing server-side, dashboard for product config without Mac, testable on Linux via mock |
| **No custom StoreProvider / MockStore** | Eliminates untestable custom wrapper; RevenueCat tests pass in CI |

**Files:**
| File | Purpose |
|------|---------|
| `Anno/Services/RevenueCatService.swift` | Thin wrapper: `Purchases.configure`, `getCustomerInfo`, `purchasePackage`, `restorePurchases` |
| `Anno/Services/EntitlementManager.swift` | Reads `CustomerInfo.entitlements.active` — pure Swift, testable on Linux |
| `Anno/ViewModels/StoreViewModel.swift` | UI-facing: packages, purchase, restore, error handling |

**Products (RevenueCat Dashboard → App Store Connect):**
- `anno.subscription.yearly` — $19.99/yr (intro: 7-day free trial)
- `anno.subscription.monthly` — $2.99/mo

**Entitlement:** `premium` (attached to both products)

### 5. CI/CD — Update Existing Build Workflow
| File | Change |
|------|--------|
| `.github/workflows/ios-build.yml` | Add `validate` job: `xcodegen validate` + `xcodebuild -analyze` (catches real compilation errors) |

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
├── fastlane/Fastfile          ← write lanes guarded, read lanes use placeholder secret names
├── fastlane/Appfile
├── fastlane/Matchfile
└── fastlane/Gemfile

PHASE 2 — DOCUMENTATION (Maps to Placeholders)
├── docs/SECRETS.md            ← exact secret names matching Fastfile
├── docs/MATCH_SETUP.md        ← exact shell commands
└── docs/RELEASE_CHECKLIST.md  ← 30-min walkthrough

PHASE 3 — CI/CD RELEASE WORKFLOW
├── .github/workflows/ios-release.yml (build + deploy jobs, cache, concurrency)
└── Update ios-build.yml validate job

PHASE 4 — REVENUECAT + ENTITLEMENTS
├── RevenueCatService.swift
├── EntitlementManager.swift
├── StoreViewModel.swift
└── (No CI test job — RevenueCat tested via dashboard)

PHASE 5 — METADATA
├── fastlane/metadata/en-US/
└── fastlane/metadata/vi/README.md

PHASE 6 — VERIFICATION
├── Tag dry-run (v0.0.0-dryrun) → confirm match readonly + build + deploy
└── Commit, push, CI green
```

---

## Acceptance Criteria

- [ ] `fastlane/Fastfile` has `beta` lane with `match(type: "appstore", readonly: true)` + write lanes guarded by `ensure_env(env: 'CI')`
- [ ] `fastlane/Gemfile` exists with `fastlane` + plugins
- [ ] `docs/SECRETS.md` exact secret names matching Fastfile
- [ ] `docs/MATCH_SETUP.md` exact `fastlane match` commands + verify readonly step
- [ ] `docs/RELEASE_CHECKLIST.md` walkable in <30 min
- [ ] `ios-release.yml`: 2 jobs (build + deploy), caching, 90min total, concurrency group, pre-flight match readonly
- [ ] `RevenueCatService.swift` + `EntitlementManager.swift` + `StoreViewModel.swift` implemented
- [ ] `ios-build.yml` validate job: `xcodegen validate` + `xcodebuild -analyze`
- [ ] `fastlane/metadata/en-US/` populated, `vi/` has placeholder README
- [ ] Dry-run tag passes end-to-end

---

## Estimated Effort

| Phase | Items | Est. Time |
|-------|-------|-----------|
| Fastlane placeholders | 1 | 45 min |
| Documentation | 2 | 30 min |
| CI/CD release workflow (2 jobs + cache) | 3 | 1.5 hrs |
| RevenueCat integration | 4 | 2 hrs |
| Metadata | 5 | 45 min |
| Verification (dry-run) | 6 | 30 min |
| **Total** | | **~6 hrs** |

All doable on ichabod (Linux). Mac session = MATCH_SETUP.md → fastlane beta.