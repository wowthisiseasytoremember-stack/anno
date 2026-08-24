import CoreLocation
import PilgrimCore
import XCTest

@testable import PilgrimCore

final class RegionSchedulerTests: XCTestCase {
    private func site(_ id: String, latitude: Double, longitude: Double) -> SanctuarySite {
        SanctuarySite(
            id: id,
            name: id,
            latitude: latitude,
            longitude: longitude,
            radiusMeters: 50,
            narrations: ["en": LocalizedNarration(audioFileName: "a", transcript: "t")]
        )
    }

    func testUnderBudgetEverythingIsScheduled() {
        let sites = [site("a", latitude: 0, longitude: 0), site("b", latitude: 1, longitude: 1)]
        let scheduler = RegionScheduler(budget: 20)
        XCTAssertEqual(scheduler.prioritySiteIDs(for: sites, near: nil), ["a", "b"])
    }

    func testOverBudgetWithoutLocationKeepsCatalogOrder() {
        let sites = (0..<25).map { site("site_\($0)", latitude: 0, longitude: 0) }
        let scheduler = RegionScheduler(budget: 20)
        let ids = scheduler.prioritySiteIDs(for: sites, near: nil)
        XCTAssertEqual(ids.count, 20)
        XCTAssertEqual(ids.first, "site_0")
    }

    func testOverBudgetWithLocationPrefersNearestSites() {
        // 25 sites spread along latitude; the pilgrim is nearest sites 20–24.
        let sites = (0..<25).map { site(String(format: "site_%02d", $0), latitude: Double($0), longitude: 0) }
        let here = CLLocation(latitude: 24.2, longitude: 0)

        let scheduler = RegionScheduler(budget: 20)
        let ids = scheduler.prioritySiteIDs(for: sites, near: here)

        XCTAssertEqual(ids.count, 20)
        XCTAssertEqual(Set(ids.first(5).map { Int($0.replacingOccurrences(of: "site_", with: "")) }),
                       Set(20...24),
                       "The five nearest sites must be scheduled")
    }

    func testTieBreakIsDeterministic() {
        let a = site("alpha", latitude: 10, longitude: 10)
        let b = site("beta", latitude: 10, longitude: 10)
        let scheduler = RegionScheduler(budget: 1)
        XCTAssertEqual(scheduler.prioritySiteIDs(for: [b, a], near: nil), ["alpha"])
        XCTAssertEqual(scheduler.prioritySiteIDs(for: [a, b], near: nil), ["alpha"])
    }
}
