import ARKit
import CoreLocation
import Foundation

/// Capability gate for future Anno pilgrimage AR.
///
/// Geotracking is outdoor-only, network-dependent, and unavailable at some
/// coordinates. Never make it the sole way to access station content.
enum AnnoPilgrimageARCapability {
    static var supportsWorldTracking: Bool {
        ARWorldTrackingConfiguration.isSupported
    }

    static var supportsGeoTrackingHardware: Bool {
        ARGeoTrackingConfiguration.isSupported
    }

    static func checkGeoTracking(
        at coordinate: CLLocationCoordinate2D,
        completion: @escaping (Bool) -> Void
    ) {
        guard supportsGeoTrackingHardware else {
            completion(false)
            return
        }

        ARGeoTrackingConfiguration.checkAvailability(at: coordinate) { available, _ in
            completion(available)
        }
    }

    static func makeGeoConfiguration() -> ARGeoTrackingConfiguration? {
        guard supportsGeoTrackingHardware else { return nil }

        let configuration = ARGeoTrackingConfiguration()
        configuration.planeDetection = [.horizontal]
        return configuration
    }
}
