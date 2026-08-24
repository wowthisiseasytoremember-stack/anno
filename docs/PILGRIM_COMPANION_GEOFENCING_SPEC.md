# Anno — Liturgical Waypoint Audio Geofencing & "Pilgrim Companion" Live Mode

**Feature Codename:** `PilgrimCompanion` / `SanctuaryGeofence`  
**Domain:** Native iOS (`CoreLocation`, `ActivityKit`, `AVFoundation`, `MapKit`, `UserNotifications`)  
**Status:** Complete Architectural & Engineering Specification  
**Target Delivery:** Phase C/D Luxury Client Feature  

---

## 1. Executive Summary & Spiritual Rationale

### 1.1 The Spiritual Problem
Traditional pilgrimage and religious travel apps force the believer to constantly stare at a screen, checking maps and searching for descriptions while standing in sacred spaces. This fractures prayerful contemplation and turns a spiritual encounter into tourist screen-glancing.

### 1.2 The Anno Breakthrough: Ambient Pilgrim Companion
**"Pilgrim Companion" Live Mode** transforms Anno into an ambient, reverent, pocket companion:
1. **Zero-Screen Walking:** The pilgrim puts their iPhone in their pocket or attaches headphones.
2. **Sacred Geofence Detection:** As the pilgrim approaches within **500 meters** of any of the 106 pilgrimage waypoints or 72 global sanctuaries, Anno gently wakes via haptic tap and presents an **ActivityKit Live Activity** and **Dynamic Island** alert on the Lock Screen.
3. **Inner Sanctuary Immersion (100m):** Upon entering the immediate sanctuary grounds (100m radius), the app offers an instant, localized **Audio Hagiographical Prayer** in English or Vietnamese with ambient liturgical chant.
4. **Digital Pilgrim Passport (*Sổ Hành Hương*):** Completing prayer at each physical station automatically unlocks an authenticated, date-stamped spiritual seal in the pilgrim's personal journal.

```
       [ 500m Outer Aura ]                    [ 100m Inner Sanctuary ]                 [ At the Altar / Crypt ]
  ═════════════════════════════════► ═════════════════════════════════════════► ═══════════════════════════════════════
   • CoreLocation Region Enter        • Live Activity Expands (Dynamic Island)    • Hagiographical Audio Narration
   • Subtle Double-Tap Haptic         • Relic & Martyr Details Surface            • Scripture & Pilgrim's Prayer
   • Lock Screen Live Activity        • "Listen to Prayer" CTA Prompt             • Station Passport Seal Unlocked
```

---

## 2. Technical Architecture & Component Flow

```
                                  ┌────────────────────────────────┐
                                  │   sacred_geography_master      │
                                  │   (18 Routes / 72 Sanctuaries) │
                                  └───────────────┬────────────────┘
                                                  │
                                                  ▼
                                  ┌────────────────────────────────┐
                                  │    PilgrimGeofenceManager      │
                                  │ (CoreLocation Circular Regions)│
                                  └───────────────┬────────────────┘
                                                  │
                      ┌───────────────────────────┴───────────────────────────┐
                      ▼                                                       ▼
      ┌────────────────────────────────┐                     ┌────────────────────────────────┐
      │   PilgrimLiveActivityService   │                     │      AudioDevotionalPlayer     │
      │   (ActivityKit / Dynamic Island│                     │    (AVFoundation Audio Stream) │
      └────────────────────────────────┘                     └────────────────────────────────┘
                      │                                                       │
                      ▼                                                       ▼
      ┌────────────────────────────────┐                     ┌────────────────────────────────┐
      │ Lock Screen Ambient Widget     │                     │ Spoken Prayer + Chant In-Ear   │
      │ (Distance, Relic, Station #)   │                     │ (Bilingual EN/VI Narration)    │
      └────────────────────────────────┘                     └────────────────────────────────┘
```

---

## 3. Core Engine Specifications

### 3.1 Proximity Geofencing Service (`PilgrimGeofenceManager.swift`)

The geofence manager registers circular monitoring zones around active route waypoints or nearest global sanctuaries.

#### Geofencing Strategy:
- **Active Pilgrimage Mode:** When the user selects "Begin Pilgrimage" on a specific route (e.g. *Our Lady of La Vang SoCal*), Anno registers `CLCircularRegion` monitors for all 5–13 sequential waypoints on that route.
- **Ambient World Mode:** When walking generally, Anno dynamically registers the top 10 geographically closest sanctuaries from `SacredGeographyLoader.shared`.
- **Battery Optimization:**
  - Uses `CLLocationManager.startMonitoring(for: region)` with 500m radius (`kCLLocationAccuracyHundredMeters`) while device is stationary or walking.
  - Switches to low-power `startMonitoringSignificantLocationChanges()` when between distant cities (>10 km away).

```swift
import CoreLocation
import Combine

public final class PilgrimGeofenceManager: NSObject, ObservableObject, CLLocationManagerDelegate {
    public static let shared = PilgrimGeofenceManager()
    
    private let locationManager = CLLocationManager()
    @Published public var activeStation: PilgrimageWaypoint?
    @Published public var activeSanctuary: Sanctuary?
    @Published public var proximityState: ProximityState = .outside
    @Published public var currentDistanceMeters: CLLocationDistance?

    public enum ProximityState {
        case outside
        case approaching(distanceMeters: Double) // 100m - 500m
        case insideSanctuary(stationNumber: Int) // < 100m
    }

    public override init() {
        super.init()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyHundredMeters
        locationManager.allowsBackgroundLocationUpdates = true
        locationManager.pausesLocationUpdatesAutomatically = true
        locationManager.activityType = .fitness // Optimized for walking pilgrimages
    }

    public func startRouteMonitoring(route: PilgrimageRoute) {
        // Clear previous monitored regions
        for region in locationManager.monitoredRegions {
            locationManager.stopMonitoring(for: region)
        }

        // Register waypoints (clamped to iOS 20-region limit)
        for wp in route.waypoints.prefix(15) {
            let center = wp.coordinate
            let region = CLCircularRegion(center: center, radius: 500, identifier: "WP_\(wp.id)")
            region.notifyOnEntry = true
            region.notifyOnExit = true
            locationManager.startMonitoring(for: region)
        }
    }
}
```

---

### 3.2 Dynamic Island & Lock Screen Live Activity (`PilgrimLiveActivity.swift`)

Anno utilizes `ActivityKit` to project ambient, liturgical station status onto the Lock Screen and Dynamic Island without requiring app unlocking.

#### Dynamic Island States:
1. **Compact Leading:** Gold Cross / Icon (`icon_st_columban.png` or `cross.fill`).
2. **Compact Trailing:** Distance countdown (e.g. `120m` or `Inside`).
3. **Expanded Banner:**
   - Station Order & Bilingual Name (*"Station 2: 117 Vietnamese Martyrs Memorial Wall"* / *"Bức Tường 117 Thánh Tử Đạo"*).
   - Sacred Relic Highlight (*"Contains original brick from 1798 La Vang Forest"*).
   - One-Tap Play Action: Triggers `AudioDevotionalPlayer` to stream the station's consecrated prayer.

```swift
import ActivityKit
import WidgetKit
import SwiftUI

public struct PilgrimCompanionAttributes: ActivityAttributes {
    public struct ContentState: Codable, Hashable {
        public var currentDistanceMeters: Double
        public var isInsideStation: Bool
        public var activeStationNameEn: String
        public var activeStationNameVi: String
        public var relicSummaryEn: String
        public var relicSummaryVi: String
        public var isAudioPlaying: Bool
    }

    public var routeTitleEn: String
    public var routeTitleVi: String
    public var totalStations: Int
    public var stationOrder: Int
}
```

---

### 3.3 Audio Player Geofence Hook (`AudioDevotionalPlayer+Geofence.swift`)

When the user enters the inner threshold ($< 100\text{m}$), the geofence service triggers an audio suggestion:

```swift
extension AudioDevotionalPlayer {
    public func playStationPrayer(waypoint: PilgrimageWaypoint, language: LanguageMode) {
        // Match audio file from Anno/Resources/Audio/
        let audioFileName = determineAudioFileName(for: waypoint.waypointId)
        guard let url = Bundle.main.url(forResource: audioFileName, withExtension: "mp3") else {
            // Fallback to text synthesis or ambient chant
            return
        }
        
        playLocalAudio(
            url: url,
            title: waypoint.name(for: language),
            subtitle: waypoint.sacredRelic(for: language)
        )
    }
}
```

---

## 4. User Interaction & Pilgrimage Passport Walkthrough

### 4.1 On-Site User Journey Example: Christ Cathedral La Vang Pilgrimage

```
                                  PILGRIM ENTERS CAMPUS (Garden Grove, CA)
                                                     │
                                                     ▼
                                    [ 500m GEOFENCE TRIGGER: Station 1 ]
                                    • Phone gently pulses with double haptic tap.
                                    • Lock Screen displays:
                                      "Approaching Our Lady of La Vang Shrine"
                                      "Đền Thờ Đức Mẹ La Vang (Christ Cathedral)"
                                                     │
                                                     ▼
                                    [ 100m INNER SANCTUARY THRESHOLD ]
                                    • Dynamic Island reveals gold Marian Halo.
                                    • Prompt: "🎧 Listen to Blessing of La Vang (3m 12s)"
                                    • Audio plays in-ear: Vietnamese/English prayer
                                      with background Gregorian Salve Regina.
                                                     │
                                                     ▼
                                    [ STATION COMPLETED: PASSPORT STAMPED ]
                                    • Digital Passport records: "Visited Aug 24, 2026 at 06:15 UTC"
                                    • Next Waypoint auto-activates: Station 2 (Martyrs Memorial Wall)
```

---

## 5. Offline Caching & Trail Doctrine

Ancient pilgrimage trails (e.g. *Camino de Santiago*, *Via Francigena mountain passes*, *Mount Sinai Ascent*) frequently lack cellular reception.

### Offline Resilience Invariants:
1. **Pre-Cached Vector Tiles & Routes:** Selecting "Begin Pilgrimage" downloads full JSON waypoints, offline satellite bounding box, and all MP3 prayer narrations to local app storage (`Library/Caches/PilgrimageOffline/`).
2. **Zero-Network Geofencing:** CoreLocation GPS hardware functions completely offline without cellular data.
3. **Bilingual Text Redundancy:** If audio assets are unavailable, the complete text, scripture reading, and pilgrim prayers are rendered locally from `sacred_geography_master.json`.

---

## 6. Privacy, Permissions & Battery Doctrine

### 6.1 Privacy & User Trust
- **Zero Location Telemetry:** GPS coordinates are evaluated **strictly on-device**. No user location is ever transmitted to remote servers or analytics providers.
- **Explicit Opt-In:** Background location is requested only when a user explicitly taps **"Begin Live Pilgrimage"** or enables **"Ambient Pilgrim Alerts"** in Settings.

### 6.2 iOS Info.plist Declarations
```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>Anno uses your location to show nearby sacred sanctuaries and guide you along pilgrimage walking routes.</string>

<key>NSLocationAlwaysAndWhenInUseUsageDescription</key>
<string>Anno uses background location to alert you when entering sacred pilgrimage stations and stream localized prayers without unlocking your phone.</string>

<key>UIBackgroundModes</key>
<array>
    <string>location</string>
    <string>audio</string>
</array>
```

---

## 7. Implementation Plan (3-Day Execution Milestone)

| Sprint / Day | Target Deliverable | Files & Services |
|---|---|---|
| **Day 1: CoreLocation Geofence Engine** | Implement `PilgrimGeofenceManager.swift`, circular region monitoring, and Xcode GPX trail simulation files. | `Anno/Services/PilgrimGeofenceManager.swift`, `tools/simulations/*.gpx` |
| **Day 2: ActivityKit Live Activity Widget** | Build Lock Screen & Dynamic Island views in SwiftUI with gold liturgical styling and distance countdowns. | `Anno/Widgets/PilgrimLiveActivity.swift`, `Anno/Widgets/PilgrimWidgetBundle.swift` |
| **Day 3: AVFoundation Audio & Passport Integration** | Wire auto-crossfade audio playback, background lock-screen controls, and persistent digital pilgrim passport stamps. | `Anno/Services/AudioDevotionalPlayer+Geofence.swift`, `Anno/Saved/PilgrimPassportView.swift` |

---

## 8. Xcode GPX Simulation Script (`christ_cathedral_pilgrimage.gpx`)

For automated testing in Xcode Simulator without physical travel:

```xml
<?xml version="1.0"?>
<gpx version="1.1" creator="Anno Sacred Geography Engine">
    <!-- Station 1: Approaching La Vang Shrine -->
    <wpt lat="33.7878" lon="-117.9783">
        <name>Our Lady of La Vang Shrine</name>
        <time>2026-08-24T06:00:00Z</time>
    </wpt>
    <!-- Station 2: Martyrs Wall -->
    <wpt lat="33.7878" lon="-117.9783">
        <name>117 Vietnamese Martyrs Memorial Wall</name>
        <time>2026-08-24T06:15:00Z</time>
    </wpt>
    <!-- Station 4: St. Columban Church -->
    <wpt lat="33.7706" lon="-117.9953">
        <name>St. Columban Church</name>
        <time>2026-08-24T06:45:00Z</time>
    </wpt>
    <!-- Station 5: St. Barbara Parish -->
    <wpt lat="33.7500" lon="-117.9650">
        <name>St. Barbara Parish Westminster</name>
        <time>2026-08-24T07:15:00Z</time>
    </wpt>
</gpx>
```
