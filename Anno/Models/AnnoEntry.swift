import Foundation

struct AnnoFixture: Codable {
    let schemaVersion: String
    let generatedOn: String
    let entries: [AnnoEntry]
}

struct WeekFixture: Codable {
    let schemaVersion: String
    let generatedOn: String
    let description: String
    let sourceFile: String
    let entryIds: [String]
}

struct AnnoEntry: Codable, Identifiable, Hashable {
    let id: String
    let date: String
    let weekday: String
    let mockPriority: String
    let liturgical: LiturgicalInfo
    let calendars: CalendarConversions
    let primary: PrimaryContent
    let place: SacredPlace?
    let artwork: ArtworkCandidate
    let sources: [SourceRef]
    let appHooks: AppHooks

    var parsedDate: Date? {
        Self.dateFormatter.date(from: date)
    }

    private static let dateFormatter: DateFormatter = {
        let formatter = DateFormatter()
        formatter.calendar = Calendar(identifier: .gregorian)
        formatter.locale = Locale(identifier: "en_US_POSIX")
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter
    }()
}

struct LiturgicalInfo: Codable, Hashable {
    let rank: String
    let color: String
    let titleEn: String
    let titleVi: String
}

struct CalendarConversions: Codable, Hashable {
    let julian: String
    let hebrew: String
    let islamicUmmAlQura: String
    let coptic: String
    let ethiopian: String
}

struct PrimaryContent: Codable, Hashable {
    let type: String
    let titleEn: String
    let titleVi: String
    let summaryEn: String
    let summaryVi: String
    let confidence: ConfidenceLevel
    let confidenceNoteEn: String
    let confidenceNoteVi: String
}

struct SacredPlace: Codable, Hashable {
    let name: String
    let latitude: Double
    let longitude: Double
    let confidence: ConfidenceLevel
    let sourceUrl: String
}

struct ArtworkCandidate: Codable, Hashable {
    let title: String
    let maker: String
    let dateLabel: String
    let sourceUrl: String
    let status: String
}

struct SourceRef: Codable, Identifiable, Hashable {
    var id: String { url }
    let label: String
    let url: String
    let type: String
}

struct AppHooks: Codable, Hashable {
    let heroLineEn: String
    let heroLineVi: String
    let prayerPromptEn: String
    let prayerPromptVi: String
}

enum ConfidenceLevel: String, Codable, Hashable {
    case confirmed
    case traditional
    case disputed
    case contextual
}
