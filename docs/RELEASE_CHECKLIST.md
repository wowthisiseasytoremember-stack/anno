# Anno — TestFlight Release Checklist (Mac, ~30 min)

Run on a Mac with Xcode installed. This produces a TestFlight build from the already-authored
Linux artifacts. No artifact authoring happens here.

## Pre-flight (once)
- [ ] `docs/MATCH_SETUP.md` completed (certs in match repo). If certs missing, run it first.
- [ ] All GitHub Secrets from `docs/SECRETS.md` are set in the repo.

## Release steps
1. Pull latest `visual-polish` and ensure working tree is clean.
2. **VIETNAMESE SIGNOFF GATE (HARD):** confirm `docs/VIETNAMESE_REVIEW_SIGNOFF.md` exists and contains
   `vi_review_complete: true`. **Do NOT proceed to step 3 without this.** A native Vietnamese speaker
   must have reviewed all user-facing strings.
3. `cd Anno && xcodegen generate` (regenerates `Anno.xcodeproj` from `project.yml`).
4. `cd .. && bundle install` (installs fastlane from `fastlane/Gemfile`).
5. `bundle exec fastlane beta_deploy` — builds + uploads to TestFlight
   (`skip_submission: true`, `skip_waiting_for_build_processing: true`, so no App Store review is triggered).
6. In App Store Connect → TestFlight, confirm the new build appears and invite internal testers.

## If CI is used instead of local
- Tag `v0.0.0-dryrun` → push → `ios-release.yml` runs `beta_validate` (build only, no upload).
- Tag `v1.0.0` → push → `ios-release.yml` runs `beta_deploy` + `test:storekit` job.

## Rollback
- TestFlight builds are immutable; to pull a bad build, expire it in App Store Connect → TestFlight.
