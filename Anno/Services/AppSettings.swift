//  AppSettings.swift
//  Anno
//
//  Lightweight, persisted user preferences backed by UserDefaults.

import SwiftUI
import Observation

/// Preferred appearance mode.
enum AppearanceMode: String, CaseIterable, Identifiable, Sendable {
    case system, light, dark
    var id: String { rawValue }

    var title: String {
        switch self {
        case .system: return "System"
        case .light: return "Light"
        case .dark: return "Dark"
        }
    }

    var colorScheme: ColorScheme? {
        switch self {
        case .system: return nil
        case .light: return .light
        case .dark: return .dark
        }
    }
}

/// Observable settings store persisting to UserDefaults.
@Observable
@MainActor
final class AppSettings {
    private let defaults = UserDefaults.standard

    enum Keys {
        static let appearance = "settings.appearance"
        static let fontScale = "settings.fontScale"
        static let hasSeenWelcome = "settings.hasSeenWelcome"
    }

    var appearance: AppearanceMode {
        didSet { defaults.set(appearance.rawValue, forKey: Keys.appearance) }
    }

    /// Additional reading font scale (1.0 = default).
    var fontScale: Double {
        didSet { defaults.set(fontScale, forKey: Keys.fontScale) }
    }

    var hasSeenWelcome: Bool {
        didSet { defaults.set(hasSeenWelcome, forKey: Keys.hasSeenWelcome) }
    }

    init() {
        appearance = AppearanceMode(rawValue: defaults.string(forKey: Keys.appearance) ?? "") ?? .system
        let scale = defaults.double(forKey: Keys.fontScale)
        fontScale = scale == 0 ? 1.0 : scale
        hasSeenWelcome = defaults.bool(forKey: Keys.hasSeenWelcome)
    }

    /// Restores all preferences to their defaults.
    func restoreDefaults() {
        appearance = .system
        fontScale = 1.0
    }
}