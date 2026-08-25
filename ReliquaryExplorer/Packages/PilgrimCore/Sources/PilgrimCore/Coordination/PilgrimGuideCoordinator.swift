import CoreLocation
import Foundation
import Observation

/// Glues the proximity subsystem to the audio subsystem *without letting
/// them know about each other*:
///
///     SanctuaryMonitoring ──events──▶  PilgrimGuideCoordinator ──▶ HagiographyPlaying
///     (iOS: CoreLocation)             (VisitPolicy dedupe)          (AVFoundation)
///                                             │
///                                             ▼
///                                    VisitNotifying (lock-screen notice,
///                                     only when app is backgrounded)
///
/// The AR subsystem's only interaction with geofencing is
/// `arViewerActive`: the AR screens flag themselves so the coordinator
/// can decide *presentation* (banner vs. local notification). Playback
/// itself is never gated on AR — the audio session is configured to mix
/// (.duckOthers), and AVFoundation's audio session is independent of the
/// ARKit tracking session, so simultaneous AR + narration "just works"
/// by construction.
@MainActor
@Observable
public final class PilgrimGuideCoordinator {
    public let catalog: SanctuaryCatalog
    public let monitor: any SanctuaryMonitoring
    public let player: any HagiographyPlaying
    public let notifier: (any VisitNotifying)?
    public let appPhase: (any AppPhaseProviding)?

    private var policy = VisitPolicy()

    public private(set) var nowPlaying: NowPlayingSnapshot?
    public private(set) var lastVisit: SanctuaryVisitEvent?
    public private(set) var recentVisitLog: [SanctuaryVisitEvent] = []
    /// Set true by AR screens while a reliquary viewer session is running.
    public var arViewerActive = false {
        didSet { PilgrimCoreLog.coordinator.debug("AR viewer active = \(self.arViewerActive)") }
    }

    private var monitorTask: Task<Void, Never>?
    private var playerTask: Task<Void, Never>?

    public init(
        catalog: SanctuaryCatalog,
        monitor: any SanctuaryMonitoring,
        player: any HagiographyPlaying,
        notifier: (any VisitNotifying)? = nil,
        appPhase: (any AppPhaseProviding)? = nil
    ) {
        self.catalog = catalog
        self.monitor = monitor
        self.player = player
        self.notifier = notifier
        self.appPhase = appPhase
    }

    // MARK: - Lifecycle

    /// Call on app launch (e.g. from the App's `init` or first scene
    /// activation). Region monitoring is armed immediately if authorized;
    /// otherwise the monitor surfaces `.requiresAuthorization` and the UI
    /// prompts.
    public func startGuidance() {
        PilgrimCoreLog.coordinator.info("Starting pilgrim guidance with \(self.catalog.sites.count) sanctuaries")
        monitor.start(catalog: catalog, lastKnownLocation: persistedLastKnownLocation)

        if let notifier {
            Task { _ = await notifier.requestAuthorization() }
        }

        monitorTask?.cancel()
        let eventStream = monitor.events
        monitorTask = Task { [weak self] in
            for await event in eventStream {
                await self?.handleVisitEvent(event)
            }
        }

        playerTask?.cancel()
        let playbackStream = player.events
        playerTask = Task { [weak self] in
            for await event in playbackStream {
                self?.syncNowPlaying(with: event)
            }
        }
    }

    public func stopGuidance() {
        monitorTask?.cancel(); monitorTask = nil
        playerTask?.cancel(); playerTask = nil
        monitor.stop()
    }

    // MARK: - Visit handling (the geofence → audio bridge)

    /// Internal so tests can drive exact event sequences.
    internal func handleVisitEvent(_ event: SanctuaryVisitEvent) async {
        lastVisit = event
        recentVisitLog.insert(event, at: 0)
        if recentVisitLog.count > 12 {
            recentVisitLog.removeLast()
        }
        let decision = policy.register(event)

        guard case .play = decision else {
            PilgrimCoreLog.coordinator.debug(
                "Skipping \(event.site.name) (\(String(describing: decision)))"
            )
            return
        }

        PilgrimCoreLog.coordinator.info("Sanctuary entered: \(event.site.name) — starting narration")
        player.play(site: event.site)

        // Lock-screen/out-of-app arrivals get a visible reason for the
        // audio (App Review also likes visible user benefit).
        let backgrounded = appPhase?.isApplicationBackgrounded ?? false
        if backgrounded, let notifier {
            let resolved = NarrationResolver().narration(for: event.site)
            await notifier.postArrivalNotification(
                siteName: event.site.name,
                transcript: resolved?.narration.transcript ?? ""
            )
        }
    }

    // MARK: - Manual playback (map callouts, visionOS museum mode)

    public func playNarration(manuallyFor site: SanctuarySite) {
        PilgrimCoreLog.coordinator.info("Manual narration: \(site.name)")
        player.play(site: site)
    }

    public func stopPlayback() { player.stop() }
    public func pausePlayback() { player.pause() }
    public func resumePlayback() { player.resume() }

    public var availability: ProximityGuidanceAvailability { monitor.availability }

    // MARK: - Demo & QA (debug builds)

#if DEBUG
    /// Drives the *real* pipeline (visit policy → narration → background
    /// notification) with a synthetic geofence event — no GPS, no walking.
    /// This is the App Review / sales-demo path on any device.
    public func debugSimulateArrival(at site: SanctuarySite) {
        PilgrimCoreLog.coordinator.info("[Demo] Simulated arrival at \(site.name)")
        Task { await handleVisitEvent(SanctuaryVisitEvent(site: site, kind: .entered, timestamp: Date())) }
    }

    public func debugSimulateDeparture(from site: SanctuarySite) {
        Task { await handleVisitEvent(SanctuaryVisitEvent(site: site, kind: .exited, timestamp: Date())) }
    }

    /// Drops the per-site cooldown so repeated demos re-trigger
    /// immediately (mirrors the default policy otherwise).
    public func debugDisableVisitCooldown() {
        policy = VisitPolicy(cooldown: 0)
        PilgrimCoreLog.coordinator.info("[Demo] Visit cooldown disabled")
    }
#endif

    // MARK: - Now-playing mirroring

    private func syncNowPlaying(with event: HagiographyPlaybackEvent) {
        switch event.kind {
        case .started, .failed:
            nowPlaying = player.snapshot
        case .finished, .stopped:
            nowPlaying = nil
        }
    }

    // MARK: - Location persistence (cold-start region ranking)

    private var lastKnownLocation: CLLocation? {
        get {
            guard let data = UserDefaults.standard.data(forKey: Self.lastLocationKey),
                  let decoded = try? JSONDecoder().decode(CodableLocation.self, from: data)
            else { return nil }
            return CLLocation(
                latitude: decoded.latitude,
                longitude: decoded.longitude,
                timestamp: decoded.timestamp
            )
        }
        set {
            guard let newValue else { return }
            let payload = CodableLocation(
                latitude: newValue.coordinate.latitude,
                longitude: newValue.coordinate.longitude,
                timestamp: newValue.timestamp
            )
            UserDefaults.standard.set(
                try? JSONEncoder().encode(payload),
                forKey: Self.lastLocationKey
            )
        }
    }

    private static let lastLocationKey = "org.pilgrimage.lastKnownLocation"

    /// The iOS monitor calls this with significant-change updates so the
    /// *next* cold start already ranks regions correctly.
    public func recordSignificantLocation(_ location: CLLocation) {
        lastKnownLocation = location
        monitor.refresh(lastKnownLocation: location)
    }

    private struct CodableLocation: Codable {
        let latitude: Double
        let longitude: Double
        let timestamp: Date
    }
}
