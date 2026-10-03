import Foundation

struct PilgrimageSystemSnapshot: Codable, Hashable, Sendable {
    enum Phase: String, Codable, Hashable, Sendable {
        case traveling
        case arrived
        case praying
        case completed
    }

    let routeId: String
    let routeTitle: String
    let chapterNumber: Int
    let chapterTitle: String
    let stationId: String
    let stationTitle: String
    let nextStationTitle: String?
    let visitedCount: Int
    let totalCount: Int
    let phase: Phase
}

@MainActor
enum PilgrimageSystemSnapshotBuilder {
    static func make(
        route: PilgrimageRoute,
        waypoint: PilgrimageWaypoint,
        language: LanguageMode,
        content: SoCalExemplarContent?,
        progress: PilgrimageProgressStore,
        phase: PilgrimageSystemSnapshot.Phase
    ) -> PilgrimageSystemSnapshot {
        let requiredIds = content?.coreRequiredStationIds
            ?? route.waypoints.map(\.waypointId)

        let visitedCount = progress.visitedCount(
            routeId: route.routeId,
            requiredStationIds: requiredIds
        )

        let isComplete = progress.hasVisitedAll(
            routeId: route.routeId,
            requiredStationIds: requiredIds
        )

        let chapter = content?.chapter(containing: waypoint.waypointId)

        let nextStationTitle: String? = requiredIds
            .drop {
                progress.isVisited(
                    routeId: route.routeId,
                    waypointId: $0
                )
            }
            .first
            .flatMap { id in
                if let station = content?.station(id: id) {
                    return station.title(for: language)
                }

                return route.waypoints.first(where: {
                    $0.waypointId == id
                })?.name(for: language)
            }

        return PilgrimageSystemSnapshot(
            routeId: route.routeId,
            routeTitle: route.title(for: language),
            chapterNumber: chapter?.order ?? 0,
            chapterTitle: chapter?.geographicName ?? route.region,
            stationId: waypoint.waypointId,
            stationTitle: content?.station(id: waypoint.waypointId)?
                .title(for: language)
                ?? waypoint.name(for: language),
            nextStationTitle: isComplete ? nil : nextStationTitle,
            visitedCount: visitedCount,
            totalCount: requiredIds.count,
            phase: isComplete ? .completed : phase
        )
    }
}
