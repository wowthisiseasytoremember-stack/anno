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
    var id: String
    var date: String
    var weekday: String
    var mockPriority: String
    var liturgical: LiturgicalInfo
    var calendars: CalendarConversions
    var primary: PrimaryContent
    var place: SacredPlace?
    var artwork: ArtworkCandidate
    var sources: [SourceRef]
    var appHooks: AppHooks

    init(id: String, date: String, weekday: String, mockPriority: String, liturgical: LiturgicalInfo, calendars: CalendarConversions, primary: PrimaryContent, place: SacredPlace?, artwork: ArtworkCandidate, sources: [SourceRef], appHooks: AppHooks) {
        self.id = id
        self.date = date
        self.weekday = weekday
        self.mockPriority = mockPriority
        self.liturgical = liturgical
        self.calendars = calendars
        self.primary = primary
        self.place = place
        self.artwork = artwork
        self.sources = sources
        self.appHooks = appHooks
    }

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
    var type: String
    var titleEn: String
    var titleVi: String
    var summaryEn: String
    var summaryVi: String
    var confidence: ConfidenceLevel
    var confidenceNoteEn: String
    var confidenceNoteVi: String
    var bodyEn: String
    var bodyVi: String

    init(type: String, titleEn: String, titleVi: String, summaryEn: String, summaryVi: String, confidence: ConfidenceLevel, confidenceNoteEn: String, confidenceNoteVi: String, bodyEn: String = "", bodyVi: String = "") {
        self.type = type
        self.titleEn = titleEn
        self.titleVi = titleVi
        self.summaryEn = summaryEn
        self.summaryVi = summaryVi
        self.confidence = confidence
        self.confidenceNoteEn = confidenceNoteEn
        self.confidenceNoteVi = confidenceNoteVi
        self.bodyEn = bodyEn
        self.bodyVi = bodyVi
    }
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
