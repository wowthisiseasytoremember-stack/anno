import CoreLocation
import Foundation

/// A localized narration track for one sanctuary.
///
/// `audioFileName` is a bundle resource name *without* extension
/// (e.g. `"hagiography_st_james_en"`); `AudioHagiographyPlayer`
/// resolves it against known audio extensions (`m4a`, `mp3`, `wav`, `aac`).
public struct LocalizedNarration: Codable, Hashable, Sendable {
    public let audioFileName: String
    public let transcript: String

    public init(audioFileName: String, transcript: String) {
        self.audioFileName = audioFileName
        self.transcript = transcript
    }
}

/// One geofenced pilgrimage site, decoded from `SanctuariesConfig.json`.
///
/// The schema is intentionally flat (`latitude`/`longitude` rather than a
/// nested coordinate object) so sanctuary data can be authored and diffed by
/// hand. Two authoring forms are accepted for `narrations`:
///
/// 1. Preferred: a `"narrations"` dictionary keyed by language code
///    (`"en"`, `"es"`, `"it"`, …), each with `audioFileName` + `transcript`.
/// 2. Legacy/flat: top-level `audioFileName` + `transcript`, which decode
///    as the `"en"` narration. This keeps older single-language configs
///    loading without modification.
///
/// Adding a sanctuary = adding an entry here + dropping the audio file into
/// the bundle. No code changes.
public struct SanctuarySite: Identifiable, Codable, Hashable, Sendable {
    public let id: String
    public let name: String
    public let latitude: Double
    public let longitude: Double
    public let radiusMeters: Double
    public let associatedReliquaryId: String?
    public let narrations: [String: LocalizedNarration]

    public var coordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
    }

    public init(
        id: String,
        name: String,
        latitude: Double,
        longitude: Double,
        radiusMeters: Double,
        associatedReliquaryId: String? = nil,
        narrations: [String: LocalizedNarration]
    ) {
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.radiusMeters = radiusMeters
        self.associatedReliquaryId = associatedReliquaryId
        self.narrations = narrations
    }

    // MARK: - Codable (flat-JSON compatibility)

    private enum CodingKeys: String, CodingKey {
        case id, name, latitude, longitude
        case radiusMeters
        case associatedReliquaryId
        case narrations
        case audioFileName
        case transcript
    }

    public init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        id = try container.decode(String.self, forKey: .id)
        name = try container.decode(String.self, forKey: .name)
        latitude = try container.decode(Double.self, forKey: .latitude)
        longitude = try container.decode(Double.self, forKey: .longitude)
        radiusMeters = try container.decode(Double.self, forKey: .radiusMeters)
        associatedReliquaryId = try container.decodeIfPresent(String.self, forKey: .associatedReliquaryId)

        if let dict = try container.decodeIfPresent([String: LocalizedNarration].self, forKey: .narrations), !dict.isEmpty {
            narrations = dict
        } else {
            // Legacy flat form: treat as English narration.
            let audio = try container.decode(String.self, forKey: .audioFileName)
            let text = try container.decode(String.self, forKey: .transcript)
            narrations = ["en": LocalizedNarration(audioFileName: audio, transcript: text)]
        }
    }

    public func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(id, forKey: .id)
        try container.encode(name, forKey: .name)
        try container.encode(latitude, forKey: .latitude)
        try container.encode(longitude, forKey: .longitude)
        try container.encode(radiusMeters, forKey: .radiusMeters)
        try container.encodeIfPresent(associatedReliquaryId, forKey: .associatedReliquaryId)
        try container.encode(narrations, forKey: .narrations)
    }
}
