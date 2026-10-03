import ActivityKit
import Foundation

/// App-side controller for Anno's active-pilgrimage Live Activity.
///
/// Kept outside the shipping target until the Widget Extension is activated.
/// Uses current ActivityContent APIs rather than deprecated contentState calls.
@MainActor
final class AnnoPilgrimageLiveActivityController {
    static let shared = AnnoPilgrimageLiveActivityController()

    private var activity: Activity<AnnoPilgrimageActivityAttributes>?

    private init() {}

    var isEnabled: Bool {
        ActivityAuthorizationInfo().areActivitiesEnabled
    }

    var activeActivityId: String? {
        activity?.id
    }

    func restore(routeId: String) {
        activity = Activity<AnnoPilgrimageActivityAttributes>.activities.first {
            $0.attributes.routeId == routeId
        }
    }

    @discardableResult
    func start(
        routeId: String,
        routeTitle: String,
        state: AnnoPilgrimageActivityAttributes.ContentState
    ) -> Bool {
        guard isEnabled else { return false }

        if let existing = Activity<AnnoPilgrimageActivityAttributes>.activities.first(
            where: { $0.attributes.routeId == routeId }
        ) {
            activity = existing
            Task {
                await update(state)
            }
            return true
        }

        let attributes = AnnoPilgrimageActivityAttributes(
            routeId: routeId,
            routeTitle: routeTitle
        )

        let content = ActivityContent(
            state: state,
            staleDate: nil
        )

        do {
            activity = try Activity.request(
                attributes: attributes,
                content: content,
                pushType: nil
            )
            return true
        } catch {
            #if DEBUG
            print("Anno Live Activity start failed: \(error)")
            #endif
            return false
        }
    }

    func update(
        _ state: AnnoPilgrimageActivityAttributes.ContentState
    ) async {
        guard let activity else { return }

        await activity.update(
            ActivityContent(
                state: state,
                staleDate: nil
            )
        )
    }

    func end(
        finalState: AnnoPilgrimageActivityAttributes.ContentState?,
        completed: Bool
    ) async {
        guard let activity else { return }

        let finalContent = finalState.map {
            ActivityContent(state: $0, staleDate: nil)
        }

        await activity.end(
            finalContent,
            dismissalPolicy: completed
                ? .after(Date().addingTimeInterval(30 * 60))
                : .immediate
        )

        self.activity = nil
    }
}
