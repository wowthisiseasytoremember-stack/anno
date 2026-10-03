---
schema: agents-md/v1
project: interfaith-devotional
initiative: monetization
family: apps
what: >-
  Native SwiftUI iOS app (working name "Anno") that pairs deterministic
  multi-calendar date conversion with sourced historical research and a
  Catholic-first devotional content layer. v1 scope: Calendar engine (12 systems),
  GPS pilgrimage routes (5 flagship: Jerusalem, Rome, Santiago, La Vang, Guadalupe),
  daily EN-primary devotional content (VI for 8 major feasts only).
  Removed from v1: AR Reliquary, Spatial Audio, Interfaith layer.
goal: >-
  Scaffold the Xcode project (requires macOS), maintain the content pipeline,
  and keep the master 182-day unified dataset normalized into the Swift fixture
  schema. Content for Jul 3–Dec 31 2026 is EN-primary (VI for 8 major feasts).
  Monetization: Free tier (calendar + basic devotional) + Premium $49.99/yr
  (5 flagship pilgrimage routes + full liturgical content + devotional deep-dives).
status: active
stack: [swift, swiftui, python]
entrypoints:
  - calendar_engine.py
modules:
  - name: Engine A — calendar conversion
    path: calendar_engine.py
    does: Deterministic Gregorian/Hebrew/Hijri conversion; pure Python, no LLM.
  - name: Engine B output gate
    path: tools/validate_engine_b_output.py
    does: Validates LLM research output and its source citations before use.
  - name: Swift fixture export
    path: tools/export_swift_fixture.py
    does: Exports calendar engine output as fixtures for the iOS target.
  - name: Content normalizer
    path: tools/normalize_fixture.py
    does: Concats fortnight, Engine B July/Sep-Dec, and August tracks into Anno/Resources/anno_unified_2026.json (182 days), aligns schema, guarantees 100% *_vi leaves for key feasts.
  - name: Localization
    path: ios/LocalizationManager.swift
    does: Swift localization manager backing the Vietnamese-ready content shape (key feasts only).
  - name: iOS Client Application
    path: Anno/
    does: SwiftUI mobile app implementing Today, Calendar, Map (pilgrimage), and Saved views.
updated: 2026-10-03 00:30 UTC
---

# Interfaith Devotional Engine — AGENTS.md
**Last updated:** 2026-10-03 00:00 UTC

## Quick Start (Read This First)

| What | Where |
|------|-------|
| **Architecture & invariants** | `ARCHITECTURE.md` |
| **Delivery roadmap (phases)** | `ROADMAP.md` |
| **Current context** | v1 scope: Catholic-first devotional + deterministic 12-calendar engine + GPS pilgrimage routes (5 flagship: Jerusalem Via Dolorosa, Rome Seven Churches, Santiago de Compostela, La Vang Vietnam, Guadalupe Mexico). Removed from v1: AR Reliquary, Spatial Audio, Interfaith layer, 18 routes → 5 flagship. VI reduced to 8 major feasts only (Christmas, Easter, Pentecost, Assumption, Immaculate Conception, Divine Mercy, Christ the King, Epiphany). Monetization: Free + Premium $49.99/yr (2 tiers). GTM: Vietnamese diaspora channels (Lang Viet orgs, VietCatholic media, parish referrals). Editorial gate for LLM content: **known risk — no human gate in v1; family/community validation only**. LLM pipeline continues for Day 183+. Next: Xcode project scaffolding & build sweep on macOS (CI via GitHub Actions). |

## Project
Native SwiftUI iOS sacred-history app with deterministic multi-calendar conversion + sourced historical research + Catholic-first content layer. Working name: Anno. v1 = Calendar (12 systems) + Pilgrimage (5 flagship routes) + Devotional (EN-primary, VI for 8 major feasts).

## Architecture: Two-Engine + Content Layer
- **Engine A** (Python): deterministic calendar conversion — pyluach, hijri-converter, convertdate
- **Engine B** (LLM): daily historical research from Engine A output
- **Layer C** (LLM): devotional content generation from Engine B structured data

## Root
`~/Projects/interfaith-devotional/`

## Setup Context
- PRD landed at `PRD.md`
- Required architecture doc exists at `ARCHITECTURE.md`
- Product bible and handoff docs live in `docs/`
- Original render/source bundle was at `/home/ichabod/01_Infrastructure/Anno/` (now archived to `/home/ichabod/07_Backups/Anno_infrastructure_archive_2026-08-19/Anno/`); key artifacts reconciled into this project root
- Engine A and 4-year JSONL exist in this project root (reconciled from archived infra bundle)
- Working project name: Anno

## Conventions
- Engine A is pure Python, no LLM, no hallucination risk
- Engine B outputs structured JSON with source citations
- Layer C does "framing" — facts rigorous, framing inspirational
- Interfaith connections only where genuine intersection exists (v1: Catholic-only; interfaith deferred)
- Native iOS implementation uses SwiftUI, StoreKit 2, MapKit, and Xcode String Catalogs
- Vietnamese localization: VI for 8 major feasts only (Christmas, Easter, Pentecost, Assumption, Immaculate Conception, Divine Mercy, Christ the King, Epiphany); EN-primary for all other days

## Ecosystem & Relationships
- **Content Factory:** Standalone app. Independent monetization app; does not consume or produce content-factory pipelines.
- **Engine A Shared Primitive:** Consumes `calendar_engine.py` (in this project root; infra copy archived).

## Known Risks (v1)
- **LLM content without human editorial gate** — family/community validation only; no theologian reviewer. Reputational risk for Catholic audience. Mitigation: source validation gates strict; confidence=disputed for uncertain entries; **VI reduced to 8 major feasts to minimize surface area**.
- **No iOS build yet** — requires macOS/Xcode. CI pipeline (GitHub Actions macOS) configured for future.
- **Vietnamese diaspora GTM unproven** — Lang Viet orgs / VietCatholic media outreach untested; no guaranteed conversion rate.
- **5 flagship routes** — may feel thin vs. competitor "unlimited" content; must execute depth (offline maps, audio, deep history) not breadth.

## Changelog

- 2026-10-03: v1 scope narrowed — removed AR Reliquary, Spatial Audio, Interfaith layer to archive/v1-removed/. Pricing collapsed to Free + Premium $49.99/yr. Added MIT LICENSE. Engine A calendar bugs fixed (JDN, Islamic epoch, Julian boundaries, PDT/PST). Normalization pipeline fail-closed. Engine B ALLOWLIST backfill removed; inline source validation added.
- 2026-08-24: Integrated ReliquaryExplorer multiplatform (iOS/visionOS) AR viewer and PilgrimCore package. Implemented SacredSpatialAudioEngine for distance-based acoustic bloom and cathedral reverberation. Wired 3D AR buttons and audio triggers across SacredSiteMapView and TodayView. Authored comprehensive README.md and engineering specifications.
- 2026-08-24: Integrated SoCal Vietnamese Catholic Pilgrimage (Christ Cathedral La Vang, St. Columban, St. Barbara), Major Asian Martyr Corridors, Eucharistic Miracles, and Desert Monastic routes into 18 linear routes (106 waypoints) + 72 singular sanctuaries in `sacred_geography_master.json`. Upgraded `SacredSiteMapView.swift` with evocative spiritual inquiry header ("Whose path will you walk today?"), liturgical temporal proximity matching, spiritual calling filters, and regional curation.
- 2026-08-24: Executed complete autonomous research, bilingual composition, coordinate verification, and schema validation for the Anno Global Sacred Geography and Pilgrimage Catalog (72 singular sanctuaries & shrines in `SacredSanctuaries/`, 14 linear pilgrimage corridors with 69 waypoints in `PilgrimageRoutes/`, and master compiled catalog `sacred_geography_master.json`). 100% schema validation gates passing.
- 2026-08-24: Completed Phase A (182 continuous days of bilingual Catholic historical content Jul 3–Dec 31 2026 with >=2 sources per entry; 365-day devotional pool) and Phase B (StoreKit 2 config, EntitlementService, 4 bilingual pilgrimage routes, 65 sacred art dossiers). All validation gates passing 100%.
- 2026-08-10: Executed orientation recovery audit. Formally mapped project to monetization/apps initiative. Restored broken uncommitted changes in AnnoMockData.swift. Confirmed lack of Vietnamese translations in August 2026 mock data as the next target task.
- 2026-08-09: Connection work order audited and confirmed. Formally documented Anno as a standalone monetizable native SwiftUI app independent of content-factory. Updated CLAUDE.md and AGENTS.md frontmatter.
- 2026-07-10: Engine A fully reconciled. Week fixture fixed. PrivacyInfo.xcprivacy + privacy policy created. App Store metadata template written. Source validation gate script written (tools/validate_engine_b_output.py). Research prompts for Engine B written (docs/research/). MMR-ingested execution plan written. Stale infra path fixed.
