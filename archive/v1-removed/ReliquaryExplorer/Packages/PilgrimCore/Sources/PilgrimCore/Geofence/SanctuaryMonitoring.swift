import CoreLocation
import Foundation

/// Whether proximity-triggered hagiography works on this platform/install.
///
/// - `available`: region monitoring is armed.
/// - `requiresAuthorization`: the feature needs the user to grant/upgrade
///   location permission (e.g. "Always" on iOS).
/// - `unsupported`: the platform cannot honor ambient geofencing at all
///   (visionOS build — see `MuseumModeSanctuaryMonitor` for the rationale).
public enum ProximityGuidanceAvailability: Equatable, Sendable {
    case available
    case requiresAuthorization(String)
    case unsupported(String)
}

/// A geofence transition for one sanctuary.
public struct SanctuaryVisitEvent: Equatable, Sendable {
    public enum Kind: Equatable, Sendable {
        case entered
        case exited
    }

    public let site: SanctuarySite
    public let kind: Kind
    public let timestamp: Date

    public init(site: SanctuarySite, kind: Kind, timestamp: Date = Date()) {
        self.site = site
        self.kind = kind
        self.timestamp = timestamp
    }
}

/// Platform seam for the proximity subsystem.
///
/// - **iOS/iPadOS**: `CoreLocationSanctuaryMonitor` implements this with
///   `CLLocationManager` region monitoring (background-capable, no
///   continuous GPS).
/// - **visionOS**: `MuseumModeSanctuaryMonitor` is an explicit no-op stub;
///   visionOS has no GNSS radio, no "Always" authorization tier, and no
///   ambulatory background-location execution model, so the shared UI
///   surfaces manual playback ("museum mode") instead.
///
/// Everything above this protocol (visit policy, audio, coordination, UI)
/// is shared and testable against a fake implementation.
@MainActor
public protocol SanctuaryMonitoring: AnyObject {
    /// Current availability; implementations keep this fresh.
    var availability: ProximityGuidanceAvailability { get }

    /// Stream of geofence transitions. Backed by an `AsyncStream` with a
    /// default buffering policy — consumers are expected to keep up; events
    /// are idempotent thanks to `VisitPolicy`.
    var events: AsyncStream<SanctuaryVisitEvent> { get }

    /// Arms monitoring for the catalog. Safe to call repeatedly; the
    /// implementation re-registers regions idempotently.
    func start(catalog: SanctuaryCatalog, lastKnownLocation: CLLocation?)

    /// Disarms monitoring entirely.
    func stop()

    /// Re-ranks monitored regions after the pilgrim has moved (used to
    /// swap distant regions out of the 20-region budget).
    func refresh(lastKnownLocation: CLLocation?)
}
