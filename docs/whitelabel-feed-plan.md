# White-Label Devotional Feed for Anno  
**Written spec + research brief + two Markdown pitch decks**  
**Date:** 2026-08-28  
**Boundary honored:** producing side remains Linux-only; no Xcode, no Swift build, no Mac dependency. The iOS app remains the flagship consumer, but the feed is specified as an optional source of truth / remote content layer.

---

# 0. Executive Summary

Anno should be packaged as a **licensable devotional content utility**, not merely as an iOS app.

The asset already exists: a Linux-generated, source-gated, bilingual EN/VI devotional dataset with deterministic calendar conversion, normalized JSON, live-source validation, and a 4-year master file. The business move is to expose that dataset as:

1. **A public static feed** for discovery and noncommercial use.
2. **A paid API** for commercial / white-label use.
3. **A parish iframe widget** for low-friction adoption.
4. **A metered B2B content license** for apps, parishes, dioceses, and publishers.

The moat is not “daily saint content.” Many sites and apps have that. The moat is:

- bilingual **English / Vietnamese** content today,
- source-gated entries with live citations,
- deterministic multi-calendar metadata,
- a repeatable generation / validation pipeline,
- and continuously updated structured data rather than one-off prose.

Spanish is **not present today**. It should be treated honestly as **Phase 4**.

---

# A. Research Brief

## A1. Competitors and adjacent offerings

### 1. Free / DIY Catholic APIs and calendar tools

| Offering | What it is | Pricing / access | Gap Anno can fill |
|---|---:|---:|---|
| **Catholic Readings API** | Free REST API on GitHub Pages for daily Mass readings, saints, and liturgical calendar data. The repo describes JSON endpoints, CORS, no keys, no rate limits, MIT license, and use cases for parish sites and apps [2](https://github.com/cpbjr/catholic-readings-api). | Free; MIT; no registration / no API keys per its README [2](https://github.com/cpbjr/catholic-readings-api). | Useful developer proof that static Catholic JSON feeds are desirable, but it appears more like an open project than a licensed content service. Anno’s differentiator: source-gated historical devotional prose, bilingual EN/VI, multi-calendar metadata, versioning, commercial licensing, and a paid support/API layer. |
| **romcal** | JavaScript library that generates Roman Rite liturgical calendars; MIT-licensed [5](https://github.com/romcal/romcal). | Free / open source. | Calendar logic, not devotional content. Anno has calendar conversion plus researched entries and app-ready devotional hooks. |
| **Liturgical Calendar API / Church Calendar API** | Public Roman Catholic liturgical calendar APIs; one listing describes free use with no authentication [3](https://publicapi.dev/church-calendar-api). | Free / unauthenticated in the public listing [3](https://publicapi.dev/church-calendar-api). | Again, calendar facts rather than licensed devotional content. Anno should not compete as “another calendar API”; it should sell the sourced devotional layer. |
| **APIVerve Liturgical Calendar API** | Commercial API marketplace endpoint for liturgical calendar dates. Its marketplace page says the free tier includes 50 tokens/month and 10 requests/minute; pro/enterprise plans raise limits [1](https://apiverve.com/marketplace/liturgicalcalendar). | Free trial-style tier; paid API marketplace. | Confirms there is a general API-pricing pattern even for religious calendar data, but Anno’s feed has richer content and source provenance. |
| **AELF** | Official French Catholic liturgical text service with free email, RSS integration, and API for more advanced use [1](https://www.aelf.org/abonnement). | Free access / RSS / API, focused on official French liturgical texts [1](https://www.aelf.org/abonnement). | Strong official-text competitor in French, but not an EN/VI devotional licensing feed. Also highlights that official liturgical text licensing is a separate rights category. |
| **Evangelizo** | Free Catholic daily Gospel/readings/saints/prayers app in 10 languages, according to its app listing/review [2](https://catholicapps.com/evangelizo/). | Free app. | Multilingual consumer devotional app, not clearly positioned as a source-gated white-label content API. Anno should not claim 10-language parity; it should claim EN/VI today and ES-ready later. |

**Takeaway:** The free ecosystem proves developer interest, but most offerings are either **calendar utilities**, **readings APIs**, or **consumer apps**. Anno’s saleable angle is **structured, bilingual, source-gated devotional content with a pipeline**, not raw liturgical date calculation.

---

### 2. Catholic devotional / parish content providers

| Offering | What it is | Pricing / access | Gap Anno can fill |
|---|---:|---:|---|
| **My Catholic Life!** | Large library of Catholic reflections and saint content. Its permission page grants Catholic / Christian organizations in union with the Catholic Church permission to use up to 5,000 words freely in nonprofit contexts, but for-profit or ad-supported use requires contacting them [3](https://mycatholic.life/copyright-permission/). | Free nonprofit use within stated limits; for-profit requires permission [3](https://mycatholic.life/copyright-permission/). | Strong content source, but not a normalized API/feed product. Also shows that Catholic devotional content often has permission boundaries, reinforcing Anno’s legal-review need. |
| **Give Us This Day** | Daily Catholic prayer / reflection subscription. Its subscription page lists app-only 12 issues at $19.99, standard print at $54.95/year, and group print pricing for parishes [4](https://digital.giveusthisday.org/Subscribe/Index). | Consumer/group subscription. | Great devotional brand, but sold as magazine/app content, not developer feed infrastructure. |
| **Magnificat English Editions** | Daily Catholic prayer app / publication. The App Store listing shows in-app purchases including a one-year subscription at $24.00 [3](https://apps.apple.com/us/app/magnificat-english-editions/id363526415). | Consumer subscription. | Strong consumer devotional competitor, not a B2B structured data feed. |
| **CatholicBrain** | Catholic education platform with daily readings and saint-of-the-day content among broader catechetical resources. Its subscription page lists individual, family, classroom, and school/parish tiers, including school/parish premium at $199/month or $1,999/year [2](https://www.catholicbrain.com/content/1503514/1/subscription-page). | Paid educational subscription. | Broader catechesis product. Anno can be much narrower and cheaper: “just the daily bilingual devotional feed/widget/API.” |
| **FORMED** | Catholic streaming/content platform. One parish renewal page lists a parish subscription cost of $2,451.31/year and individual subscriptions at $9.99/month or $100/year [1](https://stjosephbogota.org/formed-subscription/). | High-value parish subscription / streaming library. | FORMEd is a full content library. Anno should not try to be FORMED; it should be a lightweight devotional utility that complements parish websites and apps. |
| **OSV Simply Catholic Connect** | Parish/diocesan Catholic communication/content product. OSV lists a parish subscription at $49.99/month or $599.88/year, with diocesan subscription by inquiry [5](https://www.osv.com/parish-diocese/communication/simply-catholic-connect/). | Parish SaaS pricing. | Useful benchmark for parish willingness to pay around $50/month for Catholic content/communication value. |
| **Word on Fire ENGAGE via Flocknote** | Parish evangelization content included with Flocknote Complete. Flocknote says ENGAGE is included with Flocknote Complete, and Complete is Starter plus $75/month [4](https://flocknote.com/engage/). | Add-on style parish content bundle. | Shows content can be bundled into parish software. Anno can sell directly or later integrate with parish SaaS providers. |

**Takeaway:** Catholic parish software/content pricing commonly lands between **$20–$75/month** for focused tools and much higher for full libraries. Anno’s parish tier should be modest and frictionless: widget + API + rights clarity.

---

### 3. Scripture / religious content API licensing models

| Offering | What it is | Pricing / access | Lesson for Anno |
|---|---:|---:|---|
| **API.Bible** | Bible API with licensing wrapper. The official site lists Starter at $0/month with 5,000 API calls/month and strictly noncommercial use; Pro at $29+/month with 150,000 calls/month; and commercial licensing fees for copyrighted Bibles starting at $10/month per Bible and scaling by user reach [5](https://api.bible/). | Free noncommercial; paid commercial/API tiers [5](https://api.bible/). | This is the closest business-model analogy: free dev access + paid commercial license + usage limits + rights wrapper. |
| **ESV / Crossway API** | Crossway states ESV digital API access is free for noncommercial website/app use, while requests outside standard guidelines require written permission or a formal license [4](https://www.crossway.org/permissions/). | Free noncommercial; commercial/formal license required [4](https://www.crossway.org/permissions/). | Confirms the pattern: noncommercial access is a lead magnet; commercial use requires explicit license. |
| **USCCB / Lectionary permissions** | USCCB permissions state no fee is needed to display daily readings on RSS only on a website not requiring value from users, but e-books and digital applications for sale or free distribution require a license/fee; regular worship-aid reproduction requires written agreement [5](https://usccb.org/bible/permissions/index.cfm?refresh=1). | Permission-sensitive; digital/app use can require license [5](https://usccb.org/bible/permissions/index.cfm?refresh=1). | Anno should avoid redistributing protected lectionary text unless specifically licensed. Linking/citation is safer than reproducing official readings. |

**Takeaway:** The content API market already understands **free noncommercial + paid commercial rights**. Anno’s feed should mirror that pattern.

---

## A2. Recommended Anno pricing

These are realistic launch prices, not maximum prices.

### Tier 1 — Free / Developer / Noncommercial

**Price:** $0  
**Delivery:** static JSON on GitHub Pages  
**License posture:** CC-BY-NC-style intent, but see legal warning below before finalizing  
**Limits:**

- attribution required,
- noncommercial only,
- no uptime SLA,
- no support guarantee,
- public current-month or rolling 30/60/90-day feed,
- no white-label rights.

**Why:** Free static access proves the product, helps developers integrate, and creates SEO/dev credibility. Do not over-optimize monetization before proving adoption.

**Important legal note:** do not apply a Creative Commons license to material Anno does not fully own or have sublicensable rights to. Creative Commons guidance emphasizes that a licensor must hold copyright / permission to license the material [1](https://copyright.psu.edu/copyright-basics/creative-commons/).

---

### Tier 2 — Parish

**Recommended launch price:** **$29/month** or **$299/year** per parish/domain  
**Acceptable range:** $19–$49/month

**Includes:**

- iframe “saint/devotional of the day” widget,
- EN/VI toggle,
- light/dark/simple themes,
- one parish domain,
- static fallback,
- 50,000 widget/API views per month,
- attribution footer: “Powered by Anno” or small source attribution,
- email support.

**Why this price is plausible:** OSV Simply Catholic Connect lists parish pricing at $49.99/month [5](https://www.osv.com/parish-diocese/communication/simply-catholic-connect/), and Flocknote’s Word on Fire ENGAGE bundle sits inside a $75/month Complete add-on [4](https://flocknote.com/engage/). Anno is narrower than those products, so $29/month is believable.

---

### Tier 3 — White-label / App Developer

**Recommended launch price:** **$149/month** or **$1,490/year**  
**Acceptable range:** $99–$299/month for small apps

**Includes:**

- commercial license,
- no public Anno branding required, except source/citation display if legal requires,
- API key,
- 250,000 API requests/month or equivalent MAU allowance,
- full coverage window,
- versioned feed contract,
- webhook/changelog notifications,
- email support,
- domain/app bundle allowlist.

**Overage:** $0.50–$1.00 per additional 1,000 API requests, or upgrade to custom.

---

### Tier 4 — Diocese / Publisher / Enterprise

**Recommended starting price:** **$499–$1,500/month**, custom annual contract

**Includes:**

- multiple parish domains/apps,
- 1M+ requests/month,
- optional private feed bucket,
- priority support,
- custom diocesan/parish feast overlays,
- contractual SLA,
- security/legal questionnaire,
- custom attribution terms,
- Spanish/local language roadmap discussion.

---

## A3. Copyright and licensing risk

This is the legal gate most likely to affect whether White-label can ship.

### What is probably lower-risk

- Historical facts, dates, names, feast days, and biographical facts are generally not protected by copyright. The U.S. Copyright Office states that facts are not copyrightable [3](https://www.copyright.gov/comp3/chap300/ch300-copyrightable-authorship.pdf).
- Anno can likely own or control its own original selection, arrangement, metadata, summaries, and editorial apparatus to the extent they are original and lawfully created. U.S. law recognizes compilations and derivative works, but copyright protection extends only to the new material contributed, not the underlying preexisting material [5](https://www.law.cornell.edu/uscode/text/17/103).

### What is higher-risk

- The feed is compiled from cited third-party sources. Citations do **not** automatically grant permission to redistribute, summarize commercially, or sublicense source-derived expression.
- Vatican legal notes say portal contents are for personal and nonprofit use, and reproduction/collection/commercial exploitation requires prior written authorization [2](https://www.vatican.va/content/vatican/en/legal-notes.html).
- USCCB permissions distinguish linking/RSS use from digital applications and other reproductions that require licenses or fees [5](https://usccb.org/bible/permissions/index.cfm?refresh=1).
- My Catholic Life! grants broad nonprofit Catholic use within limits, but says for-profit or ad-supported use should contact them first [3](https://mycatholic.life/copyright-permission/).
- If AI output is minimally human-edited, ownership/protection of the generated prose itself may be uncertain. U.S. Copyright Office guidance, as summarized by legal commentators, reaffirms that copyright protection requires human authorship and that purely AI-generated outputs without human creative input are not eligible for protection [1](https://www.sheppard.com/insights/blogs/the-copyright-offices-latest-guidance-on-ai-and-copyrightability).

### Human legal-review decisions required before White-label launch

A human attorney or qualified rights reviewer must decide:

1. **What exactly is being licensed:**  
   - compiled static feed,  
   - API access to Anno’s database,  
   - generated summaries only,  
   - metadata only,  
   - or a service that returns source-linked devotional cards.

2. **Whether Anno can sublicense the text.**  
   The question is not only “is the content factual?” but whether the summaries are too close to source expression, structure, translations, or protected compilations.

3. **Whether CC-BY-NC is appropriate.**  
   If any feed component includes third-party material Anno cannot sublicense, do not use a blanket Creative Commons license. Use custom Free Terms until rights are cleared.

4. **Whether source categories need different policies.**  
   Example:
   - public-domain hagiography,
   - Vatican documents,
   - Catholic encyclopedia material,
   - modern Catholic articles,
   - artwork metadata,
   - images,
   - liturgical readings,
   - Vietnamese translations.

5. **Whether White-label customers may cache/store the feed.**  
   API access with limited caching may be legally safer than selling bulk downloadable files.

6. **Attribution requirements.**  
   Decide whether end users must see source URLs, Anno attribution, both, or neither.

7. **Similarity policy.**  
   Add a rule: no long quotations, no copied paragraphs, no reproduced official readings unless separately licensed, and a human spot-check for high-risk entries.

8. **Takedown policy.**  
   Paid terms must allow Anno to remove/replace entries if a rightsholder objects.

### Recommendation

Ship **P0–P2 as a technical/public beta** with conservative noncommercial terms. Do **not** sign White-label commercial redistribution contracts until a human rights review produces a source-rights matrix.

---

# B. Product / Technical Spec

## B0. Current data reality (verified 2026-08-29)

Before building, know what is actually on disk. The external plan assumed a fully-sourced 4-year master; it is not.

| File | Entries | Non-empty `sources` | Notes |
|---|---:|---:|---|
| `Anno/Resources/anno_full_2026_2029.json` | 1461 | **0 / 1461** | 4-year master exists, but carries ZERO source citations. Do NOT point `export_feed.py` at this for a sourced feed. |
| `Anno/Resources/anno_unified_2026.json` | 182 | **182 / 182** | Jul 3–Dec 31 2026, EN/VI, ≥2 live sources each. Real. |
| `Anno/Resources/anno_unified_2027.json` | 31 | **31 / 31** | Jan 2027, sourced. Real. |
| `Anno/Resources/anno_devotional_pool_365.json` | **0** | 0 | The "365-day devotional pool" referenced in §0 / Deck D does NOT exist as data — file is empty. |

**Consequences for this spec:**
- The P0 exit criterion "all entries have ≥2 live sources" is satisfiable ONLY over `anno_unified_2026.json` + `anno_unified_2027.json` (213 days total), not over the master.
- Either (a) build the feed from the unified sourced files first, or (b) run a source-enrichment pass on `anno_full_2026_2029.json` before export. Option (a) is the short path to a real P0 deliverable.
- "1461-entry master" is real as a calendar/structure file; "sourced feed" coverage today is 213 days. State this honestly in any customer-facing material.

## B1. Feed contract principles

The feed should **extend** the internal `AnnoEntry` schema. It should not replace or mutate it.

Internal Anno remains:

- strict EN/VI,
- Swift-compatible,
- app-owned,
- normalized for the iOS app.

External feed becomes:

- consumer-facing,
- license-aware,
- versioned,
- source/provenance-forward,
- shaped around a language map:
  - current: `en`, `vi`
  - reserved future: `es`, only after Phase 4.

---

## B2. `feed_entry` schema

### Top-level shape

```json
{
  "schema_version": "feed_entry.v1",
  "feed_version": "2026.08.28.001",
  "entry_id": "anno-2026-08-28",
  "source_entry_id": "internal-anno-id",
  "date": "2026-08-28",
  "weekday": "Friday",

  "license": {
    "code": "CC-BY-NC-4.0",
    "name": "Anno Free Noncommercial Feed",
    "url": "https://wowthisiseasytoremember-stack.github.io/anno/terms/feed-free.html",
    "commercial_use_allowed": false,
    "redistribution_allowed": true,
    "derivatives_allowed": true,
    "requires_source_links": true
  },

  "attribution_required": true,
  "attribution_text": "Devotional content by Anno. Sources linked in entry.",
  "canonical_url": "https://wowthisiseasytoremember-stack.github.io/anno/feed/2026/08/feed.json#anno-2026-08-28",

  "languages": ["en", "vi"],

  "content": {
    "en": {
      "title": "English title",
      "liturgical_title": "English liturgical title",
      "summary": "English short summary.",
      "body": "English body.",
      "hero_line": "English hero line.",
      "prayer_prompt": "English prayer prompt.",
      "confidence_note": "English confidence note."
    },
    "vi": {
      "title": "Vietnamese title",
      "liturgical_title": "Vietnamese liturgical title",
      "summary": "Vietnamese short summary.",
      "body": "Vietnamese body.",
      "hero_line": "Vietnamese hero line.",
      "prayer_prompt": "Vietnamese prayer prompt.",
      "confidence_note": "Vietnamese confidence note."
    }
  },

  "primary": {
    "type": "saint|event|devotional|historical|contextual",
    "confidence": "confirmed|traditional|disputed|contextual"
  },

  "liturgical": {
    "rank": "Memorial",
    "color": "White"
  },

  "calendars": {
    "gregorian": "2026-08-28",
    "julian": "...",
    "hebrew": "...",
    "islamic_umm_al_qura": "...",
    "coptic": "...",
    "ethiopian": "..."
  },

  "place": {
    "name": "Optional place name",
    "latitude": 0.0,
    "longitude": 0.0,
    "confidence": "confirmed|traditional|disputed|contextual",
    "source_url": "https://example.com"
  },

  "artwork": {
    "title": "Artwork title",
    "maker": "Artist",
    "date_label": "c. 1500",
    "source_url": "https://example.com",
    "status": "public_domain_metadata_only|licensed|unknown|link_only"
  },

  "sources": [
    {
      "label": "Source label",
      "url": "https://example.com",
      "type": "vatican|encyclopedia|publisher|museum|other",
      "live_verified": true,
      "last_verified_at": "2026-08-28T00:00:00Z"
    }
  ],

  "quality": {
    "minimum_live_sources_required": 2,
    "live_source_count": 2,
    "source_policy": "dead URLs are dropped before export",
    "human_review_status": "not_reviewed|spot_checked|approved"
  },

  "cache": {
    "ttl_seconds": 3600,
    "stale_if_error_seconds": 86400
  }
}
```

### Required fields

For `feed_entry.v1`, the exporter must require:

- `schema_version`
- `feed_version`
- `entry_id`
- `date`
- `license`
- `attribution_required`
- `languages`
- `content.en`
- `content.vi`
- `primary`
- `liturgical`
- `calendars`
- `sources`
- `quality`

### Language rules

Current production rule:

```json
"languages": ["en", "vi"]
```

Current exporter must fail if:

- `content.en` missing,
- `content.vi` missing,
- any required English or Vietnamese field empty,
- `content.es` appears before Spanish Phase 4 is explicitly enabled.

Reserved Phase 4 rule:

```json
"languages": ["en", "vi", "es"],
"content": {
  "en": {},
  "vi": {},
  "es": {}
}
```

But `es` is **not emitted in P0–P3**.

---

## B3. Mapping from internal `AnnoEntry` to `feed_entry`

| `AnnoEntry` field | `feed_entry` field |
|---|---|
| `id` | `source_entry_id`, also used to derive `entry_id` |
| `date` | `date`, `calendars.gregorian` |
| `weekday` | `weekday` |
| `liturgical.rank` | `liturgical.rank` |
| `liturgical.color` | `liturgical.color` |
| `liturgical.titleEn` | `content.en.liturgical_title` |
| `liturgical.titleVi` | `content.vi.liturgical_title` |
| `calendars.julian` | `calendars.julian` |
| `calendars.hebrew` | `calendars.hebrew` |
| `calendars.islamicUmmAlQura` | `calendars.islamic_umm_al_qura` |
| `calendars.coptic` | `calendars.coptic` |
| `calendars.ethiopian` | `calendars.ethiopian` |
| `primary.type` | `primary.type` |
| `primary.titleEn` | `content.en.title` |
| `primary.titleVi` | `content.vi.title` |
| `primary.summaryEn` | `content.en.summary` |
| `primary.summaryVi` | `content.vi.summary` |
| `primary.confidence` | `primary.confidence` |
| `primary.confidenceNoteEn` | `content.en.confidence_note` |
| `primary.confidenceNoteVi` | `content.vi.confidence_note` |
| `primary.bodyEn` | `content.en.body` |
| `primary.bodyVi` | `content.vi.body` |
| `place` | `place` |
| `artwork` | `artwork` |
| `sources` | `sources`, with live-verification metadata if available |
| `appHooks.heroLineEn` | `content.en.hero_line` |
| `appHooks.heroLineVi` | `content.vi.hero_line` |
| `appHooks.prayerPromptEn` | `content.en.prayer_prompt` |
| `appHooks.prayerPromptVi` | `content.vi.prayer_prompt` |

---

## B4. Monthly feed file shape

Path:

```text
feed/YYYY/MM/feed.json
```

Example envelope:

```json
{
  "schema_version": "feed_month.v1",
  "feed_version": "2026.08.28.001",
  "generated_at": "2026-08-28T09:10:00Z",
  "coverage": {
    "start_date": "2026-08-01",
    "end_date": "2026-08-31",
    "entry_count": 31
  },
  "languages": ["en", "vi"],
  "license": {
    "code": "CC-BY-NC-4.0",
    "terms_url": "https://wowthisiseasytoremember-stack.github.io/anno/terms/feed-free.html"
  },
  "entries": [
    {}
  ]
}
```

Optional convenience aliases for P1:

```text
feed/YYYY/MM/DD.json
feed/today.json
feed/latest.json
```

But the canonical contract should be the monthly file plus index.

---

## B5. `feed.index.json`

Path:

```text
feed/feed.index.json
```

Shape:

```json
{
  "schema_version": "feed_index.v1",
  "latest_version": "2026.08.28.001",
  "generated_at": "2026-08-28T09:10:00Z",

  "coverage_window": {
    "start_date": "2026-01-01",
    "end_date": "2029-12-31",
    "dated_entries_available": 1461,
    "thematic_pool_available": 365
  },

  "languages": ["en", "vi"],

  "months": [
    {
      "year": 2026,
      "month": 8,
      "path": "feed/2026/08/feed.json",
      "entry_count": 31,
      "sha256": "..."
    }
  ],

  "license": {
    "free": {
      "code": "CC-BY-NC-4.0",
      "terms_url": "https://wowthisiseasytoremember-stack.github.io/anno/terms/feed-free.html",
      "attribution_required": true,
      "commercial_use_allowed": false
    },
    "paid": {
      "code": "ANNO-COMMERCIAL-FEED-V1",
      "terms_url": "https://anno.example.com/legal/commercial-feed"
    }
  },

  "deprecation_policy": {
    "schema_version_supported_until": null,
    "minimum_notice_days": 90
  }
}
```

---

## B6. `export_feed.py` interface

### Purpose

Transform internal normalized Anno fixtures into the consumer-facing feed contract.

### Inputs

- normalized Anno fixture JSON:
  - e.g. `Anno/Resources/anno_full_2026_2029.json` (4-year master; actual path — not repo root)
  - or any fixture shaped as `{ schemaVersion, generatedOn, total_entries, entries }`
  - other available fixtures: `Anno/Resources/anno_unified_2026.json` (182 dated EN/VI days), `Anno/Resources/anno_unified_2027.json`, `Anno/Resources/anno_devotional_pool_365.json`
- optional devotional pool fixture,
- source verification metadata,
- license configuration,
- terms URL,
- public base URL,
- feed version/build ID,
- output directory.

### Suggested CLI

```text
python export_feed.py \
  --input Anno/Resources/anno_unified_2026.json \
  --out feed/ \
  # NOTE (verified 2026-08-29): for a SOURCED feed use the unified files, not the
  # 4-year master. anno_full_2026_2029.json has 1461 entries but 0 sources.
  # To also cover Jan 2027, run again with --input Anno/Resources/anno_unified_2027.json
  # or concat the two before export. See B0.
  --feed-version 2026.08.28.001 \
  --license-profile free \
  --terms-url https://wowthisiseasytoremember-stack.github.io/anno/terms/feed-free.html \
  --public-base-url https://wowthisiseasytoremember-stack.github.io/anno/
```

Optional flags:

```text
--start-date 2026-01-01
--end-date 2029-12-31
--include-devotional-pool true|false
--daily-aliases true|false
--strict true
--dry-run
--report build/feed_export_report.json
```

### Outputs

```text
feed/feed.index.json
feed/YYYY/MM/feed.json
feed/YYYY/MM/DD.json                 optional
feed/latest.json                      optional
feed/today.json                       optional
build/feed_export_report.json
build/feed_changelog.json
```

### Validation rules

Exporter must fail if:

- any emitted entry has fewer than 2 live sources,
- any source URL is known dead,
- English or Vietnamese fields are missing,
- Spanish appears before Phase 4 enablement,
- license config missing,
- date is malformed,
- internal confidence enum has unexpected value,
- duplicate IDs exist,
- two entries map to same date unexpectedly,
- output cannot be reproduced deterministically.

### Idempotency contract

Given the same:

- input fixture,
- exporter version,
- license profile,
- build ID/feed version,
- and config,

`export_feed.py` must produce byte-stable JSON:

- sorted keys,
- stable entry ordering by date then ID,
- normalized Unicode,
- no wall-clock timestamps unless passed explicitly,
- deterministic SHA-256 hashes in manifest.

Writes should be atomic:

1. write to temporary build directory,
2. validate,
3. compute hashes,
4. replace `feed/` paths only after full success.

---

## B7. `build_feed.py` interface

### Purpose

Wrap existing Engine A, Engine B, normalizer, validators, and exporter into one Linux-only feed build pipeline.

### Inputs

- target date range,
- existing fixtures/master file,
- Engine A path/config,
- Engine B batch config,
- source allowlist,
- validation settings,
- output/publish path,
- feed license profile,
- environment variables for LLM/API keys if needed.

### Suggested CLI

```text
python build_feed.py \
  --start-date 2026-01-01 \
  --end-date 2029-12-31 \
  --mode nightly \
  --resume \
  --input-master Anno/Resources/anno_unified_2026.json \
  # NOTE (verified 2026-08-29): see B0 — the 4-year master has 0 sources.
  # Use the unified sourced files; enrich the master in a later pass if needed.
  --out feed/ \
  --state build/feed_build_state.sqlite \
  --feed-version auto
```

Useful modes:

```text
--mode backfill
--mode nightly
--mode validate-only
--mode export-only
--mode dry-run
```

### Pipeline steps

1. Load current master fixture.
2. Detect missing or stale entries by date/month.
3. Run Engine A for deterministic calendar fields.
4. Run Engine B only for missing/dirty chunks.
5. Validate Engine B output.
6. Verify live sources.
7. Drop/replace dead URLs.
8. Normalize to internal `AnnoEntry`.
9. Merge into master fixture.
10. Export feed via `export_feed.py`.
11. Validate feed contract.
12. Write manifest and changelog.
13. Publish static files or hand off to deployment.

### Resumability

State file should track:

```json
{
  "job_id": "2026-08-28-nightly",
  "started_at": "2026-08-28T09:00:00Z",
  "target_range": ["2026-01-01", "2029-12-31"],
  "chunks": [
    {
      "chunk_id": "2027-02",
      "status": "pending|running|succeeded|failed",
      "attempts": 0,
      "input_hash": "...",
      "output_hash": "...",
      "last_error": null
    }
  ]
}
```

If interrupted, rerunning with `--resume` continues from failed/pending chunks without regenerating successful months.

### Nightly cron

Example:

```text
10 2 * * * cd /home/anno && python build_feed.py --mode nightly --resume --feed-version auto
```

Nightly should:

- check for source rot,
- revalidate sources,
- regenerate affected entries only,
- publish a new feed version if content or source status changed,
- leave feed untouched if no changes.

---

## B8. Delivery spec

## Free static delivery

Base URL already exists:

```text
https://wowthisiseasytoremember-stack.github.io/anno/
```

Recommended paths:

```text
/anno/feed/feed.index.json
/anno/feed/2026/08/feed.json
/anno/feed/latest.json
/anno/terms/feed-free.html
/anno/terms/attribution.html
```

Free feed should include:

- attribution requirement,
- noncommercial terms,
- source links,
- no SLA,
- no API keys,
- no personalized license fields.

---

## Paid API delivery

Technology:

- FastAPI or Flask,
- SQLite for customer/key registry,
- reads immutable files under `feed/`,
- can run on the existing Linux box or a small VPS,
- no Mac dependency.

### Auth

Header:

```text
Authorization: Bearer anno_live_xxx
```

Widget may use:

```text
?widget_key=anno_widget_xxx
```

API keys should be:

- generated once,
- stored hashed,
- displayed with prefix/last4 only,
- scoped by tier,
- revocable,
- tied to allowed origins/domains/app bundle IDs.

---

## B9. API surface

### Public health

```text
GET /healthz
```

Returns:

```json
{
  "ok": true,
  "feed_version": "2026.08.28.001"
}
```

---

### Index

```text
GET /v1/feed/index
```

Auth:

- optional for Free,
- required for paid license envelope.

Returns `feed.index.json`.

---

### Monthly feed

```text
GET /v1/feed/{year}/{month}
```

Example:

```text
GET /v1/feed/2026/08?lang=en,vi
```

Returns monthly feed envelope.

---

### Entry by date

```text
GET /v1/entries/{date}
```

Example:

```text
GET /v1/entries/2026-08-28?lang=en
```

Returns one `feed_entry`, optionally language-filtered.

---

### Today

```text
GET /v1/entries/today?tz=America/Los_Angeles&lang=en
```

Rules:

- server resolves date by timezone,
- default timezone can be customer-configured,
- if no dated entry exists, optionally fall back to devotional pool.

---

### Range

```text
GET /v1/entries?start=2026-08-01&end=2026-08-31&lang=vi
```

Useful for apps that pre-cache.

---

### Sources

```text
GET /v1/entries/{date}/sources
```

Returns only source metadata.

---

### Usage

```text
GET /v1/usage/current
```

Returns customer usage for current billing period.

---

### Widget

```text
GET /widget/saint-of-the-day
```

Query params:

```text
?key=anno_widget_xxx
&lang=en
&theme=light
&tz=America/Los_Angeles
&mode=compact
```

Returns embeddable HTML designed for iframe use.

Default recommendation: **iframe first**, not headless JS.

Why:

- easier for parishes,
- safer cross-site isolation,
- avoids CMS conflicts,
- makes attribution/terms easier,
- simpler to cache,
- less support burden.

A headless JS snippet can come later for advanced customers.

---

## B10. Rate limits

Recommended launch limits:

| Tier | Rate limit | Monthly included usage |
|---|---:|---:|
| Free static | GitHub Pages only | No SLA |
| Trial API | 30 req/min | 2,000 req/month |
| Parish | 60 req/min | 50,000 req/month |
| White-label | 300 req/min | 250,000 req/month |
| Enterprise | Custom | Custom |

Caching should be strongly encouraged:

```text
ETag: "sha256..."
Cache-Control: public, max-age=3600, stale-while-revalidate=86400
```

Immutable versioned files may use longer cache:

```text
Cache-Control: public, max-age=31536000, immutable
```

---

## B11. `usage_log` shape

SQLite table or JSONL stream:

```json
{
  "id": "uuid",
  "ts": "2026-08-28T09:12:30Z",
  "customer_id": "cus_123",
  "api_key_id": "key_123",
  "tier": "parish|white_label|enterprise",

  "method": "GET",
  "endpoint": "/v1/entries/today",
  "status_code": 200,
  "response_ms": 42,
  "bytes_out": 18400,

  "date_requested": "2026-08-28",
  "languages_requested": ["en"],
  "feed_version": "2026.08.28.001",

  "ip_hash": "rotating-salted-hash",
  "user_agent_hash": "hash",
  "referrer_origin": "https://exampleparish.org",
  "widget_domain": "exampleparish.org",

  "cache_status": "hit|miss|bypass",
  "billable_unit": "api_request|widget_view|monthly_active_user",
  "units": 1
}
```

Privacy rule:

- store hashed IP/user-agent only,
- rotate salt monthly,
- do not store raw devotional-user PII,
- let customers see aggregate counts.

---

## B12. `customers/` registry shape

SQLite tables:

### `customers`

```json
{
  "customer_id": "cus_123",
  "name": "St. Example Parish",
  "tier": "parish",
  "status": "trial|active|past_due|cancelled",
  "billing_provider": "stripe|manual|none",
  "stripe_customer_id": "cus_xxx",
  "license_code": "ANNO-COMMERCIAL-FEED-V1",
  "attribution_required": true,
  "allowed_domains": ["exampleparish.org"],
  "allowed_bundle_ids": [],
  "monthly_request_quota": 50000,
  "monthly_mau_quota": null,
  "created_at": "2026-08-28T00:00:00Z"
}
```

### `api_keys`

```json
{
  "api_key_id": "key_123",
  "customer_id": "cus_123",
  "prefix": "anno_live",
  "key_hash": "argon2/bcrypt hash",
  "last4": "abcd",
  "scopes": ["entries:read", "widget:read"],
  "created_at": "2026-08-28T00:00:00Z",
  "revoked_at": null
}
```

---

# B13. Phased Build Plan

## P0 — Feed contract + exporter

**Goal:** Turn `AnnoEntry` into stable external `feed_entry`.

**Work:**

- define `feed_entry.v1`,
- implement export interface,
- monthly feed files,
- `feed.index.json`,
- validation report,
- license envelope,
- strict EN/VI checks,
- no Spanish emission.

**Effort:** 1–2 days

**Infra cost:** $0

**Dependencies:** existing fixture files and validators.

**Exit criteria:**

- reproducible `feed/` directory,
- all entries have EN/VI,
- all entries have ≥2 live sources,
- `feed.index.json` correct,
- no Xcode/Mac involved.

---

## P1 — Static publish on GitHub Pages

**Goal:** Public noncommercial feed.

**Work:**

- publish `/feed/` to existing GitHub Pages site,
- add free terms page,
- add attribution instructions,
- add simple README/docs,
- add smoke test that fetches index/month/today,
- optional GitHub Actions or cron deploy.

**Effort:** 0.5–1.5 days

**Infra cost:** $0

**Spend required:** none.

**Exit criteria:**

- `feed.index.json` reachable publicly,
- monthly JSON reachable,
- docs include license/attribution/noncommercial warning,
- static feed works without any app build.

---

## P2 — Thin API + key auth

**Goal:** Paid-ready API wrapper over static files.

**Work:**

- FastAPI/Flask service,
- API key auth,
- SQLite customers/key registry,
- rate limits,
- usage logging,
- ETag/cache headers,
- `/v1/entries/today`,
- `/v1/entries/{date}`,
- `/v1/feed/{year}/{month}`,
- `/v1/usage/current`,
- deployment script.

**Effort:** 2–4 days

**Infra cost:**  
- $0 marginal if run on existing paid Linux box.  
- Otherwise $5–$20/month VPS/app host.

**Spend required:** likely small if public API uptime matters.

**Exit criteria:**

- one test API key,
- one active customer row,
- usage logs,
- 429 rate-limit behavior,
- API reads static feed, does not regenerate content live.

---

## P3 — Parish iframe widget

**Goal:** Sellable parish embed.

**Work:**

- iframe endpoint,
- compact/full themes,
- EN/VI toggle,
- domain allowlist,
- fallback state,
- copy-paste embed docs,
- sample parish landing page,
- widget view metering.

**Effort:** 2–3 days

**Infra cost:** $0 incremental if P2 exists.

**Spend required:** none beyond API hosting.

**Exit criteria:**

- parish can paste one iframe line,
- widget works on WordPress/eCatholic-style sites,
- small attribution/footer rendered,
- usage logged by domain.

---

## P4 — Spanish extension

**Goal:** Add Spanish honestly, not by pretending it already exists.

**Current state:** no Spanish field exists in internal schema.

**Work:**

- decide schema strategy:
  - Option A: add Spanish fields internally wherever EN/VI fields exist: `titleEs`, `summaryEs`, `bodyEs`, `confidenceNoteEs`, `heroLineEs`, `prayerPromptEs`, liturgical `titleEs`;
  - Option B: keep internal `AnnoEntry` unchanged and add a separate `feed_localizations_es.json` overlay keyed by `id`.
- add language enum case: `es`,
- run Engine B Spanish research/translation pass,
- validate Spanish content,
- verify Spanish-specific sources if used,
- update exporter to emit `content.es`,
- update docs/API/widget language toggle,
- update tests to require `en`/`vi` and optionally validate `es`.

**Effort:** 2–4 weeks depending on coverage and human QA.

**Infra cost:**  
- code/schema work can be $0,  
- LLM generation/backfill may cost money,  
- human review likely costs time or contractor spend.

**Spend required:** likely LLM/API cost and possibly review.

**Exit criteria:**

- `languages: ["en", "vi", "es"]` only for entries with complete Spanish,
- no partial fake Spanish,
- fallback behavior documented.

---

## P5 — B2B metering + billing

**Goal:** Turn API/widget into managed recurring revenue.

**Default billing metric:** **per-MAU tier**, not per-entry.

Why:

- per-entry pricing discourages caching and creates bad incentives,
- most customers display one daily item,
- value correlates with audience size,
- requests remain useful for abuse/rate limiting.

**Work:**

- Stripe account/products/prices,
- webhook handling,
- customer portal links,
- automatic key provisioning,
- invoices/receipts,
- tier upgrades,
- quota alerts,
- overage reporting,
- monthly usage summaries,
- admin dashboard or CLI.

**Effort:** 1–2 weeks

**Infra cost:**  
- Stripe has no large upfront platform cost but charges transaction fees,  
- API hosting/monitoring/domain likely $10–$50/month,  
- email service may add low monthly cost.

**Spend required:** yes, if operating commercially.

**Exit criteria:**

- customer can subscribe,
- key is provisioned,
- billing status controls access,
- usage is visible,
- overage/quota policy enforced.

---

# C. Honest Failure Analysis

## C1. What makes this “just a JSON file” instead of SaaS?

It becomes “just a JSON file” if:

- anyone can copy the full feed once,
- there is no license wrapper,
- there is no update cadence,
- there is no support,
- there is no versioning,
- there is no SLA,
- there is no metering,
- there is no reason to keep paying,
- and no customer pain is solved beyond “I downloaded some content.”

Static JSON alone is a distribution format, not a business.

## C2. How the plan avoids that trap

The SaaS value is not the bytes. The value is:

1. **Continuity** — nightly updates, source liveness checks, replacement of dead citations.
2. **Trust** — source-gated entries and a visible citation policy.
3. **Contract** — stable schema, versioning, deprecation policy.
4. **Rights** — clear free vs commercial terms.
5. **Convenience** — iframe widget for parishes; API for apps.
6. **Support** — parish/developer onboarding.
7. **Metering** — API keys, usage logs, quotas.
8. **Roadmap** — Spanish, diocesan overlays, custom feeds.
9. **Fallback/offline** — consumers can cache safely without owning the generation pipeline.

The product is not “download this JSON.”  
The product is “never staff a devotional content pipeline again.”

## C3. Single risk most likely to kill it

**Copyright/licensing.**

If human legal review concludes that the compiled feed cannot be commercially redistributed without permissions from many third-party sources, White-label licensing may be blocked or forced into a slower rights-clearance model.

Mitigation:

- avoid reproducing protected readings or long quotes,
- keep source links,
- build rights matrix,
- prefer public-domain / permissioned sources,
- maintain takedown workflow,
- initially sell API access with limited caching rather than bulk redistribution,
- use human-reviewed original summaries for commercial tiers.

---

# D. Customer Pitch Deck — Markdown

# Slide 1 — Daily Catholic content without a daily content team

Parishes, dioceses, and Catholic app developers need fresh devotional content every day.  
Producing it well is slow, expensive, and hard to keep sourced.

Anno gives you a ready-to-embed devotional feed.

---

# Slide 2 — The problem

Quality Catholic daily content is not just “write a saint bio.”

You need:

- accurate dates,
- trustworthy sources,
- readable summaries,
- prayer prompts,
- bilingual presentation,
- and regular updates.

Most small teams do not have time for that every day.

---

# Slide 3 — The product

Anno is a continuously updated Catholic devotional feed.

It provides:

- daily devotional / saint / Catholic-history entries,
- English and Vietnamese today,
- source links on every entry,
- calendar metadata,
- API delivery,
- and an embeddable parish widget.

Spanish is planned as a future extension.

---

# Slide 4 — Built for trust

Every shipped entry is designed around a source-first policy:

- at least two live sources,
- source URLs included,
- dead links removed before export,
- structured confidence labels,
- deterministic calendar conversion.

Your visitors can see where the content came from.

---

# Slide 5 — Built for bilingual communities

Anno is bilingual today:

- English,
- Vietnamese.

That makes it especially useful for parishes and ministries serving Vietnamese Catholic communities.

Spanish is not live yet, but the feed contract is designed to support it later.

---

# Slide 6 — Use it two ways

For parishes:

> Paste one iframe into your website and show today’s devotional entry.

For apps:

> Call the API and display the same daily entry inside your own product.

No content team required.

---

# Slide 7 — Proof already exists

Anno already has:

- a 365-day devotional pool,
- a 4-year 2026–2029 master dataset,
- bilingual EN/VI entries,
- source-gated validation,
- deterministic multi-calendar conversion,
- and a Linux-only production pipeline.

This is packaging work, not a blank-page content project.

---

# Slide 8 — Tiers

**Free**  
Static noncommercial feed with attribution.

**Parish — $29/month or $299/year**  
Embeddable widget, EN/VI toggle, one domain, support.

**White-label — from $149/month**  
Commercial API license for Catholic apps, publishers, and larger ministries.

Custom diocesan pricing available.

---

# Slide 9 — Why not just copy content from the web?

Because someone still has to:

- find it,
- verify it,
- structure it,
- translate it,
- keep links alive,
- update it,
- and make it app-ready.

Anno handles the pipeline.

---

# Slide 10 — Start simple

Start with the Free feed.

If it helps your parish or app, upgrade to Parish or White-label.

**Call to action:**  
Start on Free, then talk to us when you want the widget, API key, or commercial license.

---

# E. Internal Pitch Deck / Project Soul — Markdown

# Slide 1 — Anno is bigger than the app

The iOS app is the flagship.

But the deeper asset is the devotional content engine:

> a source-gated, bilingual, calendar-aware Catholic content utility.

That can serve many consumers, not just one App Store binary.

---

# Slide 2 — Why now

The producing side already runs on a paid-for Linux box.

No Xcode.  
No Mac.  
No App Store review.  
No Swift compile gate.

The bottleneck is not content generation.  
The bottleneck is packaging and distribution.

---

# Slide 3 — The leverage

Right now Anno has one possible revenue line:

> the iOS app, blocked by the compile gate.

The feed creates many possible revenue lines:

- parish websites,
- Catholic app developers,
- diocesan communication teams,
- publishers,
- the Anno app itself.

One dataset. Many consumers.

---

# Slide 4 — What already exists

The brief says Anno already has:

- 365-day devotional pool,
- 213 dated generated entries,
- 1461-entry 2026–2029 master file,
- EN/VI bilingual content,
- at least two live sources per shipped entry,
- deterministic multi-calendar conversion,
- resumable generation pipeline.

That is not an idea.  
That is inventory.

---

# Slide 5 — The $0-infra path

You can get surprisingly far without new spend:

- P0 exporter: $0
- P1 GitHub Pages static feed: $0
- docs/terms/attribution page: $0
- static monthly JSON: $0
- first developer integrations: $0

This proves demand before billing infrastructure.

---

# Slide 6 — Where spend begins

Spend starts when this becomes a real business:

- API hosting if uptime matters,
- domain/email/monitoring,
- Stripe fees,
- legal review,
- maybe LLM cost for Spanish,
- maybe human QA.

Do not spend on billing before the feed contract and static proof exist.

---

# Slide 7 — The phased plan

P0 — feed contract + exporter  
P1 — static GitHub Pages publish  
P2 — API + key auth  
P3 — parish iframe widget  
P4 — Spanish extension  
P5 — B2B metering + Stripe billing

Build in that order.

Do not jump to P5 before P0–P3 prove utility.

---

# Slide 8 — The honest trouble

Three things can make this fail:

1. It becomes “just a JSON file.”
2. Customers do not care enough to pay.
3. Copyright/legal review blocks commercial redistribution.

The third one is the kill-risk.

---

# Slide 9 — The legal gate

Before White-label ships, a human must decide:

- whether Anno can sublicense the compiled feed,
- whether source-derived summaries are safe,
- whether CC-BY-NC can be used,
- whether customers can cache/store entries,
- and which source categories need permission.

This is not an engineering decision.

---

# Slide 10 — What it needs from Justin

Justin needs to provide:

- the legal-review decision for White-label,
- final pricing tolerance,
- a Stripe account when P5 starts,
- customer conversations,
- and a Mac session only if/when the iOS app itself ships.

The feed does not wait on the Mac.

---

# Slide 11 — Project soul

Anno is not fundamentally an app.

Anno is a devotional content utility:  
a source-gated, bilingual, calendar-aware Catholic memory engine that turns each day into a trustworthy act of prayer and remembrance.

The invariant:

> Never ship an entry with dead, missing, or uncited sources.  
> Never pretend a language exists before the schema and research support it.  
> The moat is trust. Keep the moat.
