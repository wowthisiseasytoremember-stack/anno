# Vibe Coder Prompt: Build the Native SwiftUI Shell
Updated: 2026-07-03

Copy/paste this entire prompt into an AI coding agent that can create an Xcode/Swift project.

```text
You are building the native iOS SwiftUI shell for Anno, a premium Catholic sacred-history app.

You do not need to implement the final backend, full content pipeline, or production subscriptions. You must produce a clean, compilable native iOS shell that establishes the hard iOS architecture and visual direction.

PRODUCT

Name:
Anno

Subtitle:
This Day in Catholic History

North Star:
Every day in Catholic history, mapped.

App promise:
The user opens the app and immediately learns what happened today in Catholic history: saint/feast/event, sacred art, pilgrimage place, source confidence, and a short historically grounded prayer.

Visual direction:
Dark-mode-first Illuminated Timeline.
Gold Leaf (#C9A84C) on warm near-black Narthex (#13110E).
Surfaces use Choir (#1F1B16), text uses Vellum (#EDE7DA), secondary text uses Incense (#9B9085), dividers use Ash (#2E2A24).
Use Apple's native New York/SF stack:
- New York Display/Text for date, title, reading surfaces.
- SF Pro for navigation, metadata, controls.
- SF Pro Rounded for pills/tags.
No custom font dependency in v1.
One accent color per screen.
The art is the ornament.

REFERENCE ASSETS IN THIS REPO

Use these files as visual reference if present:
- visuals/anno-visual-board.html
- visuals/app-icon-anno.svg
- visuals/today-screen-dark.svg
- visuals/pilgrim-map-dark.svg
- visuals/archive-paywall.svg
- docs/BRAND_VISUAL_ADDENDUM.md
- docs/CATHOLIC_IOS_PRODUCT_BIBLE.md
- docs/MONETIZATION_PAYWALL_SYSTEM.md

TECHNICAL TARGET

Create a native iOS app:
- SwiftUI
- iOS 17+ minimum, unless project constraints require iOS 16
- App target named Anno
- Bundle ID placeholder: com.yourco.anno
- No third-party dependencies for the shell
- Compile in Xcode
- Dark mode default
- Light mode support present but secondary
- Local sample JSON/data only

REQUIRED FRAMEWORKS

Use:
- SwiftUI
- MapKit
- StoreKit 2
- SwiftData or local Codable JSON store for sample content/bookmarks
- Foundation

Do not use:
- UIKit app lifecycle unless unavoidable
- RevenueCat in this shell
- Firebase
- Ad SDKs
- Social/community SDKs
- AI chat

APP STRUCTURE

Create this approximate file structure:

Anno/
  AnnoApp.swift
  AppTheme.swift
  Models/
    DailyEntry.swift
    SacredSite.swift
    Artwork.swift
    SourceReference.swift
    EntitlementState.swift
  Data/
    SampleData.swift
    SampleContent.json
  Views/
    RootTabView.swift
    Today/
      TodayView.swift
      DateHeaderView.swift
      LiturgicalContextView.swift
      ArtworkCardView.swift
      PilgrimageLocationRow.swift
      ConfidenceBadgeView.swift
      PrayerSectionView.swift
      SourceSheetView.swift
    Calendar/
      CalendarView.swift
    Map/
      PilgrimMapView.swift
      SacredSiteAnnotationView.swift
      RoutePreviewSheet.swift
    Saved/
      SavedView.swift
    Premium/
      ArchivePaywallView.swift
      SubscriptionStoreShellView.swift
    Components/
      AnnoButton.swift
      EmptyStateView.swift
      LoadingSkeletonView.swift
      ErrorStateView.swift
  Localization/
    Localizable.xcstrings
  StoreKit/
    StoreKitManager.swift
    Products.storekit

MODEL REQUIREMENTS

DailyEntry:
- id
- date
- liturgicalContext
- title
- subtitle
- body
- prayer
- confidence: confirmed/traditional/disputed
- artwork
- sacredSite
- sources
- localized strings shape or comments showing English/Vietnamese-ready fields

Artwork:
- title
- artist
- year
- caption
- imageName or imageURL placeholder
- provenance

SacredSite:
- name
- region
- latitude
- longitude
- routePackCandidate

SourceReference:
- title
- citation
- url optional
- sourceType

EntitlementState:
- isPremium
- isPilgrim
- canUseArchive
- canUseFullMap
- canUseAudio

SCREENS

1. Today

Must show:
- Anno header
- Date
- liturgical context
- large artwork card
- pilgrimage location row
- confidence badge
- source sheet button
- listen sample button
- bookmark button
- short prayer
- no login gate
- no day-one paywall

Use the visual proportions from visuals/today-screen-dark.svg.

2. Calendar

Shell only is fine.
Show current month, dots on several dates, and a premium archive teaser.
Past/future full entries should call ArchivePaywallView if entitlement is false.

3. Map

Use MapKit with sample pins:
- Rome
- Assisi
- Jerusalem
- Nazareth
- Santiago
- Lourdes

Free state:
- Today/this-week pins visible.

Premium teaser:
- Full-map route preview sheet for Rome in Three Days.

4. Saved

Local-first empty state:
"Save a day, artwork, or route. Your sacred history collects here."

5. Premium

Create ArchivePaywallView:
- Title: Unlock the Catholic archive
- Benefits:
  - Read past and future entries
  - Open every pilgrimage pin
  - Sacred art gallery + provenance
  - Expanded source dossiers
  - Audio daily entries
- Buttons:
  - Start Premium
  - Monthly option
  - Restore Purchases
- Footer: No ads. No AI slop. Sources on every claim.

StoreKit:
- Include StoreKitManager with async product loading stubs.
- Include placeholder product ids:
  - anno.premium.monthly
  - anno.premium.yearly
  - anno.pilgrim.yearly
- Use StoreKit 2 patterns, but mock gracefully if products are unavailable.
- Add a Products.storekit configuration file if possible.

LOCALIZATION

Must include English and Vietnamese-ready structure.

Create Localizable.xcstrings or Localizable.strings placeholders for:
- Today
- Calendar
- Map
- Saved
- Sources
- Confirmed
- Traditional
- Disputed
- Unlock the Catholic archive
- This Day in Catholic History
- No ads. No AI slop. Sources on every claim.

Vietnamese candidates:
- Saint: Thánh
- Martyr: Tử đạo
- Pilgrimage: Hành hương
- Source: Nguồn
- Confirmed: Đã xác nhận
- Traditional: Theo truyền thống
- Disputed: Còn tranh luận
- Liturgical season: Mùa phụng vụ
- Ordinary Time: Mùa Thường Niên

Do not machine-translate long content at runtime.

VISUAL RULES

Implement AppTheme:
- narthex #13110E
- choir #1F1B16
- goldLeaf #C9A84C
- gilt #D9C06E
- lapis #2B4A7C
- crimson #8C2F3B
- vellum #EDE7DA
- incense #9B9085
- ash #2E2A24
- verdigris #3B6B52
- advent #5C3D6E
- easter #F5F0E8

Rules:
- Dark mode default.
- No pure black.
- No pure white in dark-mode surfaces.
- One accent per screen.
- 8pt spacing grid.
- 44pt minimum tap targets.
- Dynamic Type must not break layouts.
- Text must wrap, not truncate, for Vietnamese.

SAMPLE CONTENT

Include one complete sample entry:

Date: July 16
Liturgical context: Optional Memorial of Our Lady of Mount Carmel
Title: Our Lady of Mount Carmel
Subtitle: The scapular tradition and a mountain of prayer
Confidence: Traditional
Place: Mount Carmel, Israel, coordinates approximately 32.6728, 35.0468
Prayer:
Mary, keep our memory faithful: teach us to carry history as a light, not as a weight.
Sources:
- Roman Martyrology / liturgical calendar reference
- Carmelite tradition reference
- source placeholder for later verification

Also include sample sites:
- Rome
- Assisi
- Jerusalem
- Nazareth
- Santiago
- Lourdes

ACCEPTANCE CRITERIA

The result is accepted only if:

1. The Xcode project opens and builds.
2. The app launches into Today without login.
3. Dark mode visual system is implemented.
4. Four tabs exist: Today, Calendar, Map, Saved.
5. Today screen includes art, map row, source confidence, prayer, bookmark, and audio sample affordance.
6. MapKit view displays sample pins.
7. StoreKit 2 manager exists with placeholder product IDs and no crash when products are missing.
8. Localization scaffolding exists for English and Vietnamese.
9. There are no ads, no social features, no AI chat, no Grace Tokens, no paid streak repair, and no leaderboards.
10. The code is organized enough for another engineer to continue.

DELIVERABLES

Return:
- File tree.
- Build/run instructions.
- Any assumptions.
- Any known gaps.
- Screenshots if the environment can produce them.
```

