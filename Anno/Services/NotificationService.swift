//  NotificationService.swift
//  DailyDevotionKJVForWomen
//
//  Schedules optional daily devotional reminders using UserNotifications.
//

import Foundation
import UserNotifications

/// Time-of-day options for the daily reminder.
enum ReminderTime: String, CaseIterable, Identifiable, Sendable {
    case morning
    case afternoon
    case evening

    var id: String { rawValue }

    var title: String {
        switch self {
        case .morning: return "Morning"
        case .afternoon: return "Afternoon"
        case .evening: return "Evening"
        }
    }

    var symbol: String {
        switch self {
        case .morning: return "sunrise.fill"
        case .afternoon: return "sun.max.fill"
        case .evening: return "moon.stars.fill"
        }
    }

    /// Hour of day used for scheduling.
    var hour: Int {
        switch self {
        case .morning: return 7
        case .afternoon: return 13
        case .evening: return 20
        }
    }
}

/// Manages authorization and scheduling of the daily reminder.
enum NotificationService {
    static let reminderIdentifier = "daily-devotional-reminder"

    /// Requests notification permission; returns whether granted.
    @discardableResult
    static func requestAuthorization() async -> Bool {
        do {
            return try await UNUserNotificationCenter.current()
                .requestAuthorization(options: [.alert, .sound, .badge])
        } catch {
            return false
        }
    }

    static func authorizationStatus() async -> UNAuthorizationStatus {
        await UNUserNotificationCenter.current().notificationSettings().authorizationStatus
    }

    /// Schedules a daily repeating reminder at the chosen time of day.
    static func schedule(at time: ReminderTime) async {
        let center = UNUserNotificationCenter.current()
        center.removePendingNotificationRequests(withIdentifiers: [reminderIdentifier])

        let content = UNMutableNotificationContent()
        content.title = "A moment with Him"
        content.body = "Your daily devotional is ready. Take a peaceful pause."
        content.sound = .default

        var components = DateComponents()
        components.hour = time.hour
        components.minute = 0

        let trigger = UNCalendarNotificationTrigger(dateMatching: components, repeats: true)
        let request = UNNotificationRequest(
            identifier: reminderIdentifier,
            content: content,
            trigger: trigger
        )
        try? await center.add(request)
    }

    /// Cancels the daily reminder.
    static func cancel() {
        UNUserNotificationCenter.current()
            .removePendingNotificationRequests(withIdentifiers: [reminderIdentifier])
    }
}
//