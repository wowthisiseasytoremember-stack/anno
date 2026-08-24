import CoreLocation
import Foundation

// MARK: - Spiritual Calling Categories

public enum SpiritualCalling: String, CaseIterable, Identifiable {
    case all = "all"
    case marian = "marian"
    case apostolic = "apostolic"
    case martyrs = "martyrs"
    case eucharisticPassion = "eucharistic_passion"
    case monasticDesert = "monastic_desert"

    public var id: String { rawValue }

    public func title(for language: LanguageMode) -> String {
        switch self {
        case .all:
            return language == .vietnamese ? "Tất cả con đường" : "All Corridors"
        case .marian:
            return language == .vietnamese ? "Linh Địa Thánh Mẫu" : "Marian Apparitions"
        case .apostolic:
            return language == .vietnamese ? "Bước Chân Tông Đồ" : "Apostolic Journeys"
        case .martyrs:
            return language == .vietnamese ? "Đường Tử Đạo Anh Hùng" : "Way of the Martyrs"
        case .eucharisticPassion:
            return language == .vietnamese ? "Thánh Thể & Thương Khó" : "Eucharist & Passion"
        case .monasticDesert:
            return language == .vietnamese ? "Đan Tu & Tĩnh Lặng" : "Monastic & Desert"
        }
    }

    public var icon: String {
        switch self {
        case .all: return "sparkles"
        case .marian: return "heart.fill"
        case .apostolic: return "cross.fill"
        case .martyrs: return "flame.fill"
        case .eucharisticPassion: return "sun.max.fill"
        case .monasticDesert: return "mountain.2.fill"
        }
    }
}

// MARK: - Geographic Regions

public enum PilgrimageRegion: String, CaseIterable, Identifiable {
    case all = "all"
    case socalAmericas = "socal_americas"
    case vietnamAsia = "vietnam_asia"
    case romeItaly = "rome_italy"
    case holyLand = "holy_land"
    case iberiaEurope = "iberia_europe"

    public var id: String { rawValue }

    public func title(for language: LanguageMode) -> String {
        switch self {
        case .all:
            return language == .vietnamese ? "Mọi Vùng Miền" : "Global"
        case .socalAmericas:
            return language == .vietnamese ? "Miền Nam California & Châu Mỹ" : "SoCal & Americas"
        case .vietnamAsia:
            return language == .vietnamese ? "Việt Nam & Đông Nam Á" : "Vietnam & Asia"
        case .romeItaly:
            return language == .vietnamese ? "Rôma & Nước Ý" : "Rome & Italy"
        case .holyLand:
            return language == .vietnamese ? "Đất Thánh & Levant" : "Holy Land"
        case .iberiaEurope:
            return language == .vietnamese ? "Tây Ban Nha & Châu Âu" : "Iberia & Europe"
        }
    }
}

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

    public var calling: SpiritualCalling {
        let lowerId = routeId.lowercased()
        if lowerId.contains("marian") || lowerId.contains("la_vang") || lowerId.contains("guadalupe") || lowerId.contains("lauretana") {
            return .marian
        } else if lowerId.contains("paul") || lowerId.contains("santiago") || lowerId.contains("norte") || lowerId.contains("plata") || lowerId.contains("rome") || lowerId.contains("francigena") {
            return .apostolic
        } else if lowerId.contains("martyr") || lowerId.contains("vietnam") || lowerId.contains("asian") {
            return .martyrs
        } else if lowerId.contains("eucharist") || lowerId.contains("passion") || lowerId.contains("holy_land") {
            return .eucharisticPassion
        } else if lowerId.contains("desert") || lowerId.contains("monastic") || lowerId.contains("ignaciano") || lowerId.contains("olav") || lowerId.contains("cuthbert") {
            return .monasticDesert
        }
        return .apostolic
    }

    public var regionCategory: PilgrimageRegion {
        let lowerId = routeId.lowercased()
        if lowerId.contains("socal") || lowerId.contains("americas") {
            return .socalAmericas
        } else if lowerId.contains("vietnam") || lowerId.contains("asian") || lowerId.contains("martyrs_path") {
            return .vietnamAsia
        } else if lowerId.contains("rome") || lowerId.contains("francigena") || lowerId.contains("lauretana") {
            return .romeItaly
        } else if lowerId.contains("holy_land") {
            return .holyLand
        } else {
            return .iberiaEurope
        }
    }

    public func isLiturgicallyConnected(to entry: AnnoEntry) -> Bool {
        let text = "\(entry.liturgical.titleEn) \(entry.liturgical.titleVi) \(entry.primary.titleEn) \(entry.primary.titleVi) \(entry.place?.name ?? "")".lowercased()
        let rText = "\(titleEn) \(titleVi) \(spiritualThemeEn)".lowercased()

        // Marian matches
        if (text.contains("mary") || text.contains("mẹ") || text.contains("assumption") || text.contains("marian")) && calling == .marian {
            return true
        }
        // Martyrs matches
        if (text.contains("martyr") || text.contains("tử đạo") || text.contains("witness")) && calling == .martyrs {
            return true
        }
        // Passion & Cross matches
        if (text.contains("cross") || text.contains("passion") || text.contains("thánh giá") || text.contains("thánh thể")) && calling == .eucharisticPassion {
            return true
        }
        // Apostle specific
        if text.contains("paul") && rText.contains("paul") { return true }
        if text.contains("james") && rText.contains("santiago") { return true }
        if text.contains("ignatius") && rText.contains("ignaciano") { return true }
        if text.contains("thomas") && (rText.contains("asian") || rText.contains("india")) { return true }
        if text.contains("la vang") && (rText.contains("la vang") || rText.contains("socal")) { return true }

        return false
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

    public var associated3DReliquaryId: String? {
        if waypointId.contains("shroud") || waypointId.contains("textile") {
            return "reliquary_passion_textile"
        } else if waypointId.contains("cross") || waypointId.contains("relic") || waypointId.contains("cathedral") {
            return "reliquary_passion_cross"
        } else if waypointId.contains("santiago") || waypointId.contains("casket") || waypointId.contains("tomb") {
            return "reliquary_silver_casket"
        }
        return nil
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
