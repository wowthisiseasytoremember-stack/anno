import AVFoundation
import Foundation
import OSLog

/// AVFoundation-backed `AudioPlaybackEngine`.
///
/// Thin by design: everything testable lives in `AudioHagiographyPlayer`.
final class AVAudioPlaybackEngine: NSObject, AudioPlaybackEngine, AVAudioPlayerDelegate {
    private var player: AVAudioPlayer?
    private let logger = Logger(subsystem: PilgrimCoreLog.subsystem, category: "AudioEngine")

    var onFinished: (() -> Void)?

    var isPlaying: Bool { player?.isPlaying ?? false }
    var currentTime: TimeInterval { player?.currentTime ?? 0 }
    var duration: TimeInterval { player?.duration ?? 0 }

    func load(url: URL) throws {
        let player = try AVAudioPlayer(contentsOf: url)
        player.delegate = self
        player.prepareToPlay()
        self.player = player
    }

    func play() -> Bool { player?.play() ?? false }
    func pause() { player?.pause() }
    func stop() { player?.stop() }

    func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        logger.debug("Playback finished (success=\(flag))")
        onFinished?()
    }
}

/// Production `HagiographyPlaying`.
///
/// Audio-session strategy (critical to the "AR + geofence fires
/// simultaneously" requirement):
///
/// - Category `.playback`, mode `.spokenAudio`: lets narration continue
///   when the device locks or the app backgrounds (paired with the
///   `audio` background mode on iOS).
/// - Options `.duckOthers` + `.interruptSpokenAudioAndMixWithOthers`:
///   narration *ducks* other apps' music instead of claiming the audio
///   route, and only interrupts *other spoken-word* audio.
/// - The AVFoundation audio session is **completely independent of the
///   ARKit/RealityKit tracking session**. Activating it neither pauses
///   `ARView`'s session nor stalls RealityKit rendering, so a geofence
///   trigger during AR inspection simply mixes narration in.
@MainActor
public final class AudioHagiographyPlayer: HagiographyPlaying {
    public let events: AsyncStream<HagiographyPlaybackEvent>

    private let resolver: AudioFileResolving
    private let narrationResolver: () -> NarrationResolver
    private let engine: AudioPlaybackEngine
    private let logger = Logger(subsystem: PilgrimCoreLog.subsystem, category: "HagiographyPlayer")

    private let continuation: AsyncStream<HagiographyPlaybackEvent>.Continuation
    public private(set) var snapshot: NowPlayingSnapshot?

    private var sessionWasConfigured = false

    public init(
        audioFileResolver: AudioFileResolving = BundleAudioFileResolver(),
        narrationResolver: @escaping () -> NarrationResolver = { NarrationResolver() },
        engine: AudioPlaybackEngine = AVAudioPlaybackEngine()
    ) {
        self.resolver = audioFileResolver
        self.narrationResolver = narrationResolver
        self.engine = engine

        var localContinuation: AsyncStream<HagiographyPlaybackEvent>.Continuation!
        self.events = AsyncStream { localContinuation = $0 }
        self.continuation = localContinuation

        self.engine.onFinished = { [weak self] in
            Task { @MainActor in self?.handleFinished() }
        }

        observeInterruptions()
    }

    // MARK: - HagiographyPlaying

    public func play(site: SanctuarySite) {
        guard let resolved = narrationResolver().narration(for: site) else {
            emit(.init(siteID: site.id, siteName: site.name, kind: .failed("No narration available")))
            return
        }

        guard let url = resolver.audioURL(forResource: resolved.narration.audioFileName) else {
            logger.error("Missing audio asset '\(resolved.narration.audioFileName)' for site \(site.id)")
            emit(.init(siteID: site.id, siteName: site.name, kind: .failed("Audio asset not bundled")))
            return
        }

        configureSessionIfNeeded()

        do {
            engine.stop()
            try engine.load(url: url)
            guard engine.play() else {
                emit(.init(siteID: site.id, siteName: site.name, kind: .failed("Playback engine declined to start")))
                return
            }
        } catch {
            logger.error("Playback error for \(site.id): \(error.localizedDescription)")
            emit(.init(siteID: site.id, siteName: site.name, kind: .failed(error.localizedDescription)))
            return
        }

        snapshot = NowPlayingSnapshot(
            siteID: site.id,
            siteName: site.name,
            transcript: resolved.narration.transcript,
            language: resolved.language,
            state: .playing
        )
        emit(.init(siteID: site.id, siteName: site.name, kind: .started))
        logger.info("Narration started for \(site.name) [\(resolved.language)]")
    }

    public func pause() {
        engine.pause()
        mutateSnapshot { $0.state = .paused }
    }

    public func resume() {
        guard snapshot != nil, !engine.isPlaying else { return }
        configureSessionIfNeeded()
        _ = engine.play()
        mutateSnapshot { $0.state = .playing }
    }

    public func stop() {
        guard snapshot != nil else { return }
        engine.stop()
        let siteID = snapshot?.siteID
        let siteName = snapshot?.siteName
        snapshot = nil
        if let siteID, let siteName {
            emit(.init(siteID: siteID, siteName: siteName, kind: .stopped))
        }
    }

    // MARK: - Internals

    private func configureSessionIfNeeded() {
        guard !sessionWasConfigured else {
            // Re-assert active: iOS deactivates sessions after interruptions
            // in some paths; cheap and idempotent.
            try? AVAudioSession.sharedInstance().setActive(true)
            return
        }
        sessionWasConfigured = true
        do {
            let session = AVAudioSession.sharedInstance()
            try session.setCategory(
                .playback,
                mode: .spokenAudio,
                options: [.duckOthers, .interruptSpokenAudioAndMixWithOthers]
            )
            try session.setActive(true)
            logger.info("Audio session configured (.playback/.spokenAudio/duckOthers)")
        } catch {
            logger.error("Audio session configuration failed: \(error.localizedDescription)")
        }
    }

    private func handleFinished() {
        guard let current = snapshot else { return }
        snapshot = nil
        emit(.init(siteID: current.siteID, siteName: current.siteName, kind: .finished))
    }

    private func mutateSnapshot(_ change: (inout NowPlayingSnapshot) -> Void) {
        guard var snap = snapshot else { return }
        change(&snap)
        snapshot = snap
    }

    private func emit(_ event: HagiographyPlaybackEvent) {
        continuation.yield(event)
    }

    /// Pauses (rather than dies) when a phone call or Siri interrupts,
    /// matching user expectation for a walking guide.
    private func observeInterruptions() {
        NotificationCenter.default.addObserver(
            forName: AVAudioSession.interruptionNotification,
            object: AVAudioSession.sharedInstance(),
            queue: .main
        ) { [weak self] notification in
            let rawType = notification.userInfo?[AVAudioSessionInterruptionTypeKey] as? UInt
            let type = AVAudioSession.InterruptionType(rawValue: rawType ?? 0)
            Task { @MainActor in
                guard let self else { return }
                switch type {
                case .began:
                    self.engine.pause()
                    self.mutateSnapshot { $0.state = .paused }
                    self.logger.debug("Audio session interrupted; narration paused")
                case .ended:
                    self.resume()
                @unknown default:
                    break
                }
            }
        }
    }
}
