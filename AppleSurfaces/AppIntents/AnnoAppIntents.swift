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

struct AnnoPilgrimageProgressIntent: AppIntent {
    static let title: LocalizedStringResource = "My La Vang Pilgrimage Progress"
    static let description = IntentDescription(
        "Returns progress for the Orange County La Vang pilgrimage."
    )
    static let supportedModes: IntentModes = [.background]

    func perform() async throws -> some IntentResult & ProvidesDialog {
        let progress = AnnoIntentContent.laVangProgress()

        return .result(
            dialog: IntentDialog(
                stringLiteral: progress.summary
            )
        )
    }
}

struct AnnoNextPilgrimageStationIntent: AppIntent {
    static let title: LocalizedStringResource = "Next La Vang Station"
    static let description = IntentDescription(
        "Returns the next unvisited station on the Orange County La Vang pilgrimage."
    )
    static let supportedModes: IntentModes = [.background]

    func perform() async throws -> some IntentResult & ProvidesDialog {
        let progress = AnnoIntentContent.laVangProgress()

        let response: String
        if progress.isComplete {
            response = "Your Orange County La Vang pilgrimage is complete. Our Lady of La Vang, pray for us."
        } else if let next = progress.nextStationTitle {
            response = "Your next La Vang pilgrimage station is \(next). You have visited \(progress.visitedCount) of \(progress.totalCount) stations."
        } else {
            response = progress.summary
        }

        return .result(dialog: IntentDialog(stringLiteral: response))
    }
}

struct AnnoShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: AnnoTodayIntent(),
            phrases: [
                "Show today in \(.applicationName)",
                "What's today in \(.applicationName)",
                "Show today's devotion in \(.applicationName)"
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

        AppShortcut(
            intent: AnnoPilgrimageProgressIntent(),
            phrases: [
                "Show my La Vang pilgrimage progress in \(.applicationName)",
                "How far am I on my La Vang pilgrimage in \(.applicationName)"
            ],
            shortTitle: "La Vang Progress",
            systemImageName: "chart.bar.fill"
        )

        AppShortcut(
            intent: AnnoNextPilgrimageStationIntent(),
            phrases: [
                "What's next on my La Vang pilgrimage in \(.applicationName)",
                "Show my next La Vang station in \(.applicationName)"
            ],
            shortTitle: "Next La Vang Station",
            systemImageName: "mappin.and.ellipse"
        )
    }
}

private struct AnnoPilgrimageIntentProgress {
    let visitedCount: Int
    let totalCount: Int
    let nextStationTitle: String?

    var isComplete: Bool {
        totalCount > 0 && visitedCount == totalCount
    }

    var summary: String {
        if isComplete {
            return "Your Orange County La Vang pilgrimage is complete."
        }

        if totalCount == 0 {
            return "La Vang pilgrimage progress is unavailable."
        }

        return "You have visited \(visitedCount) of \(totalCount) La Vang pilgrimage stations."
    }
}

private enum AnnoIntentContent {
    private static let laVangRouteId = "socal_vietnamese_catholic_pilgrimage_la_vang"

    static func laVangProgress(
        bundle: Bundle = .main,
        defaults: UserDefaults = .standard
    ) -> AnnoPilgrimageIntentProgress {
        guard let url = bundle.url(
            forResource: "socal_la_vang_exemplar_content_v1",
            withExtension: "json"
        ),
        let data = try? Data(contentsOf: url),
        let root = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
        let variants = root["variants"] as? [[String: Any]],
        let core = variants.first(where: { ($0["id"] as? String) == "core" }),
        let chapterIds = core["chapter_ids"] as? [String],
        let chapters = root["chapters"] as? [[String: Any]] else {
            return AnnoPilgrimageIntentProgress(
                visitedCount: 0,
                totalCount: 0,
                nextStationTitle: nil
            )
        }

        let orderedChapters = chapters
            .filter { chapter in
                guard let id = chapter["id"] as? String else { return false }
                return chapterIds.contains(id)
            }
            .sorted {
                ($0["order"] as? Int ?? 0) < ($1["order"] as? Int ?? 0)
            }

        var required: [(id: String, title: String)] = []

        for chapter in orderedChapters {
            guard let stations = chapter["stations"] as? [[String: Any]] else {
                continue
            }

            for station in stations {
                if (station["station_role"] as? String) == "optional_context" {
                    continue
                }

                guard let id = (station["waypoint_id"] as? String)
                    ?? (station["station_id"] as? String) else {
                    continue
                }

                let title = station["title_en"] as? String ?? id
                required.append((id, title))
            }
        }

        let key = "anno.pilgrimage.\(laVangRouteId).visited"
        let visited = Set(defaults.stringArray(forKey: key) ?? [])
        let visitedCount = required.filter { visited.contains($0.id) }.count
        let nextStationTitle = required.first { !visited.contains($0.id) }?.title

        return AnnoPilgrimageIntentProgress(
            visitedCount: visitedCount,
            totalCount: required.count,
            nextStationTitle: nextStationTitle
        )
    }

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
