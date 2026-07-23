import Foundation

final class FixtureStore: ObservableObject {
    @Published var selectedEntryID: AnnoEntry.ID

    let fixture: AnnoFixture
    let weekEntryIDs: [String]

    var allEntries: [AnnoEntry] {
        fixture.entries
    }

    var weekEntries: [AnnoEntry] {
        let byID = Dictionary(uniqueKeysWithValues: allEntries.map { ($0.id, $0) })
        return weekEntryIDs.compactMap { byID[$0] }
    }

    var selectedEntry: AnnoEntry {
        allEntries.first { $0.id == selectedEntryID } ?? allEntries[0]
    }

    init(fixture: AnnoFixture, weekEntryIDs: [String], selectedEntryID: AnnoEntry.ID? = nil) {
        self.fixture = fixture
        self.weekEntryIDs = weekEntryIDs
        self.selectedEntryID = selectedEntryID ?? weekEntryIDs.first ?? fixture.entries[0].id
    }

    func select(_ entry: AnnoEntry) {
        selectedEntryID = entry.id
    }

    static func loadBundledOrPreview() -> FixtureStore {
        do {
            return try loadBundled()
        } catch {
            return .preview
        }
    }

    static func loadBundled(bundle: Bundle = .main) throws -> FixtureStore {
        let fixture: AnnoFixture = try decodeResource(
            "anno_full_2026_2029",
            extension: "json",
            bundle: bundle
        )
        let week: WeekFixture = try decodeResource(
            "anno_week_current",
            extension: "json",
            bundle: bundle
        )
        return FixtureStore(fixture: fixture, weekEntryIDs: week.entryIds)
    }

    private static func decodeResource<T: Decodable>(
        _ name: String,
        extension fileExtension: String,
        bundle: Bundle
    ) throws -> T {
        guard let url = bundle.url(forResource: name, withExtension: fileExtension) else {
            throw FixtureError.missingResource(name)
        }

        let data = try Data(contentsOf: url)
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return try decoder.decode(T.self, from: data)
    }
}

enum FixtureError: LocalizedError {
    case missingResource(String)

    var errorDescription: String? {
        switch self {
        case .missingResource(let name):
            return "Missing bundled fixture resource: \(name)"
        }
    }
}

extension FixtureStore {
    static let preview: FixtureStore = {
        let entry = AnnoEntry(
            id: "anno-2026-07-03-thomas",
            date: "2026-07-03",
            weekday: "Friday",
            mockPriority: "week_real_data",
            liturgical: LiturgicalInfo(rank: "Feast", color: "red", titleEn: "Saint Thomas, Apostle", titleVi: "Thánh Tôma, Tông đồ"),
            calendars: CalendarConversions(julian: "2026-06-20", hebrew: "18 Tamuz 5786", islamicUmmAlQura: "18 Muharram 1448 AH", coptic: "26 Paoni 1742", ethiopian: "26 Sene 1750"),
            primary: PrimaryContent(type: "saint", titleEn: "Saint Thomas the Apostle", titleVi: "Thánh Tôma Tông đồ", summaryEn: "The feast centers the apostle who moves from wounded doubt to one of the Church's strongest confessions of Christ.", summaryVi: "Lễ kính đặt trọng tâm nơi vị tông đồ đi từ nghi ngờ trước các vết thương đến lời tuyên xưng mạnh mẽ về Đức Kitô.", confidence: .confirmed, confidenceNoteEn: "The feast is confirmed. The Chennai martyrdom and tomb traditions should be labeled traditional.", confidenceNoteVi: "Lễ kính đã được xác nhận. Truyền thống tử đạo và mộ tại Chennai nên được ghi là theo truyền thống."),
            place: SacredPlace(name: "St. Thomas Mount National Shrine, Chennai", latitude: 13.0078, longitude: 80.1925, confidence: .traditional, sourceUrl: "https://stthomasmountbasilica.com/"),
            artwork: ArtworkCandidate(title: "The Incredulity of Saint Thomas", maker: "Caravaggio", dateLabel: "c. 1601-1602", sourceUrl: "https://en.wikipedia.org/wiki/The_Incredulity_of_Saint_Thomas_(Caravaggio)", status: "provenance_candidate"),
            sources: [
                SourceRef(label: "USCCB daily readings", url: "https://bible.usccb.org/bible/readings/070326.cfm", type: "liturgical"),
                SourceRef(label: "Vatican News saint profile", url: "https://www.vaticannews.va/en/saints/07/03/st--thomas--apostle.html", type: "church_biography")
            ],
            appHooks: AppHooks(heroLineEn: "This day remembers the apostle who asked to see the wounds.", heroLineVi: "Ngày này tưởng nhớ vị tông đồ xin được thấy các vết thương.", prayerPromptEn: "Ask for faith that can tell the truth about doubt.", prayerPromptVi: "Xin đức tin biết nói thật về sự nghi ngờ.")
        )

        return FixtureStore(
            fixture: AnnoFixture(schemaVersion: "anno.mock.v1", generatedOn: "2026-07-03", entries: [entry]),
            weekEntryIDs: [entry.id]
        )
    }()
}
