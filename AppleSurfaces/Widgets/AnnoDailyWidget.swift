// Source-complete WidgetKit prototype.
//
// Deliberately not added to the shipping Xcode target yet. When Mac/Xcode
// validation is available, activate this as an iOS Widget Extension and reuse
// the accessory views for the future watchOS widget/complication target.

import SwiftUI
import WidgetKit

struct AnnoWidgetEntry: TimelineEntry {
    let date: Date
    let glance: AnnoGlance
}

struct AnnoWidgetProvider: TimelineProvider {
    func placeholder(in context: Context) -> AnnoWidgetEntry {
        AnnoWidgetEntry(date: .now, glance: .placeholder)
    }

    func getSnapshot(in context: Context, completion: @escaping (AnnoWidgetEntry) -> Void) {
        completion(AnnoWidgetEntry(date: .now, glance: .placeholder))
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<AnnoWidgetEntry>) -> Void) {
        let entry = AnnoWidgetEntry(date: .now, glance: loadTodayGlance())
        let calendar = Calendar(identifier: .gregorian)
        let nextMidnight = calendar.nextDate(
            after: .now,
            matching: DateComponents(hour: 0, minute: 2),
            matchingPolicy: .nextTime
        ) ?? .now.addingTimeInterval(6 * 60 * 60)

        completion(Timeline(entries: [entry], policy: .after(nextMidnight)))
    }

    private func loadTodayGlance(bundle: Bundle = .main) -> AnnoGlance {
        guard let url = bundle.url(forResource: "anno_unified_2026", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let fixture = try? JSONDecoder.anno.decode(AnnoFixture.self, from: data),
              let entry = closestEntry(to: .now, entries: fixture.entries) else {
            return .placeholder
        }

        return AnnoGlance(entry: entry)
    }

    private func closestEntry(to date: Date, entries: [AnnoEntry]) -> AnnoEntry? {
        let formatter = DateFormatter.annoISODate

        return entries.min { lhs, rhs in
            let lhsDate = formatter.date(from: lhs.date) ?? .distantPast
            let rhsDate = formatter.date(from: rhs.date) ?? .distantPast
            return abs(lhsDate.timeIntervalSince(date)) < abs(rhsDate.timeIntervalSince(date))
        }
    }
}

struct AnnoDailyWidgetView: View {
    @Environment(\.widgetFamily) private var family
    let entry: AnnoWidgetEntry

    private enum Emphasis {
        case ordinary
        case feast
        case solemnity
    }

    private var emphasis: Emphasis {
        switch entry.glance.rank.lowercased() {
        case "solemnity":
            return .solemnity
        case "sunday", "feast", "memorial", "optional memorial":
            return .feast
        default:
            return .ordinary
        }
    }

    private var accent: Color {
        switch entry.glance.liturgicalColorName.lowercased() {
        case "red":
            return Color(red: 0.55, green: 0.18, blue: 0.23)
        case "purple", "violet":
            return Color(red: 0.36, green: 0.24, blue: 0.43)
        case "green", "verdigris":
            return Color(red: 0.23, green: 0.42, blue: 0.32)
        case "white", "gold":
            return Color(red: 0.79, green: 0.66, blue: 0.30)
        default:
            return Color(red: 0.79, green: 0.66, blue: 0.30)
        }
    }

    var body: some View {
        switch family {
        case .accessoryCircular:
            accessoryCircular
        case .accessoryRectangular:
            accessoryRectangular
        case .accessoryInline:
            accessoryInline
        default:
            systemWidget
        }
    }

    private var systemWidget: some View {
        ZStack(alignment: .topTrailing) {
            if emphasis == .solemnity {
                Circle()
                    .fill(
                        RadialGradient(
                            colors: [
                                Color(red: 0.85, green: 0.72, blue: 0.36).opacity(0.34),
                                .clear
                            ],
                            center: .center,
                            startRadius: 0,
                            endRadius: 90
                        )
                    )
                    .frame(width: 150, height: 150)
                    .offset(x: 55, y: -58)
            }

            VStack(alignment: .leading, spacing: 8) {
                HStack(spacing: 6) {
                    Image(systemName: "cross.fill")
                        .font(.caption2)
                        .foregroundStyle(emphasis == .ordinary ? .secondary : accent)

                    Text("ANNO")
                        .font(.caption2.weight(.semibold))
                        .tracking(1.3)

                    Spacer()

                    if emphasis != .ordinary {
                        Text(entry.glance.rank.uppercased())
                            .font(.caption2.weight(.bold))
                            .foregroundStyle(emphasis == .solemnity ? accent : .secondary)
                            .lineLimit(1)
                    }
                }
                .foregroundStyle(.secondary)

                Text(entry.glance.title)
                    .font(emphasis == .solemnity ? .title3.bold() : .headline)
                    .fontDesign(.serif)
                    .lineLimit(emphasis == .solemnity ? 3 : 2)

                Text(entry.glance.subtitle)
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .lineLimit(2)

                Spacer(minLength: 0)

                HStack(spacing: 6) {
                    Circle()
                        .fill(accent)
                        .frame(width: 7, height: 7)

                    Text(emphasis == .ordinary ? entry.glance.rank : "TODAY IS SPECIAL")
                        .font(.caption2.weight(emphasis == .solemnity ? .bold : .medium))
                        .foregroundStyle(emphasis == .solemnity ? accent : .secondary)
                }
            }
        }
        .containerBackground(for: .widget) {
            LinearGradient(
                colors: emphasis == .solemnity
                    ? [
                        Color(red: 0.10, green: 0.085, blue: 0.06),
                        accent.opacity(0.18),
                        Color(red: 0.075, green: 0.067, blue: 0.055)
                    ]
                    : [
                        Color(red: 0.075, green: 0.067, blue: 0.055),
                        accent.opacity(emphasis == .feast ? 0.10 : 0.035)
                    ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        }
    }

    private var accessoryCircular: some View {
        ZStack {
            AccessoryWidgetBackground()

            if emphasis != .ordinary {
                Circle()
                    .strokeBorder(.primary.opacity(emphasis == .solemnity ? 0.95 : 0.5), lineWidth: emphasis == .solemnity ? 2 : 1)
                    .padding(2)
            }

            VStack(spacing: 1) {
                Image(systemName: emphasis == .solemnity ? "sparkles" : "cross.fill")
                Text(dayNumber)
                    .font(.caption.weight(.bold))
            }
        }
        .widgetLabel {
            Text(entry.glance.title)
        }
    }

    private var accessoryRectangular: some View {
        HStack(spacing: 8) {
            Image(systemName: emphasis == .solemnity ? "sparkles" : "cross.fill")
                .font(.headline)

            VStack(alignment: .leading, spacing: 2) {
                Text(entry.glance.rank.uppercased())
                    .font(.caption2.weight(.semibold))
                Text(entry.glance.title)
                    .font(.headline)
                    .fontDesign(.serif)
                    .lineLimit(2)
            }
        }
    }

    private var accessoryInline: some View {
        Label(entry.glance.title, systemImage: "cross.fill")
    }

    private var dayNumber: String {
        let formatter = DateFormatter.annoISODate
        guard let date = formatter.date(from: entry.glance.date) else {
            return "•"
        }
        return String(Calendar(identifier: .gregorian).component(.day, from: date))
    }
}

struct AnnoDailyWidget: Widget {
    let kind = "org.anno.daily"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: AnnoWidgetProvider()) { entry in
            AnnoDailyWidgetView(entry: entry)
        }
        .configurationDisplayName("Today in Anno")
        .description("A glance at today's feast or devotional entry.")
        .supportedFamilies([
            .systemSmall,
            .systemMedium,
            .accessoryCircular,
            .accessoryRectangular,
            .accessoryInline
        ])
    }
}

private extension JSONDecoder {
    static var anno: JSONDecoder {
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return decoder
    }
}

private extension DateFormatter {
    static let annoISODate: DateFormatter = {
        let formatter = DateFormatter()
        formatter.calendar = Calendar(identifier: .gregorian)
        formatter.locale = Locale(identifier: "en_US_POSIX")
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter
    }()
}
