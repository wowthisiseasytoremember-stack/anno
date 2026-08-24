# Catholic iOS Product Bible
Updated: 2026-07-03

## 1. Working Name

Working brand: **Anno**.

Why it fits:

- Short, premium, and app-icon friendly.
- Calendar-native: "anno" evokes year, time, chronology, liturgical cycles, and Anno Domini without forcing a doctrinal slogan into the name.
- Catholic-adjacent without sounding like a parish bulletin or generic prayer app.
- Expandable: it works for Catholic-first v1 and still fits later Orthodox, Jewish, Islamic, Coptic, and broader sacred-history context.
- Easy to pair with descriptive subtitles for App Store search.

Recommended App Store presentation:

- Name: `Anno`
- Subtitle: `This Day in Catholic History`
- Long descriptor: `Anno: Every day in Catholic history, mapped.`
- Bundle ID target: `com.yourco.anno`

Risks to check before final commitment:

- App Store name availability.
- Trademark conflicts in education, calendar, religion, wellness, and productivity categories.
- Search ambiguity because "Anno" is short and may collide with games, calendar tools, or Latin-themed products.

If search needs more specificity, use:

- `Anno: Catholic History`
- `Anno: Saints & Sacred Time`
- `Anno: Catholic Daybook`
- `Anno: Catholic Calendar`
- `Anno Daily`

## 2. Product Thesis

This app is a native iOS Catholic sacred-history product for people who want the Church's calendar to feel alive, specific, beautiful, and physically grounded.

The launch wedge is Catholic-first:

- What happened today in Catholic history?
- Which saint, martyr, feast, council, artwork, or pilgrimage site is attached to this date?
- Where did it happen, and can I visit it?
- What source supports the claim?

The longer-term moat remains broader than Catholic content: deterministic multi-calendar conversion, interfaith context, sacred geography, and sourced research. But the paid App Store offer should not lead with "interfaith" until conversion data proves that word helps. Catholic buyers already understand saint calendars, sacred art, pilgrimages, feast days, and subscriptions for devotional content.

The app sells knowledge, continuity, beauty, and pilgrimage utility. It does not sell grace, salvation, prayer outcomes, indulgences, guilt relief, spiritual authority, or institutional affiliation.

## 3. North Star

Every day in Catholic history, mapped.

The best possible first-session reaction is:

> I had no idea this happened today, and I can see where it happened.

Everything that does not create that reaction is secondary.

## 4. Audience

Primary:

- Catholic iPhone users who already pay for Hallow, Magnificat, pilgrim guides, Catholic books, courses, or parish-adjacent subscriptions.
- Culturally Catholic users who like history, art, Rome, saints, Marian sites, or pilgrimage but may not want a prayer-routine app.
- Catholic families and homeschoolers who want a daily learning ritual.

Secondary:

- Orthodox, Anglican, Jewish, Muslim, art-history, and comparative-religion users who are attracted by serious calendar/context work.
- Travelers planning Rome, Jerusalem, Santiago, Lourdes, Fatima, or other sacred destinations.

The primary user is not asking for a generic Bible verse. They are buying a daily sense that the Church exists in time, art, geography, and memory.

## 5. Positioning

Launch positioning:

- "Every day in Catholic history, mapped."
- "Saints, sacred art, feast days, and pilgrimage sites for today."
- "The Catholic calendar as history, art, and place."

Avoid launch positioning:

- "Interfaith devotional app."
- "AI prayer app."
- "Hallow alternative."
- "Grow closer to God."
- "All religions are the same."

Why:

- "Catholic" gives immediate App Store search intent and purchase intent.
- "Interfaith" is a backend capability and an expansion path, not necessarily the first paid hook.
- "AI" lowers trust for religious content.
- "Hallow alternative" invites an unfavorable head-to-head on audio/community/prayer inventory.

## 6. Product Shape

Native SwiftUI iOS app.

Tabs:

- Today: default, instant value, no signup.
- Calendar: current month, feast archive, date search.
- Map: sacred places and pilgrimage pins.
- Saved: local bookmarks, saved art, saved routes.

No v1:

- No social feed.
- No prayer requests.
- No AI chat.
- No onboarding quiz.
- No institutional affiliation claims.
- No day-one paywall.
- No theological argument mode.
- No source-free historical claims.
- No ads.
- No consumable "grace", streak, or prayer economies.
- No leaderboards.
- No parish/community mode.

## 7. Content Model

Each daily entry should have a stable structure:

- Date: Gregorian date plus Catholic liturgical context.
- Primary event: saint, martyr, feast, council, apparition, art object, or sacred place.
- Narrative: 150-350 words, historically specific, warm, not fluffy.
- Art: one image or artwork metadata where available.
- Place: pilgrimage pin with modern name, coordinates, and optional visiting context.
- Prayer/reflection: short, tasteful, optional in tone, not manipulative.
- Source sheet: every claim classed as Confirmed, Traditional, or Disputed.
- Sacred Context: optional Jewish, Islamic, Orthodox, Coptic, Ethiopian, or broader Abrahamic context only when genuine.

For Catholic v1, use this display priority:

1. Catholic liturgical context.
2. Saint/event story.
3. Sacred art.
4. Pilgrimage place.
5. Source/confidence.
6. Optional Sacred Context.
7. Extra calendar systems.

Do not force interfaith content into every day. It is better to say nothing than to flatten traditions.

## 8. Data Invariants

Facts must be separated from framing:

- Engine A: deterministic calendar conversion, no LLM.
- Engine B: sourced research JSON, no devotional voice.
- Layer C: narrative/framing generated from sourced data only.

Every event must carry:

- `title`
- `tradition`
- `date_basis`
- `historical_confidence`: `confirmed`, `traditional`, or `disputed`
- `source_summary`
- `source_urls` or exact source citations
- `geography` when relevant
- `media` when available
- localized content fields when translated

Hard rules:

- Never recompute calendars in an LLM.
- Never publish a claim without a source affordance.
- Never hide disputed or traditional status.
- Never manufacture an interfaith bridge.
- Never use user location to imply precise liturgical correctness if permission is denied; fall back clearly.
- Never use a Garden Grove sundown anchor in production.

## 9. Native Swift iOS Architecture

Implementation target:

- SwiftUI.
- iOS first.
- StoreKit 2 for subscriptions.
- SwiftData or local JSON/SQLite cache for entries and bookmarks.
- MapKit for sacred places, pins, and route previews.
- Xcode String Catalogs for UI localization.

Apple-aligned constraints:

- Use String Catalogs for app strings and translator context. Apple documents String Catalogs as the Xcode localization workflow for app text.
- Use StoreKit 2 / StoreKit SwiftUI views where appropriate. `SubscriptionStoreView` can display localized subscription names, descriptions, and prices from App Store metadata.
- App Store Connect subscription and in-app purchase localizations are separate metadata and need their own review path.

Official references:

- String Catalogs: https://developer.apple.com/documentation/xcode/localizing-and-varying-text-with-a-string-catalog
- StoreKit: https://developer.apple.com/storekit/
- SubscriptionStoreView: https://developer.apple.com/documentation/storekit/subscriptionstoreview
- Auto-renewable subscriptions: https://developer.apple.com/app-store/subscriptions/
- In-app purchase localization metadata: https://developer.apple.com/help/app-store-connect/manage-in-app-purchases/view-and-edit-in-app-purchase-information/

## 10. Localization Strategy

Languages from day one:

- English: primary.
- Vietnamese: structurally supported from v1.

Vietnamese should be present in the architecture from the beginning, even if the first release only has a 30-90 day translated content pack.

Use:

- `Localizable.xcstrings` for UI strings.
- Localized App Store metadata in App Store Connect.
- Localized StoreKit product display names/descriptions.
- Content model with localized fields, not runtime LLM translation.

Content fields:

- `title_en`
- `title_vi`
- `body_en`
- `body_vi`
- `prayer_en`
- `prayer_vi`
- `art_caption_en`
- `art_caption_vi`
- `source_note_en`
- `source_note_vi`

Vietnamese Catholic tone:

- Use terminology familiar to Vietnamese Catholics.
- Prefer reverent, clear Catholic language over generic Christian phrasing.
- Preserve saint names and feast titles consistently.
- Avoid Protestantized wording unless the specific source context requires it.
- Do not translate doctrine loosely to fit UI space.
- Expect Vietnamese strings to be longer; design components for expansion.

Starter terminology table:

| English | Vietnamese candidate | Notes |
|---|---|---|
| Saint | Thánh | Use before names where natural: Thánh Tôma More. |
| Martyr | Tử đạo | Catholic usage is stable. |
| Feast day | Lễ kính / ngày lễ | Choose by context and reviewer preference. |
| Prayer | Lời nguyện | UI-friendly. |
| Pilgrimage | Hành hương | Core premium term. |
| Sacred art | Nghệ thuật thánh | May need reviewer tuning. |
| Source | Nguồn | Simple UI label. |
| Confirmed | Đã xác nhận | Factual confidence. |
| Traditional | Theo truyền thống | Avoid implying confirmed history. |
| Disputed | Còn tranh luận | Softer than hostile "disputed." |
| Archive | Kho lưu trữ | Clear but may feel technical; test. |
| Saved | Đã lưu | Standard iOS-friendly. |
| Map | Bản đồ | Standard. |
| Liturgical season | Mùa phụng vụ | Catholic-specific. |
| Ordinary Time | Mùa Thường Niên | Catholic-specific. |

Every Vietnamese translation should be reviewed by a Vietnamese Catholic reader before public release. Bilingual fluency alone is not enough.

## 11. Visual Identity

Recommended direction: Illuminated Timeline / Illuminated Pilgrim, dark-mode first.

Combine:

- The gold compass/app icon idea from `icon-concept.png`.
- The premium sacred-history card feel from `daily-card-ui.png`.
- The darker travel utility and map depth from `map-tab.png`.
- The dark visual system in `docs/BRAND_VISUAL_ADDENDUM.md`.

Design values:

- Sacred, but not kitsch.
- Premium, but not sterile.
- Catholic-first, but not triumphalist.
- Historical, but not dusty.
- Beautiful, but source-aware.
- Retentive, but never casino-like.
- Commercially sharp, but not trust-destroying.
- Dark, quiet, and luminous by default.

Default dark palette:

- Background / Narthex: `#13110E`
- Surface / Choir: `#1F1B16`
- Primary text / Vellum: `#EDE7DA`
- Secondary text / Incense: `#9B9085`
- Dividers / Ash: `#2E2A24`
- Gold Leaf: `#C9A84C`
- Gilt: `#D9C06E`
- Lapis: `#2B4A7C`
- Crimson: `#8C2F3B`
- Verdigris: `#3B6B52`
- Advent: `#5C3D6E`
- Easter / light background: `#F5F0E8`

Light mode is secondary:

- Background: `#F5F0E8`
- Surface: `#FFFFFF`
- Gold: `#8B7030`
- Primary text: `#1F1B16`

Discipline:

- One accent color per screen.
- No pure black `#000000`.
- No pure white in dark-mode surfaces.

Typography:

- Display/headlines: New York Display.
- Reading/body: New York Text.
- UI/nav/metadata: SF Pro.
- Pills/tags: SF Pro Rounded.
- Liturgical Latin: New York Italic.
- Numerical dates: SF Pro Tabular.
- Do not ship Cormorant Garamond in v1; native fonts reduce accessibility and Dynamic Type risk.

Avoid:

- Clipart crosses.
- Fake stained glass.
- Overdone parchment.
- Beige-only UI.
- Generic peaceful gradients.
- Theological stock imagery.
- Decorative symbols that make the app look like a multi-faith NGO brochure.
- Reward chests, XP ladders, countdown pressure, or streak guilt.
- Custom v1 font stacks that bypass Dynamic Type.
- Decorating around sacred art; the art is the ornament.

App icon:

- Single illuminated capital `A`.
- Gold Leaf `#C9A84C` on Narthex `#13110E`.
- Carolingian/Romanesque manuscript initial style.
- No other text, crosses, halos, or multi-symbol clutter.

Liturgical accent colors:

- Advent purple: `#4B325F`
- Lent purple: `#412855`
- Christmas/Easter white-gold: `#F5F0EB` / `#C8A555`
- Ordinary Time green: `#3C6E41`
- Martyr red: `#A02D2D`
- Marian blue: `#1F4E79`

## 12. Core Screens

Today:

- First screen.
- Loads instantly.
- No login.
- Full current-day content.
- Supports English/Vietnamese.
- One visible source/confidence affordance above the fold.

Calendar:

- Current month.
- Feast dots.
- Premium archive gate for past/future full entries.
- Free users can see titles/teasers.

Map:

- Free: today's pin plus this-week pins.
- Premium: all pins and filters.
- Pilgrim: curated route packs and trip mode.

Saved:

- Local-first bookmarks.
- Premium saved collections later.
- Empty state teaches one action only: save today's entry.

Progress:

- Optional "Days Discovered" reading history.
- Gentle milestones only: 3, 7, 30, 100, 365.
- Collection achievements tied to real product depth: art viewed, sources opened, Rome places saved, Marian entries read.
- No shame copy, paid streak restores, XP multipliers, clerical rank levels, or leaderboards.

Paywall:

- Appears after demonstrated interest.
- Default to annual Premium.
- Pilgrim upsell after Premium or from route interaction.
- Must include restore purchase and subscription terms clearly.

## 13. Monetization

Free:

- Today's full entry.
- Today's art.
- Today's/this-week map pins.
- Basic source sheet.
- Local bookmark sample.

Premium:

- Archive search.
- Future previews.
- Full calendar browser.
- Full art gallery.
- Saved collections.
- Audio for daily entries.
- Expanded source sheets.
- Vietnamese content pack if complete enough to support it.

Pilgrim:

- GPS route packs.
- Rome, Jerusalem, Marian routes, Camino-style packs, local cathedral trails.
- Offline route content.
- Trip checklist and "near me" sacred site utility.

Pricing to test:

- Premium: `$5.99/mo`, `$49.99/yr`.
- Pilgrim: `$9.99/mo`, `$79.99/yr`.
- Lifetime founder plan only if distribution needs early cash; otherwise avoid lifetime because route/content costs compound.

## 14. Asset Standards

All external agents producing assets must satisfy the acceptance rubric in `ASSET_ACCEPTANCE_RUBRIC.md`.

Reject assets that:

- Could be confused with Hallow clone art.
- Use generic Catholic clipart.
- Look Protestant if the brief asks for Catholic.
- Treat Judaism/Islam as decorative flavor.
- Use unsourced historical claims.
- Cannot fit Vietnamese text.
- Ignore Dynamic Type.
- Hide monetization behind guilt.
- Make religious outcome claims.

## 15. First 30-Day Product Proof

The initial content batch should not be a random month. It should be a curated proof slate selected to show:

- Saints users recognize.
- Martyrs with strong story hooks.
- Sacred art with public-domain or licensable imagery.
- Places with GPS pins.
- A few careful Sacred Context examples.
- Vietnamese translation viability.

Use `FLAGSHIP_CONTENT_SLATE.md` as the starting slate.

## 16. Success Metrics

Early validation:

- 40%+ day-2 open rate from waitlist/TestFlight users.
- 25%+ source sheet open rate on first week.
- 10%+ map pin tap rate.
- 15%+ archive tease tap rate.
- 3%+ free-to-paid conversion by day 14 for warm users.
- 60%+ annual share among paid users.

Quality metrics:

- First reported content issue hotfixed in under 24 hours.
- Zero known wrong-date reports unresolved for high-sensitivity days.
- No published item without source/confidence label.
- Vietnamese reviewer approval before release of Vietnamese content pack.

## 17. Public Founder Posture

In product:

- Do not foreground founder beliefs.
- Do not imply institutional endorsement.
- Say: "Sources on every entry. No institutional affiliation."

If asked:

- "I built this because I wanted the dates, sources, art, and places in one app. The app is not claiming authority; it shows its sources."

Do not turn outsider status into marketing copy. The product's proof is source quality.

## 18. Revenue Posture

Anno should make money directly and honestly:

- Subscription-first.
- Premium archive, art, audio, source depth, Vietnamese reviewed content, and Pilgrim routes.
- No ad-tech surveillance as a v1 business model.
- No AI slop: user-facing content must be sourced, edited, and reviewable.
- Facts +20%: use source sheets, confidence badges, art provenance, map coordinates, and date logic as visible product surfaces.

Commercial line:

> More aggressive about selling real value; less aggressive about exploiting religious anxiety.

## 19. External Feedback Policy

See `docs/EXTERNAL_FEEDBACK_TRIAGE.md` for the detailed response to the Chronicon Sacrum/gamification proposal.

Adopted:

- Art-first Today screen emphasis.
- Liturgical color accents.
- Gentle reading-history progress.
- Collection-style achievements.

Rejected:

- Ads.
- Consumable Grace Tokens.
- "Indulgence" purchase badge.
- Streak guilt and recovery purchases.
- XP/clerical rank ladders.
- Leaderboards and parish mode for v1.
