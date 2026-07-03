# Interfaith Devotional Engine — ROADMAP.md
Updated: 2026-07-03

## Phase 0: Canonical Truth Reconciliation
- [x] Create `ARCHITECTURE.md`
- [x] Create Catholic-first native iOS product bible
- [x] Create asset prompts, rubric, monetization system, and flagship content slate
- [ ] Import `/home/ichabod/01_Infrastructure/interfaith/` artifacts into canonical project structure
- [x] Set working project name: Anno

## Phase 1: Native iOS Scaffold
- [ ] Create SwiftUI app project
- [ ] Add StoreKit 2 subscription scaffolding
- [ ] Add MapKit sacred-place view shell
- [ ] Add Xcode String Catalogs for English and Vietnamese UI strings
- [ ] Add local content/cache model with localized fields

## Phase 2: Engine A — Calendar Engine
- [x] Calendar conversion script for 10+ systems exists in infrastructure bundle
- [x] 4-year JSONL generation exists in infrastructure bundle
- [ ] Import Engine A artifacts into canonical project
- [ ] Spot-check validation against known dates and local sundown cases

## Phase 3: Engine B — Catholic-First Research Agent
- [ ] Daily research prompt
- [ ] Catholic saint/feast/history pipeline
- [ ] Optional Sacred Context pipeline only where genuine
- [ ] JSON output schema
- [ ] Source/confidence validator

## Phase 4: Layer C — User-Facing Content
- [ ] Content prompt engineering
- [ ] 10 flagship entries from `docs/FLAGSHIP_CONTENT_SLATE.md`
- [ ] Vietnamese translation pass for 10 flagship entries
- [ ] Sample audio script generation

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
- [ ] Confidence badges — confirmed/traditional/disputed pills
- [ ] Translate mockup patterns into native SwiftUI components
- [ ] Premium archive paywall
- [ ] Pilgrim route pack teaser

## Changelog

- 2026-07-03: Reframed roadmap around native SwiftUI, Catholic-first launch, Vietnamese localization, and artifact reconciliation.
