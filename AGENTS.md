---
schema: agents-md/v1
project: Anno
initiative: monetization
family: apps
what: >-
  Native SwiftUI iOS app (working name "Anno") that pairs deterministic
  multi-calendar date conversion with sourced historical research and a
  Catholic-first devotional content layer, with Vietnamese localization
  structural from v1.
goal: >-
  Scaffold the Xcode project (requires macOS), maintain the bilingual
  content pipeline, and keep the master 182-day unified dataset normalized into
  the Swift fixture schema. Content for Jul 3–Dec 31 2026 is 100% bilingual (EN/VI) with full sources.
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
    does: Concats fortnight, Engine B July/Sep-Dec, and August tracks into Anno/Resources/anno_unified_2026.json (182 days), aligns schema, guarantees 100% *_vi leaves.
  - name: Localization
    path: ios/LocalizationManager.swift
    does: Swift localization manager backing the Vietnamese-ready content shape.
  - name: iOS Client Application
    path: Anno/
    does: SwiftUI mobile app implementing Today, Calendar, Map, and Saved views.
updated: 2026-08-24 03:50 UTC
---

# Interfaith Devotional Engine — AGENTS.md
**Last updated:** 2026-08-24 03:50 UTC

## Quick Start (Read This First)

| What | Where |
|------|-------|
| **Architecture & invariants** | `ARCHITECTURE.md` |
| **Delivery roadmap (phases)** | `ROADMAP.md` |
| **Current context** | Direction changed to native SwiftUI iOS, Catholic-first launch, Vietnamese-ready. Standalone monetizable app (not part of content-factory). Phase A (Server-side content expansion & 182-day archive) and Phase B (StoreKit 2, Pilgrimage routes, High-res art dossiers, Paywall triggers, Global Sacred Geography master catalog of 72 sanctuaries + 14 pilgrimage routes) 100% complete and verified on Linux. Next: Xcode project scaffolding & build sweep on macOS. |

## Project
Native SwiftUI iOS sacred-history app with deterministic multi-calendar conversion + sourced historical research + Catholic-first content layer + later Sacred Context/interfaith expansion. Working name: Anno.

## Architecture: Two-Engine + Content Layer
- **Engine A** (Python): deterministic calendar conversion — pyluach, hijri-converter, convertdate
- **Engine B** (LLM): daily historical research from Engine A output
- **Layer C** (LLM): devotional content generation from Engine B structured data

## Root
`~/Projects/Anno/`

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
- Interfaith connections only where genuine intersection exists
- Native iOS implementation uses SwiftUI, StoreKit 2, MapKit, and Xcode String Catalogs
- Vietnamese localization is structural from v1; do not hard-code English-only content shapes

## Ecosystem & Relationships
- **Content Factory:** Standalone app. Independent monetization app; does not consume or produce content-factory pipelines.
- **Engine A Shared Primitive:** Consumes `calendar_engine.py` (in this project root; infra copy archived).

## Changelog

- 2026-08-24: Executed complete autonomous research, bilingual composition, coordinate verification, and schema validation for the Anno Global Sacred Geography and Pilgrimage Catalog (72 singular sanctuaries & shrines in `SacredSanctuaries/`, 14 linear pilgrimage corridors with 69 waypoints in `PilgrimageRoutes/`, and master compiled catalog `sacred_geography_master.json`). 100% schema validation gates passing.
- 2026-08-24: Completed Phase A (182 continuous days of bilingual Catholic historical content Jul 3–Dec 31 2026 with >=2 sources per entry; 365-day devotional pool) and Phase B (StoreKit 2 config, EntitlementService, 4 bilingual pilgrimage routes, 65 sacred art dossiers). All validation gates passing 100%.
- 2026-08-10: Executed orientation recovery audit. Formally mapped project to monetization/apps initiative. Restored broken uncommitted changes in AnnoMockData.swift. Confirmed lack of Vietnamese translations in August 2026 mock data as the next target task.
- 2026-08-09: Connection work order audited and confirmed. Formally documented Anno as a standalone monetizable native SwiftUI app independent of content-factory. Updated CLAUDE.md and AGENTS.md frontmatter.
- 2026-07-10: Engine A fully reconciled. Week fixture fixed. PrivacyInfo.xcprivacy + privacy policy created. App Store metadata template written. Source validation gate script written (tools/validate_engine_b_output.py). Research prompts for Engine B written (docs/research/). MMR-ingested execution plan written. Stale infra path fixed.
