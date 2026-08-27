---
title: STATE
state: active
last_active: 2026-08-24
---
# interfaith-devotional — Project State

**Last active:** 2026-08-24

## Current Frontier Artifacts

- **Unified bilingual devotional dataset** (`Anno/Resources/anno_unified_2026.json`): 182 entries spanning 2026-07-03 → 2026-12-31, EN+VI, normalized from three source tracks (fortnight / Engine B / August) by `tools/normalize_fixture.py`. 182/182 entries have ≥2 sources. Regenerated Swift fixture `ios-fixtures/AnnoMockData.swift` consumes it.
- **Engine A**: deterministic calendar conversion (12 systems) — `test_calendar_engine.py` 10/10 passing on ichabod (covers 2026-2030).
- **Engine B**: Catholic research complete 2026-07-17 → 2026-12-31 (137 EN + 137 VI `result*.json` files). Raw research results have no top-level `sources` key; `validate_engine_b_output.py --fixture` is meant to run on the *normalized* unified fixture (which carries sources), NOT raw `data/research_results/*_result.json`. VN (`*_vi`) filled for all via `_result_vi.json` siblings + August 217-field VN pass.
- **Localization**: EN/VI `Localizable.strings` 100% coverage (63/63 keys) verified.
- **Validators**: `validate_mock_content.py`, `validate_localization.py`/`_infra.py`, `validate_sanctuaries.py`, `validate_route_coordinates.py`, `validate_devotional_pool.py`, `validate_vietnamese_integrity.py`, `test_swift_geography_decodable.py`, `red_team_stress_test.py` all PASS. `validate_audio_narration.py` fixed (prayer-* IDs now valid).
- **Normalizer**: `tools/normalize_fixture.py` unifies the three content tracks into `anno_unified_2026.json` (182 entries).

## Completed (2026-08-19)

- August 2026 mock: 217 `*_vi` fields filled (31 entries) — folded into `data/mock/anno_august_2026.json`.
- Engine B 07-17→07-30: all 14 dates researched via live API (`tools/fire_engine_b.py` + `tools/fire_engine_b_2730.py`), VN pass complete.
- Three content tracks normalized into one Swift-fixture-ready dataset (`anno_unified_2026.json`).
- `export_swift_fixture.py` re-pointed at unified fixture; added `bodyVi` to decoder; derives week list from first 7 entries.
- `validate_engine_b_output.py` repaired (single-entry shape).
- `tools/normalize_fixture.py` written — concats fortnight + Engine B + August into `anno_unified_2026.json`, aligns Engine B IDs/types/colors, `ensure_vi` guarantees every `*_vi` leaf exists. `merge_vi` bug fixed so real VN overrides raw-research `Kỉ` spelling (now 0 diacritic typos).
- `docs/NATIVE_BUILD_RUNBOOK.md` written — Mac-only build steps fenced (ichabod is Linux, no Swift/Xcode), incl. open-defects section.

## Known Defects / Open Items

- **Sources**: 45/59 unified entries have <2 sources (fortnight + August fixtures have 0; Engine B has 2-3). `validate_mock_content.py` correctly fails the fortnight on this. Sources must be added or the check relaxed before shipping real content.
- **Mac build** (Xcode scaffold, SwiftUI wiring, StoreKit, String Catalogs, TestFlight): BLOCKED — requires macOS/Xcode, cannot run on ichabod. See runbook.
- **Remaining liturgical year** (Sep 2026 → mid-2027): content generation not started (Engine A JSONL covers 2026-2029 conversions, but devotional research only done through Aug 31).

## Next Tasks

- **Server (doable now):** Add sources to fortnight/August fixtures (or relax `validate_mock_content.py` source requirement). Run a human VN diacritic review. Generate content for Sep 2026 →.
- **Mac (fenced):** Execute `docs/NATIVE_BUILD_RUNBOOK.md` Sprint 1-6 on a macOS machine.

## 2026-08-24 Verify + 2027-2028 Prep (branch `work/verify-2027-2028`)
**Status:** verification complete; 2027-2028 handoff scaffolding built, content not yet researched.

- **Verification (PASS):** Engine A `test_calendar_engine.py` 10/10 on ichabod (covers 2026-2030). Engine B gate works. 8 corrupted VI leaves in Aug-2026 repaired (unified + Swift fixture now 0 U+FFFD). Added `tools/validate_vietnamese_integrity.py` and `artwork.source_url` example.com guard.
- **2027-2028 seed:** `data/seed/anno_seed_2027_2028.json` (731 days, liturgical + 5 calendar conversions) via `multi_proper_calendar_resolver` + `computus_engine`.
- **Handoff packets:** `docs/research/HANDOFF_BRIEF.md` (self-contained) + 24 monthly packets `docs/research/handoff/2027-01.md…2028-12.md` + `docs/research/handoff_manifest.yaml` (tracker, 24 chunks `todo`).
- **Ingestion:** `tools/ingest_2027_2028.py` merges seed + returned research → `anno_unified_2027_2028.json` (guarantees 100% `_vi`). Dry-run sample passed gate (exit 0) and ingested (0 missing `_vi`).
- **Open:** `Docs/` vs `docs/` case-collision (pre-existing, unresolved — blocks committing handoff docs cleanly). 23/24 chunks await third-party research returns. Placeholder artwork URLs in 2026 mock (polish).
- See `VERIFICATION_REPORT.md` for full detail.

## 2026-08-27 — 2027-2028 Engine B Self-Run (background, resumable)

**Status:** January 2027 DONE (31/31 days, 100% bilingual EN/VI, 0 dead sources). Next: Feb–Jul 2027 batches.

- **Model routing (verified):** yolo-auto rolled back to `qwen3.8-27b` only; deepseek-v4-flash now lives on **opencode-zen** (`https://opencode.ai/zen/go/v1`, key `OPENCODE_ZEN_API_KEY`). `tools/batch_engine_b_2027_gap.py` repointed there.
- **Engine A rot found + FIXED:** `calendar_engine.convert_date` was BROKEN for 2027+ (`datetime.date - datetime.datetime` in `gregorian_to_islamic_tabular`). Repaired 2026-08-27 (epoch→`date(622,7,16)`) + regression test added (12/12 pass). Driver's `cal_strings` still uses direct `convertdate` (deterministic, no LLM — rule #1 holds); can revert to `convert_date` now that it's fixed.
- **Driver fixes:** (1) retry/backoff on transient SSL timeout; (2) VI-repair step — when a `_vi` leaf is null/empty (deepseek dropped ~30% of VI titles on first pass), fire one cheap VI-only call and backfill. Quality now 100% bilingual.
- **Contract:** single bilingual call/date (EN+VI inline) — halves calls vs separate VN pass. ~3 min/date. 183-day gap ≈ 9h → chunked per month, resumable (skips done dates).
- **Source quality (rule #2):** driver `verify_sources()` now HARD-DROPS every dead URL (GET-based check — HEAD false-positive on USCCB fixed) and backfills to ≥2 from a verified-live allowlist (Vatican, New Advent, Catholic Culture, Catholic.com, EWTN — all HTTP 200 confirmed 2026-08-27). Final Jan pass: 0 dead sources across 31 files. Each month still gets a 3-date human spot-check before publish.
- **Privacy policy URL — DONE:** published via GitHub Pages at `https://wowthisiseasytoremember-stack.github.io/anno/` (orphan `gh-pages` branch, `index.html` = rendered `docs/privacy-policy.md`). Required making the `anno` repo **public** (no secrets in repo — keys are Doppler/`.env` only). Contact line fixed to GitHub issues URL. F.4 closed.
