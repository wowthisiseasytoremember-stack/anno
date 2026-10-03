//  Haptics.swift
//  Anno
//
//  Apple-native tactile language for Anno.
//

import CoreHaptics
import UIKit

/// Centralised haptic feedback.
///
/// Ordinary controls use UIKit's lightweight feedback generators.
/// Sacred / pilgrimage moments use Core Haptics when the hardware supports it
/// and fall back gracefully to the standard generators.
@MainActor
enum Haptics {
    private static var sacredEngine: CHHapticEngine?

    static func soft() {
        let generator = UIImpactFeedbackGenerator(style: .soft)
        generator.impactOccurred(intensity: 0.7)
    }

    static func light() {
        UIImpactFeedbackGenerator(style: .light).impactOccurred()
    }

    static func medium() {
        UIImpactFeedbackGenerator(style: .medium).impactOccurred()
    }

    static func success() {
        UINotificationFeedbackGenerator().notificationOccurred(.success)
    }

    static func selection() {
        UISelectionFeedbackGenerator().selectionChanged()
    }

    /// A tactile "arrival" that scales with the importance of the sacred moment.
    static func sacredArrival(_ intensity: SacredIntensity) {
        guard supportsCoreHaptics else {
            switch intensity {
            case .ordinary:
                light()
            case .feast:
                medium()
            case .solemnity:
                success()
            }
            return
        }

        switch intensity {
        case .ordinary:
            playCorePattern([
                transient(time: 0.00, intensity: 0.42, sharpness: 0.22)
            ])

        case .feast:
            playCorePattern([
                transient(time: 0.00, intensity: 0.52, sharpness: 0.24),
                transient(time: 0.10, intensity: 0.74, sharpness: 0.42)
            ])

        case .solemnity:
            playCorePattern([
                transient(time: 0.00, intensity: 0.48, sharpness: 0.18),
                transient(time: 0.09, intensity: 0.74, sharpness: 0.36),
                transient(time: 0.20, intensity: 1.00, sharpness: 0.58)
            ])
        }
    }

    /// Completion is deliberately richer than a generic success notification.
    /// It should feel like a tiny three-note peal in the hand.
    static func pilgrimageComplete() {
        guard supportsCoreHaptics else {
            success()
            return
        }

        playCorePattern([
            transient(time: 0.00, intensity: 0.50, sharpness: 0.24),
            transient(time: 0.10, intensity: 0.72, sharpness: 0.34),
            transient(time: 0.22, intensity: 0.92, sharpness: 0.48),
            transient(time: 0.38, intensity: 1.00, sharpness: 0.62)
        ])
    }

    private static var supportsCoreHaptics: Bool {
        CHHapticEngine.capabilitiesForHardware().supportsHaptics
    }

    private static func transient(
        time: TimeInterval,
        intensity: Float,
        sharpness: Float
    ) -> CHHapticEvent {
        CHHapticEvent(
            eventType: .hapticTransient,
            parameters: [
                CHHapticEventParameter(
                    parameterID: .hapticIntensity,
                    value: intensity
                ),
                CHHapticEventParameter(
                    parameterID: .hapticSharpness,
                    value: sharpness
                )
            ],
            relativeTime: time
        )
    }

    private static func playCorePattern(_ events: [CHHapticEvent]) {
        do {
            let engine = try coreHapticEngine()
            let pattern = try CHHapticPattern(events: events, parameters: [])
            let player = try engine.makePlayer(with: pattern)
            try player.start(atTime: 0)
        } catch {
            // Haptics are delight, never a functional blocker.
            light()
        }
    }

    private static func coreHapticEngine() throws -> CHHapticEngine {
        if let sacredEngine {
            try sacredEngine.start()
            return sacredEngine
        }

        let engine = try CHHapticEngine()
        try engine.start()
        sacredEngine = engine
        return engine
    }
}
