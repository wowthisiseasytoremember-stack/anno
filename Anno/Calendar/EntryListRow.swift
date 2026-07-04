import SwiftUI

struct EntryListRow: View {
    let entry: AnnoEntry
    let language: LanguageMode
    let isSelected: Bool

    private var text: LocalizedEntryText {
        LocalizedEntryText(entry: entry, language: language)
    }

    var body: some View {
        HStack(alignment: .top, spacing: 14) {
            VStack(spacing: 2) {
                Text(dayNumber)
                    .font(.title3.monospacedDigit().weight(.semibold))
                    .foregroundStyle(isSunday ? AnnoTheme.goldLeaf : AnnoTheme.vellum)
                Text(shortWeekday)
                    .font(.caption.weight(.semibold))
                    .foregroundStyle(AnnoTheme.incense)
            }
            .frame(width: 44)

            VStack(alignment: .leading, spacing: 7) {
                Text(text.title)
                    .font(.headline)
                    .foregroundStyle(AnnoTheme.vellum)
                    .fixedSize(horizontal: false, vertical: true)

                Text(text.liturgicalTitle)
                    .font(.subheadline)
                    .foregroundStyle(isSunday ? AnnoTheme.goldLeaf : AnnoTheme.incense)
                    .fixedSize(horizontal: false, vertical: true)

                ConfidenceBadge(label: text.confidenceLabel, confidence: entry.primary.confidence)
            }
        }
        .padding(.vertical, 8)
        .contentShape(Rectangle())
        .overlay(alignment: .leading) {
            if isSelected {
                Rectangle()
                    .fill(AnnoTheme.goldLeaf)
                    .frame(width: 3)
                    .offset(x: -8)
            }
        }
    }

    private var isSunday: Bool {
        entry.weekday == "Sunday"
    }

    private var dayNumber: String {
        String(entry.date.suffix(2))
    }

    private var shortWeekday: String {
        language == .vietnamese ? viWeekday : String(entry.weekday.prefix(3))
    }

    private var viWeekday: String {
        switch entry.weekday {
        case "Monday": return "T2"
        case "Tuesday": return "T3"
        case "Wednesday": return "T4"
        case "Thursday": return "T5"
        case "Friday": return "T6"
        case "Saturday": return "T7"
        case "Sunday": return "CN"
        default: return entry.weekday
        }
    }
}
