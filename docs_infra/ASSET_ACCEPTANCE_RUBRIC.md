# Asset Acceptance Rubric
Updated: 2026-07-03

Use this rubric to judge every asset returned by external agents: names, icons, UI screens, screenshot concepts, copy, translations, route ideas, content samples, paywalls, and app-store materials.

## Decision Rule

An asset is accepted only if it makes the app feel more:

- Catholic-first.
- Premium native iOS.
- Historically specific.
- Source-aware.
- Monetizable without being gross.
- Vietnamese-ready.
- Expandable into interfaith context later.

Pretty is not enough.

## Scoring

Score each asset 0-3 in each category.

- 0: reject.
- 1: weak, needs major rewrite.
- 2: usable with edits.
- 3: strong, should influence the build.

Minimum bar:

- Total score at least 18/24.
- No 0 in Trust, Catholic Fit, Monetization Ethics, or Localization.

## Categories

### 1. Catholic Fit

3:

- Clearly Catholic without being kitsch.
- Understands saints, feast days, sacred art, pilgrimage, liturgical seasons, and Catholic devotional culture.
- Could plausibly be recommended by a Catholic teacher, parent, pilgrim, or art-history-minded priest.

Reject if:

- Looks like generic Christian clipart.
- Feels Protestant when the brief asks for Catholic.
- Treats Catholicism as only crosses, candles, and beige texture.
- Uses Marian, Eucharistic, saint, or sacramental language carelessly.

### 2. Premium Native iOS Taste

3:

- Looks like it belongs on a modern iPhone.
- Respects Dynamic Type, safe areas, hit targets, haptics, and system patterns.
- Uses depth, typography, spacing, and motion with restraint.

Reject if:

- Looks like a web landing page inside a phone.
- Depends on tiny ornamental detail.
- Uses overcrowded cards, fake skeuomorphic parchment, or heavy shadows.
- Cannot survive iPhone SE dimensions.

### 3. Historical Specificity

3:

- Uses exact dates, places, people, artwork titles, and source types.
- Avoids vague "faith journey" filler.
- Makes the user think: "I did not know this happened today."

Reject if:

- Could apply to any devotional app.
- Uses generic reflection copy without facts.
- Invents or embellishes events.

### 4. Trust and Source Discipline

3:

- Shows or plans source affordances.
- Labels confidence clearly: Confirmed, Traditional, Disputed.
- Treats "traditional" as meaningful, not as fake certainty.

Reject if:

- Makes unsupported historical claims.
- Hides source/citation UX.
- Presents contested tradition as confirmed history.
- Uses AI-generated content without a review path.

### 5. Monetization Ethics

3:

- Sells archive, art, maps, audio, pilgrimage utility, translation, and continuity.
- Gives free users a complete current-day experience.
- Uses curiosity and utility, not guilt.

Reject if:

- Sells salvation, prayer outcomes, indulgence-like value, or emotional pressure.
- Blocks first-session value.
- Makes the user feel punished for not paying.
- Uses manipulative religious fear.
- Uses ads, casino-like daily rewards, paid streak restores, Grace Tokens, or XP multipliers.

### 6. Localization Readiness

3:

- Allows Vietnamese strings to expand.
- Avoids text baked into images.
- Uses terms that can be reviewed by Vietnamese Catholic readers.
- Preserves semantic precision.

Reject if:

- Relies on English wordplay.
- Crowds text into fixed-width controls.
- Uses untranslatable slogans as core UI.
- Treats Vietnamese as machine-translation afterthought.

### 7. Interfaith Expansion Safety

3:

- Catholic-first but leaves room for Jewish, Islamic, Orthodox, Coptic, and other contexts later.
- Avoids triumphalist or flattening language.
- Handles shared figures with care.

Reject if:

- Turns Judaism/Islam into decorative symbols.
- Says or implies "all traditions say the same thing."
- Creates synthetic interfaith links where none exist.

### 8. Asset Usability

3:

- Specific enough to implement.
- Contains clear constraints and variants.
- Has obvious file/use target: app icon, Today screen, App Store screenshot, source sheet, paywall, content template, route pack.

Reject if:

- Is only vibes.
- Cannot be turned into a SwiftUI/component/content task.
- Requires hidden context not included in the asset.

## Category-Specific Checks

### App Name

Accept if:

- Searchable by Catholic users.
- Not already obviously generic.
- Works in English and Vietnamese metadata.
- Does not overpromise spiritual outcomes.

Strong candidates should contain at least one of:

- Saint
- Catholic
- Sacred
- Pilgrim
- Calendar
- History

Reject if:

- It sounds like a church, nonprofit, dating app, meditation clone, or generic interfaith NGO.

### App Icon

Accept if:

- Reads at 29px and 1024px.
- Has one dominant silhouette.
- Feels Catholic/pilgrimage/sacred-time.
- Avoids tiny multi-symbol clutter.

Prefer:

- Compass rose.
- Gold on deep field.
- Subtle cross or star marker.
- Pilgrimage/map motif.

Reject:

- Three equal religious symbols as the entire concept for Catholic-first v1.
- Detailed saint portraits.
- Fake stained glass.
- Text in the icon.

### Today Screen

Accept if:

- Date and primary event are instantly legible.
- Source/confidence affordance is visible without hunting.
- Art and place are integrated, not decorative extras.
- Free value is obvious.

Reject:

- Hero marketing layout.
- Huge inspirational quote with weak fact density.
- Source hidden at the bottom only.
- No room for Vietnamese expansion.

### Paywall

Accept if:

- Sells "Unlock the archive", "Explore every pilgrimage site", or "Listen to the daily entry."
- Shows annual/monthly clearly.
- Includes restore purchase.
- Uses concrete benefits.

Reject:

- "Deepen your faith or miss out."
- "God is calling you to subscribe."
- Free trial as the main conversion crutch.
- Claims that premium prayer is spiritually superior.
- "Protect your grace."
- "Do not break the chain."
- Any purchase badge called "Indulgence."

### Vietnamese Translation

Accept if:

- Uses Catholic phrasing.
- Preserves source/confidence nuance.
- Reads like app UI, not academic prose.
- Gets reviewed by Vietnamese Catholic speaker.

Reject:

- Machine-literal output.
- Protestantized terms for Catholic concepts.
- Loss of "traditional" vs "confirmed" distinction.

## Asset Review Template

Use this exact review format:

```text
Asset:
Intended use:

Scores:
- Catholic Fit:
- Native iOS Taste:
- Historical Specificity:
- Trust and Source Discipline:
- Monetization Ethics:
- Localization Readiness:
- Interfaith Expansion Safety:
- Asset Usability:

Decision: Accept / Revise / Reject

Why:

Required edits:

Build implication:
```
