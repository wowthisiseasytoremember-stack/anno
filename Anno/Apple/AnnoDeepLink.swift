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
}
