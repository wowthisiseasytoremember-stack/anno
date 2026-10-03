// Source-complete App Intents prototype.
//
// Kept outside the active Xcode target until Mac/Xcode validation is available.
// Uses AppIntent.supportedModes rather than deprecated openAppWhenRun.

import AppIntents
import Foundation

struct AnnoTodayIntent: AppIntent {
    static let title: LocalizedStringResource = "Today in Anno"
    static let description = IntentDescription(
        "Returns the current Anno devotional title and liturgical rank."
    )
    static let supportedModes: IntentModes = [.background]

    func perform() async throws -> some IntentResult & ProvidesDialog {
        let glance = AnnoIntentContent.todayGlance()
        return .result(
            dialog: IntentDialog(
                stringLiteral: "\(glance.title). \(glance.rank). \(glance.subtitle)"
            )
        )
    }
}

struct AnnoFeastIntent: AppIntent {
    static let title: LocalizedStringResource = "Today's Feast"
    static let description = IntentDescription(
        "Returns today's feast or devotional title from Anno."
    )
    static let supportedModes: IntentModes = [.background]

    func perform() async throws -> some IntentResult & ProvidesDialog {
        let glance = AnnoIntentContent.todayGlance()
        return .result(
            dialog: IntentDialog(
                stringLiteral: "\(glance.title) — \(glance.rank)"
            )
        )
    }
}

struct AnnoPilgrimageSummaryIntent: AppIntent {
    static let title: LocalizedStringResource = "Anno Pilgrimage Routes"
    static let description = IntentDescription(
        "Summarizes Anno's five flagship pilgrimage routes."
    )
    static let supportedModes: IntentModes = [.background]

    func perform() async throws -> some IntentResult & ProvidesDialog {
        let titles = AnnoIntentContent.routeTitles()
        let summary = titles.isEmpty
            ? "Anno's pilgrimage routes are unavailable."
            : "Anno has five flagship pilgrimage routes: " + titles.joined(separator: ", ") + "."

        return .result(dialog: IntentDialog(stringLiteral: summary))
    }
}

struct AnnoShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: AnnoTodayIntent(),
            phrases: [
                "Show today in \(.applicationName)",
                "What's today in \(.applicationName)",
                "Open today's devotion in \(.applicationName)"
            ],
            shortTitle: "Today in Anno",
            systemImageName: "sun.max.fill"
        )

        AppShortcut(
            intent: AnnoFeastIntent(),
            phrases: [
                "What's today's feast in \(.applicationName)",
                "Today's Catholic feast in \(.applicationName)"
            ],
            shortTitle: "Today's Feast",
            systemImageName: "cross.fill"
        )

        AppShortcut(
            intent: AnnoPilgrimageSummaryIntent(),
            phrases: [
                "Show pilgrimage routes in \(.applicationName)",
                "What pilgrimage routes are in \(.applicationName)"
            ],
            shortTitle: "Pilgrimage Routes",
            systemImageName: "figure.walk.motion"
        )
    }
}

private enum AnnoIntentContent {
    static func todayGlance(bundle: Bundle = .main) -> AnnoGlance {
        guard let fixture = loadFixture(bundle: bundle),
              let entry = closestEntry(to: .now, entries: fixture.entries) else {
            return .placeholder
        }
        return AnnoGlance(entry: entry)
    }

    static func routeTitles(bundle: Bundle = .main) -> [String] {
        let filenames = [
            "holy_land_passion",
            "rome_seven_churches",
            "camino_de_santiago",
            "socal_vietnamese_catholic_pilgrimage_la_vang",
            "basilica_of_our_lady_of_guadalupe"
        ]

        return filenames.compactMap { name in
            guard let url = bundle.url(
                forResource: name,
                withExtension: "json",
                subdirectory: "PilgrimageRoutes"
            ) ?? bundle.url(forResource: name, withExtension: "json"),
            let data = try? Data(contentsOf: url),
            let route = try? JSONDecoder().decode(PilgrimageRoute.self, from: data) else {
                return nil
            }
            return route.titleEn
        }
    }

    private static func loadFixture(bundle: Bundle) -> AnnoFixture? {
        guard let url = bundle.url(forResource: "anno_unified_2026", withExtension: "json"),
              let data = try? Data(contentsOf: url) else {
            return nil
        }

        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return try? decoder.decode(AnnoFixture.self, from: data)
    }

    private static func closestEntry(to date: Date, entries: [AnnoEntry]) -> AnnoEntry? {
        let formatter = DateFormatter()
        formatter.calendar = Calendar(identifier: .gregorian)
        formatter.locale = Locale(identifier: "en_US_POSIX")
        formatter.dateFormat = "yyyy-MM-dd"

        return entries.min { lhs, rhs in
            let lhsDate = formatter.date(from: lhs.date) ?? .distantPast
            let rhsDate = formatter.date(from: rhs.date) ?? .distantPast
            return abs(lhsDate.timeIntervalSince(date)) < abs(rhsDate.timeIntervalSince(date))
        }
    }
}
