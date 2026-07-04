# Blind Frontier Content And Asset Packets

Updated: 2026-07-03

Agents must return structured outputs only. They cannot browse this repo, so include all schema and policy text from the requested packet when assigning.

## Shared Content Schema

Each daily entry must match `anno.mock.v1` fields:

```json
{
  "id": "anno-YYYY-MM-DD-slug",
  "date": "YYYY-MM-DD",
  "weekday": "English weekday",
  "mock_priority": "draft_extension",
  "liturgical": {"rank": "", "color": "", "title_en": "", "title_vi": ""},
  "calendars": {"julian": "", "hebrew": "", "islamic_umm_al_qura": "", "coptic": "", "ethiopian": ""},
  "primary": {
    "type": "",
    "title_en": "",
    "title_vi": "",
    "summary_en": "",
    "summary_vi": "",
    "confidence": "confirmed|traditional|disputed",
    "confidence_note_en": "",
    "confidence_note_vi": ""
  },
  "place": null,
  "artwork": {"title": "", "maker": "", "date_label": "", "source_url": "", "status": ""},
  "sources": [{"label": "", "url": "", "type": ""}],
  "app_hooks": {"hero_line_en": "", "hero_line_vi": "", "prayer_prompt_en": "", "prayer_prompt_vi": ""}
}
```

Confidence policy: `confirmed` for liturgical rank, canonization, museum record, shrine identity, or well-sourced historical fact; `traditional` for devotional tradition, traditional tomb/martyrdom site, or approximate Gospel geography; `disputed` for conflicting claims or insufficient evidence. Do not flatten confidence notes into summaries.

## Packet A: July 17-30 Catholic Research

Return one JSON object with:

- `schema_version`: `anno.research_batch.v1`
- `date_window`: `{ "start": "2026-07-17", "end": "2026-07-30" }`
- `entries`: fourteen draft entries matching the shared content schema
- `research_notes`: array of date-scoped notes for unresolved issues

Rules: Catholic-first; English and Vietnamese sibling fields; at least three sources per date where possible; no unsourced claims; no calendar conversion invented by LLM if deterministic Engine A output is unavailable. If conversions are unavailable, put empty strings and add a research note.

## Packet B: Artwork Clearance

Input rows: use current queue shape: `entry_id`, `date`, `entry_title_en`, `entry_title_vi`, `artwork_title`, `maker`, `date_label`, `source_url`, `current_status`, `clearance_priority`, `next_action`, `ship_decision`, `notes`.

Return one JSON object with:

- `schema_version`: `anno.artwork_clearance.review.v1`
- `items`: reviewed queue rows
- `evidence`: source URL, rights URL, rights statement summary, image URL if usable, attribution text, commercial app use assessment, screenshot/App Store use assessment

Rules: do not bundle uncleared modern images; preserve attribution; store license evidence before app use; mark uncertain items `placeholder_only`.

## Packet C: Vietnamese Catholic Editorial

Return:

- reviewed Vietnamese titles, summaries, hero lines, prayer prompts, confidence notes
- terminology table for proper names and feast ranks
- unresolved terminology questions

Tone: reverent, plain, and specific. Translate Saint as `Thánh`, Blessed as `Chân phước`, Ordinary Time as `Mùa Thường Niên`, Optional Memorial as `Lễ nhớ tùy chọn`, and Marian titles idiomatically with `Đức Mẹ` where appropriate.

## Packet D: App Icon And Screenshot Assets

Return deliverable specs and prompts, not repo edits:

- app icon: 1024x1024, deep warm near-black `#13110E`, single gold illuminated capital A `#C9A84C`, no text, no halos, no crosses
- screenshot art direction for Today EN, Today VI, Calendar, Map, Source Sheet, Paywall
- safe areas, crop notes, and text overlay notes

No SVG-only hero art. Use real cleared artwork or generated bitmap placeholders until clearance is complete.
