import CoreLocation
import Foundation

/// Staged modern iBeacon monitor using Core Location condition monitoring.
///
/// Deploy only at sites that explicitly agree to host beacon hardware.
/// QR remains the guaranteed field-test fallback.
@available(iOS 17.0, *)
@MainActor
final class AnnoPilgrimageBeaconMonitor {
    static let shared = AnnoPilgrimageBeaconMonitor()

    private var monitor: CLMonitor?
    private var eventTask: Task<Void, Never>?

    private init() {}

    func start(
        beaconUUID: UUID,
        major: UInt16,
        stationByMinor: [UInt16: String],
        onArrival: @escaping @MainActor (String) -> Void
    ) {
        stop()

        eventTask = Task {
            let monitor = await CLMonitor("anno.pilgrimage.beacons")
            self.monitor = monitor

            for (minor, stationId) in stationByMinor {
                let condition = CLMonitor.BeaconIdentityCondition(
                    uuid: beaconUUID,
                    major: major,
                    minor: minor
                )

                monitor.add(
                    condition,
                    identifier: stationId
                )
            }

            do {
                for try await event in monitor.events {
                    guard !Task.isCancelled else { return }

                    if event.state == .satisfied {
                        Haptics.sacredArrival(.feast)
                        onArrival(event.identifier)
                    }
                }
            } catch {
                #if DEBUG
                print("Anno beacon monitor failed: \(error)")
                #endif
            }
        }
    }

    func stop() {
        eventTask?.cancel()
        eventTask = nil
        monitor = nil
    }
}
