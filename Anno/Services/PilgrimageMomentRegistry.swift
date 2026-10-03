import Foundation

enum PilgrimageMomentLevel: String, Codable, Sendable {
    case highlight
    case climax

    var sacredIntensity: SacredIntensity {
        switch self {
        case .highlight: return .feast
        case .climax: return .solemnity
        }
    }
}

struct PilgrimageMoment: Codable, Hashable, Sendable {
    let routeId: String
    let waypointId: String
    let level: PilgrimageMomentLevel
    let labelEn: String
    let labelVi: String

    enum CodingKeys: String, CodingKey {
        case routeId = "route_id"
        case waypointId = "waypoint_id"
        case level
        case labelEn = "label_en"
        case labelVi = "label_vi"
    }

    func label(for language: LanguageMode) -> String {
        language == .vietnamese ? labelVi : labelEn
    }
}

private struct PilgrimageMomentManifest: Codable, Sendable {
    let schemaVersion: String
    let moments: [PilgrimageMoment]

    enum CodingKeys: String, CodingKey {
        case schemaVersion = "schema_version"
        case moments
    }
}

@MainActor
final class PilgrimageMomentRegistry {
    static let shared = PilgrimageMomentRegistry()

    private(set) var moments: [PilgrimageMoment] = []

    private init() {
        load()
    }

    func moment(routeId: String, waypointId: String) -> PilgrimageMoment? {
        moments.first {
            $0.routeId == routeId && $0.waypointId == waypointId
        }
    }

    private func load(bundle: Bundle = .main) {
        guard let url = bundle.url(
            forResource: "pilgrimage_moments_v1",
            withExtension: "json"
        ),
        let data = try? Data(contentsOf: url),
        let manifest = try? JSONDecoder().decode(PilgrimageMomentManifest.self, from: data) else {
            return
        }

        moments = manifest.moments
    }
}
