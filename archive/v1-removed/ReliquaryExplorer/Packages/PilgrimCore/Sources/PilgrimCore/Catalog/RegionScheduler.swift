import CoreLocation
import Foundation

/// Decides **which** sanctuary geofences are worth registering with
/// `CLLocationManager`, honoring the OS budget.
///
/// iOS allows an app to monitor at most **20 regions simultaneously**
/// (a hard `CLLocationManager` limit). Pilgrimage networks can exceed that,
/// so the scheduler keeps the `budget` regions nearest the pilgrim's last
/// known location registered and swaps them as the pilgrim moves. With no
/// known location it falls back to catalog order, which keeps behavior
/// deterministic for cold starts and for tests.
///
/// Pure logic — no `CLLocationManager` dependency — so it is directly
/// unit-testable and shared verbatim by any platform that ever gains
/// region monitoring.
public struct RegionScheduler: Sendable {
    /// The maximum number of regions iOS will monitor for one app.
    public static let systemRegionBudget = 20

    public let budget: Int

    public init(budget: Int = RegionScheduler.systemRegionBudget) {
        self.budget = max(0, budget)
    }

    /// The set of site IDs that should be registered, ordered by priority.
    public func prioritySiteIDs(
        for sites: [SanctuarySite],
        near location: CLLocation?
    ) -> [String] {
        guard sites.count > budget else {
            return sites.map(\.id)
        }

        guard let location else {
            return Array(sites.prefix(budget).map(\.id))
        }

        return sites
            .map { site -> (String, CLLocationDistance) in
                let destination = CLLocation(latitude: site.latitude, longitude: site.longitude)
                return (site.id, location.distance(from: destination))
            }
            .sorted { lhs, rhs in
                if lhs.1 != rhs.1 { return lhs.1 < rhs.1 }
                return lhs.0 < rhs.0 // deterministic tie-break
            }
            .prefix(budget)
            .map(\.0)
    }
}
