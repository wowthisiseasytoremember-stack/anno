import Foundation
import UserNotifications

/// Abstracts `UNUserNotificationCenter` so the coordinator is testable.
public protocol VisitNotifying: AnyObject {
    func requestAuthorization() async -> Bool
    /// Returns true if the notification was scheduled.
    @discardableResult
    func postArrivalNotification(siteName: String, transcript: String) async -> Bool
}

/// Production notifier — local notifications only (no push, no servers).
public final class LocalVisitNotifier: VisitNotifying {
    private let center = UNUserNotificationCenter.current()

    public init() {}

    public func requestAuthorization() async -> Bool {
        (try? await center.requestAuthorization(options: [.alert, .sound])) ?? false
    }

    @discardableResult
    public func postArrivalNotification(siteName: String, transcript: String) async -> Bool {
        let content = UNMutableNotificationContent()
        content.title = siteName
        content.body = String(transcript.prefix(140))
        content.sound = .default

        let request = UNNotificationRequest(
            identifier: "hagiography_\(siteName)_\(UUID().uuidString)",
            content: content,
            trigger: nil
        )
        do {
            try await center.add(request)
            return true
        } catch {
            return false
        }
    }
}

/// Abstracts app lifecycle for the coordinator (iOS: UIApplication; both
/// platforms can alternatively use ScenePhase from SwiftUI).
@MainActor
public protocol AppPhaseProviding: AnyObject {
    var isApplicationBackgrounded: Bool { get }
}
