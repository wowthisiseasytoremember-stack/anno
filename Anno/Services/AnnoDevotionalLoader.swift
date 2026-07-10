//  AnnoDevotionalLoader.swift
//  Anno
//
//  Adapted from DailyDevotionKJVForWomen's DailyDevotionalLoader.
//  Cloned from DailyDevotionKJVForWomen via KJV→Anno migration plan.
//  Deterministic date-rotation engine — same date → same devotional.
//  Supports Catholic/Vietnamese content by loading from named bundle resources.

import Foundation

/// Stateless loader that resolves the devotional for any calendar date.
nonisolated enum AnnoDevotionalLoader {
    /// Loads the devotional pool from the given bundle (defaults to main).
    static func pool(bundle: Bundle = .main) -> [Devotional] {
        guard let url = bundle.url(forResource: "annodevotionals", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let decoded = try? JSONDecoder().decode([Devotional].self, from: data) else {
            return []
        }
        return decoded
    }

    /// Resolves the devotional for a date using a deterministic scheme.
    static func devotional(for date: Date = .now, bundle: Bundle = .main) -> Devotional? {
        let all = pool(bundle: bundle)
        guard !all.isEmpty else { return nil }
        let dayOfYear = Calendar.current.ordinality(of: .day, in: .year, for: date) ?? 1
        let seed = (dayOfYear &* 2654435761) & 0x7fffffff
        return all[seed % all.count]
    }
}
