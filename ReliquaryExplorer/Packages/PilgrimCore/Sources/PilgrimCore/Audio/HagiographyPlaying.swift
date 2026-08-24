import Foundation

/// Snapshot published to the UI for the "now playing" banner.
public struct NowPlayingSnapshot: Equatable, Sendable {
    public enum State: Equatable, Sendable {
        case playing
        case paused
    }

    public let siteID: String
    public let siteName: String
    public let transcript: String
    public let language: String
    public let state: State

    public init(
        siteID: String,
        siteName: String,
        transcript: String,
        language: String,
        state: State
    ) {
        self.siteID = siteID
        self.siteName = siteName
        self.transcript = transcript
        self.language = language
        self.state = state
    }
}

/// Playback lifecycle events surfaced by `HagiographyPlaying` implementers.
public struct HagiographyPlaybackEvent: Equatable, Sendable {
    public enum Kind: Equatable, Sendable {
        case started
        case finished
        case stopped
        case failed(String)
    }

    public let siteID: String
    public let siteName: String
    public let kind: Kind

    public init(siteID: String, siteName: String, kind: Kind) {
        self.siteID = siteID
        self.siteName = siteName
        self.kind = kind
    }
}

/// Platform seam for hagiography playback.
///
/// Implemented once, on top of AVFoundation, and shared by iOS and
/// visionOS (both have AVAudioSession). Tests drive it with a fake
/// `AudioPlaybackEngine` + in-memory `AudioFileResolving`.
@MainActor
public protocol HagiographyPlaying: AnyObject {
    var events: AsyncStream<HagiographyPlaybackEvent> { get }

    /// Begins narration for the site (resolving language via
    /// `NarrationResolver`). Re-entrant: starting a new site replaces the
    /// previous track. Throws nothing; failures are surfaced as
    /// `.failed` events (missing asset, engine error) so background
    /// callers need no error plumbing.
    func play(site: SanctuarySite)

    func pause()
    func resume()
    func stop()

    /// Most recent state for UI; nil when idle.
    var snapshot: NowPlayingSnapshot? { get }
}

/// Resolves a bundle audio resource name (no extension) to a file URL.
public protocol AudioFileResolving: AnyObject {
    func audioURL(forResource name: String) -> URL?
}

/// Wraps a single-file audio player enough for the hagiography player to
/// be testable without AVFoundation.
public protocol AudioPlaybackEngine: AnyObject {
    /// Loads and prepares a local file. Throws on unreadable/invalid audio.
    func load(url: URL) throws
    func play() -> Bool
    func pause()
    func stop()
    var isPlaying: Bool { get }
    var currentTime: TimeInterval { get }
    var duration: TimeInterval { get }
    /// Called on the main thread when playback finishes naturally.
    var onFinished: (() -> Void)? { get set }
}

// MARK: - Bundle resolution

/// Looks audio up in the package resources, trying the extensions AVAudioPlayer
/// handles for delivery-friendly formats.
public final class BundleAudioFileResolver: AudioFileResolving {
    public let bundle: Bundle
    public let subdirectory: String?
    public let allowedExtensions: [String]

    public init(
        bundle: Bundle = .module,
        subdirectory: String? = "Audio",
        allowedExtensions: [String] = ["m4a", "mp3", "aac", "wav"]
    ) {
        self.bundle = bundle
        self.subdirectory = subdirectory
        self.allowedExtensions = allowedExtensions
    }

    public func audioURL(forResource name: String) -> URL? {
        // SwiftPM `.process` may flatten resource directories; try the
        // subdirectory first, then the bundle root.
        for ext in allowedExtensions {
            if let url = bundle.url(forResource: name, withExtension: ext, subdirectory: subdirectory) {
                return url
            }
            if let url = bundle.url(forResource: name, withExtension: ext) {
                return url
            }
        }
        // Also accept fully-specified names ("clip.m4a").
        if let url = bundle.url(
            forResource: (name as NSString).deletingPathExtension,
            withExtension: (name as NSString).pathExtension,
            subdirectory: subdirectory
        ) ?? bundle.url(
            forResource: (name as NSString).deletingPathExtension,
            withExtension: (name as NSString).pathExtension
        ) {
            return url
        }
        return nil
    }
}
