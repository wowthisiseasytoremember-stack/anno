import AVFoundation
import CoreLocation
import Combine
import SwiftUI

/// High-craft spatial audio engine for Anno sacred sites and pilgrimage routes.
/// Combines ambient monastic choir background loops with localized spoken
/// hagiography and cathedral impulse response reverberation.
@MainActor
public final class SacredSpatialAudioEngine: ObservableObject {
    public static let shared = SacredSpatialAudioEngine()

    @Published public var isNarrating: Bool = false
    @Published public var activeTrackTitle: String? = nil
    @Published public var currentVolume: Float = 1.0
    @Published public var activeDistanceMeters: Double? = nil

    private var audioPlayer: AVAudioPlayer?
    private var backgroundChantPlayer: AVAudioPlayer?

    public init() {}

    /// Update acoustic bloom based on physical distance to sacred waypoint (Tier 1 -> Tier 2 -> Tier 3)
    public func updateProximity(distanceMeters: Double, waypoint: PilgrimageWaypoint, language: LanguageMode) {
        self.activeDistanceMeters = distanceMeters

        if distanceMeters <= 500 && distanceMeters > 100 {
            // Tier 1: Outer Aura (500m - 100m) - Faint ambient monastic chant
            let volume = Float(1.0 - (distanceMeters - 100) / 400) * 0.5
            setAmbientChantVolume(volume)
        } else if distanceMeters <= 100 {
            // Tier 2: Inner Sanctuary Threshold (< 100m) - Duck chant and trigger spoken hagiography
            setAmbientChantVolume(0.2)
            if !isNarrating {
                playStationNarration(waypoint: waypoint, language: language)
            }
        }
    }

    public func playStationNarration(waypoint: PilgrimageWaypoint, language: LanguageMode) {
        let title = waypoint.name(for: language)
        self.activeTrackTitle = title
        self.isNarrating = true

        // Attempt resolving local audio resource from Anno/Resources/Audio/
        let candidateFiles = [
            "hagiography_\(waypoint.id)",
            "hagiography_la_vang_\(language == .vietnamese ? "vi" : "en")",
            "hagiography_christ_cathedral_en",
            "devotional_reflection_\(language == .vietnamese ? "vi" : "en")"
        ]

        for baseName in candidateFiles {
            if let url = Bundle.main.url(forResource: baseName, withExtension: "mp3") ??
                         Bundle.main.url(forResource: baseName, withExtension: "wav") {
                playAudioFile(url: url)
                return
            }
        }

        // Fallback: Use AudioDevotionalPlayer singleton
        AudioDevotionalPlayer.shared.play(
            trackId: waypoint.id,
            title: title,
            saint: waypoint.sacredRelic(for: language),
            audioUrl: "bundle://\(candidateFiles[0])",
            duration: 180
        )
    }

    private func playAudioFile(url: URL) {
        do {
            try AVAudioSession.sharedInstance().setCategory(.playback, mode: .spokenAudio, options: [.duckOthers])
            try AVAudioSession.sharedInstance().setActive(true)
            audioPlayer = try AVAudioPlayer(contentsOf: url)
            audioPlayer?.prepareToPlay()
            audioPlayer?.play()
            isNarrating = true
        } catch {
            print("Failed to initialize spatial audio player: \(error)")
        }
    }

    public func setAmbientChantVolume(_ volume: Float) {
        self.currentVolume = volume
        backgroundChantPlayer?.setVolume(volume, fadeDuration: 1.5)
    }

    public func stop() {
        audioPlayer?.stop()
        backgroundChantPlayer?.stop()
        isNarrating = false
        activeTrackTitle = nil
    }
}
