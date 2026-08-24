import CoreLocation
import Foundation
import OSLog
import PilgrimCore

/// visionOS implementation of `SanctuaryMonitoring`: an **explicit no-op**.
///
/// Decision and rationale (stated deliberately, not hidden):
///
/// 1. **No GNSS.** Vision Pro has no GPS radio; Wi-Fi positioning is not
///    accurate enough for sanctuary-scale geofences.
/// 2. **No "Always" authorization tier.** visionOS CoreLocation offers
///    when-in-use only, so background region events — the entire premise
///    of the pilgrim guide — cannot be authorized.
/// 3. **No ambulatory background execution.** visionOS apps are suspended
///    when not frontmost; there is no `UIBackgroundModes`-equivalent
///    long-running location lane. A stub that *pretends* to monitor would
///    drain the (tethered/battery) device while never firing reliably.
///
/// So this build **gracefully no-ops the monitoring protocol** and exposes
/// `sitesForManualInspection` for the shared "museum mode" UI (map +
/// manual narration), which delivers the same audio hagiographies on the
/// user's terms. `availability` reports `.unsupported` with a
/// user-comprehensible reason so Settings explains itself honestly.
@MainActor
public final class MuseumModeSanctuaryMonitor: SanctuaryMonitoring {
    public let events: AsyncStream<SanctuaryVisitEvent>

    public private(set) var sitesForManualInspection: [SanctuarySite] = []
    private let logger = Logger(subsystem: PilgrimCoreLog.subsystem, category: "VisionGeofenceStub")

    private let continuation: AsyncStream<SanctuaryVisitEvent>.Continuation

    public init() {
        var localContinuation: AsyncStream<SanctuaryVisitEvent>.Continuation!
        events = AsyncStream { localContinuation = $0 }
        continuation = localContinuation
    }

    public var availability: ProximityGuidanceAvailability {
        .unsupported(
            reason: "Apple Vision Pro is not designed for ambulatory GPS pilgrimage; "
                + "browse sanctuaries on the map and play their hagiographies manually."
        )
    }

    public func start(catalog: SanctuaryCatalog, lastKnownLocation: CLLocation?) {
        sitesForManualInspection = catalog.sites
        logger.info(
            "Museum mode: \(catalog.sites.count) sanctuaries available for manual inspection (no geofencing)."
        )
    }

    public func stop() {
        sitesForManualInspection = []
    }

    public func refresh(lastKnownLocation: CLLocation?) {
        // Intentionally unimplemented: nothing to re-rank without monitoring.
    }

    /// Demo/QA affordance: synthesize an arrival so the full pipeline
    /// (coordinator → audio) can be exercised on visionOS without GPS.
    public func simulateArrival(at site: SanctuarySite) {
        continuation.yield(SanctuaryVisitEvent(site: site, kind: .entered))
    }
}
