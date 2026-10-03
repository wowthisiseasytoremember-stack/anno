import Foundation

enum AnnoDeepLink: Equatable, Sendable {
    case today(entryId: String?)
    case pilgrimage(routeId: String, stationId: String?)

    static let scheme = "anno"

    init?(url: URL) {
        guard url.scheme?.lowercased() == Self.scheme else {
            return nil
        }

        let host = url.host?.lowercased()
        let parts = url.pathComponents.filter { $0 != "/" }

        switch host {
        case "p":
            guard parts.count >= 2,
                  parts[0].lowercased() == "lv",
                  let stationId = Self.laVangPhysicalAliases[parts[1]] else {
                return nil
            }

            self = .pilgrimage(
                routeId: Self.laVangRouteId,
                stationId: stationId
            )

        case "today":
            self = .today(entryId: parts.first)

        case "pilgrimage":
            guard let routeId = parts.first else {
                return nil
            }
            self = .pilgrimage(
                routeId: routeId,
                stationId: parts.dropFirst().first
            )

        default:
            return nil
        }
    }

    var url: URL? {
        var components = URLComponents()
        components.scheme = Self.scheme

        switch self {
        case .today(let entryId):
            components.host = "today"
            if let entryId {
                components.path = "/" + entryId
            }

        case .pilgrimage(let routeId, let stationId):
            components.host = "pilgrimage"
            components.path = "/" + routeId
            if let stationId {
                components.path += "/" + stationId
            }
        }

        return components.url
    }

    static func pilgrimage(
        route: PilgrimageRoute,
        waypoint: PilgrimageWaypoint? = nil
    ) -> URL? {
        AnnoDeepLink.pilgrimage(
            routeId: route.routeId,
            stationId: waypoint?.waypointId
        ).url
    }

    static func laVangPhysicalMarkerURL(index: Int) -> URL? {
        guard Self.laVangPhysicalAliases[String(index)] != nil else {
            return nil
        }

        return URL(string: "anno://p/lv/\(index)")
    }

    private static let laVangRouteId =
        "socal_vietnamese_catholic_pilgrimage_la_vang"

    private static let laVangPhysicalAliases: [String: String] = [
        "1": "our_lady_la_vang_shrine_christ_cathedral",
        "2": "martyrs_wall_117_vietnamese_christian",
        "3": "rosary_gardens_christ_cathedral_pilgrimage",
        "4": "st_columban_church_garden_grove",
        "5": "vietnamese_catholic_center_santa_ana",
        "6": "our_lady_of_la_vang_church_santa_ana",
        "7": "st_barbara_parish_westminster"
    ]
}
