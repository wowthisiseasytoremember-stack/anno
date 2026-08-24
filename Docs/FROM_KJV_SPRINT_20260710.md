# Anno ← KJV Devotion — What Was Built, What's Available for Pickup

**Date:** 2026-07-10
**Context:** The KJV women's devotional app (DailyDevotionKJVForWomen) had a major App Store submission sprint executed. This doc indexes what was created that Anno could adapt.

## Quick Status

Files already cloned into Anno (per `CLONE_FROM_KJV.md` + `ARCHITECTURE.md` §D):

| Already Here | Location |
|-------------|----------|
| DailyDevotionalLoader → AnnoDevotionalLoader.swift | Anno/Services/ |
| DevotionalProvider.swift | Anno/Services/ |
| Bookmark.swift + BookmarkActions.swift | Anno/Models/ + Anno/Services/ |
| GlassCard.swift | Anno/Components/ |
| ShareCard.swift | Anno/Components/ |
| ShareableImage.swift | Anno/Components/ |
| VerseActionBar.swift | Anno/Components/ |
| Haptics.swift | Anno/Utilities/ |
| SearchHistory.swift | Anno/Services/ |
| NotificationService.swift | Anno/Services/ |

## New Things Built in This Sprint (Pickup Candidates)

### 1. Widget Extension Pattern — `DevotionalWidget/`

**What:** iOS 17+ home screen widget showing a daily devotional verse.

**Why Anno wants it:** Anno could ship a "Today in Sacred History" widget showing: today's saint name, calendar events for each tradition, or a prayer of the day. Same TimelineProvider pattern — inline mini-dataset for MVP, App Groups for production.

**What to copy:**
- `DevotionalWidget.swift` (147 lines) — StaticConfiguration, TimelineProvider, date-based rotation, .systemSmall/.systemMedium, containerBackground(.clear, for: .widget)
- `Info.plist` — NSExtensionPointIdentifier = com.apple.widgetkit-extension
- Widget target is already in the KJV pbxproj (but the pbxproj is gitignored — see below)

**Adaptation effort:** ~30m. Create `AnnoWidget/` directory, copy+rename the widget file, swap inline dataset for Anno content (saint names, feast descriptions, date-based rotation). Need Xcode to add the widget target.

### 2. App Store Submission Sprint Template

**What:** A 5-sprint plan (`sprints/APPSTORE_SUBMISSION_SPRINT_PLAN.md`) covering build infrastructure, privacy & legal, assets & metadata, hardening, and polish. 395 lines of step-by-step instructions with exact commands.

**Why Anno wants it:** Every iOS app needs this. Anno's architecture + Monetization Contract are more complex (subscriptions, MapKit, localization). The sprint structure is reusable — swap the app-specific details.

**What to copy:** The sprint structure + verification gates. See also `Docs/app-store-metadata.md` for the ASC copy-paste template.

### 3. App Icon Generation

**What:** Programmatic 1024pt app icon (open Bible + dove on lilac/gold gradient) + 10 scaled sizes, all in `Assets.xcassets/AppIcon.appiconset/`.

**Why Anno wants it:** The generation technique (PIL + asset catalog JSON) is reusable. Anno's eventual icon will be different but the `AppIcon.appiconset/Contents.json` with all required sizes is copy-paste ready.

**Content of Contents.json — all required image slots:**
- 20pt@2x, 20pt@3x, 29pt@2x, 29pt@3x, 40pt@2x, 40pt@3x, 60pt@2x, 60pt@3x, 76pt@2x, 83.5pt@2x, 1024pt

### 4. Privacy Compliance Pack

**What:**
- `PrivacyInfo.xcprivacy` — Apple privacy manifest declaring no tracking, no data collection
- `Docs/privacy-policy.md` — Zero-collection privacy policy ready to host

**Why Anno wants it:** Anno needs the same two files. The privacy policy text adapts (Anno may collect subscription data through StoreKit). The PrivacyInfo.xcprivacy manifest is identical (Anno also collects no user data beyond what StoreKit provides).

### 5. Accent Color Asset

**What:** `Assets.xcassets/AccentColor.colorset/` with `#B69CD6` (lilac) for both light and dark appearance.

**Why Anno wants it:** Anno needs its own accent color set. The `.colorset/Contents.json` format is copy-paste — just swap the hex values to Anno's goldLeaf or ecclesial palette.

### 6. Content That Didn't Make the Clone

These KJV files were NOT in the CLONE_FROM_KJV.md list but contain patterns Anno could reuse:

| KJV File | What It Does | Anno Adaptation |
|----------|-------------|-----------------|
| `WomanProfile.swift` | Codable data model with name, scripture, story, lesson, reflectionQuestion, keyVerse | Swap for **SaintProfile** — same fields, replace scripture with feast date + patronage + biography |
| `WomanOfTheDayProvider.swift` | Date-rotated provider (same pattern as DevotionalProvider) | Swap woman index → saint index. Reuse the deterministic rotation unchanged |
| `WomanOfTheDayView.swift` | Full-screen profile: GlassCard sections, story (scrollable), lesson, reflection question | Swap for **SaintOfTheDayView** — same layout, Catholic saint content |
| `women_of_the_bible.json` | 22 profiles, Codable | Schema template for **saint_profiles.json** — same structure, different data |
| `women_of_church_history.json` | 15 essay-profiles | Schema template for **saint_essays.json** |
| `DevotionalCard.swift` | The daily card component with verse + reflection + prayer | Adapt for **TodayCard** showing the day's sacred events |
| `AuroraBackground.swift` | Soft animated background gradient | Already has narthex atmosphere (per CLONE docs) — but AuroraBackground is lighter/simpler |
| `HomeView.swift` | Tab root — daily card + navigation | Anno's TodayView needs similar structure: scrollable daily content header + navigation |
| `SettingsView.swift` | Full settings with appearance, font, notifications, privacy link, restore defaults | Reusable structure — swap Palette colors for AnnoTheme |
| `AppSettings.swift` | Observable settings model (appearance enum, font scale, reminder toggle, notification pref) | Directly adaptable — the settings schema is canon-agnostic |
| `AppIntents.swift` | 2x App Intents: ShowDevotionalIntent + SearchScriptureIntent | Anno could add **ShowTodayIntent** for Siri + Shortcuts |
| `WelcomeView.swift` | First-launch onboarding (3-page carousel) | Anno needs onboarding — this is the pattern |
| `Devotional.swift` | Data model: reference, scripture, theme, reflection, prayer, narrator_tone | AnnoEntry already exists — compare schemas for content model alignment |

### 7. PBXFileSystemSynchronizedRootGroup (Xcode 26)

The KJV project now uses Xcode 16's file-system-synchronized groups. This means:
- Source files live in `DailyDevotionKJVForWomen/` on disk
- Xcode discovers them automatically — no PBXBuildFile entries needed
- `DevotionalWidget/` is a separate sync group

**Why Anno wants it:** If Anno was created with the same Xcode version, the same pattern applies. If it's on an older Xcode with explicit build file entries, this pattern won't work. Check `objectVersion` in Anno's pbxproj — if >= 77 (Xcode 16), you can migrate.

## Files That Are Fully Canon-Agnostic (Copy Directly)

These have zero KJV-specific content — pure utility:

| File | Copy To |
|------|---------|
| `PrivacyInfo.xcprivacy` | Same location in Anno |
| `Docs/app-store-metadata.md` | Structure reference only |
| `Assets.xcassets/AccentColor.colorset/Contents.json` | Replace hex values |
| `Assets.xcassets/AppIcon.appiconset/Contents.json` | Replace image filenames + sizes |

## ⚠️ Known Issue: pbxproj is Gitignored

The KJV project's `.gitignore` includes `*.pbxproj`. This means ALL pbxproj changes from this sprint (DEV_TEAM, display name, notification description, release stripping, widget plist config) exist on disk only — they're not in git. If you're reading this from a fresh clone on a different machine, those changes are absent.

**Fix:** Remove `*.pbxproj` from `.gitignore` before committing.

---

## Recap: What Anno Should Pick Up Next

Ordered by impact / dependency:

1. **Widget** (`AnnoWidget/`) — Ship a "Today in Sacred History" widget before or alongside v1. Low effort, high App Store visibility.
2. **Privacy compliance** (`PrivacyInfo.xcprivacy` + privacy policy) — Required for submission. Copy from KJV, adapt text.
3. **Saint profiles** — Use `WomanProfile.swift` schema + `WomanOfTheDayProvider.swift` rotation for "Saint of the Day" content. High spiritual value.
4. **Settings + Onboarding** — `AppSettings.swift`, `SettingsView.swift`, `WelcomeView.swift` are ready for adaptation. Medium effort.
5. **App Store sprint template** — Refer to the 5-sprint structure when prepping Anno's submission.
6. **Widget + Siri** (`AppIntents.swift`) — "Hey Siri, show me today's saint" for Shortcuts.
