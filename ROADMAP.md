# Interfaith Devotional Engine — ROADMAP.md
**Last updated:** 2026-10-03

## Phase 0: Canonical Truth Reconciliation
- [x] Create `ARCHITECTURE.md`
- [x] Create Catholic-first native iOS product bible
- [x] Create asset prompts, rubric, monetization system, and flagship content slate
- [x] Import Engine A artifacts from infrastructure bundle into project (reconciled; 3 bug fixes applied to infra copy)
- [x] Set working project name: Anno

## Phase 1: Native iOS Scaffold
- [ ] Create SwiftUI app project  **[MAC-BLOCKED — see docs/NATIVE_BUILD_RUNBOOK.md]**
- [ ] Add StoreKit 2 subscription scaffolding (Free + Premium $49.99/yr)  **[MAC-BLOCKED]**
- [ ] Add MapKit sacred-place view shell (5 flagship routes)  **[MAC-BLOCKED]**
- [ ] Add Xcode String Catalogs for English and Vietnamese UI strings (VI for key feasts only)  **[MAC-BLOCKED]**
- [x] Add local content/cache model with localized fields (LocalizedEntryText, LanguageMode)
- [x] Add Swift fixture export from verified mock JSON (re-pointed at anno_unified_2026.json)

## Phase 2: Engine A — Calendar Engine
- [x] Calendar conversion script for 10+ systems exists in infrastructure bundle
- [x] 4-year JSONL generation exists in infrastructure bundle
- [x] Import Engine A artifacts into canonical project — reconciled (bugs fixed in both copies)
- [x] Spot-check validation against known dates and local sundown cases (12 tests pass)
- [x] Bug fixes: JDN, Islamic epoch, Julian boundaries (Byzantine/Syriac/Armenian), PDT/PST, O(1) offset

## Phase 3: Engine B — Catholic-First Research Agent
- [x] Daily research prompt (`docs/research/anno-research-prompt-main.md`)
- [x] Catholic saint/feast/history pipeline (`tools/fire_engine_b.py` + batch script)
- [x] JSON output schema (single-entry result files in `data/research_results/`)
- [x] Source/confidence validator (`tools/validate_engine_b_output.py`)
- [x] Inline source validation (`fire_engine_b.py`) — ALLOWLIST backfill removed
- [x] Sunday/Solemnity context injection (`FEAST_NOTES_2027`)
- [x] Diacritics validation warning
- [x] Repair_vi reverse fallback removed
- [ ] Continue LLM pipeline for Day 183+ (Jan 2027+) — automated cron

## Phase 4: Layer C — User-Facing Content
- [x] Engine B research prompt written
- [x] Source validation gate script written
- [x] July 17-30 batch fired + complete (14 dates)
- [x] August 2026 VN (217 fields) + Engine B 07-17→07-30 complete; unified into `anno_unified_2026.json` (182 entries)
- [x] Normalization pipeline fail-closed (missing weekday/calendars/artwork/mock_priority, empty *_vi, <2 sources)
- [ ] **VI scope reduction**: Keep EN-primary for all 182 days; VI only for 8 major feasts (Christmas, Easter, Pentecost, Assumption, Immaculate Conception, Divine Mercy, Christ the King, Epiphany)
- [ ] **Pilgrimage routes**: Reduce from 18 to 5 flagship (Jerusalem Via Dolorosa, Rome Seven Churches, Santiago de Compostela, La Vang Vietnam, Guadalupe Mexico)

## Phase 4.5: Layer D — Devotional Engine (Cloned from KJV App)
- [x] Import AnnoDevotionalLoader.swift — deterministic date rotation
- [x] Import DevotionalProvider.swift — pool management
- [x] Import Bookmark.swift + BookmarkActions.swift — SwiftData persistence
- [x] Import GlassCard, ShareCard, ShareableImage, VerseActionBar — UI components
- [x] Import Haptics, SearchHistory, NotificationService — service wrappers
- [ ] Wire devotional engine into app (RootView / TodayView integration) **[MAC-BLOCKED]**
- [ ] Adapt VerseActionBar palette to AnnoTheme **[MAC-BLOCKED]**
- [ ] Produce Catholic devotional JSON (VI for key feasts only)
- [ ] Vietnamese translation pass for key feasts only (8 feasts)

## Phase 5: UI/UX and Monetization
- [x] Expandable calendars — collapsible extra calendar systems
- [x] Skeleton loaders — shimmer animation for loading state
- [x] Colorblind-safe pins — icon overlays on tradition dots
- [x] Sundown anchor banner — GPS-based location note
- [x] Audio narration buttons — on all 3 event cards
- [x] Map bottom sheet — 7-day pilgrimage site window with pins
- [x] Bookmark micro-feedback — gold fill + toast
- [x] Reduced motion guard — global prefers-reduced-motion
- [x] Focus-visible states — gold outline on all interactive
- [ ] Confidence badges — confirmed/traditional/disputed pills
- [ ] Translate mockup patterns into native SwiftUI components **[MAC-BLOCKED]**
- [ ] Free + Premium $49.99/yr paywall (StoreKit 2) **[MAC-BLOCKED]**
- [ ] 5 flagship route pack (offline MapKit) **[MAC-BLOCKED]**
- [x] Privacy-safe monetization trust spec
- [x] PrivacyInfo.xcprivacy created
- [x] Privacy policy written
- [x] App Store metadata template written

## Phase 6: Go-to-Market (v1)
- [ ] Family/community beta (EN + key feasts VI) → testimonials
- [ ] Vietnamese diaspora outreach: Lang Viet parish orgs, VietCatholic media, diaspora priests
- [ ] Catholic podcast/YouTube guest appearances
- [ ] App Store optimization (keywords: Catholic calendar, pilgrimage, La Vang, Vietnamese Catholic)
- [ ] **Editorial gate**: Documented known risk — no theologian reviewer; family/community validation only. Revisit pre-v2.

## Changelog

- 2026-10-03: v1 scope decisions — VI reduction (EN-primary + 8 key feasts VI), 5 flagship pilgrimage routes, Vietnamese diaspora GTM, LLM pipeline continuation, editorial risk documented.
- 2026-08-19: August 2026 VN complete (217 fields). Engine B 07-17→07-30 complete (14 dates, 14 VN siblings). Three content tracks normalized into `anno_unified_2026.json`; `AnnoMockData.swift` regenerated. Validator fixed for single-entry shape.
- 2026-07-10: Engine A fully reconciled. Privacy compliance files created. Source validation gate written. Research prompts for Engine B written. MMR-ingested execution plan written. Week fixture fixed. Stale infra path fixed in AGENTS.md.
- 2026-07-04: Sprint 1 localization complete — asset boards A/B/C, pseudo-localize tool, component rules, design brief updates. Sprint 2.1 complete — LocalizationManager (Swift), unit tests, strings validator, English .strings reference.
- 2026-07-03: Reframed roadmap around native SwiftUI, Catholic-first launch, Vietnamese localization, and artifact reconciliation.
