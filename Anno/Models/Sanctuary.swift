import CoreLocation
import Foundation

// MARK: - Sanctuary Model

public struct Sanctuary: Identifiable, Codable, Hashable {
    public var id: String { sanctuaryId }
    public let sanctuaryId: String
    public let category: String
    public let nameEn: String
    public let nameVi: String
    public let feastDayAssociation: String?
    public let location: SanctuaryLocation
    public let canonicalStatus: SanctuaryCanonicalStatus
    public let primaryRelics: [SanctuaryRelic]
    public let historicalSummaryEn: String
    public let historicalSummaryVi: String
    public let scriptureReading: String?
    public let suggestedPrayerEn: String
    public let suggestedPrayerVi: String
    public let primarySources: [SanctuarySource]?
    public let iconAssetName: String?

    enum CodingKeys: String, CodingKey {
        case sanctuaryId = "sanctuary_id"
        case category
        case nameEn = "name_en"
        case nameVi = "name_vi"
        case feastDayAssociation = "feast_day_association"
        case location
        case canonicalStatus = "canonical_status"
        case primaryRelics = "primary_relics"
        case historicalSummaryEn = "historical_summary_en"
        case historicalSummaryVi = "historical_summary_vi"
        case scriptureReading = "scripture_reading"
        case suggestedPrayerEn = "suggested_prayer_en"
        case suggestedPrayerVi = "suggested_prayer_vi"
        case primarySources = "primary_sources"
        case iconAssetName = "icon_asset_name"
    }

    public var coordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(latitude: location.latitude, longitude: location.longitude)
    }

    public func name(for language: LanguageMode) -> String {
        language == .vietnamese ? nameVi : nameEn
    }

    public func historicalSummary(for language: LanguageMode) -> String {
        language == .vietnamese ? historicalSummaryVi : historicalSummaryEn
    }

    public func suggestedPrayer(for language: LanguageMode) -> String {
        language == .vietnamese ? suggestedPrayerVi : suggestedPrayerEn
    }

    public var categoryDisplay: String {
        switch category {
        case "marian_apparition": return "Marian Apparition / Hiện Ra Đức Mẹ"
        case "apostolic_tomb": return "Apostolic Tomb / Lăng Mộ Tông Đồ"
        case "eucharistic_miracle": return "Eucharistic Miracle / Phép Lạ Thánh Thể"
        case "passion_relic": return "Passion Relic / Thánh Tích Khổ Nạn"
        case "incorruptible_saint": return "Incorruptible Saint / Thánh Thể Bất Hoại"
        case "martyrs_shrine": return "Martyrs Shrine / Đền Thánh Tử Đạo"
        case "monastic_desert": return "Desert Monastic / Đan Viện Sa Mạc"
        default: return category.replacingOccurrences(of: "_", with: " ").capitalized
        }
    }

    public var associated3DReliquaryId: String? {
        if sanctuaryId.contains("shroud") || sanctuaryId.contains("tunic") || sanctuaryId.contains("sudarium") {
            return "reliquary_passion_textile"
        } else if sanctuaryId.contains("cross") || sanctuaryId.contains("christ_cathedral") {
            return "reliquary_passion_cross"
        } else if sanctuaryId.contains("santiago") || sanctuaryId.contains("peter") || sanctuaryId.contains("francis") {
            return "reliquary_silver_casket"
        }
        return nil
    }
}

public struct SanctuaryLocation: Codable, Hashable {
    public let shrineOrBasilica: String?
    public let city: String
    public let regionOrState: String?
    public let country: String
    public let latitude: Double
    public let longitude: Double
    public let precision: String

    enum CodingKeys: String, CodingKey {
        case shrineOrBasilica = "shrine_or_basilica"
        case city
        case regionOrState = "region_or_state"
        case country
        case latitude
        case longitude
        case precision
    }
}

public struct SanctuaryCanonicalStatus: Codable, Hashable {
    public let approvalOrConsecrationDate: String?
    public let approvingAuthority: String?
    public let confidence: String
    public let confidenceNoteEn: String?
    public let confidenceNoteVi: String?

    enum CodingKeys: String, CodingKey {
        case approvalOrConsecrationDate = "approval_or_consecration_date"
        case approvingAuthority = "approving_authority"
        case confidence
        case confidenceNoteEn = "confidence_note_en"
        case confidenceNoteVi = "confidence_note_vi"
    }

    public var confidenceLevel: ConfidenceLevel {
        switch confidence.lowercased() {
        case "confirmed": return .confirmed
        case "traditional": return .traditional
        case "contextual": return .contextual
        default: return .traditional
        }
    }
}

public struct SanctuaryRelic: Codable, Hashable {
    public let relicNameEn: String
    public let relicNameVi: String
    public let relicType: String
    public let reliquaryLocation: String?

    enum CodingKeys: String, CodingKey {
        case relicNameEn = "relic_name_en"
        case relicNameVi = "relic_name_vi"
        case relicType = "relic_type"
        case reliquaryLocation = "reliquary_location"
    }

    public func name(for language: LanguageMode) -> String {
        language == .vietnamese ? relicNameVi : relicNameEn
    }
}

public struct SanctuarySource: Codable, Hashable {
    public let label: String
    public let url: String
    public let type: String?
}
