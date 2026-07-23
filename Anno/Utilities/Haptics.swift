//  Haptics.swift
//  DailyDevotionKJVForWomen
//
//  Subtle haptic feedback helpers used across the app.
//

import UIKit

/// Centralised, lightweight haptic feedback.
enum Haptics {
    static func soft() {
        let generator = UIImpactFeedbackGenerator(style: .soft)
        generator.impactOccurred(intensity: 0.7)
    }

    static func light() {
        UIImpactFeedbackGenerator(style: .light).impactOccurred()
    }

    static func success() {
        UINotificationFeedbackGenerator().notificationOccurred(.success)
    }

    static func selection() {
        UISelectionFeedbackGenerator().selectionChanged()
    }
}
//