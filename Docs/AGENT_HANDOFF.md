# Anno — High-Level Agent Handoff Document
**Date:** 2026-07-08
**Context:** Devotional iOS App ("This Day in Catholic History")

This document is designed to onboard a high-level agent (such as Claude 3 Opus or Gemini 1.5/2.0 Pro) instantly. It details the file conventions, directory structures, dependencies, design rules, testing commands, and open scopes so that you do not waste context or compute recreating existing work.

---

## 1. Project Overview & Meta-Architecture
**Anno** is a dark-mode-first, Catholic-first, Abrahamic timeline devotional. It displays daily saints, liturgical feasts, and historical facts across multiple calendar systems, integrated with a sacred pilgrimage map and source transparency.

### Core Architecture Components
1. **Engine A (Calendar Conversion):** Non-LLM, deterministic script translating Western dates to Julian, Hebrew, Hijri, Coptic, Armenian, and Byzantine calendars.
2. **Engine B (Devotional & Saint Data Pipeline):** Catholic historical research agent output schema.
3. **Layer C (UI/UX - Native SwiftUI):** A local-data native SwiftUI shell presenting the feed.

---

## 2. Directory Structure Map

```text
anno/
├── Anno/                       # SwiftUI iOS Source-Only Scaffold Target
│   ├── AnnoApp.swift           # Application entry point
│   ├── RootView.swift           # Main tab bar navigation (Today, Calendar, Map, Saved)
│   ├── Design/                 # Brand colors, typography, styles
│   ├── Today/                  # Today feed view & sub-components
│   ├── Calendar/               # Week list calendar navigation
│   ├── Map/                    # MapKit integration & pilgrim routes list
│   ├── Saved/                  # Saved bookmarks listing
│   ├── Sources/                # Source sheet and attribution listing
│   ├── Paywall/                # Monetization display (Static stub)
│   ├── Models/                 # Data model structs (AnnoEntry, Place, etc.)
│   ├── Services/               # Local JSON fixture decoding (FixtureStore)
│   └── Resources/              # Bundled JSON mock data files
├── assets/                     # Graphic resources
│   ├── extracted/              # Programmatically cropped assets (16 files)
│   └── original-renders/       # Original design reference materials
├── data/                       # Raw source content
│   ├── mock/                   # Verified JSON mock data (Week & Fortnight)
│   ├── localization/           # Raw localization source dicts (vi_terms.json)
│   └── assets/                 # Backlog logs (Artwork clearance queue)
├── docs/                       # Technical specs & guidelines (Read before building)
├── localization/               # Xcode Localizable.strings reference files (en, vi)
├── tools/                      # Validation and generation utilities
└── visuals/                    # Interactive mocks and previews
    └── previews/               # Preview images mirroring assets/extracted/
```

---

## 3. Core Specifications & Guidelines

### Coding Conventions (SwiftUI)
* **Design Palette:** Dark mode is the absolute default. Use colors defined in [AnnoTheme.swift](file:///home/justinryan/Projects/anno/Anno/Design/AnnoTheme.swift) mapping to the brand addendum:
  * Background: Narthex (`#13110E`)
  * Surface: Choir (`#1F1B16`)
  * Accent: Gold Leaf (`#C9A84C`) / Gilt (`#D9C06E`)
* **Typography:** Display text uses `New York` (System Serif). UI controls, nav, and metadata use `SF Pro` (Sans-Serif).
* **Asset Framing:** Default to clean, modern card elements. Only apply ornate frames or capitalized initials to major solemnities. Let the artwork breathe.
* **Localization:** Supports English (EN) and Vietnamese (VI) out of the box. Ensure all labels handle dynamic text wrapping without clipping on narrow devices (e.g., iPhone SE).

### Data Conventions
* Decoded using `JSONDecoder.keyDecodingStrategy = .convertFromSnakeCase`.
* **Important Files:**
  * Master 14-day mock: [anno_fortnight_2026-07-03_2026-07-16.json](file:///home/justinryan/Projects/anno/Anno/Resources/anno_fortnight_2026-07-03_2026-07-16.json)
  * Target Schema Specs: [ANNO_CONTENT_SCHEMA.md](file:///home/justinryan/Projects/anno/docs/ANNO_CONTENT_SCHEMA.md)

### Localization Conventions
* **Files:** English [Localizable.strings](file:///home/justinryan/Projects/anno/localization/en/Localizable.strings) and Vietnamese [Localizable.strings](file:///home/justinryan/Projects/anno/localization/vi/Localizable.strings).
* **Key Prefixes:** Key names must start with a valid prefix: `app`, `tab`, `action`, `label`, `setting`, `paywall`, `onboarding`, `empty`, `accessibility`, `alert`, or `section`.
* **Dynamic Content:** Content fields from JSON (e.g., `summary`, `prayer_prompt`) contain direct translations (e.g. `summary_vi`, `prayer_prompt_vi`). Proper names/sources should remain raw.

---

## 4. Verification & Testing Commands

To prevent regressions, run the following verification pipeline before committing changes. All scripts execute in `/home/justinryan/c4ai_venv/bin/python3`.

```bash
# 1. Validate bundle layout, paths, and mechanical/blind task files
python3 tools/validate_anno_local_build.py

# 2. Check translation keys overlap, placeholders, and naming conventions
python3 tools/validate_localization.py --localization-dir localization

# 3. Validate mock content calendar mappings, bilingual fields, and sources
python3 tools/validate_mock_content.py
```

---

## 5. Visual Asset Map
The design board `assets/93FD769C-A395-4F2A-ABAD-23F9185ED015.png` contains the UI layout designs.
* Cropped individual screen states: `assets/extracted/screen_1_onboarding.png` through `screen_8_paywall.png` (mirroring onboarding, feed, calendar, map, saved, art lightbox, source sheet, and paywall).
* UI Atoms: `ui_buttons_nav.png`, `ui_icons.png`, `ui_badges_chips.png`, `ui_calendar_dots.png`, `ui_artwork_frames.png`, `ui_map_pins.png`, `ui_empty_states.png`, and `ui_illustrations.png`.
* Read [visual-design.md](file:///home/justinryan/Projects/anno/visuals/visual-design.md) for full coordinates and color breakdowns.

---

## 6. Open Development Scopes (Your Tasks)

1. **Compiling local SwiftUI target:** Add the `Anno/` directory to an Xcode project target on macOS, verify UI compilation, and capture previews checking off [IOS_PREVIEW_CHECKLIST.md](file:///home/justinryan/Projects/anno/docs/IOS_PREVIEW_CHECKLIST.md).
2. **Component Implementation:** Convert mock details in [anno-real-week-mock.html](file:///home/justinryan/Projects/anno/visuals/anno-real-week-mock.html) (like calendar grids, badge views, and custom map pins) into their native counterparts.
3. **Monetization Stubbing:** Map StoreKit 2 APIs to present the paywall stub [ArchivePaywallView.swift](file:///home/justinryan/Projects/anno/Anno/Paywall/ArchivePaywallView.swift) when attempting to browse past archives.
4. **Artwork Backlog:** Coordinate rights and metadata tagging on [artwork_clearance_queue_2026-07-03_2026-07-16.json](file:///home/justinryan/Projects/anno/data/assets/artwork_clearance_queue_2026-07-03_2026-07-16.json) following the playbook in [ARTWORK_CLEARANCE_PLAYBOOK.md](file:///home/justinryan/Projects/anno/docs/ARTWORK_CLEARANCE_PLAYBOOK.md).
