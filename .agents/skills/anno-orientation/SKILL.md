---
name: anno-orientation
description: >-
  Runbook for project orientation recovery, Samba case-collision detection,
  and planning document consolidation in the Anno workspace.
---

# Anno Orientation Recovery Runbook

Use this skill when starting a new session on the Anno project, recovering context, or verifying repository integrity.

---

## 1. Verify Canonical Environment (Server vs. Client)

Always verify repository status directly on the Linux server (`ichabod`) rather than relying solely on the client terminal (Windows `surfacebook`).

1. **Check Git Status on Server:** Run `git status` over SSH on the server.
2. **Ignore Client Deletion Mismatches:** If Git status on the client (Windows/Samba) lists dozens of deleted documentation files (e.g. under `docs/`) that are *not* shown as deleted on the server, this is a **Samba Case-Insensitivity Collision**.
   * **Why it happens:** The repository contains both a `/Docs` (uppercase, app store metadata) and `/docs` (lowercase, design specs) folder. Windows merges these case-insensitively, hiding one of the directories and falsely reporting its files as deleted.
   * **Rule:** Do NOT stage, commit, or discard these deletions from the Windows side. Perform all staging and git operations directly on the Linux server (`ichabod`).

---

## 2. Verify Swift Fixture Integrity

Interrupted export scripts or manual edits can leave Swift fixture files in a corrupted state.

1. **Check file endings:** Inspect `ios-fixtures/AnnoMockData.swift` and ensure it ends with valid Swift closures/extensions, not dangling fragments like `static let augustJSON = #`.
2. **Restore clean state:** If corrupted, run `git restore ios-fixtures/AnnoMockData.swift` directly on the server to discard uncommitted, half-written files and restore build compilation safety.
3. **Verify content:** Check untracked content batches (such as `data/mock/anno_august_2026.json`) and verify that all bilingual localization fields are populated. Flag empty Vietnamese strings (`title_vi`, `summary_vi`, `body_vi`) as outstanding content generation tasks.

---

## 3. Project Metadata and Taxonomy Alignment

1. **Validate AGENTS.md:** Ensure `AGENTS.md` contains valid `agents-md/v1` frontmatter.
2. **Taxiomy keys:** Ensure the frontmatter maps correctly to the canonical initiative taxonomy in `~/plans/initiatives.yml`:
   ```yaml
   initiative: monetization
   family: apps
   project: Anno
   ```
3. **Run Validation:** Run the frontmatter validation script on the server to ensure compliance:
   ```bash
   python3 ~/Projects/icc-hearth-v5/scripts/validate_agents_frontmatter.py ~/Projects/Anno/AGENTS.md
   ```

---

## 4. Planning Document Consolidation

To prevent documentation sprawl and conflicting roadmaps, maintain the following hierarchy:

*   **ROADMAP.md:** High-level roadmap tracking phases and checkboxes.
*   **MVP_PLAN_FINAL.md:** The active, single source of truth for the TestFlight MVP scope (with cut features like Maps and Paywalls documented).
*   **STATE.md:** Active session state, next tasks, and frontier artifacts.
*   **docs/archive/:** Move stale draft plans (e.g., `MVP_PLAN.md`, `MVP_PLAN_V2.md`) and outdated site-survey plans here to keep the root directory clean.
