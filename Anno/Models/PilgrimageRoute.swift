import CoreLocation
import Foundation

// MARK: - Pilgrimage Route Model

public struct PilgrimageRoute: Identifiable, Codable, Hashable {
    public var id: String { routeId }
    public let routeId: String
    public let titleEn: String
    public let titleVi: String
    public let region: String
    public let durationDays: Int
    public let distanceKm: Double
    public let difficulty: String
    public let spiritualThemeEn: String
    public let spiritualThemeVi: String
    public let overviewEn: String
    public let overviewVi: String
    public let waypoints: [PilgrimageWaypoint]

    enum CodingKeys: String, CodingKey {
        case routeId = "route_id"
        case titleEn = "title_en"
        case titleVi = "title_vi"
        case region
        case durationDays = "duration_days"
        case distanceKm = "distance_km"
        case difficulty
        case spiritualThemeEn = "spiritual_theme_en"
        case spiritualThemeVi = "spiritual_theme_vi"
        case overviewEn = "overview_en"
        case overviewVi = "overview_vi"
        case waypoints
    }

    public func title(for language: LanguageMode) -> String {
        language == .vietnamese ? titleVi : titleEn
    }

    public func spiritualTheme(for language: LanguageMode) -> String {
        language == .vietnamese ? spiritualThemeVi : spiritualThemeEn
    }

    public func overview(for language: LanguageMode) -> String {
        language == .vietnamese ? overviewVi : overviewEn
    }

    public var coordinates: [CLLocationCoordinate2D] {
        waypoints.map(\.coordinate)
    }

    public var difficultyDisplay: String {
        switch difficulty.lowercased() {
        case "easy": return "Easy / Nhẹ nhàng"
        case "moderate": return "Moderate / Vừa phải"
        case "challenging", "difficult": return "Challenging / Thử thách"
        default: return difficulty.capitalized
        }
    }
}

// MARK: - Pilgrimage Waypoint Model

public struct PilgrimageWaypoint: Identifiable, Codable, Hashable {
    public var id: String { waypointId }
    public let waypointId: String
    public let nameEn: String
    public let nameVi: String
    public let latitude: Double
    public let longitude: Double
    public let order: Int
    public let historicalSummaryEn: String
    public let historicalSummaryVi: String
    public let sacredRelicEn: String
    public let sacredRelicVi: String
    public let scriptureReading: String
    public let suggestedPrayerEn: String
    public let suggestedPrayerVi: String

    enum CodingKeys: String, CodingKey {
        case waypointId = "waypoint_id"
        case nameEn = "name_en"
        case nameVi = "name_vi"
        case latitude
        case longitude
        case order
        case historicalSummaryEn = "historical_summary_en"
        case historicalSummaryVi = "historical_summary_vi"
        case sacredRelicEn = "sacred_relic_en"
        case sacredRelicVi = "sacred_relic_vi"
        case scriptureReading = "scripture_reading"
        case suggestedPrayerEn = "suggested_prayer_en"
        case suggestedPrayerVi = "suggested_prayer_vi"
    }

    public var coordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
    }

    public func name(for language: LanguageMode) -> String {
        language == .vietnamese ? nameVi : nameEn
    }

    public func historicalSummary(for language: LanguageMode) -> String {
        language == .vietnamese ? historicalSummaryVi : historicalSummaryEn
    }

    public func sacredRelic(for language: LanguageMode) -> String {
        language == .vietnamese ? sacredRelicVi : sacredRelicEn
    }

    public func suggestedPrayer(for language: LanguageMode) -> String {
        language == .vietnamese ? suggestedPrayerVi : suggestedPrayerEn
    }
}

// MARK: - Master Geography Catalog Root

public struct SacredGeographyMaster: Codable {
    public let schemaVersion: String
    public let compiledOn: String
    public let descriptionEn: String
    public let descriptionVi: String
    public let countriesCovered: [String]
    public let sanctuaries: [Sanctuary]
    public let pilgrimageRoutes: [PilgrimageRoute]

    enum CodingKeys: String, CodingKey {
        case schemaVersion = "schema_version"
        case compiledOn = "compiled_on"
        case descriptionEn = "description_en"
        case descriptionVi = "description_vi"
        case countriesCovered = "countries_covered"
        case sanctuaries
        case pilgrimageRoutes = "pilgrimage_routes"
    }
}
