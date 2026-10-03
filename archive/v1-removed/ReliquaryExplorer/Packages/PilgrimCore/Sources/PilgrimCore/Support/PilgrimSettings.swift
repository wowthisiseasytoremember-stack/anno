import Foundation

/// User-defaults keys shared by settings UI and service construction.
public enum PilgrimSettings {
    public static let narrationLanguageOverride = "org.pilgrimage.narrationLanguageOverride"

    /// Builds the resolver honoring the Settings override.
    public static func narrationResolver(defaults: UserDefaults = .standard) -> NarrationResolver {
        let override = defaults.string(forKey: narrationLanguageOverride)
        return NarrationResolver(overrideLanguageCode: (override?.isEmpty == true) ? nil : override)
    }
}
