# Asset Production Prompt Pack
Updated: 2026-07-03

These prompts are standalone. Give one prompt to one agent at a time. The receiving agent does not need filesystem access.

Global context for all prompts:

- Product: native SwiftUI iOS Catholic sacred-history app.
- Working name: Anno.
- North Star: Every day in Catholic history, mapped.
- User: Catholic iPhone user willing to pay for history, saints, sacred art, pilgrimage, and trusted sources.
- Monetization: Free today; Premium archive/art/audio/full map; Pilgrim route packs.
- Localization: English and Vietnamese-ready from v1.
- Tone: reverent, precise, historically specific, not generic devotional filler.
- Visual direction: dark-mode-first Illuminated Timeline, New York/SF system typography, one accent per screen.
- Hard bans: no selling salvation, no guilt paywalls, no source-free claims, no fake interfaith links, no cheap religious clipart.

## Prompt 1: Brand and Naming

```text
You are a senior brand strategist for premium iOS subscription apps.

Design the brand direction for a native SwiftUI Catholic sacred-history app.

Product:
The app tells users what happened today in Catholic history: saints, martyrs, feast days, sacred art, pilgrimage sites, source-backed history, and short prayer/reflection prompts. It is not a generic Bible verse app and not a prayer-audio clone. The simplest promise is: Every day in Catholic history, mapped.

Audience:
Catholic iPhone users who pay for devotional apps, Catholic books, pilgrimage guides, sacred art, or faith-learning content. Secondary audience includes Catholic-adjacent history/art/travel users.

Deliver:
1. Evaluate the working name "Anno" as if it is the likely winner.
2. Give the best App Store name/subtitle/keyword treatment for Anno.
3. Identify trademark/search/App Store risks for Anno.
4. Provide 10 alternate names only as backups, not as the primary task.
5. Rank the top 3 backups with rationale.
6. 3 brand positioning options for Anno.
7. 1 recommended positioning.
8. 10 tagline options.
9. Naming risks and what to avoid.

Constraints:
Catholic-first. Premium. Native iOS. Vietnamese-ready. Expandable later into broader Sacred Context, but do not lead with "interfaith" unless it clearly improves conversion. Treat Anno as the working brand unless you find a serious strategic reason to reject it.
```

## Prompt 2: App Icon Direction

```text
You are an app icon art director.

Create app icon directions for a premium native iOS Catholic sacred-history app.

Product:
Every day in Catholic history, mapped. Saints, sacred art, feast days, source-backed history, and pilgrimage sites.

Desired feel:
Illuminated Timeline / Illuminated Pilgrim: dark-mode-first premium Apple software, Catholic sacred art, compass/map/pilgrimage, gold leaf on warm near-black, manuscript restraint, depth, trust.

Deliver:
1. 8 icon concepts.
2. Rank the top 3.
3. For each top concept, provide:
   - visual description
   - symbolism
   - color palette
   - why it reads at 29px
   - image-generation prompt
   - rejection risks
4. Pick one final recommended concept.

Constraints:
No text. No saint portrait. No fake stained glass. No three equal religion symbols for v1. No clipart cross. Must read clearly at small sizes. Catholic-first but not heavy-handed. Use a single illuminated capital A in Gold Leaf #C9A84C on Narthex #13110E.
```

## Prompt 3: Today Screen SwiftUI Taste Spec

```text
You are a principal iOS product designer specializing in SwiftUI.

Design the Today screen for a native iOS Catholic sacred-history app.

Job:
The user opens the app and immediately learns what happened today in Catholic history. The screen must show date, liturgical context, saint/event story, sacred art, pilgrimage location, confidence/source badge, prayer/reflection, bookmark, and audio affordance.

Deliver:
1. Above-the-fold layout.
2. Full scroll layout.
3. SwiftUI component breakdown.
4. Interaction details and haptics.
5. Loading, offline, empty, and error states.
6. Dynamic Type and VoiceOver considerations.
7. Vietnamese long-string accommodations.
8. Free vs Premium behavior on this screen.

Design constraints:
Native iOS, premium, reverent, modern. Do not design a web card in a phone frame. Do not hide sources. Do not create a busy dashboard. Avoid generic inspirational hero copy.
```

## Prompt 4: App Store Screenshots

```text
You are an App Store conversion designer.

Create a 6-screenshot App Store sequence for a native iOS Catholic sacred-history subscription app.

Product promise:
Every day in Catholic history, mapped.

Screenshots needed:
1. Today
2. Sacred Art
3. Pilgrimage Map
4. Calendar Archive
5. Sources and Confidence
6. Premium or Pilgrim Routes

For each screenshot, provide:
- Main caption, max 7 words.
- Supporting caption, max 14 words.
- Visible UI composition.
- Emotional hook.
- Conversion purpose.
- Vietnamese localization note.

Constraints:
No fake testimonials. No unsupported claims. No "grow closer to God." No stock-photo blandness. Use concrete value: saints, dates, art, sources, maps, routes, archive.
```

## Prompt 5: Vietnamese Catholic Localization

```text
You are a Vietnamese Catholic localization reviewer and iOS UX writer.

Plan the Vietnamese localization for a Catholic sacred-history iOS app.

Product:
Daily Catholic history: saints, martyrs, feasts, sacred art, pilgrimage locations, sources, and prayer/reflection prompts.

Deliver:
1. Vietnamese style guide.
2. Translation table for 50 key UI/content terms.
3. English/Vietnamese examples for:
   - Today
   - Calendar
   - Map
   - Saved
   - Source
   - Confirmed
   - Traditional
   - Disputed
   - Unlock archive
   - Pilgrim routes
4. Risks and terms requiring priest/Catholic reviewer input.
5. How to handle saint names, feast titles, and place names.
6. QA checklist.

Constraints:
Use Vietnamese Catholic terminology, not generic machine translation. Preserve source-confidence nuance. Avoid Protestantized phrasing unless context demands it. Assume UI must fit iPhone screens and Dynamic Type.
```

## Prompt 6: Premium Feature Design

```text
You are a subscription product strategist.

Design premium features for a native iOS Catholic sacred-history app.

Free:
Users get today's full entry with saint/event, art, map pin, source preview, and prayer/reflection.

Premium:
Should make $49.99/year feel obvious without making free feel stingy.

Pilgrim:
Should make travel utility worth an additional tier.

Deliver:
1. 15 premium feature ideas.
2. Score each for revenue potential, implementation difficulty, and trust risk.
3. Pick top 5 for v1.
4. Pick top 3 to defer.
5. Write paywall copy for the top 5.
6. Define exact trigger moments for each paywall.
7. Identify features to avoid.

Constraints:
Do not sell salvation, prayer outcomes, guilt, indulgences, or spiritual authority. Sell archive, art, audio, source depth, maps, routes, localization, family use, and continuity.
```

## Prompt 7: 10 Flagship Entries

```text
You are a Catholic sacred-history editor.

Create 10 flagship daily entries for a native iOS Catholic sacred-history app.

Purpose:
These entries will power screenshots, TestFlight demos, Vietnamese translation tests, audio samples, and paywall previews.

Choose entries that have:
- Catholic recognition.
- Strong story hook.
- Date specificity.
- Sacred art potential.
- Map/pilgrimage location.
- Source/confidence clarity.
- Premium hook.

Deliver each entry as JSON-like structured content:
- date
- liturgical_context
- title_en
- hook_en
- body_en, 150-250 words
- prayer_en, 1-2 sentences
- confidence: confirmed/traditional/disputed
- sources to verify
- art candidate
- pilgrimage place and coordinates if known
- premium hook
- Vietnamese translation notes

Constraints:
Do not invent facts. If source uncertainty exists, label it. Catholic-first. Sacred Context only if genuine.
```

## Prompt 8: Pilgrim Route Packs

```text
You are a pilgrimage product designer.

Design route packs for the Pilgrim tier of a Catholic sacred-history iOS app.

Product:
Premium users can browse sacred places. Pilgrim users get curated route packs with ordered stops, maps, short readings, art, source notes, and offline trip utility.

Deliver:
1. 8 route pack concepts.
2. Rank top 3 for v1.
3. For each top route:
   - target user
   - duration
   - stops
   - map/geography story
   - sample day/stop content
   - premium value
   - complexity/risk
4. Recommend the first route to build.

Constraints:
Do not require real-time tour operations. Design as curated offline content plus Apple Maps directions. Catholic-first, travel-useful, source-aware. Avoid unsafe or politically naive route claims.
```
