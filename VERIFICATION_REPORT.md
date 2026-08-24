# Anno — Verification & 2027-2028 Readiness Report
**Generated:** 2026-08-24 | **Branch:** `work/verify-2027-2028`

## Part A — Verification (wiring & integrity)

| Check | Result | Evidence |
|-------|--------|----------|
| Engine A calendar math | **PASS** | `tools/test_calendar_engine.py` on ichabod: 10/10 tests OK, covers 2026-2030 (incl. 2027-2028) |
| Engine B validation gate | **WORKS** | `tools/validate_engine_b_output.py` runs on ichabod; fabricated 2027 sample → exit 0 |
| Corrupted Vietnamese text | **FIXED** | 8 U+FFFD leaves in Aug-2026 entries repaired at source (`data/mock/anno_august_2026.json`) → regenerated `anno_unified_2026.json` (182 entries, **0 U+FFFD**) and `AnnoMockData.swift` (**0 U+FFFD**) |
| Vietnamese integrity validator | **ADDED** | `tools/validate_vietnamese_integrity.py` → 0 problems on fixture |
| Artwork `example.com` guard | **ADDED** | rejection added to `validate_engine_b_output.py` |
| Pipeline wiring | **INTACT** | `calendar_engine.py` → `calendar_2026_2029.jsonl` → `research_results/` → `normalize_fixture.py` → `anno_unified_2026.json` → `AnnoMockData.swift` |
| Other validators | **PASS** | sanctuaries 72/72, routes 18/18 (106 waypoints), localization 100%, mock content |

### Findings
- **Historical raw 2026 outputs are non-conformant** to the Engine B schema (one has a `null` text field, one is missing `sources`). The gate correctly catches this. The 2026 *unified fixture* is post-normalized and intentionally does not satisfy the raw gate. **Action:** 2027-2028 third-party deliverables will be required to pass the gate before ingest.
- **Placeholder artwork URLs** (`example.com/placeholder.jpg`) remain in the 2026 mock source. They are not caught by `validate_mock_content` (only `sources[].url` is checked). Latent; recommend filling with real `placeholder_only` Wikimedia/museum URLs during polish.

## Part B — 2027-2028 Research Handoff (prepared)

| Artifact | Path | Notes |
|----------|------|-------|
| Seed catalog (731 days, liturgical + 5 calendar conversions) | `data/seed/anno_seed_2027_2028.json` | via repo's `multi_proper_calendar_resolver` + `computus_engine` |
| Self-contained handoff brief | `docs/research/HANDOFF_BRIEF.md` | no FS access needed; embeds full schema + worked example |
| 24 monthly handoff packets | `docs/research/handoff/2027-01.md … 2028-12.md` | each self-contained: brief + that month's seed days |
| Manifest / tracker | `docs/research/handoff_manifest.yaml` | 24 chunks, `status: todo` |
| Ingestion pipeline | `tools/ingest_2027_2028.py` | merges seed + returned research → `anno_unified_2027_2028.json`; guarantees 100% `_vi` |
| Dry-run proof | `data/research_tentative/2027_2028/sample_chunk.json` + `Anno/Resources/anno_unified_2027_2028_sample.json` | 3-day fabricated chunk → gate PASS (exit 0) → ingest OK, 0 missing `_vi` |

### End-to-end loop proven
third-party returns JSON → `validate_engine_b_output.py` (gate) → `ingest_2027_2028.py` → unified fixture → `export_swift_fixture.py`. Works; 2027-2028 content itself is **not yet researched** (awaiting third-party returns).

## Open items
1. **`Docs/` vs `docs/` case-collision** (pre-existing) — see handoff note; needs a decision before the `docs/research/*` handoff files are committed.
2. 2027-2028 devotional content not yet produced (23 of 24 chunks remain `todo`).
3. Placeholder artwork URLs in 2026 mock (polish-phase).
