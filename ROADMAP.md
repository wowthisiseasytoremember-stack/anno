# Interfaith Devotional Engine — ROADMAP.md
**Last updated:** 2026-07-04

## Phase 0: Canonical Truth Reconciliation
- [x] Create `ARCHITECTURE.md`
- [x] Create Catholic-first native iOS product bible
- [x] Create asset prompts, rubric, monetization system, and flagship content slate
- [x] Import Engine A artifacts from infrastructure bundle into project (reconciled; 3 bug fixes applied to infra copy)
- [x] Set working project name: Anno

## Phase 1: Native iOS Scaffold
- [ ] Create SwiftUI app project
- [ ] Add StoreKit 2 subscription scaffolding
- [ ] Add MapKit sacred-place view shell
- [ ] Add Xcode String Catalogs for English and Vietnamese UI strings
- [ ] Add local content/cache model with localized fields
- [x] Add Swift fixture export from verified mock JSON

## Phase 2: Engine A — Calendar Engine
- [x] Calendar conversion script for 10+ systems exists in infrastructure bundle
- [x] 4-year JSONL generation exists in infrastructure bundle
- [x] Import Engine A artifacts into canonical project — reconciled (bugs fixed in both copies)
- [ ] Spot-check validation against known dates and local sundown cases (carry to Sprint D)

## Phase 3: Engine B — Catholic-First Research Agent
- [ ] Daily research prompt
- [ ] Catholic saint/feast/history pipeline
- [ ] Optional Sacred Context pipeline only where genuine
- [ ] JSON output schema
- [ ] Source/confidence validator
- [x] Add mock content schema for first native fixture slice

## Phase 4: Layer C — User-Facing Content
- [x] Engine B research prompt written (at `docs/research/anno-research-prompt-main.md`)
- [x] Source validation gate script written (`tools/validate_engine_b_output.py`)
- [x] July 17-30 batch ready to fire (`docs/research/anno-research-batch-july17-30.md`)
- [ ] 10 flagship entries from `docs/FLAGSHIP_CONTENT_SLATE.md`
- [ ] Vietnamese translation pass for 10 flagship entries
- [x] Add bilingual July 3-16 fixture copy for native mock app

## Phase 4.5: Layer D — Devotional Engine (Cloned from KJV App)
- [x] Import AnnoDevotionalLoader.swift — deterministic date rotation
- [x] Import DevotionalProvider.swift — pool management
- [x] Import Bookmark.swift + BookmarkActions.swift — SwiftData persistence
- [x] Import GlassCard, ShareCard, ShareableImage, VerseActionBar — UI components
- [x] Import Haptics, SearchHistory, NotificationService — service wrappers
- [ ] Wire devotional engine into app (RootView / TodayView integration)
- [ ] Adapt VerseActionBar palette to AnnoTheme
- [ ] Produce Catholic devotional JSON (see `CLONE_FROM_KJV.md` + research prompt)
- [ ] Vietnamese translation pass for 365-entry devotional pool

## Phase 5: UI/UX and Monetization
- [x] Expandable calendars — collapsible extra calendar systems
- [x] Skeleton loaders — shimmer animation for loading state
- [x] Colorblind-safe pins — icon overlays (✡, ☪, +, ∞) on tradition dots
- [x] Sundown anchor banner — GPS-based location note
- [x] Audio narration buttons — on all 3 event cards (play/pause toggle)
- [x] Map bottom sheet — 7-day pilgrimage site window with pins
- [x] Bookmark micro-feedback — gold fill + toast
- [x] Reduced motion guard — global prefers-reduced-motion
- [x] Focus-visible states — gold outline on all interactive
- [ ] Confidence badges — confirmed/traditional/disputed pills (Sprint D)
- [ ] Translate mockup patterns into native SwiftUI components
- [ ] Premium archive paywall
- [ ] Pilgrim route pack teaser
- [x] Add privacy-safe monetization trust spec
- [x] PrivacyInfo.xcprivacy created
- [x] Privacy policy written
- [x] App Store metadata template written

## Changelog

- 2026-07-10: Engine A fully reconciled. Privacy compliance files created. Source validation gate written. Research prompts for Engine B written. MMR-ingested execution plan written. Week fixture fixed. Stale infra path fixed in AGENTS.md.
- 2026-07-04: Sprint 1 localization complete — asset boards A/B/C, pseudo-localize tool, component rules, design brief updates. Sprint 2.1 complete — LocalizationManager (Swift), unit tests, strings validator, English .strings reference.
- 2026-07-03: Reframed roadmap around native SwiftUI, Catholic-first launch, Vietnamese localization, and artifact reconciliation.
