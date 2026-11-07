# ANNO fortnight editorial audit — 2026-07-03 through 2026-07-16

**Claimed area:** **all 14** daily source records in `data/mock/anno_fortnight_2026-07-03_2026-07-16.json`. Audit taken **before edits**, 2026-11-06. The normalized Swift payload is `Anno/Resources/anno_unified_2026.json`. This is one 14-day tranche of [issue #36](https://github.com/wowthisiseasytoremember-stack/anno/issues/36), not a claim that the other 164 days have been cleared.

**Environment and convention:** Native SwiftUI/MapKit Catholic-first devotional app, EN-primary with VI only required on eight major feasts (none of these fourteen). Markdown docs under `docs/` hold canonical review notes. GitHub merge ships **source**, not an App Store/TestFlight release. No Mac/Xcode available. Google Drive's ANNO archive currently contains East Asian pilgrimage historical background and no July US liturgical authority; it was consulted for context, not used to validate dates.

**Source-of-truth for this audit:** [USCCB `2026cal.pdf` July, printed pp. 31–32](https://www.usccb.org/resources/2026cal.pdf) (rank/color/optional memorials/readings), plus dated `bible.usccb.org/bible/readings/MMDD26.cfm` pages. The official [Marian Days organizer](https://www.ngaythanhmau.net/en) and [Carthage city announcement](https://www.carthagemo.gov/o/parksandrec/article/3040298) explicitly date the 2026 event **Aug 6–9 in Carthage, Missouri**. This gathering is **not** a general liturgical feast on July 9–11.

## Item-by-item baseline findings — issue / severity / proposed fix

The severity ranks are for the **shipped content risk**, not claims about individual volunteer faith communities. "Feria" here denotes a weekday default; optional memorials may be legitimately observed locally without changing the default app date label. The U.S. national calendar is used because the product targets U.S. Catholic audiences; do not apply these rankings automatically to every global/local proper calendar.

### 2026-07-03 — target: Saint Thomas, Apostle

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Calendar identity shows **Feria in Ordinary Time / Feria / verdigris**, versus USCCB **Saint Thomas, Apostle / Feast / red**. | **high** | Replace rank/color/title/EN-VI memorial type with the official 2026-07-03 celebration; do not confuse annual gatherings with a liturgical rank. |
| Summary and first paragraph are recycled across days; headline never explains **John 20:24–29**. Saint Thomas's feast is entirely suppressed. | **high** | Re-author the full opening, EN/VI devotional text and original prayer around John 20:24–29 using the dated USCCB reading; keep assertions limited to established scriptures. |
| Vietnamese body starts with unlocalized English weekday (“Friday”), and its boilerplate repeats rather than contextualizing the reading. | **medium** | Remove English weekday token; draft fresh VI phrasing and mark that native-speaker Catholic review is outstanding (not certified). |
| Citation mismatch/weakness: first source points to daily readings but entry does not match it. Secondary site may describe a different saint or generic norms. | **medium** | Use day-specific 2026-07-03 USCCB readings and official 2026 USCCB calendar as authority; retain only clearly relevant background citations. |
| Artwork claims **cleared** with `example.com/placeholder.jpg`, and no license, alt text or caption. `place` asserts fabricated geolocation/provenance (Universal Church; `example.com`). | **high** | Mark artwork placeholder/unassigned and drop fake URL/site coordinates; retain artwork/captions/alt as non-shipping draft slots in reusable template. |

### 2026-07-04 — target: Saturday of the Thirteenth Week in Ordinary Time

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Calendar identity shows **Feria in Ordinary Time / Feria / verdigris**, versus USCCB **Saturday of the Thirteenth Week in Ordinary Time / Feria / green**. | **high** | Replace rank/color/title/EN-VI memorial type with the official 2026-07-04 celebration; do not confuse annual gatherings with a liturgical rank. |
| Summary and first paragraph are recycled across days; headline never explains **Matthew 9:14–17**.  | **high** | Re-author the full opening, EN/VI devotional text and original prayer around Matthew 9:14–17 using the dated USCCB reading; keep assertions limited to established scriptures. |
| Vietnamese body starts with unlocalized English weekday (“Saturday”), and its boilerplate repeats rather than contextualizing the reading. | **medium** | Remove English weekday token; draft fresh VI phrasing and mark that native-speaker Catholic review is outstanding (not certified). |
| Citation mismatch/weakness: first source points to daily readings but entry does not match it. Secondary site may describe a different saint or generic norms. | **medium** | Use day-specific 2026-07-04 USCCB readings and official 2026 USCCB calendar as authority; retain only clearly relevant background citations. |
| Artwork claims **cleared** with `example.com/placeholder.jpg`, and no license, alt text or caption. `place` asserts fabricated geolocation/provenance (Universal Church; `example.com`). | **high** | Mark artwork placeholder/unassigned and drop fake URL/site coordinates; retain artwork/captions/alt as non-shipping draft slots in reusable template. |

### 2026-07-05 — target: Fourteenth Sunday in Ordinary Time

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Calendar identity shows **Sunday in Ordinary Time / Sunday / verdigris**, versus USCCB **Fourteenth Sunday in Ordinary Time / Sunday / green**. | **high** | Replace rank/color/title/EN-VI memorial type with the official 2026-07-05 celebration; do not confuse annual gatherings with a liturgical rank. |
| Summary and first paragraph are recycled across days; headline never explains **Matthew 11:25–30**.  | **high** | Re-author the full opening, EN/VI devotional text and original prayer around Matthew 11:25–30 using the dated USCCB reading; keep assertions limited to established scriptures. |
| Vietnamese body starts with unlocalized English weekday (“Sunday”), and its boilerplate repeats rather than contextualizing the reading. | **medium** | Remove English weekday token; draft fresh VI phrasing and mark that native-speaker Catholic review is outstanding (not certified). |
| Citation mismatch/weakness: first source points to daily readings but entry does not match it. Secondary site may describe a different saint or generic norms. | **medium** | Use day-specific 2026-07-05 USCCB readings and official 2026 USCCB calendar as authority; retain only clearly relevant background citations. |
| Artwork claims **cleared** with `example.com/placeholder.jpg`, and no license, alt text or caption. `place` asserts fabricated geolocation/provenance (Universal Church; `example.com`). | **high** | Mark artwork placeholder/unassigned and drop fake URL/site coordinates; retain artwork/captions/alt as non-shipping draft slots in reusable template. |

### 2026-07-06 — target: Monday of the Fourteenth Week in Ordinary Time

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Calendar identity shows **Feria in Ordinary Time / Feria / verdigris**, versus USCCB **Monday of the Fourteenth Week in Ordinary Time / Feria / green**. | **high** | Replace rank/color/title/EN-VI memorial type with the official 2026-07-06 celebration; do not confuse annual gatherings with a liturgical rank. |
| Summary and first paragraph are recycled across days; headline never explains **Matthew 9:18–26**.  | **high** | Re-author the full opening, EN/VI devotional text and original prayer around Matthew 9:18–26 using the dated USCCB reading; keep assertions limited to established scriptures. |
| Vietnamese body starts with unlocalized English weekday (“Monday”), and its boilerplate repeats rather than contextualizing the reading. | **medium** | Remove English weekday token; draft fresh VI phrasing and mark that native-speaker Catholic review is outstanding (not certified). |
| Citation mismatch/weakness: first source points to daily readings but entry does not match it. Secondary site may describe a different saint or generic norms. | **medium** | Use day-specific 2026-07-06 USCCB readings and official 2026 USCCB calendar as authority; retain only clearly relevant background citations. |
| Artwork claims **cleared** with `example.com/placeholder.jpg`, and no license, alt text or caption. `place` asserts fabricated geolocation/provenance (Universal Church; `example.com`). | **high** | Mark artwork placeholder/unassigned and drop fake URL/site coordinates; retain artwork/captions/alt as non-shipping draft slots in reusable template. |

### 2026-07-07 — target: Tuesday of the Fourteenth Week in Ordinary Time

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Calendar identity shows **Feria in Ordinary Time / Feria / verdigris**, versus USCCB **Tuesday of the Fourteenth Week in Ordinary Time / Feria / green**. | **high** | Replace rank/color/title/EN-VI memorial type with the official 2026-07-07 celebration; do not confuse annual gatherings with a liturgical rank. |
| Summary and first paragraph are recycled across days; headline never explains **Matthew 9:32–38**.  | **high** | Re-author the full opening, EN/VI devotional text and original prayer around Matthew 9:32–38 using the dated USCCB reading; keep assertions limited to established scriptures. |
| Vietnamese body starts with unlocalized English weekday (“Tuesday”), and its boilerplate repeats rather than contextualizing the reading. | **medium** | Remove English weekday token; draft fresh VI phrasing and mark that native-speaker Catholic review is outstanding (not certified). |
| Citation mismatch/weakness: first source points to daily readings but entry does not match it. Secondary site may describe a different saint or generic norms. | **medium** | Use day-specific 2026-07-07 USCCB readings and official 2026 USCCB calendar as authority; retain only clearly relevant background citations. |
| Artwork claims **cleared** with `example.com/placeholder.jpg`, and no license, alt text or caption. `place` asserts fabricated geolocation/provenance (Universal Church; `example.com`). | **high** | Mark artwork placeholder/unassigned and drop fake URL/site coordinates; retain artwork/captions/alt as non-shipping draft slots in reusable template. |

### 2026-07-08 — target: Wednesday of the Fourteenth Week in Ordinary Time

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Calendar identity shows **Feria in Ordinary Time / Feria / verdigris**, versus USCCB **Wednesday of the Fourteenth Week in Ordinary Time / Feria / green**. | **high** | Replace rank/color/title/EN-VI memorial type with the official 2026-07-08 celebration; do not confuse annual gatherings with a liturgical rank. |
| Summary and first paragraph are recycled across days; headline never explains **Matthew 10:1–7**.  | **high** | Re-author the full opening, EN/VI devotional text and original prayer around Matthew 10:1–7 using the dated USCCB reading; keep assertions limited to established scriptures. |
| Vietnamese body starts with unlocalized English weekday (“Wednesday”), and its boilerplate repeats rather than contextualizing the reading. | **medium** | Remove English weekday token; draft fresh VI phrasing and mark that native-speaker Catholic review is outstanding (not certified). |
| Citation mismatch/weakness: first source points to daily readings but entry does not match it. Secondary site may describe a different saint or generic norms. | **medium** | Use day-specific 2026-07-08 USCCB readings and official 2026 USCCB calendar as authority; retain only clearly relevant background citations. |
| Artwork claims **cleared** with `example.com/placeholder.jpg`, and no license, alt text or caption. `place` asserts fabricated geolocation/provenance (Universal Church; `example.com`). | **high** | Mark artwork placeholder/unassigned and drop fake URL/site coordinates; retain artwork/captions/alt as non-shipping draft slots in reusable template. |

### 2026-07-09 — target: Thursday of the Fourteenth Week in Ordinary Time

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Calendar identity shows **Marian Days (Đại Hội Thánh Mẫu) / Feast / white**, versus USCCB **Thursday of the Fourteenth Week in Ordinary Time / Feria / green**. | **high** | Replace rank/color/title/EN-VI memorial type with the official 2026-07-09 celebration; do not confuse annual gatherings with a liturgical rank. |
| Summary and first paragraph are recycled across days; headline never explains **Matthew 10:7–15**. Marian Days event copy is assigned to the wrong month/site. | **high** | Re-author the full opening, EN/VI devotional text and original prayer around Matthew 10:7–15 using the dated USCCB reading; keep assertions limited to established scriptures. |
| Vietnamese body starts with unlocalized English weekday (“Thursday”), and its boilerplate repeats rather than contextualizing the reading. | **medium** | Remove English weekday token; draft fresh VI phrasing and mark that native-speaker Catholic review is outstanding (not certified). |
| Citation mismatch/weakness: first source is a festival page, not dated Roman-calendar evidence. Secondary site may describe a different saint or generic norms. | **high** | Use day-specific 2026-07-09 USCCB readings and official 2026 USCCB calendar as authority; retain only clearly relevant background citations. |
| Artwork claims **cleared** with `example.com/placeholder.jpg`, and no license, alt text or caption. `place` asserts fabricated geolocation/provenance (Christ Cathedral, Garden Grove; `example.com`). | **high** | Mark artwork placeholder/unassigned and drop fake URL/site coordinates; retain artwork/captions/alt as non-shipping draft slots in reusable template. |

### 2026-07-10 — target: Friday of the Fourteenth Week in Ordinary Time

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Calendar identity shows **Marian Days (Đại Hội Thánh Mẫu) / Feast / white**, versus USCCB **Friday of the Fourteenth Week in Ordinary Time / Feria / green**. | **high** | Replace rank/color/title/EN-VI memorial type with the official 2026-07-10 celebration; do not confuse annual gatherings with a liturgical rank. |
| Summary and first paragraph are recycled across days; headline never explains **Matthew 10:16–23**. Marian Days event copy is assigned to the wrong month/site. | **high** | Re-author the full opening, EN/VI devotional text and original prayer around Matthew 10:16–23 using the dated USCCB reading; keep assertions limited to established scriptures. |
| Vietnamese body starts with unlocalized English weekday (“Friday”), and its boilerplate repeats rather than contextualizing the reading. | **medium** | Remove English weekday token; draft fresh VI phrasing and mark that native-speaker Catholic review is outstanding (not certified). |
| Citation mismatch/weakness: first source is a festival page, not dated Roman-calendar evidence. Secondary site may describe a different saint or generic norms. | **high** | Use day-specific 2026-07-10 USCCB readings and official 2026 USCCB calendar as authority; retain only clearly relevant background citations. |
| Artwork claims **cleared** with `example.com/placeholder.jpg`, and no license, alt text or caption. `place` asserts fabricated geolocation/provenance (Christ Cathedral, Garden Grove; `example.com`). | **high** | Mark artwork placeholder/unassigned and drop fake URL/site coordinates; retain artwork/captions/alt as non-shipping draft slots in reusable template. |

### 2026-07-11 — target: Saint Benedict, Abbot

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Calendar identity shows **Marian Days (Đại Hội Thánh Mẫu) / Feast / white**, versus USCCB **Saint Benedict, Abbot / Memorial / white**. | **high** | Replace rank/color/title/EN-VI memorial type with the official 2026-07-11 celebration; do not confuse annual gatherings with a liturgical rank. |
| Summary and first paragraph are recycled across days; headline never explains **Matthew 10:24–33**. Marian Days event copy is assigned to the wrong month/site. | **high** | Re-author the full opening, EN/VI devotional text and original prayer around Matthew 10:24–33 using the dated USCCB reading; keep assertions limited to established scriptures. |
| Vietnamese body starts with unlocalized English weekday (“Saturday”), and its boilerplate repeats rather than contextualizing the reading. | **medium** | Remove English weekday token; draft fresh VI phrasing and mark that native-speaker Catholic review is outstanding (not certified). |
| Citation mismatch/weakness: first source points to daily readings but entry does not match it. Secondary site may describe a different saint or generic norms. | **medium** | Use day-specific 2026-07-11 USCCB readings and official 2026 USCCB calendar as authority; retain only clearly relevant background citations. |
| Artwork claims **cleared** with `example.com/placeholder.jpg`, and no license, alt text or caption. `place` asserts fabricated geolocation/provenance (Christ Cathedral, Garden Grove; `example.com`). | **high** | Mark artwork placeholder/unassigned and drop fake URL/site coordinates; retain artwork/captions/alt as non-shipping draft slots in reusable template. |

### 2026-07-12 — target: Fifteenth Sunday in Ordinary Time

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Calendar identity shows **Sunday in Ordinary Time / Sunday / verdigris**, versus USCCB **Fifteenth Sunday in Ordinary Time / Sunday / green**. | **high** | Replace rank/color/title/EN-VI memorial type with the official 2026-07-12 celebration; do not confuse annual gatherings with a liturgical rank. |
| Summary and first paragraph are recycled across days; headline never explains **Matthew 13:1–23**.  | **high** | Re-author the full opening, EN/VI devotional text and original prayer around Matthew 13:1–23 using the dated USCCB reading; keep assertions limited to established scriptures. |
| Vietnamese body starts with unlocalized English weekday (“Sunday”), and its boilerplate repeats rather than contextualizing the reading. | **medium** | Remove English weekday token; draft fresh VI phrasing and mark that native-speaker Catholic review is outstanding (not certified). |
| Citation mismatch/weakness: first source points to daily readings but entry does not match it. Secondary site may describe a different saint or generic norms. | **medium** | Use day-specific 2026-07-12 USCCB readings and official 2026 USCCB calendar as authority; retain only clearly relevant background citations. |
| Artwork claims **cleared** with `example.com/placeholder.jpg`, and no license, alt text or caption. `place` asserts fabricated geolocation/provenance (Universal Church; `example.com`). | **high** | Mark artwork placeholder/unassigned and drop fake URL/site coordinates; retain artwork/captions/alt as non-shipping draft slots in reusable template. |

### 2026-07-13 — target: Monday of the Fifteenth Week in Ordinary Time

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Calendar identity shows **Feria in Ordinary Time / Feria / verdigris**, versus USCCB **Monday of the Fifteenth Week in Ordinary Time / Feria / green**. | **high** | Replace rank/color/title/EN-VI memorial type with the official 2026-07-13 celebration; do not confuse annual gatherings with a liturgical rank. |
| Summary and first paragraph are recycled across days; headline never explains **Matthew 10:34–11:1**.  | **high** | Re-author the full opening, EN/VI devotional text and original prayer around Matthew 10:34–11:1 using the dated USCCB reading; keep assertions limited to established scriptures. |
| Vietnamese body starts with unlocalized English weekday (“Monday”), and its boilerplate repeats rather than contextualizing the reading. | **medium** | Remove English weekday token; draft fresh VI phrasing and mark that native-speaker Catholic review is outstanding (not certified). |
| Citation mismatch/weakness: first source points to daily readings but entry does not match it. Secondary site may describe a different saint or generic norms. | **medium** | Use day-specific 2026-07-13 USCCB readings and official 2026 USCCB calendar as authority; retain only clearly relevant background citations. |
| Artwork claims **cleared** with `example.com/placeholder.jpg`, and no license, alt text or caption. `place` asserts fabricated geolocation/provenance (Universal Church; `example.com`). | **high** | Mark artwork placeholder/unassigned and drop fake URL/site coordinates; retain artwork/captions/alt as non-shipping draft slots in reusable template. |

### 2026-07-14 — target: Saint Kateri Tekakwitha, Virgin (USA)

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Calendar identity shows **Feria in Ordinary Time / Feria / verdigris**, versus USCCB **Saint Kateri Tekakwitha, Virgin (USA) / Memorial / white**. | **high** | Replace rank/color/title/EN-VI memorial type with the official 2026-07-14 celebration; do not confuse annual gatherings with a liturgical rank. |
| Summary and first paragraph are recycled across days; headline never explains **Matthew 11:20–24**.  | **high** | Re-author the full opening, EN/VI devotional text and original prayer around Matthew 11:20–24 using the dated USCCB reading; keep assertions limited to established scriptures. |
| Vietnamese body starts with unlocalized English weekday (“Tuesday”), and its boilerplate repeats rather than contextualizing the reading. | **medium** | Remove English weekday token; draft fresh VI phrasing and mark that native-speaker Catholic review is outstanding (not certified). |
| Citation mismatch/weakness: first source points to daily readings but entry does not match it. Secondary site may describe a different saint or generic norms. | **medium** | Use day-specific 2026-07-14 USCCB readings and official 2026 USCCB calendar as authority; retain only clearly relevant background citations. |
| Artwork claims **cleared** with `example.com/placeholder.jpg`, and no license, alt text or caption. `place` asserts fabricated geolocation/provenance (Universal Church; `example.com`). | **high** | Mark artwork placeholder/unassigned and drop fake URL/site coordinates; retain artwork/captions/alt as non-shipping draft slots in reusable template. |

### 2026-07-15 — target: Saint Bonaventure, Bishop and Doctor of the Church

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Calendar identity shows **Feria in Ordinary Time / Feria / verdigris**, versus USCCB **Saint Bonaventure, Bishop and Doctor of the Church / Memorial / white**. | **high** | Replace rank/color/title/EN-VI memorial type with the official 2026-07-15 celebration; do not confuse annual gatherings with a liturgical rank. |
| Summary and first paragraph are recycled across days; headline never explains **Matthew 11:25–27**.  | **high** | Re-author the full opening, EN/VI devotional text and original prayer around Matthew 11:25–27 using the dated USCCB reading; keep assertions limited to established scriptures. |
| Vietnamese body starts with unlocalized English weekday (“Wednesday”), and its boilerplate repeats rather than contextualizing the reading. | **medium** | Remove English weekday token; draft fresh VI phrasing and mark that native-speaker Catholic review is outstanding (not certified). |
| Citation mismatch/weakness: first source points to daily readings but entry does not match it. Secondary site may describe a different saint or generic norms. | **medium** | Use day-specific 2026-07-15 USCCB readings and official 2026 USCCB calendar as authority; retain only clearly relevant background citations. |
| Artwork claims **cleared** with `example.com/placeholder.jpg`, and no license, alt text or caption. `place` asserts fabricated geolocation/provenance (Universal Church; `example.com`). | **high** | Mark artwork placeholder/unassigned and drop fake URL/site coordinates; retain artwork/captions/alt as non-shipping draft slots in reusable template. |

### 2026-07-16 — target: Thursday of the Fifteenth Week in Ordinary Time

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| Calendar identity shows **Feria in Ordinary Time / Feria / verdigris**, versus USCCB **Thursday of the Fifteenth Week in Ordinary Time / Feria / green**. | **high** | Replace rank/color/title/EN-VI memorial type with the official 2026-07-16 celebration; do not confuse annual gatherings with a liturgical rank. |
| Summary and first paragraph are recycled across days; headline never explains **Matthew 11:28–30**.  | **high** | Re-author the full opening, EN/VI devotional text and original prayer around Matthew 11:28–30 using the dated USCCB reading; keep assertions limited to established scriptures. |
| Vietnamese body starts with unlocalized English weekday (“Thursday”), and its boilerplate repeats rather than contextualizing the reading. | **medium** | Remove English weekday token; draft fresh VI phrasing and mark that native-speaker Catholic review is outstanding (not certified). |
| Citation mismatch/weakness: first source points to daily readings but entry does not match it. Secondary site may describe a different saint or generic norms. | **medium** | Use day-specific 2026-07-16 USCCB readings and official 2026 USCCB calendar as authority; retain only clearly relevant background citations. |
| Artwork claims **cleared** with `example.com/placeholder.jpg`, and no license, alt text or caption. `place` asserts fabricated geolocation/provenance (Universal Church; `example.com`). | **high** | Mark artwork placeholder/unassigned and drop fake URL/site coordinates; retain artwork/captions/alt as non-shipping draft slots in reusable template. |

## Shared rules and explicit release blockers

| Issue | Severity | Proposed fix |
| --- | --- | --- |
| All **14** source records mis-mark nonexistent art as `cleared` and use fabricated `example.com` provenance and fabricated “Universal Church” geocoded place; July 9–11 additionally place a Missouri event at Christ Cathedral. | **high** | Fix art/place metadata in both source and generated fixture for the 14 entries; do not add stock images. |
| Dates/weekday, observance, U.S. rank/color and main reading must remain authoritative on every normalization. | **high** | Create offline 14-date authority contract and tests with deliberate corruptions, executed before and after normalization on Linux. |
| All 14 stories use identical prose/hero/prayers and generic dated sources. | **high** | Create reusable **source-to-claim, ritual hook, reflection, prayer** template but write distinctive source-grounded text per day. |
| Historical context (Saint Thomas, Benedict, Kateri, Bonaventure) and optional memorials should not be presented as mandatory for every Catholic location. | medium | Keep the July 2026 USCCB U.S. calendar as authority and mark local-proper differences for future locale decisions. |
| Official USCCB biblical translations and liturgical prayers can be subject to copyright. | **high** | Use **original paraphrases**, not copy/pasted readings or Mass Collects. |
| Documented source URL **existence** is not claim-level verification or artist rights. | **high** | Keep the review queue in this file; require a human Catholic historian/editor for theological wording and native VI proofreading. |
| Neither native VoiceOver nor Dynamic Type nor button contrast can be verified without Mac access. | medium | Do no web scrollytelling/animations or invented assets; postpone native UI checks and label as not certified. |

## Source authority and traceability
- USCCB official 2026 calendar: https://www.usccb.org/resources/2026cal.pdf
- Individual readings: `https://bible.usccb.org/bible/readings/MMDD26.cfm`.
- July 9 optional Saint Augustine Zhao Rong and companions is **not** the same event as Marian Days. Optional days on July 6 (Maria Goretti), 9 (Chinese martyrs), 13 (Henry), 16 (Our Lady of Mount Carmel) require local/seasonal awareness.
- Marian Days organizer: https://www.ngaythanhmau.net/en (Aug 6–9, Carthage, Missouri) and https://www.carthagemo.gov/o/parksandrec/article/3040298.
- Some daily USCCB pages intermittently return HTTP 403 to automated scrapers. A 403 is **not** evidence that a document's claims are false; verify against the 2026 official calendar rather than weakening correctness.

## Review status before editing
14 of 14 inspected. **None is release approved**. Pending Catholic editorial review for each day's religious wording, EN↔VI cultural accuracy, source-to-claim audit, artwork/asset licensing if assets are ever added, native VoiceOver/Dynamic Type/contrast on a Mac. The audit and status belong here (existing `docs/` convention).

