# Anno MVP — Catholic Daily Devotional (Improved)
**Last updated:** 2026-07-15 19:00 UTC
**Goal:** TestFlight-ready daily devotional for Catholic iOS users (EN + VI)
**Scope:** Saints, feast days, historical figures — Catholic-first, no interfaith layer

---

## Improvements Over v1

1. **Map tab cut from MVP** — without interfaith content, the map shows the same 1-2 pins every day. Not worth the App Store review complexity. Add in v2 with pilgrim routes.
2. **3-tab MVP** — Today, Calendar, Saved. Simpler, faster to ship.
3. **Minimum viable content: 14 days** — not 30. Get to TestFlight faster, validate with real users, then expand.
4. **Content sprints are phone-deliverable** — each sprint is a self-contained LLM prompt + checklist you can run from your iPhone.
5. **Explicit file-level instructions** — every sprint says "open X, change Y to Z" not just "fix bookmarks."
6. **Vietnamese review is a gate, not a wish** — scheduled as a distinct sprint with a clear deliverable.
7. **Fallback content strategy** — if full content generation takes too long, ship with 7 days of real content + 7 days of "Ordinary Time" filler.

---

## What Ships in MVP

| Tab | Content | Status |
|-----|---------|--------|
| **Today** | Daily saint/feast, artwork, prayer, sources, calendar pills | UI done, data hollow |
| **Calendar** | Month grid, tap-to-open day detail | UI done, data hollow |
| **Saved** | Spiritual Bouquet tracker + bookmarked entries | Tracker done, bookmarks disconnected |

**What's cut from MVP:**
- Map tab (add in v2 with pilgrim routes)
- Interfaith content layer
- StoreKit paywall (ship free, validate content-market fit first)
- Audio narration
- Pilgrim routes
- Onboarding walkthrough
- Push notifications

---

## Sprint Breakdown

### Sprint 1: Xcode Project (Day 1)
**Goal:** App compiles and launches on simulator.

| # | Task | File(s) | Done When |
|---|------|---------|-----------|
| 1.1 | Create Xcode project "Anno", SwiftUI, iOS 17+, dark mode | New project | `.xcodeproj` exists |
| 1.2 | Add these files to target (they compile as-is) | See list below | All in Project Navigator |
| 1.3 | Delete these broken KJV files | See list below | Files removed from project |
| 1.4 | Fix Bookmark.swift — strip VerseReference, use String entryID | `Models/Bookmark.swift` | Compiles without errors |
| 1.5 | Fix BookmarkActions.swift — rewrite for AnnoEntry.ID | `Services/BookmarkActions.swift` | Compiles without errors |
| 1.6 | Wire .modelContainer in AnnoApp.swift | `AnnoApp.swift` | `.modelContainer(for: Bookmark.self)` present |
| 1.7 | Add Assets.xcassets (AppIcon + AccentColor) | New asset catalog | App icon shows in simulator |
| 1.8 | Add PrivacyInfo.xcprivacy to target | Move from project root | File in app target |
| 1.9 | Copy fixture JSONs to bundle | `Anno/Resources/*.json` | Files in Copy Bundle Resources |
| 1.10 | Build and fix remaining errors | — | `Cmd+B` succeeds |

**Files to add (compile as-is):**
- `AnnoApp.swift`, `RootView.swift`
- `Today/TodayView.swift`, `Today/ConfidenceBadge.swift`
- `Calendar/MonthCalendarView.swift`
- `Sources/SourceSheet.swift`, `Sources/SourceRow.swift`
- `Settings/SettingsView.swift`
- `Models/AnnoEntry.swift`, `Models/Bookmark.swift` (after fix)
- `Services/FixtureStore.swift`, `Services/BookmarkActions.swift` (after fix)
- `Localization/LanguageMode.swift`, `Localization/LocalizedEntryText.swift`
- `Design/AnnoTheme.swift`
- `Paywall/ArchivePaywallView.swift`, `Paywall/ProductCopy.swift`

**Files to delete:**
- `Components/GlassCard.swift` (references missing Palette/Metrics)
- `Components/ShareCard.swift` (references missing Palette/GoldDivider)
- `Components/ShareableImage.swift` (KJV types)
- `Components/VerseActionBar.swift` (references missing Palette/VerseReference)
- `Design/Typography.swift` (references missing Palette, redundant)
- `AppRouter.swift` (dead code, never used)
- `Services/DevotionalProvider.swift` (references missing Devotional)
- `Services/DailyDevotionalLoader.swift` (references missing Devotional)
- `Services/AnnoDevotionalLoader.swift` (references missing Devotional)

**Acceptance criteria:**
- `Cmd+B` succeeds with zero errors
- App launches on iPhone simulator
- Today tab shows the preview entry (St. Thomas)
- Calendar tab shows the month grid
- Dark mode is default

---

### Sprint 2: Week Fixture (Day 1-2)
**Goal:** App shows 7 days of real Catholic content.

| # | Task | File(s) | Done When |
|---|------|---------|-----------|
| 2.1 | Pick 7 days from the fortnight fixture that have real data | `data/mock/anno_fortnight_2026-07-03_2026-07-16.json` | 7 entries selected |
| 2.2 | Fix those entries: replace example.com URLs with real artwork/sources | Manual or LLM | All URLs are real |
| 2.3 | Write `anno_week_current.json` with those 7 entries | `Anno/Resources/anno_week_current.json` | JSON valid, 7 entries |
| 2.4 | Verify FixtureStore loads it | Run app | 7 days visible in Calendar |

**Acceptance criteria:**
- Calendar tab shows dots for 7 days
- Tapping a day with an entry opens TodayView with real content
- Artwork images load (not placeholder)
- Sources are real, clickable URLs

---

### Sprint 3: Content Generation — Batch 1 (Day 2-3, phone-deliverable)
**Goal:** 7 days of real saint feast day content.

See `CONTENT_SPRINT_1.md` for the self-contained LLM prompt and checklist.

| # | Task | Output |
|---|------|--------|
| 3.1 | Fire content sprint 1 prompt for Jul 3-9 | 7 AnnoEntry JSON objects |
| 3.2 | Validate with `tools/validate_mock_content.py` | All checks pass |
| 3.3 | Drop validated JSON into `data/content_batch_1/` | 7 files ready |

---

### Sprint 4: Content Generation — Batch 2 (Day 3-4, phone-deliverable)
**Goal:** 7 more days of content (Jul 10-16).

See `CONTENT_SPRINT_2.md` for the self-contained LLM prompt and checklist.

| # | Task | Output |
|---|------|--------|
| 4.1 | Fire content sprint 2 prompt for Jul 10-16 | 7 AnnoEntry JSON objects |
| 4.2 | Validate | All checks pass |
| 4.3 | Drop into `data/content_batch_2/` | 7 files ready |

---

### Sprint 5: Wire Content + Bookmarks (Day 4-5)
**Goal:** App loads real content from fixtures, bookmarks persist.

| # | Task | File(s) | Done When |
|---|------|---------|-----------|
| 5.1 | Merge batch 1 + batch 2 into `anno_week_current.json` | `Anno/Resources/` | 14 entries in fixture |
| 5.2 | Run validator on final fixture | `tools/validate_mock_content.py` | Zero errors |
| 5.3 | Wire bookmark button in TodayView to SwiftData | `Today/TodayView.swift` | Bookmark icon fills/unfills, persists |
| 5.4 | Wire SavedView to show real bookmarks | `Saved/SavedView.swift` | Saved entries appear in list |
| 5.5 | Test bookmark flow end-to-end | Run app | Bookmark → Saved tab → entry visible |

**Acceptance criteria:**
- Tap bookmark on TodayView → icon fills gold
- Open Saved tab → bookmarked entry appears
- Kill and relaunch app → bookmark persists

---

### Sprint 6: Polish + Ship (Day 5-7)
**Goal:** TestFlight submission.

| # | Task | File(s) | Done When |
|---|------|---------|-----------|
| 6.1 | Fix SacredSiteListView http → https | `Map/SacredSiteListView.swift:98` | URL uses https |
| 6.2 | Add guard for empty entries in FixtureStore | `Services/FixtureStore.swift:25` | No crash on empty array |
| 6.3 | Remove KJV headers from all kept files | All files | No "DailyDevotionKJVForWomen" strings |
| 6.4 | Create AppIcon (1024pt gold cross) | `Assets.xcassets` | Icon visible on home screen |
| 6.5 | Host privacy policy (GitHub Pages or similar) | `Docs/privacy-policy.md` | Working URL |
| 6.6 | Write App Store description (EN + VI) | `Docs/app-store-metadata.md` | Ready to paste |
| 6.7 | Take screenshots (Today, Calendar, Saved) | Simulator | 3 screenshots per size |
| 6.8 | Archive and upload to App Store Connect | Xcode | Build appears in TestFlight |
| 6.9 | Submit for review | App Store Connect | "Waiting for Review" |

**Acceptance criteria:**
- App appears in TestFlight
- Internal testers can install
- App Store review notes explain: free Catholic devotional, no IAP, sourced from USCCB/Roman Martyrology
- Privacy policy URL works
- Support email works

---

## Effort Summary

| Sprint | Days | What |
|--------|------|------|
| 1. Xcode Project | 1 | Project scaffold, fix broken files, compile |
| 2. Week Fixture | 0.5 | Real content for 7 days |
| 3. Content Batch 1 | 1 | 7 days of saint feast content (phone) |
| 4. Content Batch 2 | 1 | 7 more days (phone) |
| 5. Wire Content + Bookmarks | 1 | SwiftData, bookmark flow |
| 6. Polish + Ship | 2 | Assets, archive, submit |
| **Total** | **~6.5 days** | **1 week full sprint, 2 weeks part-time** |

---

## Content Minimums

| Scenario | Days of Content | Ship? |
|----------|----------------|-------|
| **Best case** | 14 days real content | Yes, full calendar |
| **Okay** | 7 days real + 7 days Ordinary Time filler | Yes, thinner content |
| **Minimum** | 7 days real content only | Yes, but Calendar tab looks sparse |
| **Worst** | No content generated | No — app shows only preview entry |

---

## What's NOT in MVP (v2 backlog)

- Map tab + pilgrim routes
- StoreKit paywall
- Interfaith content layer
- Audio narration
- Onboarding flow
- Push notifications
- Art gallery
- Search
- iPad layout
