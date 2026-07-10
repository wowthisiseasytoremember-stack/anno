# Anno ← KJV App — Clone & Adapt Plan

## What We're Doing

Take every reusable architectural piece from the KJV women's devotional app (DailyDevotionKJVForWomen, built by Rork) and bring it into Anno (interfaith sacred-history app). Anno already has a theme system, calendar engine, and bilingual infrastructure. What it lacks: a devotional engine, a bookmark system, audio pipeline, and content generation schema.

## What Clones Directly (Zero/Minimal Changes)

These files copy as-is or with a one-line namespace change:

| File | How to Clone | What Changes |
|---|---|---|
| `DailyDevotionalLoader.swift` | Copy → Anno/Services/ | s/DailyDevotionAnno/Anno/g |
| `DevotionalProvider.swift` | Copy → Anno/Services/ | Nothing — already generic ObservableObject |
| `Bookmark.swift` | Copy → Anno/Models/ | Namespace, s/KJV/Anno/ in bundle ID |
| `BookmarkActions.swift` | Copy → Anno/Services/ | Nothing |
| `AppRouter.swift` | Copy → Anno/ | Anno already has tab state, add PendingNavigation pattern |
| `VerseActionBar.swift` | Copy → Anno/Components/ | Tint, icon swap (rose → goldLeaf) |
| `ShareableImage.swift` | Copy → Anno/Components/ | Nothing |
| `ShareCard.swift` | Copy → Anno/Components/ | Theming: change Palette colors to AnnoTheme |
| `Haptics.swift` | Copy → Anno/Utilities/ | Nothing |
| `SearchHistory.swift` | Copy → Anno/Utilities/ | Nothing |
| `Typography.swift` | Copy → Anno/Design/ | Anno already has .serifDisplay approach — merge |
| `GlassCard.swift` | Copy → Anno/Components/ | Anno uses AnnoCard modifier — rename or keep as alternative |
| `NotificationService.swift` | Copy → Anno/Services/ | Customize notification content strings |

## Content Schema (Document, Don't Code Yet)

The KJV content research prompt defined a complete schema for devotionals, essays, women profiles, prayers, and sleep content. Anno needs its own content in this same structure but with Catholic/Vietnamese text:

- Themed blocks structure → map to Catholic seasons (Advent, Lent, Ordinary Time)
- Life-stage devotionals → same structure, Catholic theology
- Essays → swap writers for Catholic saints + theologians
- Prayer library → integrate with Divine Office hours
- Sleep/Comfort → universal, no changes
- Cartesia audio strategy → cheaper for Anno (free Gregorian chant)

## What Doesn't Clone

| KJV Feature | Anno Equivalent | Why Different |
|---|---|---|
| Bible Library (BibleLibrary.swift) | Already has Engine A + Engine B | Anno's data is historical, not just verse lookup |
| Palette (Theme.swift) | Already has AnnoTheme | Different color philosophy — keep Anno's ecclesial palette |
| Devotional data (devotionals.json) | Generate Catholic devotionals | Different canon, theology, and calendar |
| Bible reader views | Not needed v1 | Anno is calendar-first, not Bible-first |
| Welcome View | Anno has its own | Different onboarding flow |
| AuroraBackground | Anno has narthex atmosphere | Keep Anno's ecclesial dark |

## Prioritization

1. **P0 — Copy now:** DailyDevotionalLoader, DevotionalProvider, Bookmark, BookmarkActions, Haptics (no integration risk, standalone files)
2. **P0 — Copy now:** AppRouter's PendingNavigation pattern (tiny, enables widget/intent deep linking in Anno)
3. **P0 — Copy now:** ShareableImage, ShareCard, VerseActionBar (component pattern — no dependency on app data)
4. **P1 — Adapt:** NotificationService, SearchHistory (need localization pass)
5. **P1 — Adapt:** GlassCard (competing with existing AnnoCard — decide which wins)
6. **P2 — Schema only:** All content generation formats (essays, devotionals, prayers) — produce content, not code

## Files in Play

| KJV Source | Anno Destination |
|---|---|
| `/tmp/kjv-split-files/DailyDevotionalLoader.swift` | `Anno/Services/AnnoDevotionalLoader.swift` |
| `/tmp/kjv-split-files/DevotionalProvider.swift` | `Anno/Services/AnnoDevotionalProvider.swift` |
| `/tmp/kjv-split-files/Bookmark.swift` | `Anno/Models/Bookmark.swift` |
| `/tmp/kjv-split-files/BookmarkActions.swift` | `Anno/Services/BookmarkActions.swift` |
| `/tmp/kjv-split-files/AppRouter.swift` | `Anno/AppRouter.swift` (merge PendingNavigation into existing) |
| `/tmp/kjv-split-files/VerseActionBar.swift` | `Anno/Components/VerseActionBar.swift` |
| `/tmp/kjv-split-files/ShareableImage.swift` | `Anno/Components/ShareableImage.swift` |
| `/tmp/kjv-split-files/ShareCard.swift` | `Anno/Components/ShareCard.swift` |
| `/tmp/kjv-split-files/Haptics.swift` | `Anno/Utilities/Haptics.swift` |
| `/tmp/kjv-split-files/SearchHistory.swift` | `Anno/Services/SearchHistory.swift` |
| `/tmp/kjv-split-files/Typography.swift` | `Anno/Design/Typography.swift` |
| `/tmp/kjv-split-files/GlassCard.swift` | `Anno/Components/GlassCard.swift` |
| `/tmp/kjv-split-files/NotificationService.swift` | `Anno/Services/NotificationService.swift` |
