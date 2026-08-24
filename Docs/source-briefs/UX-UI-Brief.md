# Interfaith — UX/UI Design Brief

## 0. Data Inventory

What the app actually has to work with:

| Asset | Source | Volume | Status |
|-------|--------|--------|--------|
| Calendar conversions | Engine A | 1,461 dates × 10 calendars | Done |
| Daily events (saints, martyrdoms, interfaith) | Engine B | 365/year, ~4 events/day avg | Needs batch generation |
| Artwork metadata (title, artist, location, Wikidata) | Engine B | ~1-2 per daily event | Needs batch generation |
| GPS coordinates (biblical/modern places) | Wikidata-linked | ~1-3 per daily event | Needs batch generation |
| Devotional narrative content | Layer C | 365/year | Needs batch generation |
| Interfaith connection notes | Engine B | ~1-2 per daily entry where genuine | Needs batch generation |
| User data | None | $0 | No accounts, no personalization at v0 |

**Constraint:** No user accounts, no personalization, no social features in v0. The app speaks; the user listens. Personalization comes later as saved/starred content.

---

## 1. Emotional Pillars

### Wonder — "I had no idea this happened today"

The primary emotion. Every daily entry should surface something the user didn't know: that a saint died on this exact day 500 years ago, that this feast aligns with a Jewish fast, that Caravaggio painted this scene.

**Build it with:** The temporal hook in every headline. Specificity kills vagueness.

### Connection — "These three billion people remember the same Abraham"

The interfaith angle is the moat. Not comparative theology — just "they remember this figure too, here's how." The emotion is quiet awe at shared humanity.

**Build it with:** One "Shared Story" section per daily entry, only where genuine. Never manufactured.

### Grounding — "I could walk there"

GPS coordinates, modern place names, visiting hours. This makes ancient history feel present. The Mamertine Prison isn't a Bible footnote — it's a building in Rome you can visit.

**Build it with:** Every event gets a map pin. Distance-from-you if user allows location. Visiting hours where available.

### Reverence — not religious, just respectful

The tone is warm but not devotional. The app doesn't proselytize. It treats every tradition with the same seriousness.

**Build it with:** Consistent sourcing hierarchy. Confidence labels (confirmed/traditional/disputed). No editorializing.

---

## 2. Tab Structure

Four tabs, ordered by daily engagement funnel:

### 1. Today (default)

**Purpose:** The daily devotional card. The reason the user opens the app.
**First visit:** Today's entry, fully loaded. No onboarding, no account gate.
**Content:** Date header (all calendars), Saint/event story, Place+Map, Art, Shared Story, Prayer prompt, Source footnotes.

### 2. Map

**Purpose:** All pilgrimage pins across all dates. Filters by tradition, region, date range.
**First visit:** World map with ~365 pins (one per daily entry). User can filter.
**Content:** Pins at GPS coordinates. Tap → mini-card with event name, tradition tag, date. Tap again → full event modal or opens Today view for that date.

### 3. Calendar

**Purpose:** Browse all dates. See upcoming feasts across all traditions.
**First visit:** Current month grid. Each cell shows: Gregorian date + Hebrew date + Islamic date. Colored dots for tradition-specific events.
**Content:** Scrollable month view. Tap date → preview of that day's events. Tap again → opens Today for that date. Highlight today.

### 4. Saved

**Purpose:** User's collection. Bookmarked days, saved art, planned pilgrimages.
**First visit:** Empty state: "Save a day by tapping the bookmark. Your collection grows here."
**Content:** List of saved days, grouped by month. Saved art grid. Pilgrimage route planner (future).

---

## 3. View Hierarchy (Build Order)

### Phase 1: The Daily Card (Today tab)

The single most important screen. Everything else supports this.

**Components:**
- **Date header** — Gregorian date (large, elegant) + small subtitle showing all calendar system equivalents for today. Tap to expand the calendar list.
- **Event cards** — 1-4 scrollable sections, each with:
  - Title (saint name, event name)
  - 2-3 sentence narrative
  - Art thumbnail (tap for full-screen)
  - Map pin button (opens Map tab to this location)
  - Interfaith badge (if applicable)
  - Prayer prompt (1-2 sentences) in italic
- **Bookmark button** — top-right, standard iOS share icon
- **Footer** — source citations, confidence labels, "report inaccuracy" link

### Phase 2: Calendar Browser

- Month grid with event dots
- Tap date → preview sheet slides up
- Calendar system picker (which system to show as primary)

### Phase 3: Map

- World map with tradition-colored pins
- Tradition filter chips (Catholic, Jewish, Islamic, Orthodox, All)
- Pin tap → mini card → full event

---

## 4. Delight Mechanisms

### Hero delight moment: The Daily Reveal

The user opens the app to Today. The date header animates in as calendar systems cascade in sequence:
1. "Today is July 3, 2026"
2. "17 Tamuz 5786" slides in below
3. "17 Dhul-Hijjah 1448 AH" slides in below
4. "19 Haziran 7534 (Byzantine)"
Then the header settles, and the event cards fade in.

This is the single most important interaction. It tells the user in 1.5 seconds: "This app knows things you don't. Stay."

### Other delight moments:

| Mechanism | Where | Why | MVP? |
|-----------|-------|-----|------|
| Calendar cascade animation | Today header | Sets the "time traveler" tone immediately | Yes |
| Map pin pulse when event is from today | Map tab | Connects Today to Map — "this place is real" | Yes |
| Art full-screen pinch-to-zoom | Art modal | Makes the Caravaggio feel present, not like a thumbnail | Defer |
| Saved day: "You discovered this on [date]" | Saved tab | Personal history = emotional attachment | Defer |
| Weekly summary: "This week you visited 4 pilgrimage sites" | Push notification or Saved tab header | Retention loop | Defer |
| Distance overlay on map pins: "5,437 miles from the Mamertine Prison" | Map tab | Makes geography personal | Defer |

---

## 5. User Flows

### New user, first open (no account)

1. Open app → Today tab loads immediately
2. Date header cascades in (calendars)
3. First event card: Saint/event narrative
4. User scrolls: Art thumbnail catches eye, taps = full-screen image
5. User scrolls: Map pin button → Map tab opens to that specific GPS pin
6. User scrolls: Shared Story section
7. Footer: "Sources" link
8. User: taps bookmark = "Saved" prompt (no account needed, local-first)
9. User taps Calendar tab → sees tomorrow preview → comes back tomorrow

**Time to value:** ~5 seconds from open to content. No signup, no onboarding, no tutorials.

### Returning user, daily habit

1. Push notification: "July 3 — St. Thomas More died today in 1535"
2. Tap → opens to Today
3. Reads the Saint card, taps the Map pin for the Mamertine Prison
4. Reads the Shared Story, taps the Art thumbnail
5. Bookmarks the entry
6. Glances Calendar for tomorrow — "what's coming up?"
7. Leaves. Total time: 90-120 seconds.

### Map explorer

1. User taps Map tab
2. World map with color-coded pins (blue=Christian, gold=Jewish, green=Islamic)
3. Filters: "Show only this year's pilgrimage sites"
4. Taps pin near Jerusalem → mini-card: "18 Tammuz — Breach of Jerusalem's Walls"
5. Taps "Read more" → Today view loads for that date (July 2, 2026)
6. User reads the full entry for that past date

---

## 6. Visual Register

**Register: Product** (app UI, not marketing site). System font. No custom typefaces.

### Color tokens (v0 proposal)

| Token | Hex | Usage |
|-------|-----|-------|
| Background | #FAFAF5 | Warm off-white. Not sterile, not beige. |
| Card | #FFFFFF | Pure white for event cards (depth via shadow) |
| Text Primary | #1A1A1A | Body text |
| Text Secondary | #6B6B6B | Date subtitle, source citations |
| Accent (Christian) | #8B4513 | Saddle brown — warmth, tradition, manuscript ink |
| Accent (Jewish) | #2F6F4F | Deep green — olive, Torah scroll |
| Accent (Islamic) | #1A5276 | Deep teal — mosque tile, geometric |
| Accent (Shared) | #4A0E4E | Deep purple — interfaith intersection |
| Gold/Highlight | #C9A84C | Date numbers, bookmark icon, star ratings |

### Card treatment

- Standard white card with subtle shadow (y: 2px, blur: 12px, black/8%)
- 16px corner radius
- 16px horizontal padding, 20px vertical
- Section divider: 1px #F0EDE8 (warm gray rule)

### Typography

- System font (SF Pro on iOS)
- Date: 34pt, Semibold, Text Primary
- Calendar subtitle: 13pt, Regular, Text Secondary
- Section headers: 17pt, Semibold, Text Primary
- Body: 15pt, Regular, 1.6 line height
- Prayer prompt: 15pt, Italic, Text Secondary
- Source footer: 11pt, Regular, Text Secondary

### Micro-interactions (MVP)

| Action | Interaction |
|--------|------------|
| Calendar cascade on Today load | 300ms stagger, ease-out, opacity 0→1 + translateY 8px→0 |
| Card scroll | Standard spring scroll |
| Art thumbnail tap | Sheet slides up, no dismiss on tap-outside |
| Map pin tap | Pin scales 1.3x, mini-card fades in |
| Bookmark | Icon fills, 100ms spring scale |
| Tab switch | Crossfade, 200ms |

---

## 7. Edge Cases

| State | Behavior |
|-------|----------|
| Empty day (no events found) | "Today in [tradition]: No specific events recorded. Read the readings for this week instead." + fallback: "On this date in church history..." with broader content. |
| No artwork available | No art section. Card is still complete without it. |
| GPS pin but no user location | Show pin at fixed map zoom. No "distance from you" text. |
| User denies location | No distance feature. Map still works at default zoom. |
| First visit, Saved empty | `"Saved days appear here. Tap the bookmark on any daily entry to save it."` — centered text, soft icon. |
| Offline | Cache current day's content. Show banner: "You're offline. Showing today's cached entry." |
| Date far in the future | Engine A has 2026-2029. For dates outside that range, show: "Calendar conversions available through 2029. Generating..." |
| Slow content load (Engine B cache miss) | Skeleton card: date header fades in, then event cards appear one by one as rendered. Never a spinner. |

---

## 8. App Store Screenshots (for launch)

No screenshot design, just the pitch angles:

1. **Hero:** Wide date header with cascading calendars + one event card visible. Caption: "Every day is loaded. You just don't know which ones yet."
2. **Interfaith:** A Shared Story card visible. Caption: "Abraham. Ibrahim. Avraham. One story, three billion believers."
3. **Map:** World map with pins. Caption: "The GPS pins you didn't know you needed."
4. **Art:** Art card with Caravaggio thumbnail. Caption: "Caravaggio. In your pocket."

---

## 9. Open Design Decisions

### D1: Single card per day vs. multi-card per event?

**Option A:** One long scrollable card per day (all events, all art, all maps, all prayers in one linear flow).
**Option B:** One event per card, swipeable (Tinder-style: swipe left for next event).

**Recommendation:** Option A for v0. The user reads the day as a unit. The PRD sample shows a cohesive thread (Saint → Place → Shared Story → Art → Calendar prayer). Breaking it into swipeable cards loses the narrative arc. Revisit if daily content gets dense enough (8+ events) to warrant subdivision.

### D2: Calendar cascade — animated or static?

**Option A:** Animated cascade (calendars animate in one by one, 300ms each).
**Option B:** Static header (all calendars shown at once).

**Recommendation:** Option A for first open only. The cascade is the hero delight moment. Once the user has seen it once per session, show the collapsed header ("July 3, 2026 • +3 more calendars") with a tap-to-expand. Over-animating on every open becomes exhausting.

### D3: Map tradition colors — universal or per-entry?

**Option A:** Each pin is the tradition color of its primary event (blue=Christian, gold=Jewish, green=Islamic, purple=interfaith).
**Option B:** Single neutral pin color per entry.

**Recommendation:** Option A. The Map tab with all pins from a whole year is a beautiful color visualization. You see gold clusters in Israel, blue clusters in Rome, green in Mecca. It tells a story by itself.

### D4: Push notifications — new day alert or optional?

**Option A:** Daily push at sundown (Garden Grove anchor): "The new day is here. Open to discover [saint name]."
**Option B:** No push notifications.

**Recommendation:** Option A, optional at first launch. The retention loop needs it. Hallow sends daily prayer reminders. This app sends daily discovery hooks. Same category, same expectation.

---

## 10. What NOT to Build (v0 scope limiter)

- No user accounts. Bookmark data lives in UserDefaults / SwiftData local only.
- No social features. No sharing streaks, no "pray with friends."
- No audio. No daily podcast, no narrated prayers. Text + image only.
- No personalization. No "you liked this saint, here's another."
- No AI chat. No "ask about this figure."
- No push-to-premium upsells inside the daily card. Free tier is ad-free and complete for the current day. Upgrade CTA lives in Calendar archive and Map filter panel.
- No onboarding quiz. No "what tradition are you?" No preference cards.
