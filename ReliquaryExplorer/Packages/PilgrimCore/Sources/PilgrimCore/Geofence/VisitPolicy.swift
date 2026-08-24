import Foundation

/// Decides whether a geofence entry should trigger narration, applying:
///
/// - a per-site cooldown (a pilgrim loitering at the boundary, GPS jitter,
///   or a small sanctuary shopped in one visit should not re-trigger), and
/// - exit re-arming (leaving and genuinely returning after the cooldown
///   plays again — walking the same street twice is a real pilgrimage
///   pattern, e.g. the Franciscan circuit in Assisi).
///
/// Pure state machine: registered in tests against hand-built event
/// sequences; driven in production by `PilgrimGuideCoordinator`.
public struct VisitPolicy: Sendable {
    public let cooldown: TimeInterval

    /// siteID -> timestamp of the last *acted-upon* entry.
    private var lastTriggeredEntry: [String: Date] = [:]
    /// siteIDs the user is currently inside (per geofence state).
    private var inside: Set<String> = []

    public init(cooldown: TimeInterval = 10 * 60) {
        self.cooldown = cooldown
        assert(cooldown >= 0)
    }

    public mutating func register(_ event: SanctuaryVisitEvent) -> NarrationDecision {
        switch event.kind {
        case .entered:
            let wasInside = !inside.insert(event.site.id).inserted
            let last = lastTriggeredEntry[event.site.id]

            if let last, event.timestamp.timeIntervalSince(last) < cooldown {
                return .skip(.cooldownActive)
            }
            if wasInside {
                // Duplicate .entered for a region we never saw .exited for
                // (app relaunch inside a region, for example).
                return .skip(.alreadyInside)
            }

            lastTriggeredEntry[event.site.id] = event.timestamp
            return .play

        case .exited:
            inside.remove(event.site.id)
            return .skip(.exited)
        }
    }

    public var sitesCurrentlyInside: Set<String> { inside }
}

public enum NarrationDecision: Equatable, Sendable {
    case play
    case skip(SkipReason)
}

public enum SkipReason: Equatable, Sendable {
    case cooldownActive
    case alreadyInside
    case exited
}
