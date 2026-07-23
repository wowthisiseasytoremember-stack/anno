# Privacy and Monetization Trust Spec

Updated: 2026-07-03

## Position

Anno should make money by being worth paying for, not by extracting sensitive religious behavior. This is a commercial decision, not just a moral one: a Catholic history app that feels like surveillance will destroy the brand moat.

## Non-Negotiables

1. No sale of user data.
2. No third-party ad network in v1.
3. No targeting based on prayer, confession-adjacent text, religious struggle, grief, sexuality, addiction, fertility, politics, or family status.
4. No "streak restore" consumables framed as grace, sin, indulgence, or spiritual failure.
5. No dark-pattern paywalls: hidden close buttons, fake timers, guilt copy, or obstructed restore links.
6. No uploading free-form prayer notes or journal text unless the user explicitly opts into cloud sync.
7. No AI-generated devotional claims without source-backed factual inputs and confidence labels.

## Allowed Analytics

Use privacy-preserving product analytics for product quality and conversion:

| Event | Allowed Properties | Disallowed Properties |
|---|---|---|
| `app_opened` | app version, locale, coarse region | precise location, parish, identity |
| `entry_viewed` | entry id, date, language | inferred spirituality/personality |
| `source_sheet_opened` | entry id, source count | source-specific profiling across users |
| `paywall_viewed` | trigger surface, product ids | religious vulnerability segment |
| `purchase_started` | product id | personal religious content viewed |
| `purchase_completed` | product id, trial flag | user notes, prayer history |
| `language_toggled` | from locale, to locale | ethnicity inference label |

Retention analytics can track whether a user opened the app on a day. It must not imply that a missed day is a spiritual failure.

## Premium Features That Are Clean To Monetize

- Full archive search.
- Future previews.
- Full sacred-place map.
- Route packs and offline pilgrimage content.
- High-resolution public-domain or licensed art.
- Audio narrations.
- Saved collections.
- Expanded source notes.
- Reviewed Vietnamese content depth.
- Exportable reading plans.

## Features To Avoid Or Rename

| Avoid | Reason | Better Direction |
|---|---|---|
| Grace Token | Theological cringe and consumable dark pattern | Streak pause included in Plus, framed as calendar continuity |
| Indulgence badge | Historically loaded and commercially ugly | Founding Supporter badge |
| "Don't break your devotion" | Guilt copy | "Keep your daily history thread going" |
| Rewarded ads for prayer/audio | Cheapens trust | Free daily text, paid depth |
| Parish leaderboard | Privacy and comparison risk | Optional parish reading plan with aggregate opt-in only |

## Paywall Copy Rules

Use:

- "Unlock the archive."
- "Explore every sacred place."
- "Save art, sources, and routes."
- "Listen to daily entries."
- "Support a sourced Catholic history project."

Do not use:

- "Be more faithful."
- "God is waiting."
- "You missed your prayer."
- "Restore grace."
- "Your parish is ahead of you."

## Data Architecture Implications

Native iOS implementation should start with:

- Local-first saved entries.
- StoreKit 2 for purchases.
- Cloud sync optional and explicit.
- Analytics abstraction that can be compiled out or swapped.
- No SDK that requires broad tracking permission for core app use.
- No hard dependency on account creation for Today, source sheet, or local saves.

## Product Bet

The trust-safe version is still monetizable:

- The buyer is paying for depth, archive, art, maps, audio, and a permanent Catholic reference habit.
- The brand promise is "facts plus reverence," not manipulation.
- For this category, trust compounds. A paid app with restraint can become more valuable than a free app with surveillance.
