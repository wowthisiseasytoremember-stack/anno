import CoreLocation
import PilgrimCore
import XCTest

@testable import PilgrimCore

// MARK: - Fakes

@MainActor
final class FakeSanctuaryMonitor: SanctuaryMonitoring {
    var availability: ProximityGuidanceAvailability = .available
    let events: AsyncStream<SanctuaryVisitEvent>
    private let continuation: AsyncStream<SanctuaryVisitEvent>.Continuation
    private(set) var startCallCount = 0

    init() {
        var localContinuation: AsyncStream<SanctuaryVisitEvent>.Continuation!
        events = AsyncStream { localContinuation = $0 }
        continuation = localContinuation
    }

    func start(catalog: SanctuaryCatalog, lastKnownLocation: CLLocation?) {
        startCallCount += 1
    }

    func stop() {}
    func refresh(lastKnownLocation: CLLocation?) {}

    func send(_ event: SanctuaryVisitEvent) {
        continuation.yield(event)
    }
}

@MainActor
final class FakeHagiographyPlayer: HagiographyPlaying {
    let events: AsyncStream<HagiographyPlaybackEvent>
    private let continuation: AsyncStream<HagiographyPlaybackEvent>.Continuation

    private(set) var snapshot: NowPlayingSnapshot?
    private(set) var playedSiteIDs: [String] = []
    private(set) var stoppedCount = 0

    init() {
        var localContinuation: AsyncStream<HagiographyPlaybackEvent>.Continuation!
        events = AsyncStream { localContinuation = $0 }
        continuation = localContinuation
    }

    func play(site: SanctuarySite) {
        playedSiteIDs.append(site.id)
        snapshot = NowPlayingSnapshot(
            siteID: site.id,
            siteName: site.name,
            transcript: "t",
            language: "en",
            state: .playing
        )
        continuation.yield(.init(siteID: site.id, siteName: site.name, kind: .started))
    }

    func pause() { snapshot = nil }
    func resume() {}
    func stop() {
        stoppedCount += 1
        snapshot = nil
    }
}

final class FakeVisitNotifier: VisitNotifying {
    private(set) var posted: [(siteName: String, transcript: String)] = []
    func requestAuthorization() async -> Bool { true }
    func postArrivalNotification(siteName: String, transcript: String) async -> Bool {
        posted.append((siteName, transcript))
        return true
    }
}

@MainActor
final class FakeAppPhase: AppPhaseProviding {
    var isApplicationBackgrounded = false
}

// MARK: - Tests

@MainActor
final class PilgrimGuideCoordinatorTests: XCTestCase {
    private let site = SanctuarySite(
        id: "santiago",
        name: "Cathedral of Santiago de Compostela",
        latitude: 42.88,
        longitude: -8.54,
        radiusMeters: 60,
        narrations: ["en": LocalizedNarration(audioFileName: "a", transcript: "You are approaching.")]
    )

    private func makeCoordinator(
        backgrounded: Bool = false,
        notifier: VisitNotifying? = nil
    ) -> (PilgrimGuideCoordinator, FakeSanctuaryMonitor, FakeHagiographyPlayer) {
        let monitor = FakeSanctuaryMonitor()
        let player = FakeHagiographyPlayer()
        let phase = FakeAppPhase()
        phase.isApplicationBackgrounded = backgrounded
        let coordinator = PilgrimGuideCoordinator(
            catalog: SanctuaryCatalog(sites: [site]),
            monitor: monitor,
            player: player,
            notifier: notifier,
            appPhase: phase
        )
        return (coordinator, monitor, player)
    }

    private func flushLoops() async {
        try? await Task.sleep(nanoseconds: 150_000_000)
    }

    func testEntryPlaysNarrationOnce() async {
        let (coordinator, monitor, player) = makeCoordinator()
        coordinator.startGuidance()
        await flushLoops()

        monitor.send(SanctuaryVisitEvent(site: site, kind: .entered, timestamp: Date(timeIntervalSince1970: 0)))
        await flushLoops()

        XCTAssertEqual(player.playedSiteIDs, ["santiago"])
    }

    func testJitterWithinCooldownIsDeduplicated() async {
        let (coordinator, _, player) = makeCoordinator()
        await coordinator.handleVisitEvent(
            SanctuaryVisitEvent(site: site, kind: .entered, timestamp: Date(timeIntervalSince1970: 0))
        )
        await coordinator.handleVisitEvent(
            SanctuaryVisitEvent(site: site, kind: .exited, timestamp: Date(timeIntervalSince1970: 30))
        )
        await coordinator.handleVisitEvent(
            SanctuaryVisitEvent(site: site, kind: .entered, timestamp: Date(timeIntervalSince1970: 60))
        )
        XCTAssertEqual(player.playedSiteIDs.count, 1, "Re-entry inside cooldown must not re-trigger")
    }

    func testReturnAfterCooldownPlaysAgain() async {
        let (coordinator, _, player) = makeCoordinator()
        await coordinator.handleVisitEvent(
            SanctuaryVisitEvent(site: site, kind: .entered, timestamp: Date(timeIntervalSince1970: 0))
        )
        await coordinator.handleVisitEvent(
            SanctuaryVisitEvent(site: site, kind: .exited, timestamp: Date(timeIntervalSince1970: 100))
        )
        await coordinator.handleVisitEvent(
            SanctuaryVisitEvent(site: site, kind: .entered, timestamp: Date(timeIntervalSince1970: 999_000))
        )
        XCTAssertEqual(player.playedSiteIDs.count, 2)
    }

    func testBackgroundedArrivalPostsNotification() async {
        let notifier = FakeVisitNotifier()
        let (coordinator, _, _) = makeCoordinator(backgrounded: true, notifier: notifier)
        await coordinator.handleVisitEvent(
            SanctuaryVisitEvent(site: site, kind: .entered, timestamp: Date())
        )
        XCTAssertEqual(notifier.posted.count, 1)
        XCTAssertEqual(notifier.posted.first?.siteName, site.name)
    }

    func testForegroundArrivalPostsNoNotification() async {
        let notifier = FakeVisitNotifier()
        let (coordinator, _, _) = makeCoordinator(backgrounded: false, notifier: notifier)
        await coordinator.handleVisitEvent(
            SanctuaryVisitEvent(site: site, kind: .entered, timestamp: Date())
        )
        XCTAssertTrue(notifier.posted.isEmpty)
    }

    /// The AR + geofence concurrency contract: playback is NEVER gated on
    /// AR state (audio ducks; the AR session is untouched).
    func testArrivalDuringActiveARViewerStillPlays() async {
        let (coordinator, _, player) = makeCoordinator()
        coordinator.arViewerActive = true
        await coordinator.handleVisitEvent(
            SanctuaryVisitEvent(site: site, kind: .entered, timestamp: Date())
        )
        XCTAssertEqual(player.playedSiteIDs, ["santiago"])
    }

    func testManualPlaybackBypassesPolicy() async {
        let (coordinator, _, player) = makeCoordinator()
        coordinator.playNarration(manuallyFor: site)
        coordinator.playNarration(manuallyFor: site)
        XCTAssertEqual(player.playedSiteIDs.count, 2, "Manual taps are always honored")
    }

    func testStartGuidanceArmsMonitor() async {
        let (coordinator, monitor, _) = makeCoordinator()
        coordinator.startGuidance()
        XCTAssertEqual(monitor.startCallCount, 1)
        coordinator.startGuidance()
        XCTAssertEqual(monitor.startCallCount, 2, "Re-arming is passed through (idempotent at the monitor)")
    }
}
