# Anno — Mac-Free Build Plan (S3/S4 Infrastructure)

**Status:** Post-MMR v1 (yellow → green fold)
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

**Architecture decision (post-MMR):** Keep single Xcode project. Do NOT split into multiple SPM packages — current structure is fine.

---

## What We Can Build on Linux

### 1. Fastlane Complete Setup
| File | Purpose |
|------|---------|
| `fastlane/Fastfile` | Lanes: `beta` (TestFlight), `release` (App Store), `match_appstore`, `match_development` |
| `fastlane/Appfile` | App identifier, team ID, Apple ID |
| `fastlane/Matchfile` | Git URL for certs repo, type (appstore), readonly mode for CI |

**Key design:** `match(type: "appstore", readonly: true)` on CI — certs in a private git repo, CI pulls them, signs, uploads.

### 2. GitHub Actions — Release Workflow
| File | Purpose |
|------|---------|
| `.github/workflows/ios-release.yml` | Trigger: tag push (`v*`) or manual dispatch → `xcodegen` → `fastlane beta` → TestFlight |

**Runner:** `macos-latest` (GitHub-hosted, **90 min timeout** — post-MMR fold)

**Concurrency:** `group: release, cancel-in-progress: false` — only one release at a time

**Step timing annotations:** Each step has `name:` for failure identification

### 3. StoreKit 2 — Complete Implementation
| File | Purpose |
|------|---------|
| `Anno/Services/StoreKitService.swift` | Protocol `StoreProvider` + `ProductionStore` (iOS) + `MockStore` (Linux-testable) |
| `Anno/Services/EntitlementManager.swift` | Verifies subscription status, caches, handles grace period |
| `Anno/Services/TransactionListener.swift` | Background task for `Transaction.updates` |
| `Anno/ViewModels/StoreViewModel.swift` | UI-facing: products, purchase, restore, error handling |

**NO Package.swift refactor** (post-MMR fold) — keep single Xcode project. Testability via `StoreProvider` protocol + `MockStore`.

**Products (App Store Connect):**
- `anno.subscription.yearly` — $19.99/yr (intro: 7-day free trial)
- `anno.subscription.monthly` — $2.99/mo

**Tests:** Merge into existing `ios-build.yml` workflow as a separate `swift test` job on `macos-latest` (post-MMR fold — no separate `swift-test.yml`).

### 4. Design System (Tokens → Swift)
| File | Purpose |
|------|---------|
| `design/tokens.json` | Colors, spacing, typography, icons — single source |
| `tools/generate_design_tokens.py` | **Python script** (post-MMR fold — not Swift) reads tokens → emits `Anno/Design/Color+Theme.swift`, `Font+Theme.swift` |
| `Anno/Design/` | Generated SwiftUI modifiers — zero runtime cost |

### 5. App Store Connect Metadata
| File | Purpose |
|------|---------|
| `fastlane/metadata/en-US/description.txt` | 4000 char limit |
| `fastlane/metadata/en-US/keywords.txt` | 100 char limit |
| `fastlane/metadata/en-US/release_notes.txt` | Per version |
| `fastlane/metadata/en-US/support_url.txt` | |
| `fastlane/metadata/en-US/marketing_url.txt` | |
| `fastlane/metadata/vi/...` | Vietnamese localization (mirror EN) |

**Skip:** Screenshots generation — needs Simulator (`fastlane snapshot`). Placeholder directory only.

### 6. CI/CD Enhancements
| File | Purpose |
|------|---------|
| Update `.github/workflows/ios-build.yml` | Add `test` job: `xcodebuild test` on macos-latest |
| `.github/dependabot.yml` | Auto-update GitHub Actions |

### 7. Documentation / Handoff (CRITICAL — post-MMR)
| File | Purpose |
|------|---------|
| `docs/MATCH_SETUP.md` | Step-by-step: create private certs repo, init match on Mac, set GitHub secrets, verify with `fastlane match appstore --readonly` |
| `docs/RELEASE_CHECKLIST.md` | Mac session checklist: 1) match init 2) secrets verify 3) `fastlane beta` |
| `docs/STOREKIT_SETUP.md` | App Store Connect product config, subscription group |
| `docs/SECRETS.md` | Exact GitHub secret names + how to obtain each value |

---

## Out of Scope (Mac / Physical Device Required)

| Item | Why | Documented in |
|------|-----|---------------|
| Initial `match` cert generation | Apple Developer Portal login + keychain | `docs/MATCH_SETUP.md` |
| Device provisioning / UDID | Xcode / Apple Configurator | `docs/RELEASE_CHECKLIST.md` |
| `fastlane snapshot` screenshots | Needs Simulator + `xcrun simctl` | (post-MVP) |
| First `fastlane beta` execution | Codesign + notary + upload | `docs/RELEASE_CHECKLIST.md` |
| TestFlight internal testing | App Store Connect UI | (post-MVP) |

---

## GitHub Secrets Required (Documented in `docs/SECRETS.md`)

| Secret | Source | Required |
|--------|--------|----------|
| `MATCH_GIT_URL` | Private certs repo (created on Mac once) | ✅ |
| `MATCH_PASSWORD` | Encryption passphrase for certs repo (set during `match init`) | ✅ |
| `APP_STORE_CONNECT_API_KEY_ID` | App Store Connect → Users → Keys | ✅ |
| `APP_STORE_CONNECT_API_ISSUER_ID` | Same | ✅ |
| `APP_STORE_CONNECT_API_KEY_BASE64` | `.p8` file base64-encoded | ✅ |
| `FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD` | appleid.apple.com → App-Specific Passwords | ✅ |

**Pre-flight verification step** (post-MMR fold): `fastlane match appstore --readonly` dry-run in release workflow before full build.

---

## Execution Order

```
1. docs/SECRETS.md + docs/MATCH_SETUP.md + docs/RELEASE_CHECKLIST.md
       ↓
2. Fastlane configs (Fastfile, Appfile, Matchfile)
       ↓
3. .github/workflows/ios-release.yml (90min timeout, concurrency group, step timing)
       ↓
4. StoreKit 2 (StoreProvider protocol + ProductionStore + MockStore + EntitlementManager)
       ↓
5. Update ios-build.yml: add test job (no separate workflow)
       ↓
6. Design tokens (tokens.json + generate_design_tokens.py)
       ↓
7. App Store Connect metadata (EN + VI)
       ↓
8. Verification: ios-release.yml dry-run on dummy tag → confirm match readonly works
```

---

## Acceptance Criteria

- [ ] `docs/MATCH_SETUP.md` exact steps documented
- [ ] `docs/SECRETS.md` lists every secret name + source
- [ ] `docs/RELEASE_CHECKLIST.md` walkable in <30 min on Mac
- [ ] `Fastfile` has `beta` lane with `match(type: "appstore", readonly: true)`
- [ ] `ios-release.yml` runs on tag push with 90min timeout + concurrency group
- [ ] `StoreKitService` has protocol + MockStore (unit-testable)
- [ ] `ios-build.yml` test job passes (if tests exist)
- [ ] `design/tokens.json` → `tools/generate_design_tokens.py` produces Swift files
- [ ] `fastlane/metadata/en-US/` + `vi/` populated

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| `match` git URL / permissions wrong | Documented exactly in MATCH_SETUP.md; CI dry-run before full build |
| 90 min insufficient for full pipeline | step-level timing annotations identify bottleneck |
| macOS runner queue time | Concurrency group = one release at a time, predictable |
| StoreKit 2 API changes (iOS 18+) | Pin to iOS 17+ minimum; test on device ASAP |
| App Store Connect metadata rejection | Follow HIG; pre-fill all required fields |

---

## Estimated Effort

| Phase | Items | Est. Time |
|-------|-------|-----------|
| Docs (SETUP/CHECKLIST/SECRETS) | 1 | 30 min |
| Fastlane + CI release workflow | 2 | 1-2 hrs |
| StoreKit 2 + tests | 3 | 2-3 hrs |
| Update ios-build.yml + tests job | 4 | 30 min |
| Design tokens + Python generator | 5 | 30 min |
| App Store Connect metadata | 6 | 1 hr |
| Verification (dry-run tag) | 7 | 30 min |
| **Total** | | **7-9 hrs** |

All doable on ichabod (Linux). Mac session = MATCH_SETUP.md → fastlane beta.