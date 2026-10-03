import Foundation

/// Converts Anno's canonical pilgrimage snapshot into Apple system surfaces.
///
/// This keeps Dynamic Island, Watch, and later system integrations from
/// inventing separate state models.
enum AnnoPilgrimageAppleBridge {
    @MainActor
    static func begin(_ snapshot: PilgrimageSystemSnapshot) {
        let activityState = liveActivityState(snapshot)

        _ = AnnoPilgrimageLiveActivityController.shared.start(
            routeId: snapshot.routeId,
            routeTitle: snapshot.routeTitle,
            state: activityState
        )

        AnnoWatchConnectivityBridge.shared.activate()
        updateWatch(snapshot)
    }

    @MainActor
    static func update(_ snapshot: PilgrimageSystemSnapshot) async {
        await AnnoPilgrimageLiveActivityController.shared.update(
            liveActivityState(snapshot)
        )

        updateWatch(snapshot)
    }

    @MainActor
    static func end(
        _ snapshot: PilgrimageSystemSnapshot,
        completed: Bool
    ) async {
        await AnnoPilgrimageLiveActivityController.shared.end(
            finalState: liveActivityState(snapshot),
            completed: completed
        )

        AnnoWatchConnectivityBridge.shared.clearPilgrimageContext()
    }

    private static func liveActivityState(
        _ snapshot: PilgrimageSystemSnapshot
    ) -> AnnoPilgrimageActivityAttributes.ContentState {
        .init(
            chapterNumber: snapshot.chapterNumber,
            chapterTitle: snapshot.chapterTitle,
            currentStationTitle: snapshot.stationTitle,
            nextStationTitle: snapshot.nextStationTitle,
            visitedCount: snapshot.visitedCount,
            totalCount: snapshot.totalCount,
            phase: .init(rawValue: snapshot.phase.rawValue) ?? .traveling
        )
    }

    private static func updateWatch(
        _ snapshot: PilgrimageSystemSnapshot
    ) {
        AnnoWatchConnectivityBridge.shared.updatePilgrimageContext(
            routeId: snapshot.routeId,
            routeTitle: snapshot.routeTitle,
            chapterTitle: snapshot.chapterTitle,
            stationId: snapshot.stationId,
            stationTitle: snapshot.stationTitle,
            nextStationTitle: snapshot.nextStationTitle,
            visitedCount: snapshot.visitedCount,
            totalCount: snapshot.totalCount,
            phase: snapshot.phase.rawValue
        )
    }
}
