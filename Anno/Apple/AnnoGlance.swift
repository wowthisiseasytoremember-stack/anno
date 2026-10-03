import Foundation

/// Small, stable payload designed for glanceable Apple surfaces.
///
/// Keep this independent from app-only view state so WidgetKit, Watch,
/// Spotlight, Siri/Shortcuts, and notification content can converge on one
/// representation later.
struct AnnoGlance: Codable, Hashable, Sendable {
    let date: String
    let title: String
    let subtitle: String
    let rank: String
    let liturgicalColorName: String

    static let placeholder = AnnoGlance(
        date: "2026-10-02",
        title: "Today in Anno",
        subtitle: "Daily Catholic devotional",
        rank: "Feria",
        liturgicalColorName: "green"
    )
}

extension AnnoGlance {
    init(entry: AnnoEntry, language: LanguageMode = .english) {
        let localized = LocalizedEntryText(entry: entry, language: language)
        self.init(
            date: entry.date,
            title: localized.title,
            subtitle: localized.heroLine,
            rank: entry.liturgical.rank,
            liturgicalColorName: entry.liturgical.color
        )
    }
}
