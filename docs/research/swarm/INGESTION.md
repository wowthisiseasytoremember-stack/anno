# Engine B Swarm — Ingestion Guide

How to ingest swarm batch output into the anno app/repo. Schema reference: `docs/ANNO_CONTENT_SCHEMA.md`.

## 1. Where batch files land

Each QA'd batch JSON is committed under:

```
data/engine_b/batches/batch_XX_YYYY-MM-DD_YYYY-MM-DD.json
```

`XX` is the zero-padded batch number from `batch_schedule.json`; the two dates are the batch window start/end. One-off or pilot batches may use a descriptive prefix instead of `batch_XX` (e.g. `pilot_2026-11-23_2026-11-29.json`).

## 2. Validation gate (before any merge)

Run the repo's existing validators against the batch file:

```
python tools/validate_engine_b_output.py data/engine_b/batches/<batch>.json
python tools/validate_mock_content.py
```

Plus the QA checklist from `docs/research/swarm/ANNO_SWARM_MASTER_PROMPT.md` (§ Agent C + v2.1 lessons):

- **Schema completeness** — every entry has all required fields, incl. `summary_en/summary_vi`, `confidence_note_en/confidence_note_vi`, `app_hooks`, `vi_notes`, `audio_script`.
- **URL reality** — every `sources[]` URL resolves; retry usccb.org with a browser-like fetch before marking dead (anti-bot 403s).
- **Liturgical rank check** — rank/color match the actual USCCB calendar for the date; empty calendar days must not gain invented memorials.
- **Confidence honesty** — `confidence` reflects sourcing; unverified claims are removed or disclosed.
- **VI terminology** — glossary compliance (`hoàng đế` for Roman emperors, `Sách Tiến sĩ` for Sirach, paraphrase marking "theo bản diễn dịch", `Ngày Lễ Tạ Ơn quốc gia` for US Thanksgiving).

## 3. Merge step

Batches are in the `anno.mock.v1` fixture shape. Entries are keyed by `id`: `anno-YYYY-MM-DD`.

1. **Backup first:** copy the current `Anno/Resources/anno_full_2026_2029.json` to a dated backup (e.g. `anno_full_2026_2029.backup-YYYYMMDD.json`) before every merge.
2. For each batch entry, **replace** the placeholder entry in `Anno/Resources/anno_full_2026_2029.json` whose `id` / `date` matches.
3. **Never append duplicates** — if an `id` already exists, it is replaced in place; the file must stay one-entry-per-date.

## 4. Swift model note (required app-side task)

The schema doc maps to the Swift `AnnoEntry` model via snake_case JSON with `convertFromSnakeCase`. The swarm's output adds fields the current model does not yet carry:

- `primary.body_en` / `primary.body_vi` (long-form body text)
- `vi_notes`
- `audio_script{script_en,script_vi}`

Extending the Swift `AnnoEntry` model (and any decoding tests) for these fields is a **required app-side task before the paywall's audio + long-body features can render**. Until then, ingest keeps the fields in JSON — decoding must tolerate their presence.

## 5. Artwork

Artwork candidates from each batch land in the repo's existing artwork clearance queue format, per `docs/research/swarm/ARTWORK_PLAN.md` (exported via `tools/export_artwork_clearance_queue.py`). Status stays `placeholder_only` until human eyeball + license verification.

## 6. Rollout order

1. **Pilot batch** (2026-11-23 → 2026-11-29, already QA'd) — `data/engine_b/batches/pilot_2026-11-23_2026-11-29.json`.
2. **Remaining 52 batches** in `batch_schedule.json` order, each through the §2 validation gate before merge.
3. **Atlas site extraction** — dedupe every unique `place` across all entries into the Atlas sites DB (feeds the Pilgrim tier).
