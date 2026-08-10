# Anno MVP — Catholic Daily Devotional
**Last updated:** 2026-07-15 18:30 UTC
**Goal:** TestFlight-ready daily devotional for Catholic iOS users (EN + VI)
**Scope:** Saints, feast days, historical figures — Catholic-first, no interfaith layer

---

## What Ships in MVP

| Tab | Content | Status |
|-----|---------|--------|
| **Today** | Daily saint/feast, artwork, prayer, sources, calendar pills | UI done, data hollow |
| **Calendar** | Month grid, tap-to-open day detail | UI done, data hollow |
| **Saved** | Spiritual Bouquet tracker + bookmarked entries | Tracker done, bookmarks disconnected |
| **Map** | Sacred sites from weekly entries | UI done, data hollow |

**What's cut from MVP:**
- Interfaith/layer (Jewish, Islamic, Orthodox calendars shown but not explained)
- StoreKit paywall (ship free, validate content-market fit first)
- Audio narration
- Pilgrim routes
- Onboarding walkthrough (nice-to-have, not blocking)

---

## Phase 1: Xcode Project + Compile (Day 1-2)
**Owner:** SwiftUI developer, macOS required

### 1.1 Create Xcode project
- New iOS App project named "Anno", SwiftUI lifecycle, dark mode default
- Bundle ID: `com.anno.devotional` (or whatever the team decides)
- Deployment target: iOS 17+ (for MapKit `Map` initializer, SwiftData)

### 1.2 Wire existing Swift files into target
Move these files into the Xcode project (they're already written):

**Keep as-is (they compile):**
- `AnnoApp.swift`
- `RootView.swift`
- `Today/TodayView.swift`
- `Today/ConfidenceBadge.swift`
- `Calendar/MonthCalendarView.swift`
- `Map/SacredSiteMapView.swift`
- `Map/SacredSiteListView.swift`
- `Sources/SourceSheet.swift`
- `Sources/SourceRow.swift`
- `Settings/SettingsView.swift`
- `Models/AnnoEntry.swift`
- `Services/FixtureStore.swift`
- `Localization/LanguageMode.swift`
- `Localization/LocalizedEntryText.swift`
- `Design/AnnoTheme.swift`
- `Paywall/ArchivePaywallView.swift` (UI only, paywall stays free for now)
- `Paywall/ProductCopy.swift`

**Delete or gut (broken references to missing types):**
- `Components/GlassCard.swift` — references `Palette`, `Metrics`, `.goldSheen`. Replace with the existing `AnnoCard` modifier in `AnnoTheme.swift`.
- `Components/ShareCard.swift` — references `Palette`, `GoldDivider`, `ChapterOrnament`. Remove entirely for MVP.
- `Components/ShareableImage.swift` — references KJV types. Remove entirely for MVP.
- `Components/VerseActionBar.swift` — references `Palette`, `VerseReference`. Remove entirely for MVP.
- `Design/Typography.swift` — references `Palette`. Redundant with `AnnoTheme`. Delete.
- `Utilities/Haptics.swift` — minimal wrapper, keep but remove KJV header.
- `AppRouter.swift` — dead code, never used. Delete.

**Fix or remove (KJV carryover):**
- `Models/Bookmark.swift` — uses `@Model` (SwiftData) but references undefined `VerseReference`. **Strip VerseReference**, make Bookmark reference `AnnoEntry.id` (String) instead. Then wire into AnnoApp via `.modelContainer(for: Bookmark.self)`.
- `Services/BookmarkActions.swift` — depends on `VerseReference`. Rewrite to work with `AnnoEntry.ID` + SwiftData.
- `Services/DevotionalProvider.swift` — references undefined `Devotional`. Delete for MVP (we use `AnnoEntry` directly).
- `Services/DailyDevotionalLoader.swift` — same, delete.
- `Services/AnnoDevotionalLoader.swift` — same, delete.
- `Services/NotificationService.swift` — keep, clean up KJV header.
- `Services/SearchHistory.swift` — keep, clean up KJV header.

### 1.3 Add missing resources
- Create `Assets.xcassets` with:
  - `AppIcon.appiconset` — at minimum a 1024pt gold cross icon
  - `AccentColor` — set to `AnnoTheme.goldLeaf` (#C9A84C)
- Create `PrivacyInfo.xcprivacy` in the app target (move from project root) — declare `UserDefaults` usage with reason `C617.1`
- Copy `Anno/Resources/anno_full_2026_2029.json` and `Anno/Resources/anno_week_current.json` into the app bundle

### 1.4 Fix the week fixture
`anno_week_current.json` is currently just an ID list. The app needs entry data. Either:
- **Option A:** Populate it with the 14 entries from `data/mock/anno_fortnight_2026-07-03_2026-07-16.json` (real-ish data)
- **Option B:** Extract a 7-day slice from the full fixture and populate with real content (recommended)

### 1.5 Compile and fix
- Build in Xcode, fix any remaining compiler errors
- Expected issues: `ShimmerPlaceholder` private access in `TodayView` (make it non-private or internal)
- Run on simulator, verify Today/Calendar tabs render

**Deliverable:** App compiles, launches, shows Today + Calendar with fixture data.

---

## Phase 2: Content Generation (Day 2-5)
**Owner:** LLM pipeline + human review

### 2.1 Scope: 30 days of real Catholic content
Generate `AnnoEntry` JSON for **30 days** (July 2026) covering:

| Content Type | Examples | Quantity |
|---|---|---|
| **Saint feast days** | St. Thomas More (Jul 6), St. Kateri Tekakwitha (Jul 14), St. Mary Magdalene (Jul 22) | 8-10 |
| **Marian days** | Our Lady of Mount Carmel (Jul 16), Our Lady of Snows (Aug 5) | 2-3 |
| **Ordinary Time days** | Generic but meaningful — liturgical color green, rank "Weekday" | 15-18 |
| **Historical figures** | Thomas More, John Fisher, Bridget of Sweden | 3-5 |

### 2.2 Content requirements per entry
Every entry needs:
- `titleEn` / `titleVi` — saint name or day title
- `summaryEn` / `summaryVi` — 3-5 sentence hagiography or day description
- `heroLineEn` / `heroLineVi` — one memorable hook line
- `prayerPromptEn` / `prayerPromptVi` — short prayer
- `confidenceNoteEn` / `confidenceNoteVi` — sourcing note
- `artwork` — real Wikimedia Commons URL (Caravaggio, El Greco, Fra Angelico, etc.)
- `place` — real sacred site with coordinates (only for feast days with known locations)
- `sources` — real, verifiable URLs (USCCB, Vatican, Catholic Encyclopedia)

### 2.3 Vietnamese quality gate
- All Vietnamese text must be reviewed by a Vietnamese Catholic speaker (or at minimum a fluent speaker familiar with Catholic terminology)
- Required terms: "Lễ kính" (Feast), "Lễ nhớ" (Memorial), "Thánh" (Saint), "Tông đồ" (Apostle), "Đức Kitô" (Christ), "Thánh Thể" (Eucharist)
- Forbidden: machine-translated body text, mixed-language paragraphs

### 2.4 Fixture generation script
Write a Python script (`tools/generate_mvp_fixture.py`) that:
1. Takes a JSON array of 30 `AnnoEntry` objects
2. Validates against the `AnnoEntry` schema (use `tools/validate_mock_content.py` as base)
3. Produces `anno_week_current.json` (7-day slice) and `anno_full_mvp.json` (30 days)
4. Runs the existing validators

**Deliverable:** 30 days of real, sourced, bilingual Catholic content in fixture files.

---

## Phase 3: Wire Bookmarks + Polish (Day 5-7)
**Owner:** SwiftUI developer

### 3.1 Fix Bookmark.swift
```swift
// Simplified Bookmark model for MVP
@Model
final class Bookmark {
    var entryID: String
    var dateBookmarked: Date
    
    init(entryID: String) {
        self.entryID = entryID
        self.dateBookmarked = Date()
    }
}
```

### 3.2 Wire bookmarks into AnnoApp.swift
```swift
@main
struct AnnoApp: App {
    var body: some Scene {
        WindowGroup {
            RootView(store: FixtureStore.loadBundledOrPreview())
                .preferredColorScheme(.dark)
        }
        .modelContainer(for: Bookmark.self)
    }
}
```

### 3.3 Wire bookmark button in TodayView
Replace the cosmetic `@State isBookmarked` with actual SwiftData queries via `@Query` and `BookmarkActions`.

### 3.4 Wire SavedView to real bookmarks
Replace `mockCollections` with a `@Query` on `Bookmark` that shows saved entries.

### 3.5 Fix remaining issues
- `SacredSiteListView.swift:98` — change `http` to `https`
- `FixtureStore.swift:25` — add guard for empty entries array
- Remove KJV headers from all files
- Ensure `PrivacyInfo.xcprivacy` is in the app target

### 3.6 Localization strings
Create `Localizable.strings` for EN and VI with at minimum:
- Tab labels ("Today", "Calendar", "Saved", "Settings")
- Navigation titles
- Paywall text
- Error messages
- Empty states

**Deliverable:** Bookmarks work end-to-end. App is feature-complete for MVP.

---

## Phase 4: TestFlight Prep (Day 7-10)
**Owner:** SwiftUI developer + project owner

### 4.1 App Store assets
- App icon (1024pt, gold cross on dark background)
- Screenshots for 6.7" and 6.1" (Today view, Calendar, Saved)
- App description (EN + VI)
- Keywords
- Privacy policy URL (host the existing `Docs/privacy-policy.md` somewhere — GitHub Pages is fine)

### 4.2 Build and archive
- Product > Archive in Xcode
- Upload to App Store Connect
- Fill in App Store Connect metadata

### 4.3 TestFlight
- Add internal testers
- Test on real devices (iPhone 15, iPhone SE for small screen)
- Verify: dark mode, dynamic type, VoiceOver basics

### 4.4 Submit for review
- App Review Notes: explain the app is a free Catholic daily devotional, no in-app purchases yet, content is sourced from Roman Martyrology and USCCB
- Privacy policy link must work
- Support URL must work (can be email)

**Deliverable:** App on TestFlight, submitted for App Store review.

---

## Effort Summary

| Phase | Days | What |
|-------|------|------|
| 1. Xcode + Compile | 2 | Project scaffold, fix broken files, wire resources |
| 2. Content | 3 | Generate 30 days of real Catholic content, EN+VI |
| 3. Bookmarks + Polish | 2 | Wire SwiftData, fix bugs, localization |
| 4. TestFlight | 3 | Assets, archive, submit |
| **Total** | **~10 days** | **Part-time, or 1 week full sprint** |

---

## What's NOT in MVP (v2 backlog)

- StoreKit paywall (ship free first)
- Interfaith content layer
- Audio narration
- Pilgrim routes / GPS
- Onboarding flow
- Push notifications (beyond basic daily reminder)
- Art gallery (only one artwork per entry)
- Search
- iPad layout
