import ActivityKit
import Foundation

/// Shared state for Anno's active-pilgrimage Live Activity.
///
/// Keep ContentState tiny. ActivityKit limits encoded dynamic state to 4 KB.
struct AnnoPilgrimageActivityAttributes: ActivityAttributes {
    struct ContentState: Codable, Hashable {
        enum Phase: String, Codable, Hashable {
            case traveling
            case arrived
            case praying
            case completed
        }

        var chapterNumber: Int
        var chapterTitle: String
        var currentStationTitle: String
        var nextStationTitle: String?
        var visitedCount: Int
        var totalCount: Int
        var phase: Phase

        var progress: Double {
            guard totalCount > 0 else { return 0 }
            return min(1, max(0, Double(visitedCount) / Double(totalCount)))
        }
    }

    let routeId: String
    let routeTitle: String
}
