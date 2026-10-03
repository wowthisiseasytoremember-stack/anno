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

    static func markerURL(index: Int) -> URL? {
        URL(string: "anno://p/lv/\(index)")
    }

    /// Text payload suitable for a temporary printable QR marker.
    static func qrPayload(index: Int) -> String? {
        markerURL(index: index)?.absoluteString
    }

    /// Produces the actual NDEF URI record used by a writable NFC tag.
    ///
    /// The Core NFC write session remains staged because it requires target
    /// entitlements and physical-device validation.
    static func nfcPayload(index: Int) -> NFCNDEFPayload? {
        guard let url = markerURL(index: index) else {
            return nil
        }
        return NFCNDEFPayload.wellKnownTypeURIPayload(url: url)
    }
}
