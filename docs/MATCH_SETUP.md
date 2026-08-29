# Anno — Fastlane Match Setup (Mac session)

One-time certificate/profile generation. Requires a Mac with Xcode + the Apple ID that owns the
`org.anno.Anno` app. Run this BEFORE the first `beta_deploy`. Everything else in the release plan
is `readonly: true` (safe, non-writing) — only this step writes certs.

## Steps

```bash
# 1. Install fastlane (if not present)
brew install fastlane

# 2. Initialize match — point at your private cert repo
fastlane match init
#   - storage_mode: git
#   - git_url: <your private match repo>

# 3. Generate App Store distribution cert + profile (writes to match repo)
fastlane match appstore

# 4. Generate development cert + profile (for device debugging)
fastlane match development

# 5. Verify read-only mode works (this is what CI uses — must succeed without writing)
fastlane match appstore --readonly
fastlane match development --readonly
```

## Notes
- The `MATCH_WRITE` guard in the Fastfile blocks `match_appstore` / `match_development` lanes unless
  you explicitly run `MATCH_WRITE=1 fastlane match_appstore`. Default CI behavior is read-only.
- After this runs once, future builds only need `MATCH_PASSWORD` + `MATCH_GIT_URL` to *read* certs.
- If certs already exist in the match repo, **skip steps 3–4** and only run step 5 to verify.
