# Reliquary Explorer & Proximity-Triggered Pilgrim Guide

A multiplatform (iPhone / iPad / Apple Vision Pro) SwiftUI app with two
integrated subsystems:

1. **AR Reliquary Viewer** — place `.usdz` / `.reality` models of sacred
   reliquaries and Passion textiles onto real surfaces; tap-to-place,
   pinch-to-scale, twist-to-rotate; robust plane detection and
   interruption/relocalization handling.
2. **Proximity-Triggered Audio Hagiography** — `CLLocationManager`
   **region monitoring** (geofencing, *not* GPS polling) wakes the app
   when the pilgrim enters a sanctuary and narrates its saint/site
   history automatically — including in the background and during an
   active AR session.

Deployment targets (per project decision): **iOS/iPadOS 26.0,
visionOS 26.0**.

---

## 1. Repository layout

```
ReliquaryExplorer/
├── project.yml                     # XcodeGen spec → ReliquaryExplorer.xcodeproj
├── .github/workflows/ci.yml        # build both targets + run unit tests on every push
├── Demo/SimulatorRoutes/           # GPX routes: reviewer + simulator geofence demos
│   ├── grand_tour.gpx              #   crosses ALL four sanctuary geofences in one pass
│   └── santiago_approach.gpx       #   realistic 4-minute walk into Santiago (60 m geofence)
├── Apps/
│   ├── iOS/Sources/
│   │   ├── ReliquaryExplorerApp.swift      # @main, wires coordinator + AR cover
│   │   ├── AR/ARKitReliquarySessionService.swift   # ARKit/ARView session impl
│   │   ├── AR/ReliquaryARScreen.swift              # ARView representable + UIKit gestures + HUD
│   │   └── Location/CoreLocationSanctuaryMonitor.swift  # geofencing impl
│   └── visionOS/Sources/
│       ├── ReliquaryExplorerVisionApp.swift        # @main, window + ImmersiveSpace
│       ├── AR/ImmersiveReliquarySessionService.swift   # ARKitSession/providers impl
│       ├── AR/ReliquaryImmersiveView.swift             # RealityView + spatial gestures
│       └── Location/MuseumModeSanctuaryMonitor.swift   # explicit no-op stub
└── Packages/PilgrimCore/           # shared Swift package (business logic + SwiftUI)
    ├── Sources/PilgrimCore/
    │   ├── Domain/                 # SanctuarySite, ReliquaryItem (Codable config models)
    │   ├── Catalog/                # SanctuaryCatalog (load/validate), RegionScheduler
    │   ├── Geofence/               # SanctuaryMonitoring protocol, VisitPolicy
    │   ├── Audio/                  # HagiographyPlaying, AVAudioPlayer-based player
    │   ├── ARCore/                 # PlacementMath, ReliquarySessionServicing seam,
    │   │                           # asset loading, ReliquaryInteractionModel
    │   ├── Coordination/           # PilgrimGuideCoordinator (+ notification/phase ports)
    │   ├── UI/                     # PilgrimRootView, map, catalog, settings, banner
    │   └── Resources/
    │       ├── SanctuariesConfig.json       # THE data file: sites = data, not code
    │       └── Audio/               # placeholder narration tracks (0.5 s silence)
    └── Tests/PilgrimCoreTests/     # 7 suites, incl. fakes for both platform seams
```

Build: `xcodegen generate` (or open the generated project), then run the
`ReliquaryExplorer` (iOS) or `ReliquaryExplorerVision` (visionOS) scheme.
Unit tests: scheme test action (`PilgrimCoreTests`) — run on an
iOS/visionOS destination; the fakes mean ARKit/CoreLocation are not
required for the logic tests. CI: `.github/workflows/ci.yml` generates
the project, builds both targets, and runs the unit tests on an iOS
simulator (requires a macOS runner with Xcode 26) — it is the fastest
way to surface any SDK-surface fix-ups.

Assets: drop `CruciformReliquary.usdz` / `.reality`, `TextileCasket…`,
`SilverApostolicCasket…` into the app targets (see §6 for the asset
contract); the loader degrades to a clearly-marked placeholder box when
missing. Replace the silent WAV placeholders with produced `.m4a`
narrations by the same resource name.

---

## 2. Architecture overview

```
                        ┌───────────────────────────────┐
                        │        PilgrimRootView        │  shared SwiftUI
                        │  map · catalog · settings     │
                        └──────────────┬────────────────┘
                                       │
              ┌────────────────────────┴─────────────────────────┐
              │            PilgrimGuideCoordinator               │  @MainActor
              │  visit events → VisitPolicy → narration          │
              │  backgrounded? → local notification              │
              └──────┬───────────────────────────────┬───────────┘
        events (AsyncStream)                  play/stop intent
        ┌──────▼──────────────┐                  ┌─────▼──────────────┐
        │ SanctuaryMonitoring │                  │ HagiographyPlaying │
        │   (protocol seam)   │                  │  (protocol seam)   │
        ├─────────────────────┤                  ├────────────────────┤
        │ iOS: CLLocation-    │                  │ AVFoundation impl  │
        │   SanctuaryMonitor  │                  │ (shared, both OSes)│
        │ visionOS: Museum-   │                  └────────────────────┘
        │   ModeStub (no-op)  │
        └─────────────────────┘

        ┌──────────────────────────────────────────────────────────┐
        │              ReliquaryInteractionModel                   │
        │   tap-to-place · scale · rotate · reticle · phases       │
        │   (shared brain; gestures translate to intents)          │
        └──────────────────────────┬───────────────────────────────┘
                     intents       │      ┌─────────────────────┐
              ┌────────────────────┴─────►│ PlacementMath (pure)│
              │                            └─────────────────────┘
        ┌─────▼──────────────────────────────┐
        │    ReliquarySessionServicing       │  (protocol seam)
        ├────────────────────────────────────┤
        │ iOS: ARKitReliquarySessionService  │  ARView + ARWorldTrackingConfiguration
        │ visionOS: ImmersiveReliquary-      │  ARKitSession + providers + RealityView
        │   SessionService                   │
        └────────────────────────────────────┘
```

Everything above the two seams is written once and compiled into all
three targets. **The only `#if os(...)` in shared UI code** is the
AR-launch closure injected by each app (full-screen cover vs.
immersive space) — shared code never links an AR session or a
CLLocationManager.

---

## 3. AR subsystem: how iOS and visionOS diverge

| Aspect | iOS / iPadOS (`ARKitReliquarySessionService`) | visionOS (`ImmersiveReliquarySessionService`) |
|---|---|---|
| Rendering container | `ARView` (UIKit) behind `UIViewRepresentable` | `RealityView` in an `ImmersiveSpace` (mixed style) |
| Session | `ARView.session.run(ARWorldTrackingConfiguration)` with `planeDetection = [.horizontal]`, env texturing, light estimation | `ARKitSession.run([WorldTrackingProvider, PlaneDetectionProvider(.horizontal), SceneReconstructionProvider])` — providers only deliver in a Full Space |
| Permission | Camera (ARKit) — `NSCameraUsageDescription` | World sensing — explicit `requestAuthorization([.worldSensing])`, `NSWorldSensingUsageDescription`; denial surfaces as a UI state, not a crash |
| Surface discovery | ARKit plane anchors; readiness = ≥ 1 tracked horizontal plane | `PlaneDetectionProvider` anchors *and* scene-reconstruction meshes drive readiness |
| Hit testing | Screen-space: `ARView.raycast(from:allowing:alignment:)` from the touch point (plane geometry → estimated plane fallback); also world-ray `ARRaycastQuery` | World-space: head-pose ray (`WorldTrackingProvider.queryDeviceAnchor`) → `Scene.raycast(from:to:)` against invisible collision copies of the reconstruction meshes (occlusion material) |
| Aiming UX | The touch ray itself | Gaze reticle: ~15 Hz head-pose raycast (ARKit guidance: don't query pose at frame rate for non-rendering logic); spatial tap confirms the reticle |
| Placement anchor | `ARAnchor(transform:)` added to the session → `AnchorEntity(anchor:)` | `WorldTrackingProvider.addAnchor(WorldAnchor(originFromAnchorTransform:))` → transform re-applied on `anchorUpdates(.added/.updated)` |
| Interruption / relocalization | Explicit `ARSessionDelegate` handling + `ARCoachingOverlayView` (`sessionShouldAttemptRelocalization = true`) | OS-managed; app listens to `ARKitSession.events` and keeps ECS hierarchy intact (per-anchor transform refresh) |
| Gestures | `UITapGestureRecognizer` / `UIPinchGestureRecognizer` / `UIRotationGestureRecognizer` (incremental deltas; recognizers zeroed each callback) | `SpatialTapGesture` + `RotateGesture3D(.y) ⨯ MagnifyGesture` targeted at the entity (absolute values since gesture start) |

### How duplication is avoided

All placement/interaction policy lives above the seam:

- **`ReliquaryInteractionModel`** (shared, `@MainActor @Observable`) owns
  the phase machine (`idle → loadingAsset → searchingSurface →
  readyToPlace → placed`) and exposes *intent APIs*:
  `confirmPlacement(atScreenPoint:)` (iOS passes the touch point;
  visionOS passes `nil` → gaze reticle), `handleScaleDelta`,
  `handleYawDelta`, `updateGesture(magnification:yawFromGestureStart:on:)`
  (start-anchored variant for visionOS semantics), `settleScale`.
- **`PlacementMath`** (pure functions, no RealityKit import) computes
  upright world transforms (surface normal → Y axis, yaw facing the
  viewer), clamped uniform scale, and yaw-only quaternions — unit-tested
  on their own.
- Platform gesture code is a *thin translator*: the iOS coordinator
  zeroes `recognizer.scale` each callback and forwards incremental
  deltas; the visionOS view forwards absolute gesture values which the
  shared model anchors to a gesture-start snapshot. The difference is
  documented in one place (`updateGesture`) instead of forked logic.
- Both platforms anchor the wrapper entity under a world-fixed anchor,
  so local-Y rotation on the wrapper is world yaw — pitch/roll can
  never be disturbed by the rotation gesture, on either platform.

**UIKit usage statement (per constraints):** UIKit is confined to
`ARView` + `UIViewRepresentable` + `UIGestureRecognizer`s + one haptic
in the iOS AR screen (and `UIApplication` phase bridging). None of it
leaks into `PilgrimCore` or the visionOS target; the shared codebase is
blocked from neither platform.

**Tracking loss handling (iOS):** interruption callbacks → banner +
coaching overlay; `sessionShouldAttemptRelocalization == true` so
existing `ARAnchor`s reattach placed reliquaries after recovery; plane
removal events update surface readiness; failures surface as `.failed`
phase with actionable copy.

---

## 4. Proximity subsystem (iOS/iPadOS primary)

- **No continuous GPS.** Arming uses `CLLocationManager` region
  monitoring (`CLCircularRegion`, entry+exit), which the OS services
  without app CPU. `startMonitoringSignificantLocationChanges()` runs
  purely as a low-power companion to re-rank regions and persist a
  cold-start location.
- **20-region budget.** iOS caps monitored regions per app. The pure
  `RegionScheduler` keeps the 20 *nearest* sanctuaries registered
  (deterministic tie-breaks; catalog order on cold start) and the
  monitor swaps sets diff-based on boundary crossings / significant
  moves. The 4-site sample config never hits the cap, but the pipeline
  is built for real pilgrimage networks.
- **Data-driven sites.** `SanctuariesConfig.json` → `SanctuarySite`
  (validated: unique IDs, radius 20–5000 m, coordinate bounds, ≥ 1
  narration). Supports localized `narrations` dictionaries
  (`"en" | "es" | "it" | … → {audioFileName, transcript}`) *and* the
  legacy flat `audioFileName`/`transcript` form (decoded as English).
  `NarrationResolver` matches exact → region-stripped → English → first
  available, with a Settings override. Adding a sanctuary = one JSON
  entry + one audio file; zero code changes.
- **Authorization.** Two-step flow (`requestWhenInUseAuthorization()`
  then `requestAlwaysAuthorization()` on the auth callback) gives an
  honest Always upgrade path. Provisional Always still services region
  events. Availability (`.available` / `.requiresAuthorization` /
  `.unsupported`) is surfaced in Settings and map callouts.
- **Background arrival path.** Region event → app woken (or relaunched;
  `scenePhase == .active` re-arms) → `VisitPolicy` (10-min per-site
  cooldown, exit re-arm, duplicate-enter dedupe) → `HagiographyPlaying`
  → local notification if backgrounded (visible user benefit).
- **AR + geofence simultaneity.** Playback is never gated on
  `arViewerActive`. The audio session is configured
  `.playback / .spokenAudio / [.duckOthers,
  .interruptSpokenAudioAndMixWithOthers]`; AVFoundation's audio session
  is fully independent of the ARKit tracking session, so narration
  mixes in while ARView keeps rendering. `arViewerActive` only decides
  *presentation* (the AR screen embeds its own banner copy).

### visionOS decision: explicit no-op + museum mode

`MuseumModeSanctuaryMonitor` **gracefully no-ops** monitoring and
reports `.unsupported` with a user-comprehensible reason. Chosen over a
"best effort" implementation because: Vision Pro has **no GNSS radio**
(Wi-Fi positioning is too coarse for 40–90 m sanctuary radii); visionOS
offers **no Always authorization tier** for background region events;
and visionOS has **no ambulatory background-location execution lane**
(apps suspend; a fake monitor would burn battery and never fire
reliably). The shared museum-mode UI (map + callouts + Settings)
delivers the same audio hagiographies manually; `simulateArrival(at:)`
exercises the full pipeline in QA. We deliberately do *not* claim
background-geofencing parity on visionOS.

---

## 5. Testing

| Suite | Covers |
|---|---|
| `PlacementMathTests` | orthonormal bases, upright transforms, facing, scale clamps, yaw purity |
| `ReliquaryInteractionModelTests` | phase machine, screen-point & reticle placement, gesture deltas (incremental + start-anchored), cleanup, failure surfacing — **against a fake session service; no ARKit needed** |
| `SanctuaryCatalogTests` | both config forms, validation failures, bundled + fixture loading |
| `RegionSchedulerTests` | 20-cap, nearest-first, deterministic ordering |
| `VisitPolicyTests` | cooldown, dedupe, exit re-arm, cross-site independence |
| `NarrationResolverTests` | exact/region/English/first-available matching, override |
| `PilgrimGuideCoordinatorTests` | geofence→audio bridge, dedupe, background notification, **AR-active arrival still plays**, manual playback |
| `AudioHagiographyPlayerTests` | language resolution into the engine, missing-asset failure event, track replacement, natural finish (fake engine + resolver) |

The two platform seams (`ReliquarySessionServicing`,
`SanctuaryMonitoring`) plus `HagiographyPlaying`/`AudioPlaybackEngine`
are exactly what makes the system testable without a device.

---

## 6. Demo & QA (product verification)

The proximity pipeline is the feature reviewers and pilgrims judge, so it
has two zero-logistics demo paths — both exercise the **real** code path
(geofence event → `VisitPolicy` → narration → banner/notification):

1. **In-app simulation (debug builds)** — Settings ▸ **Demo & QA**: per-
   sanctuary *Simulate arrival / Depart* buttons, a *Disable visit
   cooldown* toggle for rapid-fire demos, and a live geofence-event log.
   Works identically on iPhone, iPad, and Vision Pro (which has no GPS at
   all — the demo is the canonical way to show the audio pipeline there).
   Compiled out of release builds (`#if DEBUG`).
2. **GPX simulation (GPS-accurate)** — `Demo/SimulatorRoutes/`:
   - `grand_tour.gpx` — one playback crosses **all four** sanctuary
     geofences (Santiago → Assisi → Torino → Christ Cathedral). This is
     the App Review artifact.
   - `santiago_approach.gpx` — a realistic 4-minute, ~335 m walk into the
     Santiago geofence for solo demos and cooldown/jitter testing.
   Load via Xcode ▸ Debug ▸ Location ▸ Custom GPX…. Region entry should
   trigger narration in both foreground and background (lock the
   simulator's device or background the app to verify the Always path).

## 7. Asset contracts

- **Models**: bundle resource named per `ReliquaryItem.modelAssetName`
  (`.usdz` or `.reality`), pivot at base center, natural size at 1.0,
  Y+ up. Missing assets → marked placeholder (flows stay testable).
- **Audio**: bundle resource per narration `audioFileName`
  (`m4a`/`mp3`/`aac`/`wav`), normalized spoken word. Placeholders in
  `Resources/Audio` are 0.5 s of silence so the pipeline runs out of
  the box.

## 8. App Store review considerations

- **Guideline 2.5.4 (background location).** The app uses region
  monitoring — not continuous GPS — and the feature is the app's core,
  user-visible promise (auto-narration at sanctuaries). Provide in
  review notes: a short demo video of driving/walking into a geofence
  with the app backgrounded, and point the reviewer at
  `Demo/SimulatorRoutes/grand_tour.gpx` (Debug ▸ Location ▸ Custom GPX
  crosses all four sanctuaries) plus the Settings ▸ Demo & QA
  "Simulate arrival" buttons for on-demand verification. The Always
  prompt copy in `Info.plist` states the exact user benefit.
- **Background audio mode** is justified by narration continuing while
  the phone is pocketed/locked; playback stops at track end (no
  infinite silence); interruptions (calls/Siri) pause, not kill.
- **Permissions strings**: camera (AR surface tracking, images never
  leave the device), When-In-Use + Always location strings, and
  visionOS world-sensing string each name the concrete feature.
- **visionOS**: no background modes are claimed at all (matching the
  no-op geofence decision); world sensing is requested only when the
  user opens the AR viewer (user-initiated Full Space entry).
- Local notifications are optional (declinable) and only used to
  explain why narration started in the background.

## 9. Known trade-offs / future work

- Placements persist per AR session only; an obvious next step is
  `ARWorldMap` persistence (iOS) and persisted `WorldAnchor`s
  (visionOS) so reliquaries survive relaunch.
- `CLMonitor` (modern CoreLocation) could replace
  `CLLocationManager` region APIs, but classic region monitoring
  remains the best-documented path for background geofence delivery.
- The package is deliberately Swift-5 language mode (RealityKit
  entities and CLLocationManager aren't Sendable); the seams are in
  place for a contained Swift 6 migration.
- Collision shapes regenerate on gesture *end*; during an in-flight
  pinch, gesture targeting uses the pre-pinch collider (imperceptible
  at reliquary scales).
