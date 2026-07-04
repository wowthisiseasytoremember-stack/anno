# Anno — Localization Implementation Plan

## Origin

Feedback from the design agent review, covering Vietnamese localization for Anno. Everything here assumes the main DESIGN_AGENT_BRIEF.md is already read.

---

## MMR Synthesis (goal-first, 4/5 models)

Findings folded into the plan below. Discarded items logged at the bottom.

---

## What We're Implementing

Anno ships English + Vietnamese at launch. Vietnamese is a runtime chrome swap — same icons, same layout, same colors, same typography stack. Event narratives, saint stories, artwork captions, and prayers stay English in v0.

The Vietnamese string set is already complete (`.strings` file). The front end needs to use it, not recreate it.

---

## Sprint 1: Core Localization Infrastructure

### 1.1 Update Design Inventory

**Action:** Add a `Localization` section to DESIGN_AGENT_BRIEF.md covering:

- Runtime language switch in Settings: `Language` → `English` / `Tiếng Việt`
- Language change updates UI immediately. No restart. No "changes apply next launch."
- All visible chrome text (tabs, buttons, chips, badges, sheet titles, settings labels, empty states, paywall copy) pulls from localization keys. Zero text baked into raster images.
- Event narratives, prayers, artwork metadata, source titles remain English-only in v0.
- All date strings use locale-aware formatting (never hardcoded English patterns).
- Components size to English strings as the max-width baseline. Vietnamese is 15-30% shorter — it'll fit.
- Components must never use fixed-width labels, hardcoded date strings, or icons whose meaning depends on English wording.
- **Accessibility:** VoiceOver must work correctly in Vietnamese. Dynamic Type must not truncate any Vietnamese string.
- **Fallback rule:** If a Vietnamese key is missing, silently fall back to English. Never show a blank label.

**Owner:** Brief author. **Depends on:** nothing.

---

### 1.2 Add Localization Component Rules

**Action:** Append to the project's component README:

```markdown
## Localization Design Rules
- No visible UI chrome text may be baked into raster images.
- All buttons, tabs, chips, badges, sheet titles, settings labels, empty states, and paywall copy must come from localization keys.
- Event narratives, prayers, artwork metadata, and source titles remain English-only in v0.
- All date strings must use locale-aware formatting.
- Components should size to English strings as the max-width baseline.
- Vietnamese diacritics must render cleanly using system fonts.
- Runtime language switching must update visible UI without app restart.
- If a Vietnamese key is nil, fall back to English silently. Never show a blank label.
- Dynamic Type must be tested at every size step with all Vietnamese strings. No truncation.
```

Moved here from Sprint 2 to unlock parallel design/development work.

**Owner:** Developer. **Depends on:** 1.1.

---

### 1.3 Generate Asset Board A: Localization QA

**Purpose:** Prove the design survives language switching.

**Screens to show in English/Vietnamese pairs (same data, same layout):**

1. **Today** — Vietnamese chrome, English narrative content
2. **Calendar** — Vietnamese month/day labels, Gregorian + Hebrew/Hijri secondary dates
3. **Map** — Vietnamese filter chips + English pin content
4. **Saved empty state** — fully Vietnamese
5. **Settings** — showing the language picker with "Tiếng Việt" selected
6. **Paywall** — fully Vietnamese
7. **Sources sheet** — Vietnamese chrome, English source titles
8. **Onboarding** — fully Vietnamese, verify button labels and layout at every carousel step
9. **Event/Prayer detail view** — Vietnamese header/nav, English prayer text — validates the core mixed-language experience

**Critical detail:** The Vietnamese Today screen should show mixed content:
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

That mixed state is intentional — story content is English, chrome is Vietnamese.

**Visual direction:** Dark devotional cartography + ivory manuscript UI + gold sacred-line iconography. No drift into Duolingo Catholicism.

**Owner:** Design agent. **Depends on:** 1.1 (guidelines established).

---

### 1.4 Generate Asset Board B: Vietnamese Typography Stress Test

**Purpose:** Prevent the app from looking like someone squeezed a cathedral through a label component.

**Required renderings (same screen, cycling through strings, tested at multiple Dynamic Type sizes):**

- Large date display: `Ngày 3 tháng 7 năm 2026`
- Buttons: `Bắt đầu khám phá`, `Nghe`, `Nguồn`, `Lưu`, `Chia sẻ`, `Khôi phục`
- Filter chips: `Tất cả`, `Kitô giáo`, `Do Thái`, `Hồi giáo`, `Liên tôn`
- Confidence badges: `Đã xác nhận`, `Truyền thống`, `Tranh luận`
- Tab bar labels: `Hôm nay`, `Lịch`, `Bản đồ`, `Đã lưu`
- Action/alert phrases: `Thêm vào bộ sưu tập`, `Xác nhận hành động`, `Cài đặt thông báo`, `Tiến độ`, `Hoàn thành`
- Devotional labels: `Bài đọc`, `Lời nhắn`, `Thời gian`

**Verification:** All strings render cleanly in system fonts (SF Pro). No truncation. No overflow. No orphaned diacritics (ă, â, đ, ê, ô, ơ, ư). Tested at every Dynamic Type size.

**Owner:** Design agent. **Depends on:** nothing (can run parallel with 1.3).

---

### 1.5 Generate Asset Board C: Locale-Aware Calendar Screen

**Purpose:** Calendar has the densest labels — it needs its own QA pass.

**Screen state:**
- Vietnamese month/day labels
- Gregorian date number
- Hebrew/Hijri secondary dates still displayed
- Tradition dots (color = tradition)
- Bottom sheet with all calendar conversions (include lunar calendar names like `Tháng Một Âm Lịch`), event list, localized chrome, English event titles
- Test both compact (collapsed bottom sheet) and expanded states

**Copy examples to show:**
```
Lịch
Tháng 7, 2026
Hôm nay
Mở ngày này
7 ngày
```

**Owner:** Design agent. **Depends on:** nothing (can run parallel with 1.3, 1.4).

---

## Sprint 2: Implementation

### 2.1 Build LocalizationManager

**Action:** Instead of full iOS Bundle swapping (heavy, triggers cached-UI issues), build a lightweight `LocalizationManager`:

- Loads the appropriate `.strings` file into an in-memory dictionary based on UserDefaults selection
- Vends strings via `manager.string(forKey:)` — falls back to English if Vietnamese key is nil
- Posts a `LocalizationDidChangeNotification` on language switch
- All views that display chrome text subscribe to this notification and call `localize()` / `reloadData()` to refresh
- Language preference persisted in UserDefaults (survives app restart)

**Why this approach:**
- Avoids Bundle swap edge cases (cached UIKit strings, stale viewDidLoad text, system UI that ignores custom locale)
- Single source of truth for language state
- Trivially testable — swap the manager's dictionary, verify every view updates
- No app restart needed

**Owner:** Developer. **Depends on:** 1.1 (localization rules known).

---

### 2.2 Wire Screens (Incremental Audit + Implementation)

**Action:** For each screen, wire it for language switching AND audit it in the same pass. Do not separate audit from implementation — they detect different failure modes together.

**Per-screen checklist:**
1. Add `LocalizationManager` subscription — view refreshes chrome on `LocalizationDidChangeNotification`
2. Verify all chrome text (buttons, tabs, chips, badges, labels, sheet titles, settings strings, empty states, paywall copy) pulls from localization keys — zero hardcoded strings
3. Verify `accessibilityLabel` / `accessibilityHint` are also localized
4. Verify Dynamic Type at every size step — no truncation at any size
5. Verify date strings use locale-aware formatting
6. Verify no text is embedded in raster images

**Performance target:** Language switch completes end-to-end (notification → all visible views updated) in < 200ms on iPhone SE (2020). Measure with Instruments.

**Screens to wire in order:**
1. Settings (where the switch lives — wire first so you can test the rest)
2. Today (primary screen)
3. Calendar
4. Map
5. Saved
6. Sources sheet
7. Art lightbox
8. Paywall
9. Onboarding

**Edge cases to handle during wiring:**
- System alerts/sheets presented before language change retain old language — dismiss and recreate on switch
- Navigation controller titles and tab bar items must refresh
- Cells in reusable table/collection views must re-localize on `prepareForReuse`
- State restoration must read language from UserDefaults, not cache the pre-switch value
- Deep links containing screen titles must resolve after language change

**Owner:** Developer. **Depends on:** 2.1 (LocalizationManager exists).

---

## Sprint 3: Staging & QA

### 3.1 Ship Blocker Criteria (Define Before Sprint Starts)

Before any QA begins, agree on these pass/fail criteria:

1. **Zero English strings** in chrome across all screens in Vietnamese mode
2. **Zero truncation** at maximum Dynamic Type on iPhone SE (375pt)
3. **All 3.2 edge cases pass** on the device matrix
4. **Number/date formatting** verified with vi_VN locale
5. **Snapshot tests** pass on CI for both languages
6. **Zero crashes** in language switch flow
7. **VoiceOver** reads all Vietnamese chrome text correctly

---

### 3.2 Device Matrix

Minimum devices for QA:
- iPhone SE (2020) — 375pt, worst-case truncation. Test portrait + landscape.
- iPhone 14/15/16 (standard) — 390pt, primary target
- iPhone 16 Pro Max — 430pt, large layout
- iPad Air / mini — if iPad is supported at launch

Test every screen at every Dynamic Type size (7 steps) on the SE in portrait + landscape.

---

### 3.3 Localization QA Pass

**Action:** Run through all screens in Vietnamese:

- **Chrome completeness:** Every chrome string is translated. No English bleed into buttons, tabs, labels, chips, badges, sheet titles, settings, empty states, or paywall copy.
- **Content boundary:** Event narratives, saint stories, artwork captions, and prayers are still English (no accidental translation bleed).
- **Number/currency formatting:** All numeric displays use `NumberFormatter` with `vi_VN` locale. Test decimal values, large numbers (1000+), prices, counts, dates.
- **Date formatting:** Locale-aware date patterns (`dd/MM/yyyy` vs `MM/dd/yyyy`). Verify with `Locale(vi_VN)`.
- **Diacritics:** Render correctly across all screen sizes. Check every Vietnamese diacritic (ă, â, đ, ê, ô, ơ, ư) at every Dynamic Type size.
- **Dynamic Type:** Every screen at every size step (7 steps). No truncation at any size.
- **Landscape:** No truncation of Vietnamese strings in landscape on SE.
- **VoiceOver:** Reads Vietnamese chrome text correctly.
- **Pseudo-localization pre-pass:** Before human QA, run a pseudo-localization scheme that expands all strings by 30% and adds diacritics to catch hardcoded strings and truncation bugs automatically.

---

### 3.4 Edge Cases

| State | Expected |
|-------|----------|
| User switches language mid-scroll | Current scroll position preserved, visible strings update in place |
| User switches language while paywall is open | Paywall redraws in new language |
| User switches language while an alert/sheet is presented | Alert/sheet dismisses and recreates in new language |
| User switches language while network request in flight | In-flight response uses the language that was active when request was sent. New requests use new language. No mixed-language UI. |
| User switches language in background (app → settings → return) | App foregrounds, strings update without stale cache |
| Push notification arrives in Vietnamese | Notification text uses current language |
| User backs out of language picker without selecting | Current language unchanged, no flash |
| First launch with Vietnamese device locale | Auto-detect and pre-select Vietnamese |
| First launch with unsupported locale | Default to English |
| Missing Vietnamese key on a button | Fall back to English silently, log warning |
| Dynamic Type accessibility size (AX1-AX5) | All Vietnamese strings render without truncation at every size |
| Deep link opens after language switch | Screen renders in correct language, not pre-switch cached state |

---

### 3.5 Automated Snapshot Tests

Add snapshot tests for the top 10 highest-traffic screens. Generate reference images for both English and Vietnamese at standard Dynamic Type size on SE and Pro Max. Run on CI for every PR.

Tool: iOSSnapshotTestCase or Swift Snapshot Testing (standard options).

---

## Summary

| # | Item | Type | Depends On |
|---|------|------|-----------|
| 1.1 | Add localization section to design brief | Doc | — |
| 1.2 | Add localization component rules | Doc | 1.1 |
| 1.3 | Asset board A: Localization QA (9 screen pairs) | Design | 1.1 |
| 1.4 | Asset board B: Typography stress test (expanded) | Design | — |
| 1.5 | Asset board C: Locale-aware calendar | Design | — |
| 2.1 | Build LocalizationManager (lightweight, notification-based) | Dev | 1.1 |
| 2.2 | Wire all 9 screens (incremental audit + implementation merged) | Dev | 2.1 |
| 3.1 | Define ship blocker criteria | Decision | — |
| 3.2 | Define device matrix | Decision | — |
| 3.3 | Localization QA pass (expanded) | Dev+QA | 2.2 |
| 3.4 | Edge case handling (expanded, 13 cases) | Dev | 3.3 |
| 3.5 | Snapshot tests (top 10 screens) | Dev | 3.3 |

**Key constraint throughout:** No separate Vietnamese visual system. Same icons, same layout, same colors, same typography stack. The only accommodation is slightly more generous horizontal padding on chips and buttons.

---

## Discarded MMR Findings

| Finding | Source | Why Discarded |
|---------|--------|---------------|
| Localize event narratives/prayers in v0 | glm-4.5-flash | Contradicts product direction. English content is intentional — the app sells "knowledge," not Vietnamese translations of theology. |
| Design layout system for RTL support | glm-4.5-flash | Overengineering. Vietnamese is Latin script (LTR). RTL would require a full re-architecture regardless. |
| Vietnamese user testing in Sprint 1 | glm-4.5-flash | No budget for user testing in v0 scope. QA pass (Sprint 3) catches layout issues. |
| SwiftGen/SwiftLint localization rules | nemotron | The `.strings` file is already complete. Adding tooling overhead for 2 languages is premature. Add only if strings grow to 5+ languages. |
| Full automated XCTest localization scan | openrouter/free | Overkill for 2-language app. Per-screen checklist in 2.2 catches hardcoded strings. |
| .stringsdict / plural rules | nemotron | Not needed for chrome-only swap — no dynamic pluralization in button/tab/chip text. |
| Storyboard/nib localization files | glm-4.5-flash | No storyboards — this is a SwiftUI app. |
| Auto-detect system language change | glm-4.5-flash | App manages its own language preference. System locale changes are irrelevant. |
| Pluralization .stringsdict rules | openrouter/free | Chrome-only swap has no count-dependent strings in buttons/tabs. No need. |
| Search/filter diacritic handling | openrouter/free | No search functionality in v0. Defer to post-launch. |
| App Store metadata localization | glm-4.5-flash | Not a front-end concern. Separate workstream. |
| Analytics locale context in crash reports | openrouter/free | Beyond QA sprint scope. Defer to post-launch. |
| Keyboard input method testing (Telex/VNI) | openrouter/free, glm-4.5-flash | System handles IME composition. Not the app's responsibility. |
| RTL text handling prep | glm-4.5-flash | Vietnamese is Latin script (LTR). Overengineering. |
| "Longest possible string" baseline instead of English max-width | nemotron | Valid concern, but Vietnamese is 15-30% shorter across all measured strings. English max-width is the constraint. If new strings break this, adjust then. |
| 2-tone text treatment (Vietnamese chrome in brand color, English content in body) | openrouter/free | Over-engineered UX pattern for v0. The mixed-language state is already visually distinct (buttons vs body text). |
