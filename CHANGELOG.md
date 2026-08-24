# CHANGELOG — Anno

## [Unreleased] - 2026-08-24

### Content Pipeline & Master Dataset Expansion (Phase A)
- **Primary Source Citation Backfill:** Created `tools/backfill_citations.py` and populated >=2 verified, high-authority liturgical/historical source citations across all fortnight and August entries.
- **Engine B September–December Expansion (122 Days):** Created `tools/batch_generate_engine_b.py` and generated daily historical research dossiers and sibling Vietnamese files for 2026-09-01 through 2026-12-31 based on the General Roman Calendar 2026 and multi-calendar math.
- **Master 182-Day Unified Dataset:** Upgraded `tools/normalize_fixture.py` and compiled `Anno/Resources/anno_unified_2026.json` to 182 continuous days (July 3, 2026 – December 31, 2026) with 100% complete Vietnamese fields and zero validation errors.
- **Swift Mock Data Exporter:** Updated `tools/export_swift_fixture.py` and regenerated `ios-fixtures/AnnoMockData.swift` with the full 182-day dataset.
- **365-Day Devotional Pool:** Created `Anno/Resources/anno_devotional_pool_365.json` with 365 bilingual daily meditations across 12 spiritual seasons (Thomas à Kempis, Francis de Sales, Augustine, Brother Lawrence, Montfort, and Scripture), accompanied by `tools/validate_devotional_pool.py` and `Anno/Models/Devotional.swift`.

### Monetization Assets & Schemas (Phase B)
- **StoreKit 2 Configuration:** Created `Anno/Configuration/AnnoProducts.storekit` defining Day Pass ($1.99 non-consumable), Premium Annual ($49.99/yr), Premium Monthly ($4.99/mo), Pilgrim Annual ($79.99/yr), and Pilgrim Monthly ($9.99/mo).
- **Product Metadata & Paywall Triggers:** Added `Anno/Resources/product_metadata.json` and `Anno/Resources/paywall_triggers.json` formalizing client trigger rules for archive access, routes, audio, and spiritual bouquets.
- **Entitlement Service:** Created `Anno/Services/EntitlementService.swift` with StoreKit 2 transaction listeners, tier states, preview mock overrides, and paywall view bindings.
- **Pilgrimage Route Packs:** Defined `docs/PILGRIMAGE_ROUTE_SCHEMA.md` and authored 4 bilingual route packs in `Anno/Resources/PilgrimageRoutes/` (Rome 7 Churches, Holy Land Passion, European Marian Shrines, Vietnam Shrines) validated with `tools/validate_route_coordinates.py`.
- **Sacred Art Dossiers Catalog:** Curated 65 verified public-domain masterpieces in `Anno/Resources/ArtDossiers/art_dossiers_catalog.json` with bilingual theological commentary and verified HTTP reachability via `tools/verify_artwork_links.py`.
- **Localization Expansion:** Expanded `localization/en/Localizable.strings` and `localization/vi/Localizable.strings` to 63 keys with 100.0% coverage verified by `tools/validate_localization.py`.

### Verification & 2027-2028 Handoff Preparation (2026-08-24)
- **Verification pass (PASS):** Engine A `test_calendar_engine.py` 10/10 on ichabod (covers 2026-2030); Engine B gate `validate_engine_b_output.py` confirmed working. 8 corrupted Vietnamese (U+FFFD) leaves in Aug-2026 entries repaired at source and regenerated into `anno_unified_2026.json` (182 entries, 0 U+FFFD) and `AnnoMockData.swift`.
- **New validators:** Added `tools/validate_vietnamese_integrity.py` (flags U+FFFD / empty `_vi`) and an `artwork.source_url` `example.com` rejection in `validate_engine_b_output.py`.
- **2027-2028 seed catalog:** `data/seed/anno_seed_2027_2028.json` — 731 days (2027-01-01→2028-12-31) with liturgical rank/color/title + 5 calendar conversions, via `multi_proper_calendar_resolver` + `computus_engine`.
- **Self-contained third-party handoff:** `docs/research/HANDOFF_BRIEF.md` (no FS access required) + 24 monthly packets `docs/research/handoff/2027-01.md…2028-12.md` + `docs/research/handoff_manifest.yaml` tracker.
- **Ingestion pipeline:** `tools/ingest_2027_2028.py` merges seed + returned research into `anno_unified_2027_2028.json` (guarantees 100% `_vi`); end-to-end dry-run passed the gate (exit 0) and ingested cleanly.
- Branch `work/verify-2027-2028`; full detail in `VERIFICATION_REPORT.md`.

## [Unreleased] - 2026-08-10

### Documentation & Repository Health
- Executed orientation recovery audit and verified project state.
- Discovered and discarded a broken, uncommitted modification to `ios-fixtures/AnnoMockData.swift` that left the file in a syntactically invalid state (ending in a dangling `static let augustJSON = #`). This restores compile safety to the Swift files.
- Updated `AGENTS.md` frontmatter with `initiative: monetization` and `family: apps` to match the canonical `~/plans/initiatives.yml` mapping.
- Added "iOS Client Application" to the modules list in the `AGENTS.md` frontmatter.
- Audited the untracked August 2026 mock data batch (`data/mock/anno_august_2026.json`) and confirmed that all 31 entries are missing Vietnamese translations, setting up a clear future content generation task.

## [Unreleased] - 2026-08-09

### Documentation & Ecosystem Relationships
- Executed connection work order auditing project relationship to `content-factory`.
- Confirmed ground truth: `Anno` is a standalone monetizable native SwiftUI iOS Catholic/interfaith devotional app.
- Clarified that `Anno` does not consume from or produce into `content-factory` pipelines (keyword overlaps like `annotate_beats.py` are unrelated).
- Updated `/home/ichabod/Projects/Anno/CLAUDE.md` and `/home/ichabod/Projects/Anno/AGENTS.md` to reflect ecosystem status, shared primitives (`calendar_engine.py`), and updated timestamps.
