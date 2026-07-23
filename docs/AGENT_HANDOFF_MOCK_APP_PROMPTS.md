# Agent Handoff Prompts: Anno Mock App

Updated: 2026-07-03

These prompts are designed for agents that have no filesystem access. Give them the relevant files or pasted excerpts when possible. If they cannot receive files, the embedded brief below is enough to produce useful first-pass assets.

## 1. Native SwiftUI Mock App Agent

```text
You are building a native iOS SwiftUI mock app for Anno, a premium Catholic daily-history app.

Brand:
- App name: Anno
- Subtitle: This Day in Catholic History
- Visual direction: dark-mode first, warm near-black background #13110E, gold #C9A84C as the only accent on the Today screen.
- Fonts: Apple's system stack. New York for reading/display, SF Pro for UI metadata.
- Tone: scholarly, reverent, specific. No generic inspirational quotes. No casino energy.
- Monetization posture: premium but not predatory. Free daily entry stays useful; Plus gates archive depth, high-res art, audio, offline maps, route packs, and saved-library scale.

Core screen:
- Today tab with date, liturgical context, hero sacred art placeholder, confidence badge, map row, source button, prayer/reflection prompt, and bottom tab bar.
- Calendar tab with the 7 mock dates.
- Map tab with sacred-site pins where place exists.
- Sources sheet showing source labels, URL strings, type, and confidence notes.
- Language toggle EN/VI that swaps bilingual fields.

Data shape:
- One fixture has entries[].
- Each entry includes id, date, weekday, liturgical{rank,color,title_en,title_vi}, calendars{julian,hebrew,islamic_umm_al_qura,coptic,ethiopian}, primary{type,title_en,title_vi,summary_en,summary_vi,confidence,confidence_note_en,confidence_note_vi}, optional place{name,latitude,longitude,confidence,source_url}, artwork{title,maker,date_label,source_url,status}, sources[], app_hooks{hero_line_en,hero_line_vi,prayer_prompt_en,prayer_prompt_vi}.
- Decode snake_case with JSONDecoder.convertFromSnakeCase.

Build requirements:
- Create a polished but compact SwiftUI app shell, not a marketing page.
- Use local fixture data only. Do not add networking.
- Make Vietnamese text fit without clipping.
- Preserve confidence labels. Traditional claims must never look identical to confirmed claims.
- Use MapKit if available; otherwise provide a map-placeholder list view with coordinates.
- Keep the first screen useful without sign-in.

Deliverables:
- Swift files for models, fixture loading, TodayView, CalendarView, MapView, SourceSheet, and LocalizedText helper.
- A short README explaining how to paste the fixture JSON and run the mock.
```

## 2. Asset Production Agent

```text
Create Anno mock-app visual assets from this art direction:

App: Anno, a premium Catholic daily-history app.
Icon: single illuminated capital A in gold #C9A84C on warm near-black #13110E. Carolingian/Romanesque manuscript initial, restrained, 2-3 tendrils maximum, no cross, no halo, no extra text.
UI background: #13110E. Surface: #1F1B16. Primary text: #EDE7DA. Secondary text: #9B9085.
Design rule: the art is the ornament. Do not add decorative bokeh, gradient blobs, Renaissance-faire borders, or multiple accent colors.

Produce:
1. 1024x1024 app icon.
2. 1290x2796 iPhone Today screen mockup for July 3, Saint Thomas the Apostle.
3. 1290x2796 iPhone Map screen mockup with 7-day sacred-site pins.
4. 1290x2796 iPhone Source Confidence sheet mockup.

Style:
- Quiet, native, expensive, and readable at bedside.
- Use sacred art placeholders as framed image fields, but do not invent fake paintings.
- Include a visible confidence pill: Confirmed or Traditional.
- Include Vietnamese-localization-safe spacing.
```

## 3. Vietnamese Catholic Editor Agent

```text
Review Anno's Vietnamese Catholic localization for tone, accuracy, and UI fit.

Product context:
- Anno is a Catholic daily-history app, not a generic wellness app.
- Voice should be reverent, plain, historically specific, and natural to Vietnamese Catholics.
- Avoid over-florid devotional language unless the source tradition warrants it.

Review targets:
- App subtitle: "Ngày này trong lịch sử Công giáo"
- Terms: Thánh, Chân phước, Tông đồ, Tử đạo, Đức Mẹ, Lễ kính, Lễ nhớ, Lễ nhớ tùy chọn, Mùa Thường Niên, Hành hương, Địa điểm thánh, Đã xác nhận, Theo truyền thống, Còn tranh luận.
- Entry copy for July 3-9: Saint Thomas, Saint Elizabeth of Portugal, Fourteenth Sunday in Ordinary Time, Saint Maria Goretti, Blessed Pope Benedict XI, Saints Aquila and Priscilla, Saint Augustine Zhao Rong and Companions.

Return:
- Corrections as a table: original, corrected, reason.
- Any terms that should differ between Vietnamese Catholic communities in Vietnam and diaspora communities.
- UI warnings where Vietnamese expansion needs a different layout.
```

## 4. Monetization/Paywall Agent

```text
Design Anno's first monetizable paywall without cheapening the brand.

Product:
- Native iOS Catholic daily-history app.
- Differentiator: sourced sacred history, art, maps, liturgical rhythm, Vietnamese support.
- Free tier must feel honest: today's entry, one artwork, basic source transparency, map pin, daily prayer prompt.
- Plus tier should sell depth: full archive, high-res art, audio reflections, offline maps, route packs, unlimited saved library, advanced source notes, Vietnamese/Latin enhancements.

Constraints:
- No "Grace Token" consumables.
- No guilt copy.
- No fake scarcity.
- No aggressive data harvesting.
- Retention should come from daily historical specificity and saved collection value.

Deliverables:
- One paywall screen spec.
- StoreKit product names.
- Trial and annual pricing recommendation.
- Three conversion moments that are contextual and tasteful.
- Copy that sounds premium and Catholic-literate, not AI slop.
```
