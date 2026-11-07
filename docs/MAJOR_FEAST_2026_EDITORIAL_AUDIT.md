# ANNO 2026 major-feast devotional content — complete pre-edit audit

**Claimed area:** all four of the eight *v1 mandatory bilingual* feast dates actually inside the shipped 2026 July 3–December 31 fixture. Four out-of-range feasts (Epiphany, Divine Mercy, Easter, Pentecost) are **not** present and are not silently included. Audit date 2026-11-06.

**Environment:** native Catholic-first SwiftUI devotional; canonical generation inputs: `data/mock/anno_august_2026.json` (Aug 15) and `data/research_results/2026-{11-22,12-08,12-25}_result.json` with a separate 2026-11-22 VI overlay. `tools/normalize_fixture.py` builds `Anno/Resources/anno_unified_2026.json`. Publication means actual iOS TestFlight/App Store release, *not* a GitHub merge. Drive's ANNO archive currently contains East Asian pilgrimage research, **not** authoritative 2026 feast-day editorial guidance. Editorial policy: source-aware, distinguish historic dogma from pious tradition, preserve human review for Vietnamese Catholic phrasing and rights clearance.

## All four items: issue / severity / proposed fix (baseline before any edit)

### August 15 — Assumption of the Blessed Virgin Mary

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| `app_hooks.hero_line_en` says **heavenly coronation**, a distinct Marian mystery rather than the Assumption. | **high** | Describe Mary's Assumption, body and soul, without conflating it with Coronation; align VI hero. |
| `primary.confidence_note_en` implies Pius XII's 1950 dogma *established the August 15 date*, when the Church celebrated the feast long before the definition. | **high** | Distinguish the ancient feast from the dogmatic definition in 1950; cite `Munificentissimus Deus`. |
| `primary.body_vi` contains likely mistranslation/typo (“thiên đang ở trong tầm tay”); Francis attribution lacks a specific cited address. | medium | Remove unsupported quotation attribution; replace with concise EN/VI sourced framing, flag Vietnamese style review. |
| `place` is a **traditional** Jerusalem tomb location, not empirical proof of the dogma; artwork is `placeholder_only`, no cleared rights/alt text. | medium | Preserve `place.confidence=traditional` and art placeholder, do not embed as verified hero imagery; log rights and provenance review. |
| Existing USCCB day-specific readings and papal constitution are strong links; app has no per-clause citation mapping for the entry. | medium | Keep source links, record primary claims in the existing docs editorial audit, and enforce known date/rank/source contract. |

### November 22 — Christ the King

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| **Wrong feast**: fixture calls it “33th Sunday in Ordinary Time” with **Sunday/green** instead of the **Solemnity of Christ the King / white**; contradicts USCCB 2026. | **high** | Replace titles, rank, color, type, summaries, body, hero and prayers in source + VI overlay + normalized fixture. |
| Unsourced generic Ordinary Time prose and awkward English tokens (“33th”, “Sunday” left untranslated in VI). | **high** | Re-author concise Christ the King material in EN/VI around USCCB Nov 22 readings and documented theological theme. No invented quotes. |
| Generic liturgical link does not establish the specific 2026 observance; artwork placeholder references generic unspecified symbol. | medium | Point to `https://bible.usccb.org/bible/readings/112226.cfm`; update art metadata as pending selection, not cleared. |
| This v1 required VI feast passed a *nonempty strings* gate despite being entirely wrong; normalizer fallback can silently copy EN to VI. | **high** | Add semantic rank/title invariants and an English-equals-Vietnamese guard, with fail-closed Linux tests. |
| Existing universal Sunday text misses the central Gospel theme of serving the hungry, sick and imprisoned (Mt 25). | medium | Improve the opening/hook with the feast's particular moral witness; source to USCCB readings and avoid overlong citation quotations. |

### December 8 — Immaculate Conception

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Doctrine/date/rank broadly correct, but `body` says the 1858 Lourdes apparition *confirmed* doctrine as unqualified historical fact. | **high** | Mark reported Lourdes tradition as traditional belief or remove its evidentiary role; anchor to Pius IX's 1854 definition. |
| Generic USCCB homepage rather than date-specific Mass readings; patronal status and a quoted Lourdes phrase require explicit verification. | medium | Link USCCB `120826.cfm`; avoid unsourced quotation and keep official constitution linked. |
| English and Vietnamese editorial tone are ornate, have no recorded human Catholic translation approval. | medium | Tighten prose and make no claim of Vietnamese review. |
| Artwork metadata is placeholder-only; no alt/caption/clearance, physical shrine illustration is unrelated to feast location. | low | Preserve placeholder status; flag art rights/alt text rather than promoting images. |

### December 25 — Nativity / Christmas

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Describes a stable/cave as if directly documented by Luke 2, whereas Gospel explicitly describes the manger; stable/cave elaborations are devotional tradition. | medium | Prefer Luke's documented manger wording; distinguish artistic tradition if mentioned. |
| Attribution to Athanasius with exact English/Vietnamese quoted text was not paired to a specific primary citation. | medium | Remove the direct quotation in favor of sourced Christian teaching on Incarnation; do not invent a quote. |
| USCCB source is generic daily reading homepage, not the direct Christmas liturgical page. | medium | Link `https://bible.usccb.org/bible/readings/122526.cfm`. |
| Artwork placeholder rights/attribution not cleared; repeated prayer language lacks device accessibility verification. | medium | Keep asset `placeholder_only`, leave rights/captions/alt and device checks open. |
| Vietnamese is present but the product lacks human Catholic proofreading. | **high** | Keep translation review as an explicit release blocker for all four feast records. |

## Shared format, accessibility, metadata and engineering findings

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Fiesta dates were treated as generic days despite required v1 status; current Engine B CI is `continue-on-error: true` and checks URL reachability across 182 daily records. | **high** | Add **offline deterministic, fail-closed check for these four dates** on Linux rather than make all legacy 182 source URLs a new hidden blocker. |
| Normalizer `ensure_vi` copies English content into empty VI fields, so nonempty checks can be mistaken for translated copy. | **high** | Reject required feast VI values that are identical to EN before fallback; preserve explicit editorial approval requirement. |
| Source URL “exists” is not equivalent to supporting a date, count, or dogma; broad pages provide poor provenance. | **high** | Add date-specific USCCB URL and source checks per feast; maintain this claim-level review table. |
| Calendar/UI metadata must obey ranks/colors and same-day date/weekday, not just syntactic fields. | **high** | Validate titles, solemnity/white, canonical date and source URL for all four, plus CI tests that mutate one field and expect failure. |
| Artwork/alt and voice-over are outside JSON and remain untested; no web scrollytelling or animated hero treatment belongs in a native devotional data pipeline. | medium | Avoid invented assets; preserve original art placeholders; defer real iPhone accessibility and image clearance. |
| Source normalization is reproducible but the generated `anno_unified_2026.json` is materialized and can drift from underlying research. | **high** | Edit both upstream and generated output, compare normalized output in Linux CI, and detect repeatability regressions. |
| Domain-specific reviewer approval absent. | **high** | Explicit pending human Catholic review of EN theology, VI terminology, art provenance and site contextual accuracy; use this document as one canonical queue. |

## Canonical fact links / scope of verification

- [USCCB Nov 22, 2026: Christ the King](https://bible.usccb.org/bible/readings/112226.cfm), `Solemnity`, white; Gospel Matthew 25:31–46.
- [USCCB Aug 15, 2026: Assumption](https://bible.usccb.org/bible/readings/081526.cfm); [Pius XII `Munificentissimus Deus` (1950)](https://www.vatican.va/content/pius-xii/en/apost_constitutions/documents/hf_p-xii_apc_19501101_munificentissimus-deus.html).
- [USCCB Dec 8, 2026: Immaculate Conception](https://bible.usccb.org/bible/readings/120826.cfm); Pius IX `Ineffabilis Deus` (1854) already referenced in fixture.
- [USCCB Dec 25, 2026: Nativity](https://bible.usccb.org/bible/readings/122526.cfm), including Vigil/Night/Dawn/Day.
- Official USCCB yearly calendar: https://www.usccb.org/committees/divine-worship/liturgical-calendar.

**Not established:** individual artwork licenses/attribution or image alt; direct support for every historic/theological clause without a full Catholic-editor review; human Vietnamese translation approval; app voiceover/contrast/render testing. Treat the four revised entries as **edited, pending human review**, not release certified.

**Next area (not part of this claim):** scan every other day of the 182-entry fixture for liturgical calendar collisions, stale/placeholder URLs and generic text.
