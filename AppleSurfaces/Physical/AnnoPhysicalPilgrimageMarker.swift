import CoreNFC
import Foundation

/// Stable physical-marker identities for the Orange County field-test route.
///
/// These IDs are deliberately aligned with Anno station IDs so QR, NFC, and
/// future beacon payloads all resolve through the same deep-link router.
enum AnnoPhysicalPilgrimageMarker {
    static let routeId = "socal_vietnamese_catholic_pilgrimage_la_vang"

    static let christCathedralStations: [String] = [
        "our_lady_la_vang_shrine_christ_cathedral",
        "martyrs_wall_117_vietnamese_christian",
        "rosary_gardens_christ_cathedral_pilgrimage"
    ]

    static func deepLinkURL(stationId: String) -> URL? {
        var components = URLComponents()
        components.scheme = "anno"
        components.host = "pilgrimage"
        components.path = "/\(routeId)/\(stationId)"
        return components.url
    }

    /// Text payload suitable for a temporary printable QR marker.
    static func qrPayload(stationId: String) -> String? {
        deepLinkURL(stationId: stationId)?.absoluteString
    }

    /// Produces the actual NDEF URI record used by a writable NFC tag.
    ///
    /// The Core NFC write session remains staged because it requires target
    /// entitlements and physical-device validation.
    static func nfcPayload(stationId: String) -> NFCNDEFPayload? {
        guard let url = deepLinkURL(stationId: stationId) else {
            return nil
        }
        return NFCNDEFPayload.wellKnownTypeURIPayload(url: url)
    }
}
