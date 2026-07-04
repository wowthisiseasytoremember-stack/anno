# Anno — Front-End Design Inventory

## What This Is

An iOS daily devotional app. Opens to today's date and shows you what happened on this day in Catholic, Orthodox, Jewish, and Islamic history — with art, pilgrimage locations, source citations, and prayers. Think "historical timeline meets daily devotional."

**Tagline:** This day in Catholic history.

**Audience:** Catholics, daily devotional readers, church history enthusiasts, pilgrims, anyone interested in Abrahamic religious heritage.

---

## Data Available to Display

**Calendar conversions** — every Gregorian date from 2026-01-01 through 2029-12-31, mapped to: Hebrew (pyluach, molad-based), Islamic Umm al-Qura, Islamic Tabular, Julian, Coptic, Ethiopian, Byzantine (Anno Mundi), Armenian, Syriac/Seleucid, Talmudic notations. Sundown-aware (Garden Grove, CA anchor). About 1,461 dates × 10 calendars.

**Daily events** — per-date entries: saint names, feasts, martyrdoms, biblical events, interfaith connection notes. ~4 events per day average. Each event has: title, narrative (2-3 sentences), tradition tag, liturgical color.

**Artwork** — per-event sacred art reference. Each piece has: title, artist name, date/period, provenance/source credit (museum, collection), Wikidata link, image.

**GPS coordinates** — per-event pilgrimage locations. Each pin has: latitude, longitude, place name, modern address/description. Some have visiting hours.

**Prayer content** — per-day short devotional prayer (2-3 lines), tied to the day's primary event.

**Source citations** — per-event confidence label (confirmed / traditional / disputed) and source list with title, author, link, reliability indicator.

**Subscription state** — three tiers: Free (today only), Premium (full archive + map), Pilgrim (GPS route packs). Device-local subscription tracking (StoreKit).

**User bookmarks** — locally stored list of saved dates (UserDefaults / SwiftData). No accounts, no server. Per bookmark: date, event title, tradition tag.

**User preferences** — home tradition selection, notification toggle, language (English / Vietnamese), calendar anchor timezone.

**Vietnamese localization** — full UI string set in Vietnamese.

---

## Screens That Need a Front End

### 1. Onboarding (first launch only)

User sees:
- 3-step carousel (swipe or tap dots): app value proposition, multi-calendar hook, "no account needed"
- "Start Exploring" button
- "Skip" link
- Page indicator dots

What triggers it: first launch ever.
What comes after: Today tab, first-visit calendar cascade animation.

---

### 2. Today (default tab)

User sees:
- Current date displayed in multiple calendar systems (Gregorian large + Hebrew, Hijri, Julian, Byzantine, Coptic as secondary)
- Feast/event info with tradition-colored indicator
- Art thumbnail (4:3) with title and provenance caption
- Map location pin with place name
- Source confidence badge and source count
- Listen button
- Daily prayer (2-3 lines, serif)
- Bookmark button
- Tab bar: Today, Calendar, Map, Saved (4 tabs)

Interaction:
- Tap art → full-screen Art Lightbox
- Tap map location → Map tab opens to that pin
- Tap sources → Sources Sheet
- Tap bookmark → saves day locally
- Tap listen → plays audio narration

States: first visit (calendar cascade animation once), no events (fallback broader history), no artwork (omit art section), offline (cached content).

---

### 3. Calendar

User sees:
- Month grid (7 columns, Sunday start)
- Each date cell: date number, Hebrew date, Hijri date, event dots (color = tradition)
- Today highlighted
- Year navigation
- Calendar system picker (choose primary: Gregorian/Hebrew/Hijri/Julian/Byzantine)
- "Today" jump button
- Tap date → bottom sheet: all calendar systems for that date + event list + "Open" button

Interaction:
- Scroll months vertically
- Tap date → preview sheet → "Open" loads Today view for that date

Data shown: all 10 calendar systems per date, event names, tradition tags.

---

### 4. Map

User sees:
- Full-screen world map
- Tradition filter chips (Christian, Jewish, Islamic, Interfaith, All)
- Color-coded pins (one color per tradition)
- Pin interaction: tap → mini-card with event name, tradition tag, date, "Read more"
- Route pack cards (premium pilgrim tier): curated pilgrimage routes with title, site count, preview

Interaction:
- Free: sees today's pin only. Attempt to explore beyond → subscribe prompt.
- Premium: sees all pins, filters, reads full entries.
- Tap "Read more" → Today view for that date.
- Tap route pack → route detail.

Data used: GPS coordinates per event, event names, tradition tags, route pack metadata.

---

### 5. Saved

User sees:
- Empty state: icon + "Saved days appear here. Tap the bookmark on any daily entry to save it."
- Populated: month-grouped list. Each row: date, event name, tradition indicator, art thumbnail.
- "Edit" button → bulk delete mode.
- Swipe left on row → "Unsave."

Interaction:
- Tap entry → Today view for that date.
- Swipe → unsave. Edit → multi-select delete.

Data used: local bookmarks (UserDefaults/SwiftData).

---

### 6. Art Lightbox

User sees:
- Full-screen image on black
- Pinch-to-zoom
- Caption overlay: title, artist, date, provenance, Wikidata link
- ✕ dismiss (tap or swipe down)
- Share button

Interaction:
- Tap art thumbnail on Today → open lightbox
- Pinch zoom. Swipe down or ✕ to close. Share sheet.

Data used: artwork image, metadata.

---

### 7. Sources Sheet

User sees:
- Bottom sheet (half-height)
- Confidence badge (confirmed / traditional / disputed)
- Numbered source list: title, author, link, reliability indicator
- "Report inaccuracy" link

Interaction:
- Tap "Sources (N)" on Today → sheet slides up
- Tap link → Safari. Tap report → feedback.

Data used: confidence labels, source citations.

---

### 8. Premium Paywall

User sees:
- Full-screen modal
- Headline: "Unlock the Catholic archive"
- Feature checklist: past/future entries, all map pins, art gallery, source dossiers
- Pricing: $49.99/year (primary CTA), $5.99/month (secondary)
- Trust footer: "No ads. No AI slop. Sources on every claim." + Restore/Terms/Privacy

Gate sequence (when it appears):
- Session 1: never shown
- Sessions 2-3: small archive teaser links only
- Sessions 4-5: dismissible toast on map exploration
- Session 7+: full-screen on archive date tap

Data used: subscription state, which gate triggered it.

---

### 9. Settings

User sees:
- Home tradition picker (Catholic / Orthodox / Jewish / Islamic / None)
- Notification toggle (daily push at sundown)
- Language selector (English / Vietnamese)
- Calendar anchor timezone (auto GPS / manual)
- About section: version, source methodology, contact, privacy, terms

Interaction:
- Toggle/preference changes reflect immediately in Today and Calendar data.

---

### 10. Navigation Structure

Four-tab bar: Today | Calendar | Map | Saved.

Settings accessed via gear icon (header or tab overflow).

Onboarding shown once on first launch, then never again.

No accounts. No signup. No onboarding quiz. No social features. Bookmarks local-only.

---

## 11. Localization

Anno ships in English and Vietnamese at launch. Vietnamese is a **runtime chrome swap** — same icons, same layout, same colors, same typography stack. Event narratives, saint stories, artwork captions, and prayers stay English-only in v0.

The Vietnamese string set is already complete. The front end uses it via standard iOS localization keys — no recreation needed.

### Design Rules

- **No text in images.** Every button, tab, chip, badge, sheet title, settings label, empty state, and paywall string must come from a localization key. Zero text baked into raster images.
- **Runtime switch.** Settings has a `Language` row: `English` / `Tiếng Việt`. Switching updates the UI immediately. No restart. No "changes apply next launch."
- **Locale-aware dates.** All date strings use system locale formatting. Never hardcode English date patterns.
- **English max-width baseline.** Size components to English string widths. Vietnamese is 15–30% shorter — it fits without adjustment.
- **No fixed-width labels.** Never design a label that can't grow or shrink by 30%.
- **Fallback rule.** If a Vietnamese key is missing at runtime, fall back to English silently. Never show a blank label.
- **Mixed-language state is intentional.** Screens show Vietnamese chrome (tabs, buttons, labels) around English content (narratives, prayers, art captions, source titles). Example:

  ```
  Hôm nay
  July 3, 2026
  St. Thomas More
  Conscience Before Power
  [English narrative remains here]
  Nguồn (5)
  Nghe
  Lưu
  ```

- **Dynamic Type.** Test every screen at every Dynamic Type size with Vietnamese strings. No truncation. No overflow.
- **Accessibility.** VoiceOver must work correctly in Vietnamese.

### Screens Requiring Localization QA (pair with English originals)

| Screen | What to Verify |
|--------|---------------|
| Today | Vietnamese chrome, English narrative — mixed state works |
| Calendar | Month/day labels, Hebrew/Hijri secondary dates still present |
| Map | Vietnamese filter chips, English pin content |
| Saved empty state | Fully Vietnamese |
| Settings | Language picker with "Tiếng Việt" selected |
| Paywall | Fully Vietnamese |
| Sources sheet | Vietnamese chrome, English source titles |
| Onboarding | All 3 carousel steps fully Vietnamese |
| Event/Prayer detail view | Vietnamese header, English prayer text |

### Vietnamese Strings to Test (typography stress)

| Type | Strings |
|------|--------|
| Date display | Ngày 3 tháng 7 năm 2026 |
| Buttons | Bắt đầu khám phá, Nghe, Nguồn, Lưu, Chia sẻ, Khôi phục |
| Filter chips | Tất cả, Kitô giáo, Do Thái, Hồi giáo, Liên tôn |
| Confidence badges | Đã xác nhận, Truyền thống, Tranh luận |
| Tab bar labels | Hôm nay, Lịch, Bản đồ, Đã lưu |
| Action phrases | Thêm vào bộ sưu tập, Xác nhận hành động, Cài đặt thông báo, Tiến độ, Hoàn thành |
| Devotional labels | Bài đọc, Lời nhắn, Thời gian |

All must render cleanly in SF Pro / system fonts. No truncation. No orphaned diacritics (ă, â, đ, ê, ô, ơ, ư).

