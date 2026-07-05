# Anno · Sacred Atlas & Pilgrim Mode Completion Plan
## Architectural Analysis, Component Deduplication, and Engineering Roadmap

This document provides a rigorous architectural audit of the 4 implementations of the **Sacred Atlas** and **Pilgrim Mode** features found within [/home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt). It details their structural boundaries, deduplicates overlapping components, evaluates them across key technical dimensions, and defines a unified hybrid implementation roadmap for production.

---

## 1. Implementation Boundaries & Architectural Patterns

### Implementation 1: The Early Multi-File Prototype
* **Boundary**: [Line 22 to Line 3013](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L22-L3013)
* **Components**:
  * Models: [Models.swift (L22-175)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L22-L175)
  * Mock Data: [MockData.swift (L176-654)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L176-L654)
  * Localization: [L10n.swift (L655-748)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L655-L748)
  * Visual Theme: [Theme.swift (L749-837)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L749-L837)
  * Location Manager & In-Memory Store: [Services.swift (L838-949)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L838-L949)
  * ViewModels: [AtlasViewModel.swift (L950-1130)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L950-L1130)
  * UI Views & Components: [SharedComponents.swift (L1131-1329)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L1131-L1329), [SacredAtlasView.swift (L1330-1873)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L1330-L1873), [LocationCardView.swift (L1874-2004)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L1874-L2004), [LocationDetailView.swift (L2005-2255)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L2005-L2255), [NearbyPanelView.swift (L2256-2348)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L2256-L2348), [RoutePackViews.swift (L2349-2610)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L2349-L2610), [PilgrimModeView.swift (L2611-2872)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L2611-L2872), [PassportView.swift (L2873-3013)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L2873-L3013)
* **Architectural Patterns**: Traditional multi-file SwiftUI MVVM pattern. It utilizes simple structs for domain models and relies on a centralized in-memory class [PilgrimSessionStore](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L893) for tracking pilgrim journey state. It contains no persistence layer (data is lost on relaunch) and features hardcoded string-based localizations. The implementation of views (such as `PassportView`'s notes tab) is incomplete and cut off.

### Implementation 2: The Monolithic Synthesis V1 (Visual & SwiftData Intro)
* **Boundary**: [Line 3014 to Line 5590](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L3014-L5590)
* **Components**: Single monolithic Swift file containing:
  * Localization Catalog: [L Catalog (L3048-3153)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L3048-L3153)
  * Visual Theme: [AnnoTheme (L3154-3204)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L3154-L3204)
  * Domain Models: [Models (L3226-3393)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L3226-L3393)
  * SwiftData Models: [JourneySession, FieldNote, PassportStamp (L3411-3473)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L3411-L3473)
  * Repository & Services: [SacredAtlasRepository & LocationService (L3474-3936)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L3474-M3936)
  * ViewModels: [SacredAtlasViewModel & JourneyViewModel (L3937-4149)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L3937-L4149)
  * Views: [SacredAtlasModuleView & Map/Detail/Route/Pilgrim Surfaces (L4150-5514)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L4150-L5514)
* **Architectural Patterns**: Monolithic MVVM-R. This approach introduces SwiftData for local persistence of the pilgrim passport, wraps core location tracking with a simulated route provider for testing, and leverages SwiftUI `@Observable` view models. The localization layer is upgraded to type-safe `LocalizedStringKey` tags.

### Implementation 3: The Monolithic Synthesis V2 (Interactive & Live Proximity)
* **Boundary**: [Line 5591 to Line 8308](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L5591-L8308)
* **Components**: Single monolithic Swift file containing:
  * Localization Catalog: [L Catalog (L5639-5733)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L5639-L5733)
  * Visual Theme: [AnnoTheme (L5734-5796)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L5734-L5796)
  * Domain Models: [Models (L5797-5958)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L5797-L5958)
  * SwiftData Models: [JourneySession, FieldNote, PassportStamp (L5959-6024)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L5959-L6024)
  * Repository & Services: [SacredAtlasRepository & LocationService (L6025-6499)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L6025-L6499)
  * ViewModels: [SacredAtlasViewModel & JourneyViewModel (L6500-6700)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L6500-L6700)
  * Views: [SacredAtlasMapView & Map/Detail/Route/Pilgrim Surfaces (L6701-8211)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L6701-L8211)
  * Previews: [PreviewHarness (L8212-8285)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L8212-L8285)
* **Architectural Patterns**: Monolithic MVVM-R. Iterates directly on Monolithic Synthesis V1. It integrates advanced UI mechanics including custom drawing (trim-based circular progress gauges), `SafariServices` sheet bridges for source citation viewing, and a core location-driven proximity check that shows a contextual `"On This Ground"` proximity banner when the user is within 100 meters of a sacred site. A specialized `PreviewHarness` injects an in-memory SwiftData container for Xcode previews.

### Implementation 4: The Production Multi-File Architecture
* **Boundary**: [Line 8309 to Line 14146](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L8309-L14146)
* **Components**: This section is divided into two distinct iterations:
  1. **Transitional Value-Type Architecture (L8309-10835)**:
     * Contains separate files: [AtlasModels.swift (L8547-8744)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L8547-L8744), [AnnoL10n.swift (L8745-8956)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L8745-L8956), [MockSacredAtlasRepository.swift (L8957-9257)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L8957-L9257), [SacredAtlasViewModel.swift (L9258-9486)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L9258-L9486), [Components.swift (L9487-9603)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L9487-L9603), [SacredAtlasView.swift (L9604-9926)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L9604-L9926), [LocationDetailView.swift (L9927-10131)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L9927-L10131), [RoutePacksView.swift (L10132-10258)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L10132-L10258), [PilgrimModeView.swift (L10259-10443)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L10259-L10443), [PilgrimPassportView.swift (L10444-10603)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L10444-L10603), [SacredAtlasPreviews.swift (L10604-10678)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L10604-L10678)
     * *Architectural Pattern*: Multi-file MVVM-R. Decouples state using protocol-oriented design (`SacredAtlasRepository`). It manages session records strictly using value-type structs (`JourneySession`, `JourneyVisit`, `JourneyNote`), lacking a persistence layer.
  2. **SwiftData-Integrated Production Architecture (L10836-14146)**:
     * Contains separate production-ready files: [AnnoTheme.swift (L10881-10995)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L10881-L10995), [Models.swift (L10996-11326)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L10996-L11326), [L.swift (L11327-11542)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L11327-L11542), [MockData.swift (L11543-12282)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L11543-L12282), [Services.swift (L12283-12462)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L12283-L12462), [ViewModels.swift (L12463-12795)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L12463-L12795), [Components.swift (L12796-13398)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L12796-L13398), [SacredAtlasView.swift (L13399-13711)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L13399-L13711), [LocationDetailView.swift (L13712-14146)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L13712-L14146)
     * *Architectural Pattern*: Clean, production-grade modular MVVM-R. Resolves structural coupling by isolating logic into distinct files. It integrates SwiftData `@Model` classes (`Journey`, `Visit`, `FieldNote`) with cascading delete rules and proper transaction routing, utilizes decoupled location management (supporting coordinate simulation), implements granular entitlement mappings, and provides a polished multi-tab UI.

---

## 2. Component Deduplication

Across the four implementations, there are significant overlaps in domain logic, models, view models, and views. The variations must be consolidated to define the production codebase.

### 2.1 Models (Domain & Persistence)
* **Tradition Enum**:
  * *Prototypes & V1/V2/V3*: Simple enum (`catholic`, `orthodox`, `jewish`, `islamic`, `interfaith`).
  * *Production Variant (L11004)*: Adds hexadecimal color mappings (`color` property returning strings like `"E8D5A3"`) and Unicode symbols (`symbol` property returning symbols like `✝` or `☦`) to enable server-driven map marker rendering.
* **Confidence Enum**:
  * *V1/V2/V3*: Named `Confidence` ([Line 3263](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L3263)).
  * *Production (L11035)*: Named `ConfidenceLabel` to prevent collisions with foundation libraries. Integrates localized key bindings (`L10nKey`).
* **Sacred Location**:
  * *V1/V2/V3*: [SacredLocation (L3314)](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L3314) uses `String` identifiers, holds an optional `artworkID`, and links a list of sources.
  * *Production (L11100)*: Renamed categories to `[SacredSiteCategory]` (introducing specific cases like `saints`, `martyrs`, `relics`). Adds `onThisGroundNarrative` (for proximity alerts) and `isTodayConnected` (to drive the calendar/liturgical event engine).
* **SwiftData Models**:
  * *V1/V2/V3*: Defines `JourneySession` ([Line 3413](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L3413)), `FieldNote`, and `PassportStamp`.
  * *Production (L11241)*: Simplifies naming to `Journey`, `Visit` (replacing `PassportStamp`), and `FieldNote`. Links relationships bidirectionally with inverse cascades.
  * *Sigil Variation*: Monolithic Synthesis V2 introduces `localizedStampCode` generation logic inside the stamp initializer (`"SIGIL-\(Int.random(in: 1000...9999))-\(String(location.name.prefix(3).uppercased()))"`).

### 2.2 ViewModels
* **SacredAtlasViewModel**:
  * *V1/V2/V3*: Manages map coordinate ranges, filtering arrays, and active location selection state.
  * *Production (L12464)*: Introduces cleaner protocol integration, loading mock data via `SacredAtlasRepository`. Coordinates the calendar sub-system and filters locations dynamically based on active map style layer flags.
* **JourneyViewModel**:
  * *V1/V2/V3 (L4069)*: Bound to SwiftData contexts, managing active sessions and appending stamps.
  * *Production (L12403)*: Integrates with `CLLocationManager` updates, checking user distance to next stops, verifying active pilgrimage bounds, and handling transaction commit/rollback points.

### 2.3 Services
* **Location Manager**:
  * *Prototypes*: Implements a direct standard CoreLocation delegate ([Line 847](file:///home/ichabod/Downloads/Anno_Sacred_Atlas_Product_Plan_Dump.txt#L847)).
  * *Production (L12294)*: Named `AnnoLocationManager`. Supports location simulation hooks, allowing test coordinate tracks to mock pilgrimage walks in Simulator environments.
* **Entitlement Service**:
  * *V1/V2/V3 (L3934)*: Checked tier levels directly within the UI components.
  * *Production (L12338)*: Isolates gating logic into a service interface `EntitlementService` checking properties like `canStartPilgrimage` and `canSaveUnlimited`, decoupling views from App Store transaction models.

### 2.4 Views & UI Components
* **Map Pin View**:
  * *Prototype*: Basic marker pin.
  * *Monolithic V2 (L4322)*: Implements a custom bezier `TeardropShape` and draws tradition symbols inside it.
* **Detail Card / Proximity Banners**:
  * *Monolithic V2 (L6925)*: Adds a live proximity layout (`"On This Ground"`) when user is close to a site.
* **Progress Ring**:
  * *Monolithic V2 (L7050)*: Implements a custom SwiftUI `ProgressRing` view using stroke trimming.

---

## 3. Implementation Comparison Rubric

| Dimension | Implementation 1 (Prototype) | Implementation 2 (Monolithic V1) | Implementation 3 (Monolithic V2) | Implementation 4 (Production Multi-File) |
| :--- | :--- | :--- | :--- | :--- |
| **Completeness** | **Low**: Missing SwiftData schemas. Passport and field note views are incomplete and cut off. | **Medium**: Features basic map, detail cards, and in-app paywall, but lacks advanced details. | **High**: Contains complete map, detail card, route list, pilgrim mode HUD, and working stamps grid. | **Very High**: All features are implemented in separate files with modular folder architecture. |
| **SwiftData / Persistence** | **None**: Keeps all session records in-memory via `PilgrimSessionStore`. | **Basic**: Defines `JourneySession`, `FieldNote`, and `PassportStamp` schemas. | **Polished**: Adds random sigil code generation inside the persistent stamp schema. | **Production-Grade**: Features bidirectional relationships (`Journey` ↔ `Visit` ↔ `FieldNote`) with cascading deletes. |
| **SwiftUI State Design** | **Basic**: Classic `@Observable` usage. Hardcoded coordinate maps. | **Standard**: Modern `@Observable` view models with simple dependency injection. | **Advanced**: Adds custom drawing (`TeardropShape`, `ProgressRing`), and `SFSafariViewController` sheet wrappers. | **Production-Ready**: Decouples UI from business logic using protocols. Leverages `@Bindable` bindings. |
| **Entitlements / Gating** | **Low**: Performs inline tier evaluations inside SwiftUI views. | **Medium**: Standardizes `EntitlementTier` and `EntitlementService` semantic accessors. | **High**: Integrates a QA tier switcher widget directly into views and previews. | **Production-Ready**: Uses clean semantic gates mapped to explicit feature flags. |
| **Localization** | **Static Enum**: Relies on static string properties. Vietnamese translations are comments only. | **LocalizedStringKey**: Uses localization keys mapped to a centralized catalog enum `L`. | **LocalizedStringKey**: Inherits catalog keys from V1. | **Type-Safe Catalog**: Implements localized keys backed by localized string resources. |

---

## 4. Strengths, Weaknesses, and Unique Contributions

### Implementation 1: The Early Multi-File Prototype
* **Strengths**: High-fidelity modular files; maps out a clear conceptual division of views.
* **Weaknesses**: Incomplete code (cut off); lacks a persistent database layer; localization is hardcoded.
* **Unique Contribution**: Established the initial domain boundaries for the feature set and defined the early mock data structure.

### Implementation 2: The Monolithic Synthesis V1
* **Strengths**: Unified structure; first implementation of SwiftData schemas; robust entitlement gates.
* **Weaknesses**: The code is contained in a single large file, which increases cognitive load and complicates code reviews.
* **Unique Contribution**: Introduced the custom `TeardropShape` map marker and designed data-driven paywall cards.

### Implementation 3: The Monolithic Synthesis V2
* **Strengths**: Outstanding UX design elements; interactive proximity alerts; Xcode preview testing harness.
* **Weaknesses**: Tight coupling of view layouts and services within a single monolithic file.
* **Unique Contribution**: Created the `"On This Ground"` live location banner, `SafariServices` integration, and cryptographic stamp sigils.

### Implementation 4: The Production Multi-File Architecture
* **Strengths**: Professional file separation; clean protocol-based repository decoupling; production-grade database relations.
* **Weaknesses**: Higher initial boilerplate overhead; requires structured environment injection.
* **Unique Contribution**: Production-ready code structure with robust relationship bindings and clean dependency management.

---

## 5. Unified Hybrid Recommendation

To deliver a high-quality implementation of the **Sacred Atlas** feature for Anno, we recommend a **hybrid architecture** that combines the modular, protocol-driven foundation of **Implementation 4** with the advanced UX enhancements of **Implementation 3**.

### 5.1 Architecture Diagram
The following diagram illustrates the relationship between views, view models, database engines, and core location systems:

```mermaid
graph TD
    subgraph View Layer [SwiftUI Views]
        V_Map[SacredAtlasView]
        V_Detail[LocationDetailView]
        V_Pilgrim[PilgrimModeView]
        V_Passport[PilgrimPassportView]
    end

    subgraph Business Logic [ViewModels & Theme]
        VM_Atlas[SacredAtlasViewModel]
        VM_Journey[JourneyViewModel]
        Theme[AnnoTheme]
    end

    subgraph Data & Services [Core Engines]
        R_Repo[SacredAtlasRepository]
        S_Loc[AnnoLocationManager]
        S_Ent[EntitlementService]
        DB_Context[SwiftData ModelContext]
    end

    subgraph Database [Local Storage]
        M_Journey[Journey Model]
        M_Visit[Visit Model]
        M_Note[FieldNote Model]
    end

    %% Interactions
    V_Map --> VM_Atlas
    V_Detail --> VM_Atlas
    V_Pilgrim --> VM_Journey
    V_Passport --> VM_Journey
    
    VM_Atlas --> R_Repo
    VM_Journey --> DB_Context
    VM_Journey --> S_Loc
    
    V_Map -.-> S_Ent
    V_Pilgrim -.-> S_Ent
    
    DB_Context <--> M_Journey
    M_Journey -->|Cascades| M_Visit
    M_Journey -->|Cascades| M_Note
    
    Theme -.-> View Layer
```

### 5.2 Folder Structure

We recommend placing the code files in the following directory layout under the Anno project's root:

```text
Anno/
└── Features/
    └── SacredAtlas/
        ├── Models/
        │   ├── AtlasModels.swift         // Pure domain models (SacredLocation, SacredEvent, Artwork, RoutePack)
        │   └── Schema/
        │       ├── Journey.swift         // SwiftData @Model for Pilgrim journey sessions
        │       ├── Visit.swift           // SwiftData @Model for visited site records
        │       └── FieldNote.swift       // SwiftData @Model for pilgrim reflections
        ├── ViewModels/
        │   ├── SacredAtlasViewModel.swift // Coordinates map viewport, filters, and selected cards
        │   └── JourneyViewModel.swift    // Coordinates active pilgrimages, proximity checks, and SwiftData commits
        ├── Services/
        │   ├── AnnoLocationManager.swift // Location manager with simulation support
        │   └── EntitlementService.swift  // Subscription status checker
        ├── Views/
        │   ├── SacredAtlasView.swift     // Map view with filters and detail sheets
        │   ├── LocationDetailView.swift  // Detail sheet for sites, events, artworks, and sources
        │   ├── PilgrimModeView.swift     // Active HUD guiding the pilgrim between stops
        │   ├── PilgrimPassportView.swift // Visited site grid with sigils and note reviews
        │   └── Components/
        │       ├── TeardropShape.swift   // Bezier map pin shape
        │       ├── ProgressRing.swift    // Trim-based radial progress ring
        │       └── SafariView.swift      // SFSafariViewController wrapper
        └── Infrastructure/
            ├── AnnoTheme.swift           // Parchment/Gold visual styling token declarations
            ├── L.swift                   // Localization key registry
            └── MockSacredAtlasRepository.swift // Mock data repository loading JSON fixtures
```

### 5.3 Technical Specifications for Key Components

#### A. Database Schema
Use the production-ready schemas from **Implementation 4**, but incorporate the cryptographic sigil stamp generator from **Implementation 3**:

```swift
import Foundation
import SwiftData

@Model
final class Journey {
    @Attribute(.unique) var id: UUID = UUID()
    var startDate: Date = Date()
    var endDate: Date?
    var routePackID: String?
    var routePackTitle: String?
    var statusRaw: String = JourneyStatus.active.rawValue
    var totalDistanceWalked: Double = 0.0

    @Relationship(deleteRule: .cascade) var visits: [Visit] = []
    @Relationship(deleteRule: .cascade) var notes: [FieldNote] = []

    init(routePackID: String? = nil, routePackTitle: String? = nil) {
        self.id = UUID()
        self.startDate = Date()
        self.routePackID = routePackID
        self.routePackTitle = routePackTitle
    }
}

@Model
final class Visit {
    @Attribute(.unique) var id: UUID = UUID()
    var locationID: String = ""
    var placeName: String = ""
    var traditionRaw: String = ""
    var arrivalDate: Date = Date()
    var stampCode: String = "" // Injected from Monolithic V2
    var latitude: Double = 0.0
    var longitude: Double = 0.0

    init(locationID: String, placeName: String, tradition: String, latitude: Double, longitude: Double) {
        self.id = UUID()
        self.locationID = locationID
        self.placeName = placeName
        self.traditionRaw = tradition
        self.latitude = latitude
        self.longitude = longitude
        self.arrivalDate = Date()
        self.stampCode = "SIGIL-\(Int.random(in: 1000...9999))-\(String(placeName.prefix(3).uppercased()))"
    }
}
```

#### B. Proximity Detection System
Integrate the live proximity detection banner from **Implementation 3**. The `AnnoLocationManager` reports location changes to the `JourneyViewModel`. If the distance to any site is less than 100 meters, the banner is displayed:

```swift
// Added to JourneyViewModel.swift
func evaluateProximity(to locations: [SacredLocation], currentCoordinate: CLLocationCoordinate2D) {
    if let closest = locations.first(where: { loc in
        let distance = loc.distance(from: currentCoordinate)
        return distance < 100.0 // 100 meters
    }) {
        self.proximitySite = closest
    } else {
        self.proximitySite = nil
    }
}
```

#### C. Type-Safe Localization with Vietnamese Fallback
Ensure all UI strings pass through the `L` localization registry. In production, connect this to `Localizable.xcstrings`:

```swift
// L.swift
import SwiftUI

enum L {
    static let sacredAtlas       = LocalizedStringKey("anno.section.sacredAtlas")
    static let pilgrimMode       = LocalizedStringKey("anno.section.pilgrimMode")
    static let routePacks        = LocalizedStringKey("anno.section.routePacks")
    static let passport          = LocalizedStringKey("anno.section.passport")
    static let onThisGround      = LocalizedStringKey("anno.section.onThisGround")
    static let stamps            = LocalizedStringKey("anno.section.stamps")
    static let confirmed         = LocalizedStringKey("anno.confidence.confirmed")
    static let traditional       = LocalizedStringKey("anno.confidence.traditional")
    static let disputed          = LocalizedStringKey("anno.confidence.disputed")
}
```

---

## 6. Resolved Design Decisions

See `SACRED_ATLAS_DECISIONS.md` in this directory for the complete resolution
of all divergences across the 4 implementation options. Key outcomes:

| Decision | Resolution |
|----------|------------|
| Foundation | Option 4 (Production Multi-File, lines 10836-14146) |
| Entitlement model | 3-tier (`free`/`premium`/`pilgrim`) from Opt4 with semantic accessors |
| Confidence naming | `ConfidenceLabel` to avoid Foundation collision |
| Map pins | `SacredPinView` — drop `TeardropShape` |
| SwiftData IDs | Add `@Attribute(.unique)` to Journey.id and Visit.id |
| SwiftData naming | `Journey` → `Visit` → `FieldNote` (Opt4) |
| Stamp sigils | Import from Opt3 |
| Proximity | Opt4's implementation is the most complete (30 refs) |
| Progress | Both `ProgressRing` (visual) + `JourneyProgressView` (layout) |
| SafariView | Import from Opt3 |
| PreviewHarness | Import from Opt3, adapt to 3-tier |
| Missing views | PilgrimModeView, PilgrimPassportView, RoutePacks — extract from Opt3 |
| File structure | Plan's §5.2 folder layout |

## 7. Verification and Deployment Steps

1. **Database Schema Integration**: Create the SwiftData model container in the App initialization block:
   ```swift
   .modelContainer(for: [Journey.self, Visit.self, FieldNote.self])
   ```
2. **Xcode Preview Validation**: Embed the `PreviewHarness` from Monolithic Synthesis V2 in preview files to verify view layouts across all entitlement levels.
3. **CoreLocation Simulation Audits**: Use the location simulation hooks to verify the `"On This Ground"` banner displays correctly when crossing geo-fences.
4. **Localization Resource Bundling**: Verify that all `LocalizedStringKey` keys are defined in both English and Vietnamese localizable string files.
