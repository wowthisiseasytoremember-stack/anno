# Interfaith Devotional Engine — AGENTS.md
**Last updated:** 2026-07-04

## Quick Start (Read This First)

| What | Where |
|------|-------|
| **Architecture & invariants** | `ARCHITECTURE.md` |
| **Delivery roadmap (phases)** | `ROADMAP.md` |
| **Current context** | Direction changed to native SwiftUI iOS, Catholic-first launch, Vietnamese-ready. Engine A/render artifacts exist in `/home/ichabod/01_Infrastructure/interfaith/` and need reconciliation into this project root before implementation. |

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
- Original render/source bundle lives at `/home/ichabod/01_Infrastructure/interfaith/`
- Engine A and 4-year JSONL exist in the infrastructure bundle and need canonical import
- Working project name: Anno

## Conventions
- Engine A is pure Python, no LLM, no hallucination risk
- Engine B outputs structured JSON with source citations
- Layer C does "framing" — facts rigorous, framing inspirational
- Interfaith connections only where genuine intersection exists
- Native iOS implementation uses SwiftUI, StoreKit 2, MapKit, and Xcode String Catalogs
- Vietnamese localization is structural from v1; do not hard-code English-only content shapes

## Changelog

- 2026-07-03: Added Quick Start and updated status for native SwiftUI/Catholic-first/Vietnamese-ready direction.
