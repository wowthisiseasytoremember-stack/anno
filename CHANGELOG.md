# CHANGELOG — Anno

## [Unreleased] - 2026-08-10

### Documentation & Repository Health
- Executed orientation recovery audit and verified project state.
- Discovered and discarded a broken, uncommitted modification to `ios-fixtures/AnnoMockData.swift` that left the file in a syntactically invalid state (ending in a dangling `static let augustJSON = #`). This restores compile safety to the Swift files.
- Updated `AGENTS.md` frontmatter with `initiative: monetization` and `family: apps` to match the canonical `~/plans/initiatives.yml` mapping.
- Added "iOS Client Application" to the modules list in the `AGENTS.md` frontmatter.
- Audited the untracked August 2026 mock data batch (`data/mock/anno_august_2026.json`) and confirmed that all 31 entries are missing Vietnamese translations, setting up a clear future content generation task.

## [Unreleased] - 2026-08-09

### Documentation & Ecosystem Relationships
- Executed connection work order auditing project relationship to `content-factory`.
- Confirmed ground truth: `Anno` is a standalone monetizable native SwiftUI iOS Catholic/interfaith devotional app.
- Clarified that `Anno` does not consume from or produce into `content-factory` pipelines (keyword overlaps like `annotate_beats.py` are unrelated).
- Updated `/home/ichabod/Projects/Anno/CLAUDE.md` and `/home/ichabod/Projects/Anno/AGENTS.md` to reflect ecosystem status, shared primitives (`calendar_engine.py`), and updated timestamps.
