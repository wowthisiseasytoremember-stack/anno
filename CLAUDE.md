# CLAUDE.md — Anno

**Last Updated:** 2026-08-09 08:38 UTC

## What This Is

Native SwiftUI iOS devotional app. Catholic-first launch, Vietnamese-ready. Monetization target: Hallow-scale freemium (daily content free, premium deep-dive packs + pilgrimage routes paid). Working name: Anno.

## Architecture: Two-Engine + Content Layer

| Layer | What | Where |
|---|---|---|
| Engine A | Deterministic calendar conversion (Python: pyluach, hijri-converter, convertdate). No LLM, no hallucination risk. | `~/Projects/Anno/` |
| Engine B | LLM daily historical research from Engine A output. Outputs structured JSON with source citations. | LLM-backed |
| Layer C | Devotional content generation from Engine B data. "Facts rigorous, framing inspirational." | LLM-backed |

## Key Docs (read before working)

| File | Purpose |
|---|---|
| `AGENTS.md` | Quick-start context and current state |
| `PRD.md` | Full product spec + monetization model |
| `ARCHITECTURE.md` | Invariants and system design |
| `ROADMAP.md` | Delivery phases |
| `STATE.md` | Current session state |
| `MVP_PLAN_FINAL.md` | MVP scope |

## Stack

SwiftUI, StoreKit 2, MapKit, Xcode String Catalogs. Python for Engine A. Xcode + macOS required to build — **ichabod cannot build this; Mac only.**

## Conventions

- Engine A is pure Python — no LLM calls, no hallucination risk. Treat it as ground truth.
- Vietnamese localization is structural from v1. Never hard-code English-only content shapes.
- Interfaith connections only where genuine historical intersection exists.
- Source citations required on all Engine B output.

## Monetization Model

Freemium: daily content free, premium packs (deep dives, pilgrimage routes) via StoreKit 2 IAP.

## Initiative & Relationships

- Standalone `anno` initiative (iOS app, standalone revenue target).
- **Ecosystem Relationship:** Completely standalone consumer app. Does **not** consume from or produce to `content-factory` (name matches like `annotate_beats.py` in `content-factory` are unrelated text tools).
- Shared Primitives: Consumes deterministic calendar conversions from Engine A (`calendar_engine.py`) in this project root.

## Constraints

- Xcode/macOS required for native build. No ichabod-side build step.
- Infrastructure Engine A copy was at `/home/ichabod/01_Infrastructure/Anno/` (archived 2026-08-19); this project root is now canonical.

