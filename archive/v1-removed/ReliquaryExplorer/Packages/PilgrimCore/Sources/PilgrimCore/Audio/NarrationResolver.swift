import Foundation

/// Picks the best narration track for a sanctuary given the user's
/// preferred languages.
///
/// Matching order:
/// 1. Exact language-code match (`"es"` → `"es"`).
/// 2. Primary-language (region-stripped) match (`"es-MX"` → `"es"`).
/// 3. English fallback (the lingua franca of pilgrimage routes).
/// 4. Whatever track exists (deterministic: lowest language code).
///
/// An explicit `overrideLanguageCode` (from Settings) wins over the
/// system list. Pure and unit-tested.
public struct NarrationResolver: Sendable {
    public let preferredLanguages: [String]
    public let overrideLanguageCode: String?

    public init(
        preferredLanguages: [String] = Locale.preferredLanguages,
        overrideLanguageCode: String? = nil
    ) {
        self.preferredLanguages = preferredLanguages
        self.overrideLanguageCode = overrideLanguageCode
    }

    /// Returns `(languageCode, narration)` or nil if the site has no
    /// narrations (catalog validation normally prevents this).
    public func narration(for site: SanctuarySite) -> (language: String, narration: LocalizedNarration)? {
        let available = site.narrations
        guard !available.isEmpty else { return nil }

        func primary(_ code: String) -> String {
            String((Locale(identifier: code).language.languageCode?.identifier ?? code).prefix(8))
        }

        var candidates: [String] = []
        if let overrideLanguageCode, !overrideLanguageCode.isEmpty {
            candidates.append(overrideLanguageCode)
        }
        candidates.append(contentsOf: preferredLanguages)

        for candidate in candidates {
            if let exact = available[candidate] {
                return (candidate, exact)
            }
        }
        let preferredPrimaries = candidates.map(primary)
        for candidate in candidates {
            if let match = available[primary(candidate)], preferredPrimaries.contains(primary(candidate)) {
                return (primary(candidate), match)
            }
        }
        if let english = available["en"] {
            return ("en", english)
        }
        let fallback = available.sorted { $0.key < $1.key }[0]
        return (fallback.key, fallback.value)
    }
}
