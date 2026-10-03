import Combine
import Foundation

struct SoCalExemplarContent: Codable, Sendable {
    let schemaVersion: String
    let routeId: String
    let translationStatus: String
    let contentPrinciple: String
    let opening: Opening
    let variants: [Variant]
    let chapters: [Chapter]
    let completion: Completion

    enum CodingKeys: String, CodingKey {
        case schemaVersion = "schema_version"
        case routeId = "route_id"
        case translationStatus = "translation_status"
        case contentPrinciple = "content_principle"
        case opening
        case variants
        case chapters
        case completion
    }

    struct Opening: Codable, Sendable {
        let titleEn: String
        let titleVi: String
        let hookEn: String
        let hookVi: String
        let primaryCtaEn: String
        let primaryCtaVi: String
        let secondaryCtaEn: String
        let secondaryCtaVi: String

        enum CodingKeys: String, CodingKey {
            case titleEn = "title_en"
            case titleVi = "title_vi"
            case hookEn = "hook_en"
            case hookVi = "hook_vi"
            case primaryCtaEn = "primary_cta_en"
            case primaryCtaVi = "primary_cta_vi"
            case secondaryCtaEn = "secondary_cta_en"
            case secondaryCtaVi = "secondary_cta_vi"
        }
    }

    struct Variant: Codable, Identifiable, Sendable {
        let id: String
        let titleEn: String
        let titleVi: String
        let chapterIds: [String]

        enum CodingKeys: String, CodingKey {
            case id
            case titleEn = "title_en"
            case titleVi = "title_vi"
            case chapterIds = "chapter_ids"
        }

        func title(for language: LanguageMode) -> String {
            language == .vietnamese ? titleVi : titleEn
        }
    }

    struct Chapter: Codable, Identifiable, Sendable {
        let id: String
        let order: Int
        let geographicName: String
        let city: String
        let address: String
        let officialUrl: String
        let roleEn: String
        let roleVi: String
        let stations: [Station]

        enum CodingKeys: String, CodingKey {
            case id
            case order
            case geographicName = "geographic_name"
            case city
            case address
            case officialUrl = "official_url"
            case roleEn = "role_en"
            case roleVi = "role_vi"
            case stations
        }

        func role(for language: LanguageMode) -> String {
            language == .vietnamese ? roleVi : roleEn
        }
    }

    struct Station: Codable, Identifiable, Sendable {
        let waypointId: String?
        let stationId: String?
        let stationRole: String
        let momentLevel: String
        let momentLabelEn: String?
        let momentLabelVi: String?
        let titleEn: String
        let titleVi: String
        let arriveEn: String
        let arriveVi: String
        let lookEn: String
        let lookVi: String
        let knowEn: String
        let knowVi: String
        let prayEn: String
        let prayVi: String
        let continueEn: String
        let continueVi: String
        let officialUrl: String

        enum CodingKeys: String, CodingKey {
            case waypointId = "waypoint_id"
            case stationId = "station_id"
            case stationRole = "station_role"
            case momentLevel = "moment_level"
            case momentLabelEn = "moment_label_en"
            case momentLabelVi = "moment_label_vi"
            case titleEn = "title_en"
            case titleVi = "title_vi"
            case arriveEn = "arrive_en"
            case arriveVi = "arrive_vi"
            case lookEn = "look_en"
            case lookVi = "look_vi"
            case knowEn = "know_en"
            case knowVi = "know_vi"
            case prayEn = "pray_en"
            case prayVi = "pray_vi"
            case continueEn = "continue_en"
            case continueVi = "continue_vi"
            case officialUrl = "official_url"
        }

        var id: String {
            waypointId ?? stationId ?? titleEn
        }

        func title(for language: LanguageMode) -> String {
            language == .vietnamese ? titleVi : titleEn
        }

        func momentLabel(for language: LanguageMode) -> String? {
            language == .vietnamese ? momentLabelVi : momentLabelEn
        }

        func arrive(for language: LanguageMode) -> String {
            language == .vietnamese ? arriveVi : arriveEn
        }

        func look(for language: LanguageMode) -> String {
            language == .vietnamese ? lookVi : lookEn
        }

        func know(for language: LanguageMode) -> String {
            language == .vietnamese ? knowVi : knowEn
        }

        func pray(for language: LanguageMode) -> String {
            language == .vietnamese ? prayVi : prayEn
        }

        func continueText(for language: LanguageMode) -> String {
            language == .vietnamese ? continueVi : continueEn
        }
    }

    struct Completion: Codable, Sendable {
        let titleEn: String
        let titleVi: String
        let bodyEn: String
        let bodyVi: String
        let invocationEn: String
        let invocationVi: String

        enum CodingKeys: String, CodingKey {
            case titleEn = "title_en"
            case titleVi = "title_vi"
            case bodyEn = "body_en"
            case bodyVi = "body_vi"
            case invocationEn = "invocation_en"
            case invocationVi = "invocation_vi"
        }

        func title(for language: LanguageMode) -> String {
            language == .vietnamese ? titleVi : titleEn
        }

        func body(for language: LanguageMode) -> String {
            language == .vietnamese ? bodyVi : bodyEn
        }

        func invocation(for language: LanguageMode) -> String {
            language == .vietnamese ? invocationVi : invocationEn
        }
    }

    func chapter(containing stationId: String) -> Chapter? {
        chapters.first { chapter in
            chapter.stations.contains { $0.id == stationId }
        }
    }

    func station(id: String) -> Station? {
        chapters.lazy.flatMap(\.stations).first { $0.id == id }
    }
}

@MainActor
final class SoCalExemplarContentLoader: ObservableObject {
    static let shared = SoCalExemplarContentLoader()

    @Published private(set) var content: SoCalExemplarContent?

    private init() {
        load()
    }

    private func load(bundle: Bundle = .main) {
        guard let url = bundle.url(
            forResource: "socal_la_vang_exemplar_content_v1",
            withExtension: "json"
        ),
        let data = try? Data(contentsOf: url),
        let decoded = try? JSONDecoder().decode(SoCalExemplarContent.self, from: data) else {
            return
        }

        content = decoded
    }
}
