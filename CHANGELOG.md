# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.2.0] - 2026-10-03

### Scope & Strategy (v1 Decisions)
- **Vietnamese scope reduction**: EN-primary for all 182 days; VI only for 8 major feasts (Christmas, Easter, Pentecost, Assumption, Immaculate Conception, Divine Mercy, Christ the King, Epiphany). Removes ~174 VI translations from v1 scope.
- **Pilgrimage routes**: Reduced from 18 to 5 flagship routes (Jerusalem Via Dolorosa, Rome Seven Churches, Santiago de Compostela, La Vang Vietnam, Guadalupe Mexico). 13 routes deferred to v2.
- **Go-to-Market**: Primary channel = Vietnamese diaspora (Lang Viet parish orgs, VietCatholic media, parish priest referrals). Secondary = SEO/content marketing (Catholic calendar, pilgrimage, La Vang keywords).
- **Editorial gate**: Documented known risk — no theologian reviewer in v1; family/community validation only. LLM pipeline continues for Day 183+.
- **Content pipeline**: Engine B LLM automation continues for Day 183+ (Jan 2027+); no human review queue.

### Documentation
- **UPDATED**: `AGENTS.md` — v1 scope (5 routes, 8 feasts VI), GTM, known risks, current context
- **UPDATED**: `PRD.md` — Vietnamese scope, 5 flagship routes, GTM section added
- **UPDATED**: `ROADMAP.md` — VI reduction, 5 flagship routes, GTM phase, editorial risk
- **UPDATED**: `CHANGELOG.md` (this file)

---

## [1.1.0] - 2026-10-03

### Scope & Strategy
- **Narrowed v1 scope** to 3 core features: Calendar Engine (12 systems), GPS Pilgrimage Routes (18 routes, 106 waypoints, 72 sanctuaries), Catholic-First Devotional Content (bilingual EN/VI).
- **Removed from v1** (archived to `archive/v1-removed/`):
  - AR Reliquary (RealityKit, `ReliquaryExplorer/`, `Anno/Reliquary/`)
  - Spatial Audio Engine (`SacredSpatialAudioEngine.swift`)
  - Interfaith layer (Jewish/Islamic parallel observances beyond calendar conversions)
- **Collapsed pricing** from 3 tiers (Premium/Pilgrim/Scholar) to 2 tiers: Free + Premium **$49.99/yr**
- **Added MIT LICENSE** to repository root
- **Removed** `Anno/CLONE_FROM_KJV.md` (code confirmed original)

### Engine A — Calendar Conversion (`calendar_engine.py`)
- **FIXED**: JDN off-by-one — constant `1721424` → `1721425`
- **FIXED**: Tabular Islamic epoch 3-day error — `date(622,7,16)` → `date(622,7,19)` (Julian epoch)
- **FIXED**: Byzantine year boundary — now uses `julian_dt.month` (not Gregorian)
- **FIXED**: Syriac year boundary — now uses `julian_dt.month/year` (not Gregorian)
- **FIXED**: Armenian year boundary — uses `julian_dt`; `epoch_year` corrected `550`→`551`
- **FIXED**: Sundown timezone — uses `%Z` format (shows PST/PDT correctly); removed sinusoidal fallback (now raises `RuntimeError`)
- **OPTIMIZED**: `compute_julian_offset` — O(n) loop → closed-form `(year//100 - year//400 - 2)`
- **CLEANED**: Removed unused imports (`timezone`, `math`, `convertdate.julian`)
- **VERIFIED**: All 12 `test_calendar_engine.py` tests pass (including 2027-2030 future years)

### Engine B — Research Pipeline
- **REMOVED**: ALLOWLIST homepage URL backfill (`vatican.va/`, `newadvent.org/`) — now marks entries needing manual review if `<2` live citations
- **ADDED**: Inline source validation to `fire_engine_b.py` (reuses `_url_live()` from batch script)
- **ADDED**: Sunday/Solemnity context injection via `FEAST_NOTES_2027` dict (Jan–Jul 2027 major feasts)
- **REMOVED**: Reverse fallback in `repair_vi()` that corrupted EN fields with VI content
- **ADDED**: Vietnamese diacritics validation warning in `validate_engine_b_output.py`

### Normalization Pipeline (`tools/normalize_fixture.py`)
- **ADDED**: `normalize_generic_entry()` — applies consistent type/rank/confidence/source normalization to ALL tracks (fortnight, august, Engine B)
- **ADDED**: Blocking validator (fail-closed) before write:
  - Missing required fields: `weekday`, `calendars`, `artwork`, `mock_priority`
  - Empty `*_vi` fields (recursive scan)
  - Entries with `<2` sources
- **VERIFIED**: 182 entries, 0 empty VI fields, 0 entries with `<2` sources

### CI/CD
- **ADDED**: `.github/workflows/ios-build.yml` — GitHub Actions macOS runner for:
  - Xcode project generation (xcodegen)
  - SPM dependency resolution
  - Build + unit tests on iOS Simulator
  - Archive + unsigned IPA export on main branch push
  - Engine A calendar tests (Linux)
  - Engine B validation gate (Linux)
  - Normalization pipeline verification (Linux)

### Documentation
- **UPDATED**: `AGENTS.md` — v1 scope, pricing, known risks, current context
- **UPDATED**: `PRD.md` — v1 scope, 2-tier pricing ($49.99/yr), roadmap with removed features
- **CREATED**: `CHANGELOG.md` (this file)

---

## [1.0.0] - 2026-08-24

### Added
- Engine A: Deterministic 12-calendar conversion (pure Python)
- Engine B: LLM Catholic research pipeline with source validation
- Layer C: Devotional content generation (bilingual EN/VI)
- 182-day unified dataset (Jul 3 – Dec 31 2026)
- 18 pilgrimage routes (106 waypoints) + 72 sacred sanctuaries
- Swift fixture export for iOS integration
- StoreKit 2 configuration (original 3-tier pricing)
- AR Reliquary module (RealityKit, iOS/visionOS)
- Spatial Audio engine (monastic choir + cathedral reverb)
- Vietnamese localization (String Catalogs, structural from v1)

### Known Issues (Pre-1.1)
- Engine A calendar bugs (JDN, Islamic epoch, Julian boundaries)
- Normalization pipeline track asymmetry (fortnight/august unnormalized)
- Engine B ALLOWLIST homepage backfill
- No blocking validator (fail-open)
- AR/Spatial Audio/Interfaith in v1 scope
- 3-tier monthly pricing

---

## Legend
- **ADDED** — new features
- **FIXED** — bug fixes
- **OPTIMIZED** — performance improvements
- **REMOVED** — deleted features/code
- **UPDATED** — documentation/configuration changes
- **VERIFIED** — test validation