import Foundation
import WatchConnectivity

/// Mirrors the latest pilgrimage state to the companion Watch app.
///
/// Application context is appropriate here because only the newest pilgrimage
/// snapshot matters; older snapshots should be replaced rather than queued.
final class AnnoWatchConnectivityBridge: NSObject, WCSessionDelegate {
    static let shared = AnnoWatchConnectivityBridge()

    private override init() {
        super.init()
    }

    func activate() {
        guard WCSession.isSupported() else { return }

        let session = WCSession.default
        session.delegate = self
        session.activate()
    }

    func updatePilgrimageContext(
        routeId: String,
        routeTitle: String,
        chapterTitle: String,
        stationId: String,
        stationTitle: String,
        nextStationTitle: String?,
        visitedCount: Int,
        totalCount: Int,
        phase: String
    ) {
        guard WCSession.isSupported() else { return }

        var context: [String: Any] = [
            "route_id": routeId,
            "route_title": routeTitle,
            "chapter_title": chapterTitle,
            "station_id": stationId,
            "station_title": stationTitle,
            "visited_count": visitedCount,
            "total_count": totalCount,
            "phase": phase,
            "updated_at": Date().timeIntervalSince1970
        ]

        if let nextStationTitle {
            context["next_station_title"] = nextStationTitle
        }

        do {
            try WCSession.default.updateApplicationContext(context)
        } catch {
            #if DEBUG
            print("Anno Watch context update failed: \(error)")
            #endif
        }
    }

    func clearPilgrimageContext() {
        guard WCSession.isSupported() else { return }

        do {
            try WCSession.default.updateApplicationContext([
                "active": false,
                "updated_at": Date().timeIntervalSince1970
            ])
        } catch {
            #if DEBUG
            print("Anno Watch context clear failed: \(error)")
            #endif
        }
    }

    func session(
        _ session: WCSession,
        activationDidCompleteWith activationState: WCSessionActivationState,
        error: Error?
    ) {}

    #if os(iOS)
    func sessionDidBecomeInactive(_ session: WCSession) {}

    func sessionDidDeactivate(_ session: WCSession) {
        session.activate()
    }
    #endif
}
