# Anno — Finish, Merge, Publish, Move Forward (execution plan)

**Created:** 2026-11-19
**Status:** proposed, awaiting operator go
**Repo:** `/home/ichabod/Projects/anno` — `main` @ `24771cc`, clean, == `origin/main`
**Builds on:** `/home/ichabod/.opencode/plan/anno-liturgical-truth-20261119.md` (v2, 326 lines) — that plan stays the
**technical specification**; this file is the **sequencing, correction, and merge/publish layer** and overrides it where the two disagree.

---

## 1. What the last session actually produced, and what three audits found

The last session did **no repo work** (verified: `grep -rl 'liturgical_groundtruth_2027|apply_liturgical_groundtruth|ferial_composer|vi_status|liturgical_status'`
over `*.py/*.swift/*.json/*.yml` → **zero hits**; `git status` clean; no open PRs). Its deliverable was the 326-line plan plus a
failed MMR attempt (0/8 responses) that it correctly substituted with two yolo-auto reviews.

I ran **three read-only yolo-auto audits** against the plan and the repo: (A) plan executability, (B) defect-claim fact-check,
(C) merge/publish readiness. Findings that change this plan:

### 1.1 Corrections to the technical plan (B)

| Plan says | Reality | Impact |
|---|---|---|
| Epiphany **missing entirely** | **Misdated**: fixture pins Epiphany at `2027-01-06` (Feast/white) with `title_vi: "Chúa Nhật Lễ Chúa Hiển Linh"`; USCCB puts it on Sunday `2027-01-03`. Only **Baptism of the Lord** is title-absent (no entry anywhere carries a "Baptism" title) | Phase 0 expected-defect list must count Epiphany as *misdated*, and Phase 3 must handle a **date move**, not just a field overwrite |
| ~227 post-repair ferial days | **234** (240 Feria − the 6 Feria-ranked Sundays; the 6 Memorial + 1 OM Sundays were never in the Feria count) | Phase 6 scope, and R7's "~62%" figure |
| **157** entries cite the `newadvent.org/cathen/` homepage | **79** exact / 83 slash-tolerant (research corpus and fixture agree) | Phase 5b is ~half the assumed work |
| 147 warnings = 129 source-URL + 11 + 4 + 3 misc | 147 total is exact: **132** source-URL (91 newadvent / 25 vatican / 16 pattern) + 11 + 4. There is no separate 3-warning class | Phase 5a scope is 132, not 129+3 |
| 240 ferial days are shared **template** text ("This date marks a Thursday…") | That template appears **4× in the whole file** and **0× in any of the 240 Feria `body_en` fields** — the bodies are individually LLM-written | The quoted evidence is invalid; the *thinness* conclusion still stands and Phase 6 is still justified, but the PR must not repeat the template claim |
| — | **New defect class the plan missed:** EN/VI weekday disagreement (`2027-01-13` EN says Wednesday, VI says *thứ Ba* / Tuesday) | Added to Phase 0 measurement and to Phase 3 (deterministic, Engine-A-derived fix) |
| — | **`primary` block contradicts the `liturgical` block** on `2027-08-29` (`primary.title_en` = "19th Sunday in Ordinary Time (Year C)" vs `liturgical.title_en` = "The Passion of St. John the Baptist") | Phase 3's overwrite must cover `primary.{title_en,type}` too, not only `liturgical.*` |

### 1.2 Executability fixes (A)

1. **Wrong exceptions filename.** Plan says `data/liturgical_exceptions_<year>.json`; the tool reads
   `data/editorial_exceptions_{year}.json` (`all_days_editorial.py:36`). Use the real name or Phase 2 maintains a file nothing reads.
2. **`audit --year 2027` hard-fails today** (`rc=1`, `missing ground truth data/liturgical_groundtruth_2027.json`). Phase 1 must land first;
   any gate run before it is a false alarm. Also, `audit` is **not write-free** — it writes `build/audit_*.json` and `docs/AUDIT_{year}_REMAINING_DAYS.md`,
   which violates Phase 0's "nothing written outside `build/usccb_cache`" guard if run during the spike.
3. **Ground-truth row schema is 13 fields, not 11** — the plan omits `celebration_id` and `disambiguation_tokens`. Phase 7's round-trip test must assert those too.
4. Everything else checks out: `parse_usccb_calendar.py --fetch --year N` → `data/liturgical_groundtruth_<year>.json`; both PDFs return `HTTP 200`;
   `pdftotext` present; `--fixture` genuinely absent from the audit tool (as the plan assumes); all four verification-gate commands run;
   `normalize_fixture --year 2027 --out …` is **byte-identical** to the committed fixture; `pytest tools -q` = **53 passed**;
   `CYA-GOAL:`/`CYA-EVIDENCE:` commit trailers are enforced by `core.hooksPath → cya-gate`.

### 1.3 Merge/publish reality (C)

- **No unrecovered work.** All 8 local branches (`docs/reconcile-20261119`, `feat/2027-*`, `feat/2028-pilot`, `feat/audit-tooling-20261116`,
  `feat/engine-b-2027-gap`) are **squash-merge residue** — `git diff --diff-filter=A origin/main..<branch>` shows zero branch-only files.
  **Delete nothing** (no ref deletions without a per-ref operator verdict); this is tidiness, not recovery.
- **CI is green** (10/10 recent runs success). Blocking: Engine A tests, Engine B validation, 2026 liturgical audit (fail-closed),
  normalization + route integrity, Swift decode gates. **Advisory already exists**: `continue-on-error: true` on the 2027 validator (ios-build.yml L163/L170).
  `native-build` and `field-marker-kit` are `workflow_dispatch` only — **skipped in every run; the app has never compiled in CI.**
- **"Publish" = cut a semver tag** → `ios-release.yml` → macOS runner → `fastlane beta_deploy`. Only tag ever cut: `v0.0.0-dryrun`; no GitHub Releases.
  GitHub Pages is an orphan `gh-pages` branch holding only the privacy policy — independent, green, untouched by this plan.
- Open issues: **#40** is the lane tracker (3 of its items already closed by #45–#48, re-verify then close); **#10** (`repair_vi` corrupts EN with VI) sits
  **inside Phase 3's driver blast radius**; **#24** closes when coverage claims are re-posted; #50/#33 explicitly out of scope.

---

## 2. Operator decisions (locked, 2026-11-19)

| Decision | Choice |
|---|---|
| PR shape | **Never one giant PR.** Eight small PRs, each independently gated and revertable. |
| `title_vi` source | **Bootstrap + LLM for gaps, both provenance-tagged.** Derive `data/liturgical_vi_lexicon.json` from the fixture's existing `title_vi` + seed `title_vi` aligned to ground-truth rows; days whose identity changed get a yolo-auto draft marked `vi_source: "llm-draft"`, `vi_status: "pending-review"`. Never a silent null, never an unattributed invention. |
| Publish this cycle | **Merge to main + docs, dispatch `native-build` once, defer the tag.** Cut `v0.1.0` only if that first-ever compile succeeds (separate decision). |
| CI on 2027 audit | Advisory only, `continue-on-error: true` (unchanged from the technical plan). |
| Branches/refs | No deletion of any kind this cycle. |
| Execution workspace | **Sequential, main checkout, feature branches in place.** Disk: **23 GiB free / 90% used, `~/DISK-WARNING.txt` present (warn line 30 GiB)**. Read `~/wiki/concepts/disk-and-memory-pressure-runbook.md` first. No worktrees, never `/tmp` (use `/tmp/opencode`). |

---

## 3. Execution — eight PRs

Each PR: claim the issue first, own only its listed files, every commit carries `CYA-GOAL:`/`CYA-EVIDENCE:` trailers,
`python3 -m pytest tools -q` green before push, squash-merge on green, **no branch deletion after merge**.

| PR | Lane | Owns | Depends on | Gate to merge |
|---|---|---|---|---|
| **A** | Pin ground truth + measure | `tools/parse_usccb_calendar.py`, `data/liturgical_groundtruth_2027.json`, `_2028.json`, `build/` | — | 365+365 rows, sha intact, spot-check recorded |
| **B** | Year-aware advisory audit | `tools/all_days_editorial.py`, `.github/workflows/ios-build.yml` | A | `audit --year 2026` still green; new 2027 step advisory |
| **C** | Repair tooling + dry-run diff | `tools/apply_liturgical_groundtruth.py`, `data/liturgical_vi_lexicon.json`, `build/` | A | diff artifact committed, **no data file changed** |
| **D** | Identity overwrite (the risky one) | `data/research_results/2027-*`, `tools/batch_engine_b_2027_gap.py`, `Anno/Resources/anno_unified_2027.json(+.meta)` | C + **operator approval of C's diff** | all six verification gates |
| **E** | Subject-mismatch prose regen | the ~15 `data/research_results/2027-0*-result.json` on the mismatch list, fixture regen | D | programmatic GT match + operator spot-check |
| **F** | Citations + confidence | `tools/validate_engine_b_output.py`, driver, 2027 research sources | D | 0 errors; warning classes 5a/5d/5e cleared |
| **G** | Ferial composer (234 days) | `tools/ferial_composer.py`, 2027 research ferial days, fixture regen | D | min-content assertion + byte-stable regen |
| **H** | Guards + docs + deferred tasks | `tools/test_json_roundtrip_fields.py`, `tools/preflight_sample.py`, workflow, `AGENTS.md`, `CHANGELOG.md`, `STATE.md` | B–G | pytest, round-trip pass, doc grep |

Optional parallelism once A lands: **B ∥ C** (file-disjoint). Everything else is sequential — D is the single ordering spine.

### PR A — Pin 2027 + 2028 ground truth and publish the real defect list

1. `python3 tools/parse_usccb_calendar.py --fetch --year 2027` then `--year 2027`; same for 2028. Both PDFs already verified reachable.
2. **Abort** if row count ≠ 365/366 or any date duplicates. Add `jurisdiction: "United States (USCCB)"` to both headers (new parser code).
3. **Do not hand-edit any parsed row.** If parsing fails, fix the parser.
4. Spot-check 10 rows against the PDF by eye; record which 10 in the commit message.
5. **Phase 0 measurement**, written to `build/` only (not the editorial tool — see §1.2(2)), diffing all 365 fixture days vs ground truth on
   `rank`/`color`/`title_en`/`readings` **plus the four measurements the old plan missed**:
   `primary`-vs-`liturgical` block disagreements; EN/VI weekday mismatches; days where `title_vi`'s identity no longer matches the English
   ground truth (this becomes the VI lexicon worklist); the exact misdated-date list (Epiphany Jan 6 → Jan 3).
6. Publish the defect list as a comment on **#40** (claim it as this lane's tracker) and reference it in the PR body.
   Expected: 13 misranked Sundays, 1 misdated Solemnity, 1 missing Feast, N name/color drifts, plus the two new classes.

### PR B — Make the editorial audit year-aware (advisory)

- Year-aware `source_file_for()` (2027/2028 → `data/research_results/<date>_result.json`); **2026 mock tracks stay 2026-only**.
- Add `--fixture PATH` **defaulting to the 2026 fixture**, so today's green CI cannot break early (`FIXTURE_DEFAULT` already exists unused at L34).
- Add `GT-MISSING-FEAST` hard-fail (a Solemnity/Feast absent or carried at lower rank is an error, not a warning) — in-tool assertion only, CI behaviour unchanged.
- Exceptions mechanism keeps using the **real** filename `data/editorial_exceptions_{year}.json`.
- Add the EN/VI weekday check as an S1 finding (deterministic, Engine-A weekday as the reference).
- CI: add `audit --year 2027` as `continue-on-error: true` with `build/audit_2027.json` + the `docs/AUDIT_2027_*` report uploaded as artifacts;
  also upload the **2028 January pin-vs-truth diff** so pinned-but-unrepaired 2028 reads as a known gap, not a promise.

### PR C — Repair tooling, VI lexicon, and the committed dry-run diff (rollback boundary)

New `tools/apply_liturgical_groundtruth.py`, **in this order**:

1. Snapshot `build/liturgical_identity_snapshot.sha256` over all 365 research files.
2. `--dry-run` → `build/liturgical_identity_diff.md`; **commit it and stop**. No research or fixture file is touched in this PR.
3. Build `data/liturgical_vi_lexicon.json`:
   - bootstrap every day from fixture `title_vi`, falling back to seed `title_vi`, keyed to the ground-truth row;
   - classify `vi_source: "fixture" | "seed" | "llm-draft" | "none"` and `vi_status: "verified" | "pending-review" | "pending"`;
   - days on the PR A identity-changed list get a **yolo-auto draft** (concurrency ≤ 2, `timeout`-wrapped) with `vi_source: "llm-draft"`,
     `vi_status: "pending-review"` — reviewed in PR D's spot-check, never silently trusted;
   - a true miss writes `title_vi: null` + `vi_status: "pending"` + `vi_source: "none"` (visible, never invented).
4. `--dry-run` output must enumerate: identity overwrites, `primary` block fixes, EN/VI weekday fixes, VI lexicon hits/misses, and
   `build/liturgical_subject_mismatch.json` (expected: `2027-01-03`, `2027-01-06`, `2027-01-11`, + the 11 remaining wrongly-ranked Sundays).

**Hard gate:** operator reads `build/liturgical_identity_diff.md` and approves before PR D exists.

### PR D — The 365-file identity overwrite (highest risk in this plan)

- Apply the dry-run exactly: `liturgical.{rank,color,title_en}` **and `primary.{title_en,type}`**, `title_vi` from the lexicon, plus grounded
  `readings`, `psalter_week`, `season`, `week`, `holyday_of_obligation`; EN/VI weekday corrected from Engine A.
- **Date moves are data moves:** Epiphany `2027-01-06 → 2027-01-03`, Baptism of the Lord placed per ground truth. Each moved day's prose
  becomes a subject-mismatch case for PR E; the vacated date gets a correct ferial identity.
- Harden `tools/batch_engine_b_2027_gap.py`: stop using the seed as liturgical authority (`seed_context()` becomes free-text context only);
  write-time assertion over the **whole** identity block (`rank`/`color`/`title_en`/`title_vi`/`readings`/`psalter_week`) raising `RuntimeError`;
  docstring rule that **any** tool writing `_result.json` carries the same assertion. **Claim #10 here** — audit `repair_vi` and fix its EN/VI
  reverse-fallback corruption while this file is open.
- Regenerate the fixture, then run **all six verification gates** (normalize must run *before* the `cmp`):
  ```
  python3 tools/normalize_fixture.py --year 2027 --out /tmp/opencode/regen.json
  cmp Anno/Resources/anno_unified_2027.json /tmp/opencode/regen.json
  python3 tools/validate_fixture_decode.py --fixture Anno/Resources/anno_unified_2027.json
  python3 tools/validate_fixture_freshness.py --year 2027
  python3 tools/validate_engine_b_output.py --fixture Anno/Resources/anno_unified_2027.json
  python3 tools/all_days_editorial.py audit --year 2027
  python3 -m pytest tools -q
  ```
- PR body: every changed day listed with its ground-truth row. Verify `git revert` of the overwrite commit restores the exact prior state on one file before merging.

### PR E — Regenerate subject-mismatch prose only

- Driver over the mismatch list with ground truth injected. **Programmatic validation before write** on `rank`/`color`/`title_en`/`readings`;
  mismatch ⇒ reject and re-queue. Operator spot-check is the *additional* step, not the only gate.
- Batch small, concurrency ≤ 2, `timeout`-wrapped, long batches backgrounded. Every regenerated day + its ground-truth row listed in the PR.

### PR F — Citations and confidence

- **5a** Derive `source.type` from URL host (driver + backfill over all 365): clears **132** warnings (91/25/16).
- **5b** Replace the **79** homepage citations with date-specific `https://bible.usccb.org/bible/readings/MMDDYY.cfm` first, pinned calendar PDF for
  liturgical context, per-saint article only where deterministically derivable.
- **5c** Keep `confidence` as the *historical/prose* signal; add `liturgical_source: "usccb_<year>"` + `liturgical_status: "authoritative"`;
  **change the validator rule** so it never infers confidence from rank; it instead warns when the `liturgical` block disagrees with ground truth.
  File the deferred Swift task (relabel UI indicator to "Historical certainty", surface `liturgical_status` separately) as a new issue — no Swift edits here.
- **5d** Fix the 4 `confidence_note_vi` entries lacking diacritics.
- **5e** After 5b lands, add a class-based check to `tools/validate_engine_b_output.py` rejecting section-index pages (path depth ≤ 1, no slug), not a URL allowlist.

### PR G — Deterministic ferial composer (234 days)

- New `tools/ferial_composer.py`, strategies `deterministic_v1` (now) and `llm_v1` (reserved, documented in the module docstring).
- Per day: identity + psalter week + real readings citation + **one substantive sentence drawn from the cited passage** + explicit
  "no proper memorial today", EN + VI with diacritics. Tag `ferial_composer: "deterministic_v1"`.
- **Minimum-content assertion:** readings citation, psalter week, season sentence, EN body ≥ 25 words; reject schema-valid but empty.
- **Never fabricate antiphons, collects, or prayers** — absent means absent.
- Deterministic: same input ⇒ byte-identical output. Scope = the **234** post-repair Feria days, not the old 227/240 figures.

### PR H — Guards, docs, deferred tasks

1. `tools/test_json_roundtrip_fields.py` — `ferial_composer`, `holyday_of_obligation`, `psalter_week`, `season`, `week`, `readings`,
   `liturgical_source`, `liturgical_status`, `vi_status`, **and the two ground-truth fields the old plan omitted** (`celebration_id`,
   `disambiguation_tokens`) survive load → dump → load through `normalize_fixture.py`.
2. `tools/preflight_sample.py --year 2027 --days 3` — schema → Swift decode → freshness → editorial → citation quality; opt-in, **not** wired into CI.
3. `AGENTS.md` / `CHANGELOG.md` / `STATE.md`: seed is not a liturgical authority; ground-truth files + sha provenance; **US jurisdiction scope**;
   `ferial_composer` strategy and how to add `llm_v1`; the deferred Swift confidence-label task. PR body states
   `liturgical_status: authoritative` means "matches the official USCCB calendar", **not** "theologically reviewed".
4. Repost coverage on **#24**; when A–H are green, close **#40** (and **#10** with it).

---

## 4. Publish lane (after PR H merges)

1. Re-run the six verification gates **once more on merged `main`**.
2. **Dispatch `native-build` via `workflow_dispatch`** — the first-ever compile of this app in CI (it has been `skipped` in all 10 recent runs).
   Success ⇒ evidence for **#38/#18**; failure ⇒ capture the log, file/append on #38, and stop here.
3. Docs already updated by PR H; GitHub Pages privacy policy untouched.
4. **Tag `v0.1.0` is deferred** — a separate operator decision made only if step 2 succeeds. Nothing tags otherwise.
5. Report completion per policy: scope, changes, validation evidence, anything left unverified, external state changed (CI dispatch only).

---

## 5. Risks carried forward

- **R-disk:** 23 GiB free, 90% used, `~/DISK-WARNING.txt` live (warn 30 GiB). Read the runbook before starting; sequential main-checkout work only;
  every generated artifact goes to `build/` or `/tmp/opencode`; no worktrees, no clones, no `/tmp` checkouts.
- **R-overwrite:** PR D is the one genuinely dangerous commit (365 files + fixture). Mitigated by the snapshot manifest, the committed dry-run diff in C,
  the operator gate between C and D, and a verified single-file `git revert`.
- **R-VI:** bootstrap covers most days; the identity-changed days depend on yolo drafts marked `pending-review`. "Visible but pending" still ships —
  **somebody must review the drafts**; no owner assigned yet. This remains the most likely thing to be quietly skipped.
- **R-thinness:** 234 ferial days (~64%) stay correct-but-thin after PR G. `ferial_composer` tag keeps `llm_v1` cheap later. Do not repeat the
  invalidated "template text" claim in any PR body.
- **R-advisory CI:** the 2027 audit cannot block regressions. The real guards are write-time assertions (D), `GT-MISSING-FEAST` (B), the citation
  class check (F), and the round-trip test (H). File the scheduled USCCB-sha drift alarm as an issue; do not build it here.
- **R-jurisdiction:** USCCB is a **US proper** calendar; the app targets a Vietnamese diaspora audience. Nothing here resolves that — every PR must say so.

## 6. Out of scope

Native/iOS build beyond the single dispatch proof (#33), Swift confidence-label and multi-year loader patches (defer issues only), 2028 full-year
generation/repair (#50), artwork rights, any branch/ref deletion, any tag cut, GitHub Pages changes.

---

## 7. Audit brief — for the external/cloud reviewer

**You are being asked to audit this plan before it executes.** You may have only the GitHub API (no local checkout). Everything you need is in this
document; the repo is `wowthisiseasytoremember-stack/anno`, default branch `main` @ `24771cc`, CI ("Anno CI") currently green.

**Provenance of this plan:** it was built by an agent that ran three read-only yolo-auto audits of an earlier 326-line technical plan
(`anno-liturgical-truth-20261119.md`): (A) executability of every command/path, (B) fact-check of every quantitative claim against the fixture,
(C) merge/publish readiness. Audit B produced six corrections, audit A produced four fixes — all are already folded into §1 of this document.
An earlier attempt to get 5-model MMR consensus returned 0/8 responses (provider auth/cooldown failures), so **this plan has had no independent
review beyond those self-audits. That is why you are reading it.**

Answer as directly as you can, and say "no finding" where you have none. Number your answers to match.

1. **Sequencing.** Are the eight PRs ordered correctly? Is anything marked sequential that could safely run in parallel (or vice versa)?
   Specifically: is it right that only B ∥ C may overlap, and that D is the single ordering spine?
2. **PR D rollback.** The plan accepts a single 365-file identity overwrite as the one dangerous commit, guarded by a snapshot manifest, a committed
   dry-run diff, an operator gate, and a verified single-file `git revert`. Is that sufficient, or should the overwrite be split (by field, by month,
   or by defect class)? What is the realistic failure mode that guard set does *not* cover?
3. **Missed defect classes.** Given the fixture shape (duplicated `primary` and `liturgical` title blocks, `_result.json` + `_result_vi.json` sidecars,
   five Engine A calendar strings per entry, 13-field ground-truth rows), what else should Phase 0 measure that the plan does not list?
4. **Vietnamese titles.** The chosen approach bootstraps `title_vi` from the existing fixture + seed and uses yolo-auto drafts for
   identity-changed days, provenance-tagged (`fixture`/`seed`/`llm-draft`/`none`). Is there an authoritative Vietnamese liturgical source we have
   overlooked (Vatican-approved VI translations, Vietnamese diocesan calendars, existing VI missals) that would make the LLM-draft step unnecessary?
5. **Claim discipline.** `liturgical_status: "authoritative"` plus a `jurisdiction: "United States (USCCB)"` header is meant to mean "matches the US
   calendar", not "universally correct" or "theologically reviewed". Is that enough to keep app-facing copy, App Store metadata, and future agents
   from over-claiming? What wording would you require in the PR bodies?
6. **Ferial content.** 234 days (~64%) get deterministic readings-forward text under a ≥25-word minimum-content assertion, tagged
   `ferial_composer: "deterministic_v1"`. Is that floor meaningful, and is deferring `llm_v1` the right call for a devotional product?
7. **Publish lane.** Deferring the `v0.1.0` tag until one `workflow_dispatch` of the never-yet-run `native-build` job succeeds — is anything else
   required first (code signing, `fastlane match_appstore`, StoreKit config, entitlements) that this plan does not anticipate?
8. **Advisory CI.** The 2027 editorial audit stays `continue-on-error: true` (operator-locked). The plan leans on four write-time guards instead.
   Are those guards actually fail-closed, or is there a path where bad liturgical data reaches the fixture without any gate firing?
9. **Scope.** What in these eight PRs is scope creep you would cut, and what is missing to honestly claim "finished, merged, published, advanced"?
10. **Verdict.** `EXECUTE AS WRITTEN` / `EXECUTE WITH CHANGES` (list them) / `DO NOT EXECUTE` (why).

**Do not** soften a finding to be agreeable. A wrong number, an unreachable command, a guard that does not actually fail closed, or an over-claim in
the publish lane is exactly what this review exists to catch.
