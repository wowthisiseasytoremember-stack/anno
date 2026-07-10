---
title: STATE
state: active
last_active: 2026-07-10
---
# interfaith-devotional — Project State

**Last active:** 2026-07-10

## Current Frontier Artifacts

- Verified Catholic-first mock data exists for 2026-07-03 through 2026-07-16.
- First mock-app week is 2026-07-03 through 2026-07-09.
- Vietnamese UI terms and flat `Localizable.strings` exist.
- `ios-fixtures/AnnoMockData.swift` can be regenerated from JSON with `tools/export_swift_fixture.py`.
- `tools/validate_mock_content.py` validates bilingual copy, calendar conversions, and source coverage.
- Trust-safe monetization guardrails live in `docs/PRIVACY_MONETIZATION_TRUST_SPEC.md`.
- Real-data interactive mock: `visuals/anno-real-week-mock.html`.

## Completed (2026-07-10)

- Engine A fully reconciled from infrastructure bundle at `/home/ichabod/01_Infrastructure/Anno/`
- 3 bugs in infrastructure calendar engine fixed (Ethiopian year, Armenian year, Hebrew year type)
- Both project copies (root + tools/) now match
- Week fixture fixed — points to Jul 3-9 entries, schema validated
- Fortnight fixture extracted from full dataset to `data/mock/`
- `data/mock/` directory created with both fixtures
- `PrivacyInfo.xcprivacy` created — zero-collection, no tracking declared
- `Docs/privacy-policy.md` written
- `Docs/app-store-metadata.md` — full App Store Connect reference template
- `tools/validate_engine_b_output.py` — 12 checks: schema, sources, bilingual, confidence, place, content quality
- `docs/research/anno-research-prompt-main.md` — self-contained per-date Engine B prompt
- `docs/research/anno-research-batch-july17-30.md` — 14 dates ready to fire
- `docs/research/anno-source-validation-gate.md` — verification rubric
- `docs/research/anno-site-survey-plan.md` — MMR-ingested 6-sprint execution plan
- AGENTS.md stale infra path fixed
- ROADMAP.md up to date with checkmarks

## Next Tasks

- **Sprint A (macOS required):** Xcode project scaffold, wire data models, widget target stub
- **Sprint C (Linux):** Fire Engine B research prompts for July 17-30 or full year
- **Engine B research pipeline:** Start with 14-day pilot, then scale to 365-day Catholic liturgical year
