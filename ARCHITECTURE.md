# Interfaith Devotional Engine — Architecture
**Last updated:** 2026-07-04

## Product Direction

The implementation target is now a native SwiftUI iOS app with a Catholic-first launch wedge and an interfaith-capable data engine.

Launch promise:

> Every day in Catholic history, mapped.

The broader architecture remains useful for Jewish, Islamic, Orthodox, Coptic, Ethiopian, and other sacred-context layers, but v1 should present Catholic sacred history first unless product validation shows that interfaith-first positioning converts better.

## Governing Invariants

- Engine A is deterministic calendar conversion. No LLM may compute or correct calendar dates.
- Engine B produces structured, sourced research data. It may discover claims; it may not publish claims without source metadata.
- Layer C produces narrative devotional/history framing from Engine B data only.
- Every factual event must expose source and confidence: `confirmed`, `traditional`, or `disputed`.
- Interfaith or Sacred Context appears only where a genuine historical, textual, geographic, liturgical, or artistic relationship exists.
- Production Hebrew/Islamic sundown-sensitive dates must use device timezone/location or a clearly labeled fallback, not a hardcoded Garden Grove anchor.
- Vietnamese localization must be a first-class data shape, not an afterthought applied to rendered English strings.
- The app sells knowledge, beauty, archive access, audio, maps, and pilgrimage utility. It must not sell salvation, indulgences, prayer outcomes, guilt relief, or spiritual authority.

## System Boundaries

### Engine A: Calendar Conversion

Pure deterministic computation.

Inputs:

- Gregorian date range.
- Location/timezone for sundown-sensitive presentation.

Outputs:

- Calendar conversion rows, one per Gregorian date.
- Calendar metadata and certainty notes.

Current artifact evidence:

- `/home/ichabod/01_Infrastructure/interfaith/calendar_engine.py`
- `/home/ichabod/01_Infrastructure/interfaith/calendar_2026_2029.jsonl`

The project root may not yet contain those files; reconcile before implementation.

### Engine B: Research

Structured research pipeline.

Inputs:

- One Engine A date row.
- Source policy and prompt.

Outputs:

- Events.
- Sources.
- Confidence labels.
- Artwork metadata.
- Geography.
- Optional Sacred Context.

Engine B output should be reviewable before it becomes user-facing content.

### Layer C: Narrative Content

Content transformation pipeline.

Inputs:

- Engine B structured data.
- Tone/style rules.
- Localization target.

Outputs:

- English user-facing entry.
- Vietnamese user-facing entry when requested/reviewed.
- Short prayer/reflection.
- App UI captions.

Layer C must not introduce new facts not present in Engine B.

### Native iOS App

SwiftUI app with:

- Today tab.
- Calendar tab.
- Map tab.
- Saved tab.
- StoreKit 2 subscriptions.
- String Catalog localization.
- Local cache/bookmarks.
- MapKit sacred-place view.

## Localization Contract

UI strings:

- Managed through Xcode String Catalogs.
- English and Vietnamese from v1.

Content strings:

- Stored as localized fields, for example `title_en`, `title_vi`, `body_en`, `body_vi`.
- Vietnamese Catholic terminology requires human review before public release.

Store metadata:

- App Store metadata and StoreKit product metadata need separate localization review in App Store Connect.

## Trust and Correction Contract

Every published daily entry needs:

- Source sheet.
- Confidence label.
- Report concern affordance.
- Correction queue item when reported.

High-sensitivity dates include:

- Easter/Pascha-related dates.
- Christmas and Marian solemnities.
- Ramadan/Eid/Hajj context if surfaced.
- Passover/Tisha B'Av/Yom Kippur context if surfaced.
- Any date where local sundown may shift display.

Corrections should be hotfixable without App Store release where possible by shipping content as updateable data.

## Monetization Contract

Free:

- Today's full entry.
- Today's art and source preview.
- Today's/this-week map preview.

Premium:

- Archive.
- Full calendar.
- Full map archive.
- Art gallery.
- Saved collections.
- Audio.
- Expanded source sheets.

Pilgrim:

- Route packs and offline travel utility.

No monetized feature may imply paid spiritual superiority.
No v1 monetized feature may depend on ads, rewarded ads, data resale/share, paid streak repair, Grace Tokens, XP multipliers, or guilt-based religious pressure.
Premium may be commercially sharp only when it sells real product value: archive, art, audio, source depth, reviewed localization, maps, and routes.

## Canonical Planning Docs

- Product bible: `docs/CATHOLIC_IOS_PRODUCT_BIBLE.md`
- Asset rubric: `docs/ASSET_ACCEPTANCE_RUBRIC.md`
- Asset prompts: `docs/ASSET_PRODUCTION_PROMPT_PACK.md`
- Monetization: `docs/MONETIZATION_PAYWALL_SYSTEM.md`
- Flagship slate: `docs/FLAGSHIP_CONTENT_SLATE.md`
- Synthesis prompt: `docs/FRONTIER_ASSET_SYNTHESIS_PROMPT.md`
- External feedback triage: `docs/EXTERNAL_FEEDBACK_TRIAGE.md`
- Brand visual addendum: `docs/BRAND_VISUAL_ADDENDUM.md`

## Changelog

- 2026-07-03: Created architecture doc; set native SwiftUI, Catholic-first, Vietnamese-ready direction while preserving deterministic multi-calendar and sourced research invariants.
