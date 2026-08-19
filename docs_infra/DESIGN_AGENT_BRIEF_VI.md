# Anno — Addendum: Vietnamese Localization

## Follow-up to the Design Inventory — read after the main brief.

Anno ships in English and Vietnamese at launch. The Vietnamese UI string set is already complete (`localization/vi/Localizable.strings`).

## What This Means for the Front End

**Every screen must support runtime language switching.** The user picks their language in Settings and the UI flips immediately — no app restart needed.

**Scoped to UI chrome only.** Event narratives, saint stories, artwork captions, and prayer content are in English for v0 regardless of UI language. The Vietnamese translation scope is limited to:

| Area | Translations Done |
|------|-----------------|
| Tab bar labels | ✅ Today, Calendar, Map, Saved |
| Date/calendar headers | ✅ Month names, day names, "Today" |
| Onboarding carousel | ✅ All 3 slides + CTA |
| Settings screen | ✅ All labels, picker options |
| Paywall screen | ✅ Headline, feature checklist, pricing, footer |
| Map filter chips | ✅ Tradition names, "All" |
| Sources sheet | ✅ Confidence badges, "Report inaccuracy" |
| Saved tab empty state | ✅ Guide text |
| Bookmark / share / dismiss | ✅ Button labels |
| Listen / Sources buttons | ✅ Button labels |
| "7 days" badge | ✅ Calendar tab jump button |
| Liturgical labels | ✅ "Optional Memorial", "Feast", "Solemnity" etc. |

## Design Implications

**Dynamic text length.** Vietnamese strings are 15-30% shorter than English (no articles, no prepositions). But label widths should be sized to the English strings for safety — Vietnamese will fit.

**No character set issues.** Vietnamese uses Latin script with diacritics (ă, â, đ, ê, ô, ơ, ư). SF Pro / system fonts handle these natively. No custom typeface needed.

**Date formatting.** Vietnamese date format is "Ngày N tháng M năm Y" (Day N month M year Y). Calendar headers and date display should use system locale-aware date formatting, not hardcoded English patterns.

**Layout test:** the longest Vietnamese string is shorter than the longest English string in every UI position above. No layout stretching expected.

## Implementation Note

The Localizable.strings file is standard iOS `.strings` format. If the design agent is producing static mockups (not a SwiftUI prototype), they can ignore the mechanism — just design each screen assuming the chrome text can swap. If they're producing a working SwiftUI prototype, use `Text("key")` with `LocalizedStringKey` and the strings file handles the rest.
