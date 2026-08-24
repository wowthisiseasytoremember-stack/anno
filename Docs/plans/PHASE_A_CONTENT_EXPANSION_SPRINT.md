# Phase A: Server-Side Content Expansion — Granular Sprint Plan

**Parent Plan:** [`docs/plans/CONSOLIDATED_AUDIT_AND_EXPANSION_PLAN.md`](file:///home/ichabod/Projects/Anno/docs/plans/CONSOLIDATED_AUDIT_AND_EXPANSION_PLAN.md)  
**Execution Environment:** Linux Server (`ichabod`)  
**Target Output:** 182-day continuous bilingual Catholic historical dataset (July 3, 2026 – December 31, 2026) with $\ge 2$ validated primary sources per entry and 365-day rotation pool.  
**Concurrency Profile:** High (Sprints A.1, A.2, and A.5 can run in parallel; A.2 & A.3 are pipelined per month; A.4 is the final sync barrier).

---

## Sprint A.1: Source Citation Backfill & Verification Gate (45 Days) `[PARALLELIZABLE — IMMEDIATE]`
**Target:** 2026-07-03 → 2026-07-16 (14 days) and 2026-08-01 → 2026-08-31 (31 days)  
**Dependencies:** None. Can run immediately in parallel with Sprint A.2, A.5, and all Phase B sprints.

### Context & Problem
Currently, 45 of 59 entries in [`Anno/Resources/anno_unified_2026.json`](file:///home/ichabod/Projects/Anno/Anno/Resources/anno_unified_2026.json) have empty `sources: []` lists. [`tools/validate_mock_content.py`](file:///home/ichabod/Projects/Anno/tools/validate_mock_content.py) strictly requires at least 2 primary source citations per entry.

### Tasks
- [x] **A.1.1 — Create Citation Backfill Engine (`tools/backfill_citations.py`):**
  Write a Python script that iterates over all 45 unreferenced entries, looks up the corresponding saint/feast day, and generates structured citation objects compliant with [`docs/ANNO_CONTENT_SCHEMA.md`](file:///home/ichabod/Projects/Anno/docs/ANNO_CONTENT_SCHEMA.md).
- [x] **A.1.2 — Sourcing Standard Adherence:**
  Ensure every entry includes at least 2 valid, high-authority references:
  * *Primary Liturgical:* *Martyrologium Romanum* (Editio Altera 2004) or USCCB Liturgical Calendar.
  * *Historical/Hagiographical:* Alban Butler's *The Lives of the Fathers, Martyrs, and Other Principal Saints* (1866/1886 editions, public domain via New Advent/Internet Archive) or *Acta Sanctorum* (Bollandists).
  * *Patristic/Doctor Writings:* St. Augustine, Eusebius' *Ecclesiastical History*, St. Jerome's *De Viris Illustribus*, St. Thomas Aquinas' *Summa Theologiae*.
- [x] **A.1.3 — Ingest Citations into Unified Dataset:**
  Update entries in `data/mock/anno_fortnight_2026-07-03_2026-07-16.json` and `data/mock/anno_august_2026.json`.
- [x] **A.1.4 — Gate Verification:**
  Run `python3 tools/validate_mock_content.py Anno/Resources/anno_unified_2026.json` and verify 0 errors.

---

## Sprint A.2: Engine B Batch Research Generation (Sep 1 – Dec 31, 2026 / 122 Days) `[PARALLELIZABLE BY MONTH]`
**Target:** 122 daily research dossiers generated in `data/research_results/`  
**Dependencies:** None. Can run immediately. Batches 1–4 (Sep, Oct, Nov, Dec) can be executed concurrently by separate batch workers.

### Batch Breakdown
* **Batch 1 (September 2026 — 30 days):** St. Gregory the Great (Sep 3), Nativity of the Blessed Virgin Mary (Sep 8), Exaltation of the Holy Cross (Sep 14), Our Lady of Sorrows (Sep 15), St. Matthew (Sep 21), St. Padre Pio (Sep 23), Archangels Michael, Gabriel, Raphael (Sep 29), St. Jerome (Sep 30).
* **Batch 2 (October 2026 — 31 days):** St. Thérèse of Lisieux (Oct 1), Holy Guardian Angels (Oct 2), St. Francis of Assisi (Oct 4), Our Lady of the Rosary (Oct 7), St. Teresa of Ávila (Oct 15), St. Ignatius of Antioch (Oct 17), St. Luke (Oct 18), St. John Paul II (Oct 22), Sts. Simon and Jude (Oct 28).
* **Batch 3 (November 2026 — 30 days):** Solemnity of All Saints (Nov 1), All Souls' Day (Nov 2), St. Charles Borromeo (Nov 4), Dedication of the Lateran Basilica (Nov 9), St. Leo the Great (Nov 10), St. Martin of Tours (Nov 11), St. Frances Xavier Cabrini (Nov 13), St. Cecilia (Nov 22), St. Catherine of Alexandria (Nov 25), Our Lord Jesus Christ, King of the Universe (Nov 22/29), St. Andrew (Nov 30).
* **Batch 4 (December 2026 — 31 days):** St. Francis Xavier (Dec 3), St. Nicholas (Dec 6), St. Ambrose (Dec 7), Solemnity of the Immaculate Conception (Dec 8), Our Lady of Guadalupe (Dec 12), St. Lucy (Dec 13), St. John of the Cross (Dec 14), Nativity of the Lord / Christmas (Dec 25), St. Stephen (Dec 26), St. John the Apostle (Dec 27), Holy Innocents (Dec 28), Holy Family of Jesus, Mary and Joseph.

### Tasks
- [ ] **A.2.1 — Batch Orchestrator (`tools/batch_generate_engine_b.py`):**
  Write an automated runner feeding date payloads from `calendar_2026_2029.jsonl` into Engine B prompt templates (`docs/research/anno-research-prompt-main.md`).
- [ ] **A.2.2 — Rate Limit & Error Handling:**
  Implement exponential backoff, response caching, and error logs (`data/research_results/errors.log`).
- [ ] **A.2.3 — Validation Sweep:**
  Validate all 122 generated JSON files with `tools/validate_engine_b_output.py`.

---

## Sprint A.3: Vietnamese Localization & Diacritic Audit (122 Days) `[PIPELINED PER MONTH]`
**Target:** 122 sibling `_result_vi.json` files generated and audited for grammatical/liturgical accuracy.  
**Dependencies:** Pipelined per month slice as Sprint A.2 completes each month (e.g. Sep translation runs while Oct research generates).

### Tasks
- [ ] **A.3.1 — Vietnamese Translation Batch Runner (`tools/translate_batch_vi.py`):**
  Translate all 122 English research outputs into Vietnamese using standard Catholic Vietnamese ecclesiastical terminology (e.g. *Lễ Trọng*, *Lễ Kính*, *Lễ Nhớ*, *Thánh Tử Đạo*, *Kinh Cầu*).
- [ ] **A.3.2 — Terminology & Diacritic Enforcement:**
  Run automated regex audits to ensure proper Vietnamese tone mark rules:
  * Strict distinction between `Kỷ lục/Kỷ nguyên` vs old forms.
  * Correct capitalization for Catholic honorifics (*Đức Mẹ Maria*, *Thánh Cả Giuse*, *Chúa Giêsu Kitô*).
- [ ] **A.3.3 — Sibling Files Output:**
  Write corresponding `data/research_results/anno-YYYY-MM-DD_result_vi.json` for every day.

---

## Sprint A.4: Unified Fixture Merging & Normalization (182-Day Archive) `[SYNCHRONIZATION BARRIER]`
**Target:** [`Anno/Resources/anno_unified_2026.json`](file:///home/ichabod/Projects/Anno/Anno/Resources/anno_unified_2026.json) expanded to 182 days.  
**Dependencies:** Requires completion of Sprints A.1, A.2, and A.3.

### Tasks
- [ ] **A.4.1 — Update Normalizer (`tools/normalize_fixture.py`):**
  Expand input sources to concatenate:
  * July 3 – July 16 (Fortnight)
  * July 17 – July 30 (Engine B Initial Batch)
  * July 31 (Engine B)
  * August 1 – August 31 (August Batch)
  * September 1 – December 31 (Sprints A.2 + A.3 Batch)
- [ ] **A.4.2 — Guarantee Schema Compliance:**
  Verify that all 182 entries have identical schema keys, valid colors, valid icon tokens, and zero null localized leaves (`title_vi`, `summary_vi`, `body_vi`, `prayer_vi`).
- [ ] **A.4.3 — Export Swift Mock Data:**
  Run `python3 tools/export_swift_fixture.py` to regenerate [`ios-fixtures/AnnoMockData.swift`](file:///home/ichabod/Projects/Anno/ios-fixtures/AnnoMockData.swift).

---

## Sprint A.5: Devotional Pool (365-Day Rotation) Synthesis `[PARALLELIZABLE — IMMEDIATE]`
**Target:** [`Anno/Resources/anno_devotional_pool_365.json`](file:///home/ichabod/Projects/Anno/Anno/Resources/anno_devotional_pool_365.json)  
**Dependencies:** None. Fully independent of daily liturgical calendar generations.


### Tasks
- [ ] **A.5.1 — Pool Structure Definition:**
  Create a rotating pool of 365 daily devotionals indexed by day-of-year (1–365) for fallback and Ordinary Time meditation.
- [ ] **A.5.2 — Content Sourcing:**
  Extract and curate public domain readings from:
  * *The Imitation of Christ* (Thomas à Kempis)
  * *Introduction to the Devout Life* (St. Francis de Sales)
  * *Confessions* (St. Augustine)
  * Daily Scripture verses from Catholic Public Domain Version (CPDV) / Douay-Rheims.
- [ ] **A.5.3 — Bilingual Pairing (EN + VI):**
  Pair English devotional texts with Vietnamese Catholic translations.
- [ ] **A.5.4 — Swift Integration:**
  Ensure loader compatibility with [`Anno/Services/AnnoDevotionalLoader.swift`](file:///home/ichabod/Projects/Anno/Anno/Services/AnnoDevotionalLoader.swift).

---

## Phase A Acceptance Criteria & Done Definition
1. `python3 tools/validate_mock_content.py Anno/Resources/anno_unified_2026.json` passes with **zero errors** across all 182 days.
2. Every entry contains $\ge 2$ primary source citations with non-empty titles and authors.
3. Every entry has 100% complete Vietnamese mirror fields with zero missing diacritics.
4. `ios-fixtures/AnnoMockData.swift` compiles cleanly and contains valid static JSON strings.
