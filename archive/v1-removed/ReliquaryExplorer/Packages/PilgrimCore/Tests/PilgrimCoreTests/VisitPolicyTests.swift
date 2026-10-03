import PilgrimCore
import XCTest

@testable import PilgrimCore

final class VisitPolicyTests: XCTestCase {
    private let site = SanctuarySite(
        id: "santiago",
        name: "Santiago",
        latitude: 42.88,
        longitude: -8.54,
        radiusMeters: 60,
        narrations: ["en": LocalizedNarration(audioFileName: "a", transcript: "t")]
    )

    private func event(
        _ kind: SanctuaryVisitEvent.Kind,
        at seconds: TimeInterval
    ) -> SanctuaryVisitEvent {
        SanctuaryVisitEvent(
            site: site,
            kind: kind,
            timestamp: Date(timeIntervalSince1970: seconds)
        )
    }

    func testFirstEntryPlays() {
        var policy = VisitPolicy(cooldown: 600)
        XCTAssertEqual(policy.register(event(.entered, at: 0)), .play)
    }

    func testRepeatEntryWithinCooldownIsSkipped() {
        var policy = VisitPolicy(cooldown: 600)
        XCTAssertEqual(policy.register(event(.entered, at: 0)), .play)
        XCTAssertEqual(policy.register(event(.exited, at: 60)), .skip(.exited))
        XCTAssertEqual(policy.register(event(.entered, at: 120)), .skip(.cooldownActive))
    }

    func testReturnAfterCooldownPlaysAgain() {
        var policy = VisitPolicy(cooldown: 600)
        XCTAssertEqual(policy.register(event(.entered, at: 0)), .play)
        XCTAssertEqual(policy.register(event(.exited, at: 300)), .skip(.exited))
        XCTAssertEqual(policy.register(event(.entered, at: 700)), .play)
    }

    func testDuplicateEntryWithoutExitIsSkipped() {
        var policy = VisitPolicy(cooldown: 600)
        XCTAssertEqual(policy.register(event(.entered, at: 0)), .play)
        XCTAssertEqual(policy.register(event(.entered, at: 1)), .skip(.alreadyInside))
    }

    func testSitesAreIndependent() {
        let other = SanctuarySite(
            id: "assisi",
            name: "Assisi",
            latitude: 43.07,
            longitude: 12.39,
            radiusMeters: 70,
            narrations: ["en": LocalizedNarration(audioFileName: "b", transcript: "t")]
        )
        var policy = VisitPolicy(cooldown: 600)
        XCTAssertEqual(policy.register(event(.entered, at: 0)), .play)
        XCTAssertEqual(
            policy.register(
                SanctuaryVisitEvent(site: other, kind: .entered, timestamp: Date(timeIntervalSince1970: 1))
            ),
            .play
        )
        XCTAssertEqual(policy.sitesCurrentlyInside, ["santiago", "assisi"])
    }
}
