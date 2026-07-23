# Interfaith Devotional Engine — AGENTS.md
**Last updated:** 2026-07-04

## Quick Start (Read This First)

| What | Where |
|------|-------|
| **Architecture & invariants** | `ARCHITECTURE.md` |
| **Delivery roadmap (phases)** | `ROADMAP.md` |
| **Current context** | Direction changed to native SwiftUI iOS, Catholic-first launch, Vietnamese-ready. Engine A reconciled (bugs in infra copy fixed). Week fixture fixed. Privacy compliance files created. Source validation gate written. MMR-ingested execution plan at `docs/research/anno-site-survey-plan.md`. Next: Xcode project scaffold (macOS required). |

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
- Original render/source bundle lives at `/home/ichabod/01_Infrastructure/Anno/`
- Engine A and 4-year JSONL exist in the infrastructure bundle and infrastructure bundle — reconciled and bugs fixed on both project copies (root + tools/)
- Working project name: Anno

## Conventions
- Engine A is pure Python, no LLM, no hallucination risk
- Engine B outputs structured JSON with source citations
- Layer C does "framing" — facts rigorous, framing inspirational
- Interfaith connections only where genuine intersection exists
- Native iOS implementation uses SwiftUI, StoreKit 2, MapKit, and Xcode String Catalogs
- Vietnamese localization is structural from v1; do not hard-code English-only content shapes

## Changelog

- 2026-07-10: Engine A fully reconciled. Week fixture fixed. PrivacyInfo.xcprivacy + privacy policy created. App Store metadata template written. Source validation gate script written (tools/validate_engine_b_output.py). Research prompts for Engine B written (docs/research/). MMR-ingested execution plan written. Stale infra path fixed.
