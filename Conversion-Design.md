# Interfaith — Conversion Design: Separating the Faithful from Their Wallets

## The Rubes Know Who They Are

Religious consumers are the most reliable recurring revenue demographic in software. They tithe. They subscribe to Hallow. They buy $40 rosaries on Etsy. They pay for CatholicTV. The WTP ceiling is not the problem — the *value articulation* is. You don't need to convince them to spend money on faith. You need to convince them that *this* is where their $4.99 should go instead of (or in addition to) Hallow.

The difference between you and Hallow: Hallow sells access to God. You sell access to knowledge *about God*. That's a different pocket. They keep Hallow for prayer and add you for learning. You're not displacing — you're augmenting. Less friction.

---

## The Three Conversion Levers

### Lever 1: The Calendar Archive (Scarcity + FOMO)

The free tier shows today. That's it. Yesterday is gone unless you subscribed. The user opens the app on July 3 and sees "Today is July 3, 2026 — 17 Tamuz." They think: "What was yesterday? What's tomorrow?" The answer is locked.

**Psychology:** Religious users hate missing a day of devotion. Hallow plays on this (streaks). You play on it differently — the *knowledge* is finite. There are only 365 entries per year. Every day they don't subscribe, yesterday's entry is permanently paywalled. Not "you broke your streak" — "you missed Peter's martyrdom, it's gone."

**Implementation:**
- Free: current day only, full content
- Premium: archive. All past days, all future days (pre-generated preview)
- Archive is searchable by saint, date, tradition, keyword
- The paywall copy: "Thomas More was beheaded on July 2. You missed it. Subscribe to never miss a day."

**Caveat:** This only works if the daily content is good enough that users *care* about missing it. If the content is mid, no one pays to see yesterday's mid content. The archive lever is directly proportional to content quality.

### Lever 2: The Map + GPS (Tangible Value)

The map pin is the easiest conversion because it has real-world utility. "I'm going to Rome next month. Let me see what's nearby." This is a concrete, measurable value — not "spiritual growth" but "I can plan my vacation around pilgrimage sites."

**Psychology:** Religious tourism is a $5B+ market. The Catholic pilgrimage industry alone (Rome, Jerusalem, Santiago, Lourdes, Fatima, Medjugorje) is enormous. These people *travel* for faith. Giving them a GPS-guided pilgrimage tool they can use on their actual trip is the easiest premium sell in the world.

**Implementation:**
- Free: see today's pin (one per day)
- Premium: see ALL pins across ALL dates, filterable, navigable
- Pilgrim tier ($9.99): turn-by-turn route planning. "Walk Mary's path from Nazareth to Ein Kerem" — a 7-day GPS-guided itinerary with readings and prayers for each stop along the way.
- The pilgrimage routes are pre-generated content sequences. You don't need real-time anything — just a curated list of pins in order with content for each stop. The GPS is just a line on a map and a "you're here" dot.

**Conversion trigger:**
- Free user reads "The Mamertine Prison, Rome. 41.8936° N, 12.4853° E."
- Taps the map pin → Map tab opens, centered on Rome
- Sees other pins in Rome (St. Peter's, St. Paul's, Scala Sancta)
- Taps one → "Subscribe to see this event"
- User: "I'm going to Rome in October. I want this."

**This is your strongest conversion lever.** Tangible, travel-adjacent, easy to explain. The archive lever requires the user to care about knowledge. The map lever requires the user to care about their *next vacation* — which they already do.

### Lever 3: The Full Calendar System (Institutional Authority)

Some users will pay just to see their tradition's full calendar. A Byzantine Catholic who opens the app and sees *only* the Gregorian date will feel alienated. "Where's my calendar?" The unlock is: "Subscribe to see your tradition's calendar year-round."

**Psychology:** Religious identity is tribal. Catholic users want to know when Ash Wednesday is. Jewish users want the full Hebrew year. Muslim users want the Hijri year with Ramadan dates. The free tier shows *today* in all calendars — teasing the depth. Premium shows the entire calendar system for every day of the year.

**Implementation:**
- Free: today's date shown in all calendars (teaser)
- Premium: full calendar browser with any date, any calendar system
- Calendar picker lets you set your "home" tradition (Catholic, Jewish, Islamic, Orthodox)
- Home tradition dates are highlighted. Other traditions are visible context.

---

## The Paywall Sequence (Which Screen, When)

### First Session: No Paywall

User opens app → sees Today. Full content. No upsell. Let them fall in love with the product on day one.

**Rationale:** Religious users are suspicious of commercialized faith. Hallow does this too — generous free tier, late paywall. If the first interaction is "subscribe to continue," they bounce and leave a 1-star review saying "this app is about money, not faith."

### Session 2-3: The Archive Tease

The daily entry includes a footer section: "**Yesterday:** St. Thomas More. **Tomorrow:** The Visitation." Both are grayed out with a small "Subscribe to explore" link. Not a full-screen paywall — just a curiosity gap.

### Session 4-5: The Map Hook

User reads a daily entry with a map pin. Taps the pin → Map tab opens, shows today's pin. User tries to zoom out to see other pins → paywall toast slides in: "See every pilgrimage site from every tradition. Subscribe for $4.99/mo." Dismissible. Not blocking.

### Session 7+: The Archive Paywall

User tries to view any past date → the full-screen paywall. This is the first aggressive gate. By now they've read 7+ entries. They know the quality. They've seen the archive teasers. They've explored the map. The rationalization is: "I've been reading this for a week. I want to read yesterday's. $4.99 is a cup of coffee."

---

## Pricing Psychology

### The Numbers

| Tier | Price | Feeling |
|------|-------|---------|
| Free | $0 | "I get value every day without paying" |
| Premium | $4.99/mo | "Less than a latte. I spend more on coffee before Mass." |
| Pilgrim | $9.99/mo | "I'd pay $10 for a single guidebook. This is a year of guidebooks." |
| Annual Premium | $49.99/yr | "That's $4.17/mo — I'm saving $10. The annual discount is the ethical choice." |

### The Annual Trap

Default to annual billing in the paywall: "$49.99/year (save 16%)" vs " $4.99/month." The annual price is the conversion — $49.99 feels like "one nice dinner" not "another subscription." The monthly price exists to make the annual look good.

**For an atheist operating a religious app:** The annual subscription is your best friend because religious users churn slower than any demographic. A Catholic who subscribes to a daily devotional is likely to stay subscribed for years. Annual billing captures that loyalty upfront. Monthly billing lets them reconsider every 30 days.

### The Pilgrim Upsell

Pilgrim tier should not show in the initial paywall. It shows *after* Premium purchase, in the Map tab: "You're on Premium. Upgrade to Pilgrim for GPS-guided pilgrimage routes." This is a post-purchase upsell, not a gate. The user who just bought Premium feels good about the app and is more receptive to spending more.

---

## App Store Listing Conversion

### App Name

| Option | Tradeoff |
|--------|----------|
| **Interfaith: Daily Saints & History** | The word "Interfaith" is the differentiator. "Daily Saints" is the search term. |
| **Sacred Timeline: Bible History Today** | Broader appeal but less specific. Could attract secular users too. |
| **The Daily Pilgrim** | Memorable, but loses the interfaith positioning. |
| **Todah — Today in Sacred History** | "Todah" (תודה) means "thanks/gratitude" in Hebrew. Nice double meaning but needs explanation. |

Recommend: **Interfaith: Daily Saints & History** — searchable, descriptive, differentiated.

### Subtitle (App Store subtitle row)

"Daily saint stories, GPS pilgrimage maps, Abrahamic history"

### Keywords

`catholic, daily saint, saint of the day, bible history, jewish calendar, islamic, rosary, hallow alternative, pilgrimage, christian, church history, hebrew calendar, hijri`

### Screenshot Sequence

1. **Hero:** Full daily card. Date header with the three-calendar cascade. One saint card visible. Caption: "Every day is loaded. You just don't know which ones yet."
2. **Calendars:** The calendar cascade animation midpoint. Caption: "Today in every tradition. Hebrew, Islamic, Byzantine, Coptic — one tap."
3. **Map:** Map tab with tradition-colored pins across the Holy Land. Caption: "Every saint has a GPS pin. Every story has a place you can visit."
4. **Art:** Art card with Caravaggio. Caption: "Caravaggio. Michelangelo. Rembrandt. Sacred art in your pocket."
5. **Interfaith:** Shared Story card. Caption: "Abraham. Ibrahim. Avraham. One story, three billion believers."
6. **Review:** App Store quote if you can get one. "Finally, an app that takes all traditions seriously."

---

## The "Atheist Operator" Conversion Problem

The question: does it matter that the founder doesn't believe?

**In the app:** No. The app is the app. The content is respectful. The sourcing is rigorous. The user never needs to know.

**In the press/App Store review:** Potentially. If the app gets attention, someone will ask. The right answer is not "I'm an atheist" — it's "I'm not religious, but I respect every tradition enough to get the dates right." This is disarming. It frames the atheism as a *feature* (no agenda) rather than a *liability* (doesn't believe).

**In marketing copy:** The app speaks as itself, not as a person. "We believe the facts matter" not "I believe the facts matter."

**The real risk:** Not the atheism — it's the *slop*. If the content is AI-generated and shallow, users will smell it regardless of who built it. If the content is rigorous and beautiful, they won't care who built it. The atheism is only a problem if the quality gives them a reason to ask.

---

## Conversion Metrics to Track (v0)

| Metric | Target | Why |
|--------|--------|-----|
| Daily open rate (free users) | > 40% | Are they coming back? |
| Session 7 conversion rate | > 3% | Are they subscribing by week 2? |
| Archive attempt → subscribe | > 15% | Are they trying to see yesterday and paying? |
| Map pin tap → paywall view | > 10% | Is the map generating curiosity? |
| Annual vs monthly split | > 60% annual | Is the annual pricing working? |
| Pilgrim upsell from Premium | > 5% | Is the GPS route premium a real tier? |

---

## What NOT to Do

- **Don't sell indulgences.** No "pray for your sins" upsell. No "sponsor a prayer." No premium rosary. You're selling *knowledge*, not salvation. Stay in that lane.
- **Don't do a free trial.** Religious users will take the 7-day trial, binge the archive, and cancel before the charge. The free tier is the trial. The archive is the conversion. Give them two weeks of free content, then let the archive gate do its work.
- **Don't do "prayer requests" or community features.** Hallow has social prayer. You shouldn't. Keeping the app as a solo reader experience reduces moderation risk and avoids theological landmines.
- **Don't use "you'll grow closer to God" in marketing copy.** You don't believe that. The user might, but you saying it sounds hollow. Stick to "you'll understand more." That's true, it's sellable, and it doesn't require belief to deliver.
- **Don't make the paywall blocking on day one.** Let them fall in love first. The first time they see the paywall should be "oh, right, that makes sense" not "are you kidding me?"
- **Don't put the atheist angle anywhere in the public product.** The user finding out the founder is an atheist is a growth risk, a review-bomb risk, and a Hallow-competitor-dirt-file risk. If asked, the answer is above. If not asked, the answer stays unwritten.
