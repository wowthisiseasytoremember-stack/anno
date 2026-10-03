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
        precondition(!fixture.entries.isEmpty, "FixtureStore requires at least one entry")
        self.fixture = fixture
        self.weekEntryIDs = weekEntryIDs
        self.selectedEntryID = selectedEntryID ?? weekEntryIDs.first ?? fixture.entries[0].id
    }

    func select(_ entry: AnnoEntry) {
        selectedEntryID = entry.id
    }

    static func loadBundledOrFallback() -> FixtureStore {
        do {
            return try loadBundled()
        } catch {
            assertionFailure("Failed to load canonical Anno fixture: \(error)")
            return .contentUnavailable
        }
    }

    static func loadBundled(bundle: Bundle = .main) throws -> FixtureStore {
        let fixture: AnnoFixture = try decodeResource(
            "anno_unified_2026",
            extension: "json",
            bundle: bundle
        )
        guard !fixture.entries.isEmpty else {
            throw FixtureError.emptyResource("anno_unified_2026.json")
        }

        let formatter = DateFormatter()
        formatter.calendar = Calendar(identifier: .gregorian)
        formatter.locale = Locale(identifier: "en_US_POSIX")
        formatter.dateFormat = "yyyy-MM-dd"

        let now = Date()
        let selectedEntry = fixture.entries.min { lhs, rhs in
            let lhsDate = formatter.date(from: lhs.date) ?? .distantPast
            let rhsDate = formatter.date(from: rhs.date) ?? .distantPast
            return abs(lhsDate.timeIntervalSince(now)) < abs(rhsDate.timeIntervalSince(now))
        } ?? fixture.entries[0]

        let selectedDate = formatter.date(from: selectedEntry.date) ?? now
        let calendar = Calendar(identifier: .gregorian)
        let weekDateKeys = Set((-3...3).compactMap { offset -> String? in
            guard let date = calendar.date(byAdding: .day, value: offset, to: selectedDate) else {
                return nil
            }
            return formatter.string(from: date)
        })

        let weekIDs = fixture.entries
            .filter { weekDateKeys.contains($0.date) }
            .map(\.id)

        return FixtureStore(
            fixture: fixture,
            weekEntryIDs: weekIDs,
            selectedEntryID: selectedEntry.id
        )
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
    case emptyResource(String)

    var errorDescription: String? {
        switch self {
        case .missingResource(let name):
            return "Missing bundled fixture resource: \(name)"
        case .emptyResource(let name):
            return "Bundled fixture contains no entries: \(name)"
        }
    }
}

extension FixtureStore {
    static let contentUnavailable: FixtureStore = {
        let entry = AnnoEntry(
            id: "anno-content-unavailable",
            date: "2026-10-03",
            weekday: "Saturday",
            mockPriority: "error_fallback",
            liturgical: LiturgicalInfo(
                rank: "Unavailable",
                color: "gold",
                titleEn: "Content unavailable",
                titleVi: "Nội dung không khả dụng"
            ),
            calendars: CalendarConversions(
                julian: "—",
                hebrew: "—",
                islamicUmmAlQura: "—",
                coptic: "—",
                ethiopian: "—"
            ),
            primary: PrimaryContent(
                type: "error",
                titleEn: "Anno content could not be loaded",
                titleVi: "Không thể tải nội dung Anno",
                summaryEn: "The bundled devotional data is unavailable. This is an app-data error, not a devotional entry.",
                summaryVi: "Dữ liệu nội dung đi kèm không khả dụng. Đây là lỗi dữ liệu ứng dụng, không phải nội dung suy niệm.",
                confidence: .contextual,
                confidenceNoteEn: "No devotional claim is being shown.",
                confidenceNoteVi: "Không hiển thị tuyên bố nội dung suy niệm."
            ),
            place: nil,
            artwork: ArtworkCandidate(
                title: "Content unavailable",
                maker: "Anno",
                dateLabel: "",
                sourceUrl: "",
                status: "unavailable"
            ),
            sources: [],
            appHooks: AppHooks(
                heroLineEn: "Content failed closed instead of substituting preview data.",
                heroLineVi: "Ứng dụng dừng an toàn thay vì thay thế bằng dữ liệu xem trước.",
                prayerPromptEn: "Reopen the app after the content bundle is repaired.",
                prayerPromptVi: "Mở lại ứng dụng sau khi gói nội dung được sửa."
            )
        )

        return FixtureStore(
            fixture: AnnoFixture(
                schemaVersion: "anno.error.v1",
                generatedOn: "2026-10-03",
                entries: [entry]
            ),
            weekEntryIDs: [entry.id],
            selectedEntryID: entry.id
        )
    }()

    static let preview: FixtureStore = {
        let entry = AnnoEntry(
            id: "anno-2026-07-03-thomas",
            date: "2026-07-03",
            weekday: "Friday",
            mockPriority: "preview",
            liturgical: LiturgicalInfo(rank: "Feast", color: "red", titleEn: "Saint Thomas, Apostle", titleVi: "Thánh Tôma, Tông đồ"),
            calendars: CalendarConversions(julian: "2026-06-20", hebrew: "18 Tamuz 5786", islamicUmmAlQura: "18 Muharram 1448 AH", coptic: "26 Paoni 1742", ethiopian: "26 Sene 2018"),
            primary: PrimaryContent(
                type: "saint",
                titleEn: "Saint Thomas the Apostle",
                titleVi: "Thánh Tôma Tông đồ",
                summaryEn: "Preview content for SwiftUI development.",
                summaryVi: "Nội dung xem trước cho quá trình phát triển SwiftUI.",
                confidence: .confirmed,
                confidenceNoteEn: "Preview only.",
                confidenceNoteVi: "Chỉ dùng để xem trước."
            ),
            place: nil,
            artwork: ArtworkCandidate(
                title: "The Incredulity of Saint Thomas",
                maker: "Caravaggio",
                dateLabel: "c. 1601–1602",
                sourceUrl: "https://en.wikipedia.org/wiki/The_Incredulity_of_Saint_Thomas_(Caravaggio)",
                status: "preview"
            ),
            sources: [],
            appHooks: AppHooks(
                heroLineEn: "SwiftUI preview content.",
                heroLineVi: "Nội dung xem trước SwiftUI.",
                prayerPromptEn: "Preview.",
                prayerPromptVi: "Xem trước."
            )
        )

        return FixtureStore(
            fixture: AnnoFixture(schemaVersion: "anno.preview.v1", generatedOn: "2026-07-03", entries: [entry]),
            weekEntryIDs: [entry.id]
        )
    }()
}
