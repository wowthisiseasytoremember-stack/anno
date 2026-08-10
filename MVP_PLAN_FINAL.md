# Anno MVP — Catholic Daily Devotional (Final)
**Last updated:** 2026-07-15 19:30 UTC
**Goal:** TestFlight-ready daily devotional for Catholic iOS users (EN + VI)
**Scope:** Saints, feast days, historical figures — Catholic-first
**MMR reviewed:** goal-first (4/5 models) + red-team (4/5 models) — feedback integrated below

---

## MMR Feedback Applied

| Finding | Severity | Fix Applied |
|---------|----------|-------------|
| Map tab code still in project but cut from MVP | High | **Sprint 1: Delete all Map files** — SacredSiteMapView, SacredSiteListView, Map/ folder |
| Paywall code included but paywall is cut | High | **Sprint 1: Delete Paywall folder** — ArchivePaywallView, ProductCopy. Add back in v2. |
| FixtureStore crashes on missing/malformed JSON | Critical | **Sprint 1: Add guard** — catch file-not-found and JSON decode errors, fall back to preview |
| Manual JSON merge is fragile | Critical | **Sprint 5: Automate** — write merge script with validation, not hand-editing |
| Empty calendar days look broken | Medium | **Sprint 2: Add empty state** — "No entry yet" message when tapping day with no content |
| Vietnamese UI strings missing | High | **Sprint 1: Create Localizable.strings** — EN + VI for all UI labels |
| No theological review step | High | **Sprint 6: Add gate** — human reviews content before ship |
| Bookmark only stores entryID | Medium | **Sprint 5: Store title + date** — richer bookmark for meaningful Saved view |
| Content generation on phone unreliable | Medium | **Accept risk** — prompts work, but have fallback: pre-generated Ordinary Time filler |
| Liturgical clock vs timezone | Medium | **Sprint 1: Use device date** — `Date()` for Today, not hardcoded |
| Artwork hotlinking may fail | Medium | **Sprint 2: Test URLs** — click-test artwork, fallback to Wikipedia thumbnails |
| No onboarding or feedback mechanism | Info | **v2** — out of scope for MVP |

---

## What Ships in MVP

| Tab | Content | Status |
|-----|---------|--------|
| **Today** | Daily saint/feast, artwork, prayer, sources, calendar pills | UI done |
| **Calendar** | Month grid, tap-to-open day detail | UI done |
| **Saved** | Spiritual Bouquet tracker + bookmarked entries | Tracker done |

**Deleted from MVP (v2 backlog):**
- Map tab — entire folder removed
- Paywall — entire folder removed
- StoreKit paywall
- Interfaith content layer
- Audio narration
- Pilgrim routes
- Onboarding walkthrough
- Push notifications

---

## Sprint 1: Xcode Project + Clean Build (Day 1)
**Goal:** App compiles, launches, zero dead code.

| # | Task | File(s) | Done When |
|---|------|---------|-----------|
| 1.1 | Create Xcode project "Anno", SwiftUI, iOS 17+, dark mode | New project | `.xcodeproj` exists |
| 1.2 | Add compile-ready files to target | See keep list | All in Project Navigator |
| 1.3 | **Delete Map folder entirely** | `Map/SacredSiteMapView.swift`, `Map/SacredSiteListView.swift` | Folder gone |
| 1.4 | **Delete Paywall folder entirely** | `Paywall/ArchivePaywallView.swift`, `Paywall/ProductCopy.swift` | Folder gone |
| 1.5 | Delete broken KJV files | See delete list | Files removed |
| 1.6 | Fix Bookmark.swift — strip VerseReference, add title/date fields | `Models/Bookmark.swift` | Compiles, stores entryID + title + date |
| 1.7 | Fix BookmarkActions.swift — rewrite for AnnoEntry.ID | `Services/BookmarkActions.swift` | Compiles |
| 1.8 | Wire .modelContainer in AnnoApp.swift | `AnnoApp.swift` | `.modelContainer(for: Bookmark.self)` present |
| 1.9 | **Add FixtureStore error handling** — guard for missing file, malformed JSON | `Services/FixtureStore.swift` | Falls back to preview, no crash |
| 1.10 | Add Assets.xcassets (AppIcon + AccentColor) | New asset catalog | App icon shows |
| 1.11 | Add PrivacyInfo.xcprivacy to target | Move from root | File in app target |
| 1.12 | Copy fixture JSONs to bundle | `Anno/Resources/*.json` | In Copy Bundle Resources |
| 1.13 | **Create Localizable.strings** — EN + VI for all UI labels | `Localization/` | Both files exist |
| 1.14 | Build and fix | — | `Cmd+B` zero errors |

**Files to keep (compile as-is after 1.6-1.7 fixes):**
- `AnnoApp.swift`, `RootView.swift`
- `Today/TodayView.swift`, `Today/ConfidenceBadge.swift`
- `Calendar/MonthCalendarView.swift`
- `Sources/SourceSheet.swift`, `Sources/SourceRow.swift`
- `Settings/SettingsView.swift`
- `Models/AnnoEntry.swift`, `Models/Bookmark.swift` (after fix)
- `Services/FixtureStore.swift` (after error handling), `Services/BookmarkActions.swift` (after rewrite)
- `Localization/LanguageMode.swift`, `Localization/LocalizedEntryText.swift`
- `Design/AnnoTheme.swift`
- `Services/NotificationService.swift`, `Services/SearchHistory.swift`
- `Utilities/Haptics.swift`

**Delete entirely:**
- `Map/` folder (both files)
- `Paywall/` folder (both files)
- `Components/GlassCard.swift`, `ShareCard.swift`, `ShareableImage.swift`, `VerseActionBar.swift`
- `Design/Typography.swift`
- `AppRouter.swift`
- `Services/DevotionalProvider.swift`, `DailyDevotionalLoader.swift`, `AnnoDevotionalLoader.swift`

**Acceptance criteria:**
- `Cmd+B` zero errors
- App launches on simulator
- Today tab shows preview entry
- Calendar tab shows month grid
- Dark mode default
- No KJV references anywhere in codebase

---

## Sprint 2: Week Fixture + Empty States (Day 1-2)
**Goal:** 7 days of real content visible, empty days handled gracefully.

| # | Task | File(s) | Done When |
|---|------|---------|-----------|
| 2.1 | Pick 7 days from fortnight fixture with real data | `data/mock/anno_fortnight_2026-07-03_2026-07-16.json` | 7 entries selected |
| 2.2 | Replace example.com URLs with real artwork/sources | Manual/LLM | All URLs real |
| 2.3 | Test artwork URLs — click-test 5+ to confirm they load | Browser | All return 200 |
| 2.4 | Write `anno_week_current.json` with those 7 entries | `Anno/Resources/` | Valid JSON, 7 entries |
| 2.5 | **Add empty day state** to MonthCalendarView | `Calendar/MonthCalendarView.swift` | Tapping empty day shows "No entry for this day" instead of blank |
| 2.6 | Verify FixtureStore loads week | Run app | 7 days visible in Calendar |

**Acceptance criteria:**
- Calendar shows dots for 7 days
- Tapping day with entry → TodayView with real content
- Tapping empty day → graceful "no entry" message
- Artwork loads (not placeholder)
- Sources are real URLs

---

## Sprint 3: Content Batch 1 (Day 2-3, phone-deliverable)
**Goal:** 7 days of saint feast content (Jul 3-9).

See `CONTENT_SPRINT_1.md` — self-contained LLM prompt + checklist. Run from iPhone.

| # | Task | Output |
|---|------|--------|
| 3.1 | Fire prompt for Jul 3-9 | 7 AnnoEntry JSON |
| 3.2 | Validate | All checks pass |
| 3.3 | Save to `data/content_batch_1/` | 7 files ready |

---

## Sprint 4: Content Batch 2 (Day 3-4, phone-deliverable)
**Goal:** 7 more days (Jul 10-16).

See `CONTENT_SPRINT_2.md` — self-contained LLM prompt + checklist.

| # | Task | Output |
|---|------|--------|
| 4.1 | Fire prompt for Jul 10-16 | 7 AnnoEntry JSON |
| 4.2 | Validate | All checks pass |
| 4.3 | Save to `data/content_batch_2/` | 7 files ready |

---

## Sprint 5: Wire Content + Bookmarks (Day 4-5)
**Goal:** Real content loads, bookmarks persist with rich data.

| # | Task | File(s) | Done When |
|---|------|---------|-----------|
| 5.1 | **Run merge script** (not manual) to combine batches into `anno_week_current.json` | `tools/merge_content.py` (write this) | 14 entries, valid JSON |
| 5.2 | Run validator on final fixture | `tools/validate_mock_content.py` | Zero errors |
| 5.3 | Wire bookmark button to SwiftData | `Today/TodayView.swift` | Bookmark fills/unfills, persists |
| 5.4 | Bookmark stores entryID + title + date | `Models/Bookmark.swift` | Rich data in Saved tab |
| 5.5 | Wire SavedView to real bookmarks | `Saved/SavedView.swift` | Bookmarked entries appear |
| 5.6 | Test end-to-end | Run app | Bookmark → Saved → entry visible → relaunch → persists |

**Acceptance criteria:**
- Tap bookmark → icon fills gold
- Open Saved → bookmarked entry shows title + date
- Kill relaunch → bookmark persists
- 14 days of content in Calendar

---

## Sprint 6: Polish + Ship (Day 5-7)
**Goal:** TestFlight submission.

| # | Task | File(s) | Done When |
|---|------|---------|-----------|
| 6.1 | Remove KJV headers from all kept files | All files | Zero "KJV" strings |
| 6.2 | Create AppIcon (1024pt gold cross) | `Assets.xcassets` | Icon on home screen |
| 6.3 | Host privacy policy (GitHub Pages) | `Docs/privacy-policy.md` | Working URL |
| 6.4 | Write App Store description EN + VI | `Docs/app-store-metadata.md` | Ready to paste |
| 6.5 | Take screenshots (Today, Calendar, Saved) | Simulator | 3 per size |
| 6.6 | **Theological review** — human checks 3-5 entries for accuracy | Manual | Sign-off |
| 6.7 | Archive + upload to App Store Connect | Xcode | Build in TestFlight |
| 6.8 | Submit for review | App Store Connect | "Waiting for Review" |

**Acceptance criteria:**
- App in TestFlight
- Internal testers can install
- Review notes: free Catholic devotional, no IAP, USCCB/Martyrology sourced
- Privacy policy URL works
- Support email works
- No placeholder URLs in shipped content

---

## Effort Summary

| Sprint | Days | What |
|--------|------|------|
| 1. Clean Build | 1 | Project, delete dead code, compile |
| 2. Week Fixture | 0.5 | Real content + empty states |
| 3. Content Batch 1 | 1 | 7 days (phone) |
| 4. Content Batch 2 | 1 | 7 days (phone) |
| 5. Wire + Bookmarks | 1 | SwiftData, merge script |
| 6. Polish + Ship | 2 | Assets, review, archive |
| **Total** | **~6.5 days** | **1 week full sprint** |

---

## Content Minimums

| Scenario | Days | Ship? |
|----------|------|-------|
| Best | 14 real | Yes |
| Okay | 7 real + 7 Ordinary Time filler | Yes |
| Minimum | 7 real only | Yes, sparse |
| Worst | None | No |

**Pre-generated filler:** Write 7 generic "Ordinary Time" entries (green, rank "Feria", generic prayer) and keep in `data/ordinary_time_filler.json` as insurance.

---

## v2 Backlog

- Map tab + pilgrim routes
- StoreKit paywall + subscriptions
- Interfaith content layer
- Audio narration
- Onboarding flow
- Push notifications
- Art gallery
- Search
- iPad layout
