# Monetization and Paywall System
Updated: 2026-07-03

## Principle

The app should feel generous before it asks for money.

It monetizes continuity, depth, art, audio, archive, and pilgrimage utility. It does not monetize guilt, salvation, prayer outcomes, or religious anxiety.

## Tiers

### Free

Purpose: create daily habit and trust.

Includes:

- Today's full entry.
- Today's Catholic liturgical context.
- Today's sacred art.
- Today's source/confidence sheet preview.
- Today's pilgrimage pin.
- This-week map preview.
- Local bookmark sample.
- English UI.
- Vietnamese UI if available.
- No ads in v1.

Do not cripple today's content. A weak free tier kills habit formation.

### Premium

Purpose: sell time travel and permanence.

Price to test:

- `$5.99/mo`
- `$49.99/yr`, default selected

Includes:

- Full archive.
- Future previews.
- Calendar search.
- Full sacred art gallery.
- All pilgrimage pins.
- Saved collections.
- Expanded source sheets.
- Audio daily entries.
- Full Vietnamese content pack when enough days are reviewed.

Core promise:

> Never lose a day of Catholic history.

### Pilgrim

Purpose: sell travel utility.

Price to test:

- `$9.99/mo`
- `$79.99/yr`

Includes:

- Curated pilgrimage routes.
- Rome route pack.
- Jerusalem/Holy Land route pack.
- Marian route pack.
- Offline route content.
- Nearby sacred places.
- Route-based readings and art.

Core promise:

> Turn sacred history into places you can visit.

## Conversion Levers

### 1. Archive

Trigger:

- User taps yesterday/tomorrow.
- User searches a saint.
- User taps a grayed-out feast in Calendar.

Copy:

- "Unlock the archive"
- "Read every day, not just today"
- "Search saints, feasts, art, and places"

Avoid:

- "You missed it."
- Anything that feels punitive.

### 2. Map

Trigger:

- User opens Map and pans beyond free week.
- User taps a non-free pin.
- User filters by city or route.

Copy:

- "Explore every sacred place"
- "Plan Rome, Jerusalem, and Marian routes"
- "Open the full pilgrimage map"

This is likely the highest-converting premium lever because it has tangible travel utility.

### 3. Art

Trigger:

- User opens art lightbox.
- User taps related artworks.
- User saves multiple artworks.

Copy:

- "Unlock the sacred art gallery"
- "Browse the art behind each feast"
- "Save art, captions, and source notes"

### 4. Audio

Trigger:

- User taps Listen more than 3 times.
- User background-locks the app.

Copy:

- "Listen to today's entry"
- "Audio for your commute, walk, or morning prayer"

Use caution:

- Audio is a competitive expectation because Hallow/Glorify lead with it, but this product should not become a prayer-audio app unless data demands it.

### 5. Vietnamese

Trigger:

- Device language Vietnamese.
- User toggles Vietnamese.
- User shares Vietnamese content.

Copy:

- "Read the daily entry in Vietnamese"
- "Vietnamese Catholic terminology, reviewed for clarity"

Do not ship broad Vietnamese content before review. UI localization can ship first; daily content should be reviewed.

## Paywall Timing

No paywall:

- First app open.
- Today's full entry.
- Source preview.
- Today's map pin.

Soft paywall:

- After an archive interaction.
- After map expansion attempt.
- After saving several items.
- After audio habit signal.

Hard paywall:

- Reading archived content.
- Full map archive.
- Route packs.
- Bulk save/export.

Recommended gates:

- Archive: after 3 archive taps, show full paywall.
- Map: show one free this-week map; paywall all-pins view.
- Saved: allow 5 local saves, then upsell collections.
- Audio: allow 3 listens/week, then upsell daily audio.

## Paywall Structure

Header:

- "Unlock the Catholic archive"

Subheader:

- "Saints, sacred art, sources, and pilgrimage places for every day of the year."

Benefits:

- Full archive search.
- Every pilgrimage pin.
- Sacred art gallery.
- Audio daily entries.
- Saved collections.
- Expanded source sheets.

Primary plan:

- Annual Premium, `$49.99/year`.

Secondary:

- Monthly Premium, `$5.99/month`.

Required:

- Restore purchases.
- Terms and privacy links.
- Subscription auto-renewal language.
- No hidden close button.

## Paywall Copy Variants

### Archive Variant

Title:

> Unlock the Catholic archive

Body:

> Search saints, feasts, councils, artworks, and sacred places for every day of the year.

Bullets:

- Read past and future entries.
- Search by saint, date, place, or feast.
- Save entries into collections.
- Open expanded source notes.

CTA:

> Start Premium

### Map Variant

Title:

> Open the full pilgrimage map

Body:

> Today's pin is free. Premium unlocks every sacred place in the archive.

Bullets:

- Browse Rome, Jerusalem, Lourdes, Fatima, Santiago, and more.
- Filter by saint, feast, country, or route.
- Save places for future trips.
- Open directions in Apple Maps.

CTA:

> Unlock the Map

### Pilgrim Variant

Title:

> Travel with the saints

Body:

> Curated route packs turn sacred history into trips you can actually take.

Bullets:

- Rome in 3 days.
- Marian pilgrimage route.
- Jerusalem and the Passion sites.
- Offline readings, art, and map pins.

CTA:

> Upgrade to Pilgrim

## What Not To Monetize

Reject these:

- Paid prayer requests.
- Premium blessings.
- "More powerful prayers."
- Sin/guilt language.
- Sponsored intentions.
- Community pressure.
- Streak shame.
- Artificially withholding sources from factual claims.
- Grace Tokens.
- Paid streak repair.
- Rewarded ads.
- Banner/interstitial ads.
- XP multipliers.
- Clerical status levels.
- "Indulgence" purchase badges.
- Tip jar as a primary monetization surface.

Sources can have expanded detail in Premium, but minimum source/confidence must remain visible for trust.

## Sharper Revenue, Cleaner Trust

Use this line when choosing between mechanics:

> Evil -20%, AI slop -100%, facts +20%, monetization +20%.

Approved sharper monetization:

- Gate archive depth, not today's core value.
- Gate full map archive and route planning, not today's place.
- Gate high-res art gallery, not basic art context.
- Gate full audio library, but allow limited samples.
- Gate expanded source dossiers, but always show source/confidence basics.
- Gate reviewed Vietnamese content packs only when quality is real.
- Sell seasonal passes only if editorial quality is high.

Rejected sharper monetization:

- Ads.
- Rewarded ads.
- Data sale/share as a business model.
- Streak anxiety.
- Paid "grace" mechanics.
- Religious guilt copy.

## StoreKit Notes

Use StoreKit 2 and App Store Connect subscription metadata as the source of truth for localized product names, descriptions, price, and duration. StoreKit SwiftUI views can display localized subscription details, but a custom branded paywall may still be needed for taste and Catholic-specific value framing.

Localize:

- Product display name.
- Product description.
- Paywall benefit copy.
- Restore/terms/privacy.
- Subscription group display copy.

Test:

- Sandbox purchase.
- Restore purchase.
- Lapsed subscription.
- Refund/revoked entitlement.
- Vietnamese storefront/device language display.
- Offline entitlement cache.
