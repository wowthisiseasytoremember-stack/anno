# EVERGREEN — Anno standing work

This is a perpetual checklist, not a sprint plan. It never reaches zero — see
[TODO.md](TODO.md) for near-term tactical work instead. This file is for the recurring
maintenance an operator always has more of.

## How to run this (any agent, cold, no other context needed)

1. Read this file top to bottom.
2. Find the most recent `[x]` item in the Queue below. Read its dated note — that's the
   last thing that was checked/done and what it found.
3. Resume at the next `[ ]` item below it.
4. Do that item's actual work (run the command it names, read what it says to read, produce
   the output it asks for).
5. Check it off `[x]`, and add a one-line dated note directly under it: what you found or
   did, and anything worth a human's attention.
6. Replenish: if fewer than 4 unchecked items remain below the one you just did, add 3-5
   new concrete items to the end of the Queue, pulled from the Standing categories menu
   below — rotate through categories that haven't run recently, or prioritize one a recent
   note flagged as needing follow-up. Phrase each new item as a specific, actionable task.
7. Stop after one item per run unless told to do more. Don't touch DISAGREEMENTS.md,
   STATE.md, or any other human-owned decision file — note it and move on if you hit one.

## Standing categories (menu — pull new Queue items from here)

- Content pipeline health: run Engine B generation/normalize for the next uncovered month — `tools/batch_engine_b_2027_gap.py` (resumable, chunked per month) then `tools/normalize_fixture.py --year <Y>` → `Anno/Resources/anno_unified_<Y>.json`.
- Validation gate: re-run the deterministic validators and confirm green — `validate_vietnamese_integrity.py`, `validate_engine_b_output.py --fixture`, `validate_mock_content.py`, `validate_devotional_pool.py`, `validate_sanctuaries.py`, `validate_route_coordinates.py`, `test_calendar_engine.py`.
- Source health: verify citations are live and ≥2 per entry — `tools/backfill_citations.py` + `verify_sources()` in the validate gate; flag any dead URL for backfill from the verified-live allowlist (Vatican, New Advent, Catholic Culture, Catholic.com, EWTN).
- Calendar engine integrity: confirm deterministic conversions still pass across the full 2026–2030 dataset — `python3 tools/test_calendar_engine.py`; add a regression test if a new conversion path is touched.
- Bilingual parity: confirm EN/VI string catalog (63 keys) + dataset `_vi` leaves stay 100% — `validate_vietnamese_integrity.py`; run a human diacritic spot-check on the newest month.
- Doc freshness: find and fix one stale claim in AGENTS.md / CLAUDE.md / STATE.md / ROADMAP.md / wiki page (`~/wiki/projects/Anno-visual-polish.md`). Cross-reference, never merge into TODO.md.
- Asset/artwork clearance: surface unverified or placeholder artwork URLs — `tools/export_artwork_clearance_queue.py`; clear one batch.
- Monetization asset scan: confirm StoreKit product metadata + paywall triggers still match the freemium model (daily free, packs/routes/archive paid) — `Anno/Resources/product_metadata.json`, `paywall_triggers.json`, `Anno/Configuration/AnnoProducts.storekit`. Note: do NOT add a second/free fork target (decision 2026-08-28 — see wiki page).

## Queue

- [ ] 2026-08-28 Extend Engine B 2027 content past January: run `tools/batch_engine_b_2027_gap.py` for 2027-02, normalize (`tools/normalize_fixture.py --year 2027`), gate with `validate_vietnamese_integrity.py` + `validate_engine_b_output.py`.
- [ ] 2026-08-28 Validation sweep: run all deterministic validators in the "Validation gate" category and report pass/fail per file.
- [ ] 2026-08-28 Source health pass on `anno_unified_2027.json` (once generated): confirm every entry has ≥2 live citations; backfill any gaps via `tools/backfill_citations.py`.
- [ ] 2026-08-28 Bilingual parity check on newest month: run `validate_vietnamese_integrity.py`; flag any empty `_vi` leaf for the VI-repair backfill step.
- [ ] 2026-08-28 Doc freshness: read `~/wiki/projects/Anno-visual-polish.md` and `CLAUDE.md`; confirm the 2026-08-28 "no free fork" decision is stated and the stale `[NEXT]` fork idea is gone. Fix if drifted.
- [ ] 2026-08-28 Artwork clearance: run `tools/export_artwork_clearance_queue.py`; clear the oldest batch of placeholder/example.com URLs.
