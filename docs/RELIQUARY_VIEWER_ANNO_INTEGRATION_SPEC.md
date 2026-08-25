# Anno — AR Reliquary Viewer & Spatial Sacred Integration Specification

**Subsystems:** `Anno` (Core Devotional & Sacred Geography Platform) $\longleftrightarrow$ `ReliquaryExplorer` / `PilgrimCore` (AR Reliquary & Geofenced Audio Engine)  
**Platforms:** iOS / iPadOS 26.0 (ARKit + RealityKit) & Apple Vision Pro visionOS 26.0 (RealityKit + ImmersiveSpace)  
**Status:** Canonical Integration Architecture & Visual Craft Specification  

---

## 1. Product Vision & Spiritual Reverence

Sacred relics and historic reliquaries (*Thánh Tích & Hòm Thánh Tích*) represent tangible anchors of Catholic and ancient Christian heritage—from the **Holy Shroud of Turin** and the **True Cross Staurothèke** to the **Silver Apostolic Casket of St. James** and the **Our Lady of La Vang Marian Statue**.

The integration of `ReliquaryExplorer` into `Anno` creates an unprecedented sacred experience:
1. **Sacramental Tactility:** Believers and historians can place high-fidelity 3D reliquary models onto a physical altar, home prayer table, or chapel floor at **1:1 true scale**.
2. **Illuminated Craft & Materials:** Physically-based rendering (PBR) faithfully replicates hammered 12th-century repoussé gold leaf, oxidized Carolingian silver, Byzantine samite silk embroidery, and cabochon sapphire reflections reacting dynamically to real-world room lighting.
3. **Harmonious Audio-Spatial Atmosphere:** While rotating and inspecting the relic, localized bilingual audio hagiography (*Tiếng Việt & English*) plays softly over gentle ambient Gregorian or Vietnamese chant.

```
       [ Today Devotional / Sacred Map ]               [ Tap "Contemplate in AR" ]               [ AR Spatial Reliquary Room ]
  ════════════════════════════════════════════► ════════════════════════════════════════► ════════════════════════════════════════
   • Feast of the Day or Waypoint Relic          • Full-Screen Modal Cover (iOS)          • 1:1 Scale Tabletop Raycast Placement
   • Golden "✨ View in AR" Action Button         • Spatial ImmersiveSpace (visionOS)      • Pinch-to-Scale, Twist-to-Rotate
   • Historical Era & Provenance Badge           • Ambient Candlelight Atmosphere         • Spoken Hagiography + Salve Regina
```

---

## 2. Interaction Touchpoints Across Anno

### 2.1 Touchpoint A: The Map & Sanctuary Atlas (`SacredSiteMapView.swift`)
When tapping any of the 72 global sanctuaries or 106 pilgrimage waypoints:
- If the station contains a venerated reliquary, the detail drawer renders an illuminated gold action button:
  - **English:** `[ 🏛️ View 3D Sacred Reliquary in AR ]`
  - **Vietnamese:** `[ 🏛️ Chiêm Ngắm Thánh Tích 3D Trong Không Gian ]`
- Tapping opens the AR viewport (`ReliquaryARScreen`), pre-loading the specific 3D USDZ asset (e.g. `SilverApostolicCasket` for Santiago de Compostela, `CruciformReliquary` for Santa Croce / Christ Cathedral).

### 2.2 Touchpoint B: The Daily Devotional (`TodayView.swift`)
When the day's liturgical feast connects to a historic relic (e.g. *Feast of the Holy Cross on Sep 14*, *St. James on Jul 25*, *Vietnamese Martyrs on Nov 24*):
- The `artworkCard` or `liturgicalPilgrimageCard` displays a glowing golden **AR Badge** in the top-right corner.
- Tapping triggers a prayerful transition into the 3D reliquary contemplation mode with spoken hagiography.

### 2.3 Touchpoint C: Geofenced Arrival on Holy Ground (`PilgrimGuideCoordinator.swift`)
When the pilgrim physically walks into a sanctuary geofence (e.g. *approaching Christ Cathedral campus or Santiago crypt*):
- The **ActivityKit Dynamic Island / Lock Screen banner** presents:
  - *"Approaching Santiago de Compostela Crypt"*
  - Direct Action: **[ Listen to Prayer & Inspect Reliquary ]**
- Opening the notification launches directly into the AR viewer with the localized audio track streaming automatically.

---

## 3. Visual Craft, Materials & HUD Design System

To ensure `ReliquaryExplorer` matches Anno's luxury ecclesial brand, all AR overlay elements adhere to `AnnoTheme`:

```
               ┌──────────────────────────────────────────────────────────┐
               │  ◄ Exit          Apostolic Silver Casket       🔊 Audio  │  ← Frosted Narthex Bar
               ├──────────────────────────────────────────────────────────┤
               │                                                          │
               │                                                          │
               │                        ┌────────┐                        │
               │                        │  ╔══╗  │                        │  ← Specular Gold Reticle
               │                        │  ╚══╝  │                        │    (Snaps to detected floor)
               │                        └────────┘                        │
               │                                                          │
               │                                                          │
               ├──────────────────────────────────────────────────────────┤
               │  [ 9th Century Carolingian ]            Scale: 100% (1:1)│  ← Gilded Bottom HUD
               │  "Oxidized silver chassis with arcade of apostle figures"│
               └──────────────────────────────────────────────────────────┘
```

1. **Top Bar:** Frosted Narthex glass (`AnnoTheme.narthex.opacity(0.85)`) with gold title and audio playback status indicator.
2. **Placement Reticle:** Elegant circular golden filigree reticle that animates from pulsing gold (`AnnoTheme.goldLeaf`) to solid gilt when a stable horizontal surface (table, altar, floor) is detected via ARKit raycasting.
3. **Bottom Relic Dossier:** Sliding glass drawer displaying the relic's era, historical provenance, scripture citation, and tactile reset buttons.
4. **Haptic Feedback:**
   - Soft impact haptic (`UIImpactFeedbackGenerator(style: .light)`) when surface plane is locked.
   - Distinctive crisp haptic when placed (`.medium`) or when snapping back to 100% true scale.

---

## 4. Shared Data Architecture & Seams

```swift
// Bridging Anno Sanctuary with ReliquaryExplorer ReliquaryItem
// NOTE: Anno's model key is `associated3DReliquaryId` — NOT `primaryRelicId`
// (the latter does not exist on Sanctuary / PilgrimageWaypoint).
extension Sanctuary {
    public var associatedReliquary: ReliquaryItem? {
        associated3DReliquaryId.flatMap { ReliquaryItem.item(withID: $0) }
    }
}

extension PilgrimageWaypoint {
    public var associatedReliquary: ReliquaryItem? {
        associated3DReliquaryId.flatMap { ReliquaryItem.item(withID: $0) }
    }
}

// Geofence mapping (spec originally omitted this): convert Anno Sanctuary →
// PilgrimCore SanctuarySite. PilgrimCore's SanctuaryCatalog.validated() rejects
// sites with empty `narrations`, so hagiography audio + transcripts must be
// authored per sanctuary before enabling geofenced narration in production.
// Implemented in Anno/Reliquary/ReliquaryBridge.swift (guarded by
// `#if canImport(PilgrimCore)` so it no-ops until the package dependency exists).
extension Sanctuary {
    public var asPilgrimSite: SanctuarySite? { /* see Anno/Reliquary/ReliquaryBridge.swift */ }
}
```

### Curated 3D Reliquary Catalog Matrix

| Reliquary ID | Title & Era | Associated Sanctuaries / Routes | 3D Model Asset |
|---|---|---|---|
| `reliquary_passion_cross` | **Cruciform Passion Reliquary** *(12th C. Romanesque)* | • Santa Croce in Gerusalemme (Rome)<br>• Christ Cathedral La Vang (SoCal)<br>• Notre-Dame de Paris | `CruciformReliquary.usdz` |
| `reliquary_passion_textile` | **Holy Textile Casket** *(14th C. Byzantine)* | • Royal Chapel of the Holy Shroud (Turin)<br>• Holy Tunic (Argenteuil / Trier)<br>• Sudarium of Oviedo | `TextileCasket.usdz` |
| `reliquary_silver_casket` | **Apostolic Silver Casket** *(9th C. Carolingian)* | • Cathedral of Santiago de Compostela<br>• Basilica of St. Peter (Vatican)<br>• Basilica of St. Francis (Assisi) | `SilverApostolicCasket.usdz` |
| `reliquary_la_vang_crown` | **Our Lady of La Vang Marian Regalia** *(18th C. Vietnamese)* | • Our Lady of La Vang Shrine (Quảng Trị)<br>• Christ Cathedral La Vang Shrine (Orange County) | `LaVangRegalia.usdz` |

---

## 5. Summary of Engineering Guarantees

1. **Zero Runtime Crashing:** If a 3D `.usdz` asset is missing or still downloading, `ReliquaryAssetLoading` gracefully falls back to an illuminated gilded wireframe placeholder box with zero runtime errors.
2. **Swift Concurrency & Actor Safety:** All AR session management, entity manipulation, and coordinator state are isolated to `@MainActor`.
3. **Battery & Thermal Conservation:** ARKit sessions automatically pause rendering and release camera hardware the moment the user dismisses the AR viewport or background the app.

---

## 6. From-Linux Status & Next Steps (2026-08-25)

The incorporation below was performed on the Linux server (ichabod) where the code
can be **written and statically reviewed but not built** — `PilgrimCore` imports
ARKit / RealityKit / CoreLocation / AVFoundation, none of which exist on Linux, and
Anno's app build manifest is not committed in this repo.

### Done (source-level, no build)
- **Fixed two compile-blocking bugs in `PilgrimCore`:**
  - `ReliquaryInteractionModel.swift`: assignments used `sessionIsActive`; the
    property is declared `isSessionActive` → renamed the 4 assignment sites.
  - `PilgrimGuideCoordinator.swift`: `recentVisitLog` was used but never declared →
    added `public private(set) var recentVisitLog: [SanctuaryVisitEvent] = []`.
- **Corrected the bridge snippet above** (was `primaryRelicId`, which does not exist).
- **Wrote `Anno/Reliquary/ReliquaryBridge.swift`** — `associatedReliquary` +
  `asPilgrimSite` mappings, guarded by `#if canImport(PilgrimCore)` so it compiles
  to nothing until the package is linked.
- **Wired the 6 dropped prayer `.mp3`s** into `Anno/Resources/audio_narration_catalog.json`
  (18 tracks total); `AudioNarrationTrack.audioURL(for:)` now resolves local bundle
  files (CDN https URLs still take precedence).
- **Wired the 5 dropped icon `.png`s**: added `icon_asset_name` to `Sanctuary`,
  mapped `la_vang_shrine_icon` → `our_lady_of_la_vang` and `martyrs_wall_icon` →
  `north_american_martyrs_auriesville`, and registered all 5 in the new
  `Anno/Resources/sacred_icons_registry.json` (3 icons have no matching sanctuary
  yet — pending a Saints feature).

### macOS / Xcode-only (cannot be done from Linux)
1. **Add the local package dependency** on `ReliquaryExplorer/Packages/PilgrimCore`
   to Anno's build (Xcode project / `project.yml` / `Package.swift`). PilgrimCore
   requires **iOS 26 / visionOS 26** and `swift-tools-version: 6.0` — Anno's current
   manifests (e.g. `ios/Package.swift` is iOS 17) must be bumped or kept separate.
2. **Generate the missing `Info.plist`s** referenced by `ReliquaryExplorer/project.yml`
   (`Apps/iOS/Info.plist`, `Apps/visionOS/Info.plist`) — currently absent, so
   `xcodegen` would fail.
3. **Add the `.github/workflows/ci.yml`** the README claims exists (it does not) so CI
   can build both targets and run `PilgrimCoreTests`.
4. **Activate the inert map buttons** in `SacredSiteMapView.swift` (lines ~754, ~926
   currently call only `Haptics.selection()`) to present the AR viewer via a
   `ReliquaryInteractionModel` host + `ARKitReliquarySessionService`.
5. **Reconcile audio engines:** Anno has `SacredSpatialAudioEngine`; PilgrimCore has
   `AudioHagiographyPlayer` — pick one owner for geofenced narration.
6. **Author hagiography audio + transcripts** for Anno's 72 sanctuaries so
   `SanctuaryCatalog.validated()` passes (currently `asPilgrimSite` ships empty
   `narrations`).
