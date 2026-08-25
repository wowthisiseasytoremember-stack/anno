//  ReliquaryBridge.swift
//  Anno
//
//  Bridges Anno's domain models to PilgrimCore so the AR Reliquary Viewer and
//  geofenced hagiography engine can be hosted inside Anno once the
//  `ReliquaryExplorer/Packages/PilgrimCore` package is added as a dependency.
//
//  Guarded by `canImport(PilgrimCore)` so this file compiles to nothing on
//  platforms / build configs where the package is not yet linked (e.g. Linux
//  CI or before the Xcode/macOS integration step). When the dependency is
//  present the extensions activate automatically.

#if canImport(PilgrimCore)
import Foundation
import CoreLocation
import PilgrimCore

extension Sanctuary {
    /// The 3D reliquary associated with this sanctuary, if any.
    /// Uses Anno's real key `associated3DReliquaryId` (the integration spec's
    /// `primaryRelicId` does not exist on this model).
    public var associatedReliquary: ReliquaryItem? {
        associated3DReliquaryId.flatMap { ReliquaryItem.item(withID: $0) }
    }

    /// Best-effort mapping to PilgrimCore's `SanctuarySite` for geofenced audio.
    /// NOTE: PilgrimCore's `SanctuaryCatalog.validated()` rejects sites whose
    /// `narrations` are empty — hagiography audio + transcripts must be authored
    /// for each Anno sanctuary before enabling geofenced narration in production.
    public var asPilgrimSite: SanctuarySite? {
        SanctuarySite(
            id: sanctuaryId,
            name: nameEn,
            latitude: location.latitude,
            longitude: location.longitude,
            radiusMeters: 120,
            associatedReliquaryId: associated3DReliquaryId,
            narrations: [
                "en": LocalizedNarration(audioFileName: "", transcript: historicalSummaryEn),
                "vi": LocalizedNarration(audioFileName: "", transcript: historicalSummaryVi)
            ]
        )
    }
}

extension PilgrimageWaypoint {
    /// The 3D reliquary associated with this waypoint, if any.
    public var associatedReliquary: ReliquaryItem? {
        associated3DReliquaryId.flatMap { ReliquaryItem.item(withID: $0) }
    }
}
#endif
