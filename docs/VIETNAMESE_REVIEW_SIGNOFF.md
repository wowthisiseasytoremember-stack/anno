# Anno — Vietnamese Localization Review Sign-off

Hard release gate. TestFlight build is **blocked** until `vi_review_complete` is `true` and a native
Vietnamese speaker has signed below.

- reviewer_name:
- review_date:
- vi_review_complete: false

## Review checklist (all must pass)
- [ ] Every user-facing English string has a Vietnamese equivalent (no missing `vi` keys).
- [ ] No English hardcoded in SwiftUI views — all copy flows through `LocalizationManager` / String Catalog.
- [ ] StoreKit paywall copy is localized (titles, price labels, trial wording).
- [ ] Date/liturgical labels render correctly in Vietnamese locale.
- [ ] No untranslated placeholders (e.g. "TODO", "Lorem") remain in VI strings.

> Set `vi_review_complete: true` only after a native Vietnamese speaker confirms the above.
> The release checklist (`docs/RELEASE_CHECKLIST.md`) refuses to proceed without this line present and true.
