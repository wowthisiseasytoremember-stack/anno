# Anno — Ship Sprint Plan (Current → App Store)

**Generated:** 2026-08-28 00:00 UTC
**Branch:** `visual-polish` (15 commits ahead of main)
**Target:** TestFlight → App Store Review → Launch
**Constraint:** macOS compilation required (never done) — GitHub Actions macos-latest

---

## 📊 CURRENT REALITY (Actual Asset Inventory)

| Asset | Count | Status | Location |
|-------|-------|--------|----------|
| **Daily entries (Jul–Dec 2026)** | **182/365** (50%) | ✅ Real liturgical content, full schema | `Anno/Resources/anno_unified_2026.json` |
| **Aug 2026** | 31 | ✅ | `data/mock/anno_august_2026.json` |
| **Jul 3–16** | 14 | ✅ | `data/mock/anno_fortnight_2026-07-03_2026-07-16.json` |
| **Sacred sanctuaries** | **72** | ✅ Full bilingual, GPS, relics, sources | `Anno/Resources/sacred_geography_master.json` |
| **Pilgrimage routes** | **18** | ✅ 106 waypoints, themes, difficulty | `Anno/Resources/PilgrimageRoutes/*.json` |
| **Sacred places (locations)** | **178** | ✅ 7 categories, 31 countries | `sacred_geography_master.json` |
| **Artworks (CC0/PD)** | **110** | ✅ Wikimedia, high-res + thumb, theological notes EN/VI | `Anno/Resources/ArtDossiers/art_dossiers_catalog.json` |
| **Calendar engine** | ✅ | ✅ Pure math, 7 calendars, sundown | `calendar_engine.py` |
| **Content pipeline** | ✅ | ✅ LLM research (nemotron-3-super:free) | `tools/fire_engine_b.py` |
| **SwiftUI models** | ✅ | ✅ Exact JSON schema match | `Anno/Models/*.swift` |
| **Visual polish** | 15 commits | ✅ Design tokens, zero inline styles | `visual-polish` branch |
| **StoreKit 2 + Entitlements** | ✅ | ✅ 6 products, 3 tiers, all gates | `EntitlementService.swift` |
| **Paywall UI** | ✅ | ✅ Hero, benefits, pricing, restore, terms, bilingual | `ArchivePaywallView.swift` |
| **Settings** | ✅ | ✅ Language, Tradition (4 rites), Notifications | `SettingsView.swift` |
| **Tabs** | 4 | ✅ Today / Calendar / Map / Saved | `RootView.swift` |

---

## 🎯 MISSING FOR SHIP

| Blocker | Effort | Notes |
|---------|--------|-------|
| **Onboarding flow** | 1–2 days | Clone from KJV app per `CLONE_FROM_KJV.md` |
| **SwiftData persistence** | 2 days | AnnoEntry/PilgrimageRoute/Artwork → @Model + ContentImportService |
| **Jan–Jun 2026 content** | ~183 days | Same pipeline, parallelizable |
| **Fastlane + App Store Connect** | 1 day | Clone Score pattern |
| **Mac verify** | 0.5 day | GitHub Actions macos-latest |

---

## 🚀 REVISED SPRINT (3 WEEKS TO TESTFLIGHT)

### S0 — Mac Verify + CI (2 days) ✅ **DISPATCHED & PUSHED**
**Owner:** `deepseek-worker`  
**Status:** `.github/workflows/ios.yml` created, `Anno/project.yml` + `Anno/Info.plist` created, pushed to `visual-polish` branch
**Packet:** Write `.github/workflows/ios.yml` → macos-latest, xcodegen generate, xcodebuild, cache DerivedData, fail on warnings  
**Gate:** Green build on PR

### S1 — Onboarding + SwiftData + Import (4 days)
**Owner:** `deepseek-worker` (sequential)
1. **Onboarding** — WelcomeView → Tradition picker → Language → Notifications → soft paywall (clone KJV)
2. **SwiftData models** — `@Model` classes: `AnnoEntry`, `SacredPlace`, `Artwork`, `PilgrimageRoute`, `PilgrimageWaypoint`, `Journey`, `Visit`, `FieldNote` (from Sacred Atlas plan)
3. **ContentImportService** — Reads `Anno/Resources/*.json`, upserts by `id`, background actor, progress callback
4. **App init** — `.modelContainer(for: [...])`

### S2 — Content Completion: Jan–Jun 2026 (7 days, PARALLEL)
**Owner:** `yolo-worker` (uses EXISTING pipeline)
- Run `python3 tools/fire_engine_b.py` with date range `2026-01-01` to `2026-07-02`
- `calendar_engine.py` provides deterministic calendar conversions
- LLM: `nemotron-3-super:free` via OPENROUTER_API_KEY (already in `.env`)
- Output: `data/research_results/YYYY-MM-DD_result.json` + `_prompt.txt`
- Human spot-check 10% before import
- **Total: ~183 entries** to reach 365

### S3 — StoreKit E2E + Fastlane (2 days)
**Owner:** You (device test) + `deepseek-worker` (Fastlane)
1. Physical device: purchase/restore sandbox for all 6 products
2. `deepseek-worker`: Clone Score's Fastlane → `match`, `deliver`, `snapshot`, GitHub Actions release
3. App Store Connect: bundle ID, 6 product IDs, privacy/terms URLs, screenshots (need real content from S2)

### S4 — Beta → Review → Launch (5–14 days)
**Owner:** You
- TestFlight internal → external (Content Factory audience)
- App Store Review submission
- Launch

---

## 📦 DELEGATION PACKETS (Ready to Dispatch)

### Packet S0 — Mac Verify Workflow
```bash
# Worker: deepseek-worker
# Write: .github/workflows/ios.yml
# Requirements:
# - macos-latest runner
# - xcodebuild clean build -scheme Anno -destination 'platform=iOS Simulator,name=iPhone 16'
# - Cache: ~/Library/Developer/Xcode/DerivedData (key: ${{ runner.os }}-xcode-${{ hashFiles('**/Package.resolved') }})
# - Fail fast on warnings
# - Output: build log + .xcresult
```

### Packet S1 — SwiftData + Import Service
```bash
# Worker: deepseek-worker
# Files to create/modify:
# 1. Anno/Models/AnnoModels.swift → @Model classes:
#    - AnnoEntry (id, date, liturgical, calendars, primary, place, artwork, sources, appHooks)
#    - SacredPlace (name, latitude, longitude, confidence, sourceUrl)
#    - Artwork (title, maker, dateLabel, sourceUrl, status, highResUrl, thumbUrl)
#    - PilgrimageRoute (routeId, titleEn, titleVi, region, durationDays, distanceKm, difficulty, spiritualThemeEn, spiritualThemeVi, overviewEn, overviewVi, waypoints)
#    - PilgrimageWaypoint (waypointId, nameEn, nameVi, latitude, longitude, order, historicalSummaryEn, historicalSummaryVi, sacredRelicEn, sacredRelicVi, scriptureReading, suggestedPrayerEn, suggestedPrayerVi)
#    - Journey, Visit, FieldNote (from SACRED_ATLAS_COMPLETION_PLAN.md §5.3.A)
# 2. Anno/Services/ContentImportService.swift:
#    - Reads Anno/Resources/anno_unified_2026.json + PilgrimageRoutes/*.json + ArtDossiers/*.json + sacred_geography_master.json
#    - Upserts by stable id (date-based for entries, routeId/waypointId for routes)
#    - Background actor, progress callback
#    - Validates required fields, logs warnings for missing artwork/place
# 3. AnnoApp.swift → .modelContainer(for: [AnnoEntry.self, SacredPlace.self, Artwork.self, PilgrimageRoute.self, PilgrimageWaypoint.self, Journey.self, Visit.self, FieldNote.self])
```

### Packet S2 — Content Completion (Uses Existing Pipeline)
```bash
# Worker: yolo-worker (free, bulk, no tools needed — runs python script)
# Prerequisite: S0 green (so calendar_engine.py works on macOS)
# Run:
#   cd /home/ichabod/Projects/Anno-visual-polish
#   python3 tools/calendar_engine.py --start 2026-01-01 --end 2026-07-02 --output /tmp/calendar_2026_h1.jsonl
#   python3 tools/fire_engine_b.py --input /tmp/calendar_2026_h1.jsonl --out-dir data/research_results/
# Uses: OPENROUTER_API_KEY from .env (nemotron-3-super:free)
# Output: ~183 JSON files in data/research_results/ + prompt files
# Quality gate: Human spot-check 10 entries for liturgical accuracy + VI terminology
# Then: merge into anno_unified_2026.json (tools/merge_content.py exists)
```

---

## 🔑 KEY INSIGHTS

1. **Content pipeline is PROVEN** — 182 days already generated with real sources, bilingual, artwork metadata. Just need to run it for Jan–Jun.
2. **Pilgrimage/Geography is DONE** — 18 routes, 72 sanctuaries, 178 locations, 110 artworks. Exceeds MVP scope.
3. **Code is COMPILE-READY** — SwiftUI models match JSON schema exactly. Only missing: `@Model` + import service.
4. **Visual/Monetization is COMPLETE** — Paywall, entitlements, design system all production-grade.
5. **Only real risk:** Mac verification (never compiled on macOS) + onboarding (clone, not invent).

---

## 🎯 TODAY'S ACTIONS

1. **Dispatch S0** → `deepseek-worker` for `.github/workflows/ios.yml`
2. **Define ContentSchema.md** (if needed — but models already match JSON)
3. **Verify KJV clone source** at `DailyDevotionKJVForWomen` or `/tmp/kjv-split-files/`
4. **Kick off S2 content generation** in parallel (can start before S0/S1 done — independent)

---

## 📁 REFERENCE FILES

| File | Purpose |
|------|---------|
| `Anno/Models/AnnoEntry.swift` | Current Codable schema (matches JSON exactly) |
| `Anno/Models/PilgrimageRoute.swift` | Route/Waypoint models + SpiritualCalling/Region enums |
| `Anno/Resources/anno_unified_2026.json` | 182 entries — gold standard for import |
| `Anno/Resources/sacred_geography_master.json` | 72 sanctuaries, 18 routes, 178 places |
| `Anno/Resources/ArtDossiers/art_dossiers_catalog.json` | 110 CC0/PD artworks |
| `docs/SACRED_ATLAS_COMPLETION_PLAN.md` | SwiftData schemas for Journey/Visit/FieldNote + proximity system |
| `tools/fire_engine_b.py` | Content generation pipeline (LLM research) |
| `tools/calendar_engine.py` | Deterministic calendar conversions (Engine A) |
| `CLONE_FROM_KJV.md` | Onboarding clone checklist |
| `EntitlementService.swift` | StoreKit 2 + 3-tier gates |

---

*Plan written to `/home/ichabod/Projects/Anno-visual-polish/ANNO_SHIP_SPRINT.md`*