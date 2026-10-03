import Combine
import Foundation

@MainActor
final class PilgrimageProgressStore: ObservableObject {
    static let shared = PilgrimageProgressStore()

    @Published private var revision = 0

    private let defaults: UserDefaults

    init(defaults: UserDefaults = .standard) {
        self.defaults = defaults
    }

    func isVisited(routeId: String, waypointId: String) -> Bool {
        visitedWaypointIds(routeId: routeId).contains(waypointId)
    }

    func visitedCount(route: PilgrimageRoute) -> Int {
        visitedCount(
            routeId: route.routeId,
            requiredStationIds: route.waypoints.map(\.waypointId)
        )
    }

    func visitedCount(
        routeId: String,
        requiredStationIds: [String]
    ) -> Int {
        let visited = visitedWaypointIds(routeId: routeId)
        return requiredStationIds.reduce(into: 0) { count, stationId in
            if visited.contains(stationId) {
                count += 1
            }
        }
    }

    func hasVisitedAll(
        routeId: String,
        requiredStationIds: [String]
    ) -> Bool {
        guard !requiredStationIds.isEmpty else { return false }
        return visitedCount(
            routeId: routeId,
            requiredStationIds: requiredStationIds
        ) == requiredStationIds.count
    }

    func completionDate(routeId: String) -> Date? {
        defaults.object(forKey: completionDateKey(routeId: routeId)) as? Date
    }

    func markVisited(route: PilgrimageRoute, waypoint: PilgrimageWaypoint) {
        var visited = visitedWaypointIds(routeId: route.routeId)
        visited.insert(waypoint.waypointId)
        saveVisited(visited, routeId: route.routeId)

        revision += 1
    }

    func markCompleted(routeId: String) {
        guard completionDate(routeId: routeId) == nil else { return }
        defaults.set(Date(), forKey: completionDateKey(routeId: routeId))
        revision += 1
    }

    func reset(routeId: String) {
        defaults.removeObject(forKey: visitedKey(routeId: routeId))
        defaults.removeObject(forKey: completionDateKey(routeId: routeId))
        revision += 1
    }

    private func visitedWaypointIds(routeId: String) -> Set<String> {
        Set(defaults.stringArray(forKey: visitedKey(routeId: routeId)) ?? [])
    }

    private func saveVisited(_ visited: Set<String>, routeId: String) {
        defaults.set(Array(visited).sorted(), forKey: visitedKey(routeId: routeId))
    }

    private func visitedKey(routeId: String) -> String {
        "anno.pilgrimage.\(routeId).visited"
    }

    private func completionDateKey(routeId: String) -> String {
        "anno.pilgrimage.\(routeId).completedAt"
    }
}
