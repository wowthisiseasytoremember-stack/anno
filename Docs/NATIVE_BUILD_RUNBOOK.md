# Anno — Native iOS Build Runbook (Mac-Gated)

**Why this file exists:** ichabod (Linux) cannot compile Swift/Xcode or run the iOS
simulator. Every step below REQUIRES macOS + Xcode 15+ + a paid/hobby Apple Developer
account. They are staged here so the work is finished on a Mac without re-deriving it.

---

## Open Defects (server-side, doable now — not Mac-gated)

1. **Sources gap (45/59 unified entries have <2 sources).** Fortnight (Jul 3-16) and
   August (all 31) fixtures have 0 sources; Engine B (Jul 17-30) has 2-3. `validate_mock_content.py`
   correctly fails the fortnight on this. Fix: add `sources[]` to fortnight/August entries
   (USCCB daily readings URL pattern: `https://bible.usccb.org/bible/readings/MMDDYY`),
   OR relax the source-count requirement in the validator if 0-source is acceptable for
   preview/build fixtures.
2. **Engine B `place.name` missing** on all 14 Engine B dates (place object has
   lat/long/source_url but no `name`). Non-blocking — Swift `SacredPlace` is optional
   (`SacredPlace?`) — but the `validate_engine_b_output.py` gate flags it. Either add a
   `name` to each Engine B place, or downgrade that check from FAIL to WARN.
3. **Remaining liturgical year not generated** (Sep 2026 → mid-2027). Engine A JSONL
   covers 2026-2029 conversions, but devotional research (Engine B) only done through
   Aug 31. Generate the rest with `tools/fire_engine_b.py` (edit its `dates` range) + VN pass.

Status of each step as of 2026-08-19 (server-side prep done unless noted):

| Step | Mac required? | Server prep done? | Status |
|------|---------------|-------------------|--------|
| Xcode project scaffold (`Anno.xcodeproj`) | YES | content fixtures ready | ⛔ BLOCKED — do on Mac |
| Wire SwiftUI views (Today/Calendar/Saved) | YES | EN+VI fixtures exist | ⛔ BLOCKED |
| StoreKit 2 subscription scaffolding | YES | copy written | ⛔ BLOCKED (v2 scope per MVP) |
| String Catalogs (vi.lproj) | YES | `Localizable.strings` EN/VI 100% | ⛔ BLOCKED (import only) |
| MapKit sacred-place view | YES | removed from MVP scope | ⛔ CUT (v2) |
| Build + simulator launch (`Cmd+B`) | YES | n/a | ⛔ BLOCKED |
| TestFlight upload | YES | privacy policy + metadata ready | ⛔ BLOCKED |
| **Server-side (ichabod) — DONE** | | | |
| August 2026 VN pass (217 `*_vi`) | NO | ✅ | done |
| Fortnight VN pass | NO | ✅ (already filled) | done |
| Engine B batch 07-17→07-30 | NO | ✅ (API run) | done |
| Validators fixed (`validate_engine_b_output`) | NO | ✅ | done |
| Localization EN/VI 100% coverage | NO | ✅ | done |

---

## On-Mac Execution Checklist (Sprint 1 from MVP_PLAN_FINAL.md)

1. **Scaffold.** Xcode → New Project → App → "Anno", SwiftUI, iOS 17+, dark mode default.
   Bundle ID `com.anno.app`.
2. **Add kept files to target** (compile as-is after bookmark fixes):
   - `AnnoApp.swift`, `RootView.swift`
   - `Today/TodayView.swift`, `Today/ConfidenceBadge.swift`
   - `Calendar/MonthCalendarView.swift`
   - `Sources/SourceSheet.swift`, `Sources/SourceRow.swift`
   - `Settings/SettingsView.swift`
   - `Models/AnnoEntry.swift`, `Models/Bookmark.swift`
   - `Services/FixtureStore.swift`, `Services/BookmarkActions.swift`
   - `Localization/LanguageMode.swift`, `Localization/LocalizedEntryText.swift`
   - `Design/AnnoTheme.swift`
   - `Services/NotificationService.swift`, `Services/SearchHistory.swift`
   - `Utilities/Haptics.swift`
3. **Delete (per MMR review):** `Map/` folder, `Paywall/` folder, `Components/GlassCard.swift`,
   `ShareCard.swift`, `ShareableImage.swift`, `VerseActionBar.swift`, `Design/Typography.swift`,
   `AppRouter.swift`, `Services/DevotionalProvider.swift`, `DailyDevotionalLoader.swift`,
   `AnnoDevotionalLoader.swift`.
4. **Fix `Bookmark.swift`** — strip `VerseReference`, add `title`/`date` fields; rewire
   `BookmarkActions.swift` for `AnnoEntry.ID`; add `.modelContainer(for: Bookmark.self)` in
   `AnnoApp.swift`.
5. **`FixtureStore` error guard** — catch file-not-found + JSON decode errors, fall back to
   preview (prevents the crash noted in MMR).
6. **Bundle resources** — copy `Anno/Resources/*.json` (incl. regenerated `AnnoMockData.swift`
   content) into Copy Bundle Resources. Add `PrivacyInfo.xcprivacy`.
7. **String Catalogs** — import `localization/en` + `localization/vi`; Xcode auto-builds
   `vi.lproj`. Confirm both languages render in simulator (device language toggle).
8. **Build & launch** — `Cmd+B` zero errors, simulator shows Today with preview entry,
   Calendar month grid, dark mode default, zero "KJV" strings in codebase.

## Content-pipeline integration note (DECISION REQUIRED)
There are three content tracks with mismatched schemas:
- `data/mock/anno_fortnight_2026-07-03_2026-07-16.json` (14 entries, EN+VI, **0 sources**,
  IDs `anno-YYYY-MM-DD`, consumed by `export_swift_fixture.py`)
- `data/research_results/2026-07-{17..30}_result_en.json` (Engine B, has sources, IDs like
  `2026-07-18-bvm-saturday`, `primary.type` holds a rank not a type)
- `data/mock/anno_august_2026.json` (31 entries, EN-only→now EN+VI, 0 sources)

Before the app ships real content the fixture exporter must consume ONE normalized schema.
The `validate_engine_b_output.py` gate (fixed) documents the required shape:
`id=anno-YYYY-MM-DD`, `primary.type ∈ {saint,feast,liturgical_day,...}`,
`liturgical.color` lowercase, `sources>=2`. **Reconcile these three tracks into a single
normalized fixture and re-point `export_swift_fixture.py` at it — this is server-doable but
needs a normalization decision (which track wins for overlapping dates, how to map Engine B
ranks/types).** Flagged, not silently done.

## Pre-TestFlight (Sprint 6)
- AppIcon 1024pt (gold cross) in `Assets.xcassets`.
- Host `Docs/privacy-policy.md` (GitHub Pages) → working URL.
- App Store description EN+VI in `Docs/app-store-metadata.md`.
- Simulator screenshots (Today/Calendar/Saved), 3 per size.
- **Theological review** — human signs off 3-5 entries.
- Archive + upload to App Store Connect → TestFlight → "Waiting for Review".
