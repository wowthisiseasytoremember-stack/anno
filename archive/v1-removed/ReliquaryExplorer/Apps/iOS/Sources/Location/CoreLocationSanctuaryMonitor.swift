import CoreLocation
import Foundation
import OSLog
import PilgrimCore

/// iOS/iPadOS implementation of `SanctuaryMonitoring` using
/// **CLLocationManager region monitoring** — hardware/baseband-assisted
/// geofencing with zero CPU while the pilgrim walks between sites.
/// Deliberately *not* `startUpdatingLocation()` polling.
///
/// Key behaviors:
/// - Requests Always authorization; supports the iOS 13.4+ two-step
///   flow (When-In-Use first, then Always) so the user sees the honest
///   upgrade path. Region monitoring functions under provisional Always.
/// - Honors the 20-region budget via `RegionScheduler`, re-ranking when
///   significant location changes arrive.
/// - Uses `startMonitoringSignificantLocationChanges()` (~cell/Wi-Fi
///   granularity, not GPS polling) purely to re-rank regions and persist
///   the last known location for cold-start ranking.
/// - Region events delivered while suspended relaunch the app; the app's
///   `scenePhase` hook re-arms monitoring after such wakes.
///
/// Delegate callbacks arrive on the main thread; this class is
/// `@MainActor` and hops through `MainActor.assumeIsolated` in the
/// nonisolated `CLLocationManagerDelegate` entry points.
@MainActor
public final class CoreLocationSanctuaryMonitor: NSObject, SanctuaryMonitoring {
    public let events: AsyncStream<SanctuaryVisitEvent>

    /// App-provided sink for significant location changes (persistence
    /// + region re-ranking lives in the coordinator).
    public var onSignificantLocationChange: ((CLLocation) -> Void)?

    private let locationManager = CLLocationManager()
    private let scheduler = RegionScheduler()
    private let continuation: AsyncStream<SanctuaryVisitEvent>.Continuation

    private var sites: [SanctuarySite] = []
    private var sitesByID: [String: SanctuarySite] = [:]
    private var wantsMonitoring = false
    private var didStartSignificantChanges = false
    private var hasEmittedAvailability = false

    public init(onSignificantLocationChange: ((CLLocation) -> Void)? = nil) {
        var localContinuation: AsyncStream<SanctuaryVisitEvent>.Continuation!
        events = AsyncStream { localContinuation = $0 }
        continuation = localContinuation
        self.onSignificantLocationChange = onSignificantLocationChange
        super.init()
        locationManager.delegate = self
        locationManager.activityType = .fitness
    }

    // MARK: - Availability

    public var availability: ProximityGuidanceAvailability {
        let auth = locationManager.authorizationStatus
        let monitoringSupported = CLLocationManager.isMonitoringAvailable(for: CLCircularRegion.self)

        switch auth {
        case .authorizedAlways:
            return monitoringSupported
                ? .available
                : .unsupported(reason: "Region monitoring is unavailable on this device.")
        case .authorizedWhenInUse:
            return .requiresAuthorization(
                "Upgrade location to “Always” so narration can begin while the app is in the background."
            )
        case .notDetermined:
            return .requiresAuthorization("Allow location access to arm sanctuary narration.")
        case .denied, .restricted:
            return .unsupported(
                reason: "Location access is denied. Enable it in Settings to arm sanctuary narration."
            )
        @unknown default:
            return .unsupported(reason: "Location authorization state unknown.")
        }
    }

    // MARK: - SanctuaryMonitoring

    public func start(catalog: SanctuaryCatalog, lastKnownLocation: CLLocation?) {
        sites = catalog.sites
        sitesByID = Dictionary(uniqueKeysWithValues: catalog.sites.map { ($0.id, $0) })
        wantsMonitoring = true

        if locationManager.authorizationStatus == .notDetermined {
            // iOS 13.4+: asking When-In-Use first, then Always, presents
            // the explicit Always upgrade (no provisional limbo).
            locationManager.requestWhenInUseAuthorization()
        } else {
            armRegions(near: lastKnownLocation)
        }
        armAvailabilityRebroadcast()
    }

    public func stop() {
        wantsMonitoring = false
        sites = []
        sitesByID = [:]
        locationManager.monitoredRegions.forEach { locationManager.stopMonitoring(for: $0) }
        if didStartSignificantChanges {
            locationManager.stopMonitoringSignificantLocationChanges()
            didStartSignificantChanges = false
        }
        PilgrimCoreLog.geofence.info("Sanctuary region monitoring stopped.")
    }

    public func refresh(lastKnownLocation: CLLocation?) {
        guard wantsMonitoring else { return }
        armRegions(near: lastKnownLocation)
    }

    // MARK: - Region arming

    /// Diff-based (de)registration; re-arming is idempotent.
    private func armRegions(near location: CLLocation?) {
        guard case .available = availability else { return }
        guard CLLocationManager.isMonitoringAvailable(for: CLCircularRegion.self) else { return }

        let desiredIDs = Set(scheduler.prioritySiteIDs(for: sites, near: location))
        let currentIDs = Set(locationManager.monitoredRegions.map(\.identifier))

        for stale in currentIDs.subtracting(desiredIDs) {
            if let region = locationManager.monitoredRegions.first(where: { $0.identifier == stale }) {
                locationManager.stopMonitoring(for: region)
            }
        }

        for siteID in desiredIDs.subtracting(currentIDs) {
            guard let site = sitesByID[siteID] else { continue }
            let region = CLCircularRegion(
                center: site.coordinate,
                radius: site.radiusMeters,
                identifier: site.id
            )
            // Exits matter: they re-arm the visit policy and trigger
            // region re-ranking.
            region.notifyOnEntry = true
            region.notifyOnExit = true
            locationManager.startMonitoring(for: region)
            PilgrimCoreLog.geofence.info("Monitoring sanctuary geofence: \(site.name)")
        }

        // Low-power companion: gives us occasional fixes for re-ranking
        // (and persists a cold-start location via the app's callback).
        if !didStartSignificantChanges,
           locationManager.authorizationStatus == .authorizedAlways {
            locationManager.startMonitoringSignificantLocationChanges()
            didStartSignificantChanges = true
        }
    }

    private func armAvailabilityRebroadcast() {
        // Availability is UI-visible; emit an event-equivalent heartbeat
        // by touching authorization once per start (cheap no-op).
        _ = locationManager.authorizationStatus
        hasEmittedAvailability = true
    }

    // MARK: - Event emission

    private func emit(_ site: SanctuarySite, _ kind: SanctuaryVisitEvent.Kind) {
        continuation.yield(SanctuaryVisitEvent(site: site, kind: kind))
    }
}

// MARK: - CLLocationManagerDelegate

extension CoreLocationSanctuaryMonitor: CLLocationManagerDelegate {
    public nonisolated func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        MainActor.assumeIsolated {
            switch manager.authorizationStatus {
            case .authorizedAlways:
                armRegions(near: nil)
            case .authorizedWhenInUse:
                // iOS 13.4+ two-step flow: now that When-In-Use is
                // granted, explicitly request the Always upgrade so the
                // background narration path is honestly consented to
                // (provisional Always would technically work, but the
                // explicit prompt is the right UX and the review-safe
                // path). The system only ever shows this prompt once;
                // later calls are silent no-ops.
                if wantsMonitoring, !didRequestAlwaysUpgrade {
                    didRequestAlwaysUpgrade = true
                    manager.requestAlwaysAuthorization()
                }
                armRegions(near: nil)
            default:
                break
            }
        }
    }

    public nonisolated func locationManager(_ manager: CLLocationManager, didEnterRegion region: CLRegion) {
        MainActor.assumeIsolated {
            guard let site = sitesByID[region.identifier] else { return }
            PilgrimCoreLog.geofence.info("Entered sanctuary region: \(site.name)")
            emit(site, .entered)
        }
    }

    public nonisolated func locationManager(_ manager: CLLocationManager, didExitRegion region: CLRegion) {
        MainActor.assumeIsolated {
            guard let site = sitesByID[region.identifier] else { return }
            PilgrimCoreLog.geofence.info("Exited sanctuary region: \(site.name)")
            emit(site, .exited)
            // Boundary crossings are a good moment to re-rank the 20
            // monitored regions.
            refresh(lastKnownLocation: nil)
        }
    }

    public nonisolated func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        MainActor.assumeIsolated {
            guard let latest = locations.last, latest.horizontalAccuracy >= 0 else { return }
            onSignificantLocationChange?(latest)
        }
    }

    public nonisolated func locationManager(
        _ manager: CLLocationManager,
        monitoringDidFailFor region: CLRegion?,
        withError error: Error
    ) {
        MainActor.assumeIsolated {
            PilgrimCoreLog.geofence.error(
                "Region monitoring failed for \(region?.identifier ?? "nil"): \(error.localizedDescription)"
            )
        }
    }
}
