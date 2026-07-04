//
//  LocalizationManager.swift
//  Anno iOS
//
//  Runtime language manager for Anno's Vietnamese localization.
//
//  Principles:
//  - No bundle swapping — loads .strings files into memory, avoiding cached-UIKit-text edge cases.
//  - Posts Notification on switch so every subscribed view refreshes without app restart.
//  - Falls back to English for any missing Vietnamese key — never shows a blank label.
//  - Language preference persists in UserDefaults (survives app restart).
//
//  Usage:
//    let title = LocalizationManager.shared.string(forKey: "tab.today")
//    LocalizationManager.shared.setLanguage(.vietnamese)
//
//  Views subscribe to LocalizationManager.didChangeNotification and call
//  their localization refresh in response.

import Foundation
import SwiftUI

// MARK: - Notification

extension Notification.Name {
    /// Posted when the active language changes. Observing views should re-localize
    /// all visible chrome and call reloadData() / invalidate() as needed.
    static let localizationDidChange = Notification.Name("com.anno.localizationDidChange")
}

// MARK: - Manager

@MainActor
final class LocalizationManager: ObservableObject {

    // MARK: Singleton

    static let shared = LocalizationManager()

    // MARK: Language Definition

    enum Language: String, CaseIterable, Identifiable {
        case english  = "en"
        case vietnamese = "vi"

        var id: String { rawValue }

        var displayName: String {
            switch self {
            case .english:   return "English"
            case .vietnamese: return "Tiếng Việt"
            }
        }

        /// The .lproj directory name expected in the app bundle.
        var lprojName: String {
            "\(rawValue).lproj"
        }
    }

    // MARK: Published State

    /// The currently active language. Changing this persists the preference,
    /// reloads the string dictionary, and posts `localizationDidChange`.
    @Published private(set) var currentLanguage: Language {
        didSet {
            UserDefaults.standard.set(currentLanguage.rawValue, forKey: storageKey)
        }
    }

    // MARK: Private State

    private let storageKey = "com.anno.selectedLanguage"

    /// Vietnamese string dictionary, loaded once per language switch.
    private var viStrings: [String: String] = [:]

    /// English string dictionary, loaded once per language switch.
    private var enStrings: [String: String] = [:]

    // MARK: Initialization

    private init() {
        let saved = UserDefaults.standard.string(forKey: storageKey) ?? ""
        currentLanguage = Language(rawValue: saved) ?? .english
        loadDictionaries(for: currentLanguage)
    }

    // MARK: Public API

    /// Returns the localized string for `key` in the current language.
    /// Falls back to English when the Vietnamese key is missing.
    /// Falls back to the raw key when neither language has the key
    /// (visible signal to developers during development).
    func string(forKey key: String) -> String {
        switch currentLanguage {
        case .vietnamese:
            return viStrings[key] ?? enStrings[key] ?? key
        case .english:
            return enStrings[key] ?? key
        }
    }

    /// Returns an English-localized value for the given key.
    /// Used for mixed-language states where chrome is Vietnamese but
    /// a specific string (e.g. source title) should remain English.
    func englishString(forKey key: String) -> String {
        enStrings[key] ?? key
    }

    /// Switch the active language. Persists immediately, reloads string
    /// dictionaries, and posts `localizationDidChange`.
    func setLanguage(_ language: Language) {
        guard language != currentLanguage else { return }
        currentLanguage = language
        loadDictionaries(for: language)
        NotificationCenter.default.post(name: .localizationDidChange, object: nil)
    }

    /// Convenience: returns the opposite language (for toggle UIs).
    func toggledLanguage() -> Language {
        currentLanguage == .english ? .vietnamese : .english
    }

    // MARK: Dictionary Loading

    /// Load both English and Vietnamese string dictionaries from the bundle.
    /// The manager always holds English as the fallback regardless of current language,
    /// so switching between them never requires disk access.
    private func loadDictionaries(for _: Language) {
        enStrings = loadStrings(fromLproj: Language.english.lprojName) ?? [:]
        viStrings = loadStrings(fromLproj: Language.vietnamese.lprojName) ?? [:]

        if enStrings.isEmpty {
            // During development before .strings files are in the bundle,
            // fall back to NSLocalizedString for the system-provided defaults.
            // Log a single warning so developers know the .strings files are missing.
            #if DEBUG
            print("[LocalizationManager] Warning: No English .strings file found at \(Language.english.lprojName)/Localizable.strings")
            #endif
        }
    }

    /// Loads a .strings file from the given .lproj directory in the main bundle.
    /// Returns nil if the directory or file doesn't exist.
    private func loadStrings(fromLproj lprojName: String) -> [String: String]? {
        guard let lprojPath = Bundle.main.path(forResource: lprojName, ofType: nil) else {
            return nil
        }
        let stringsPath = (lprojPath as NSString).appendingPathComponent("Localizable.strings")
        guard FileManager.default.fileExists(atPath: stringsPath) else {
            return nil
        }
        return NSDictionary(contentsOfFile: stringsPath) as? [String: String]
    }
}

// MARK: - SwiftUI Property Wrapper

/// A property wrapper that reads a localized string and auto-refreshes when
/// the language changes.
///
/// Usage:
/// ```swift
/// struct MyView: View {
///     @Localized("tab.today") var title
///     var body: some View { Text(title) }
/// }
/// ```
@propertyWrapper
struct Localized: DynamicProperty {

    @StateObject private var observer = LocalizationObserver()
    private let key: String

    init(_ key: String) {
        self.key = key
    }

    var wrappedValue: String {
        LocalizationManager.shared.string(forKey: key)
    }
}

/// Internal observer that triggers view refresh on language change.
private final class LocalizationObserver: ObservableObject {
    init() {
        NotificationCenter.default.addObserver(
            forName: .localizationDidChange,
            object: nil,
            queue: .main
        ) { [weak self] _ in
            self?.objectWillChange.send()
        }
    }
}

// MARK: - View Modifier

extension View {
    /// Refreshes the view tree when the localization changes.
    /// Apply to any root view that displays localized chrome.
    func onLocalizationChange(perform action: @escaping () -> Void) -> some View {
        self.onReceive(
            NotificationCenter.default.publisher(for: .localizationDidChange)
        ) { _ in action() }
    }
}
