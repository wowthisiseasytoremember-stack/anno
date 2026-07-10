//  DevotionalProvider.swift
//  DailyDevotionKJVForWomen
//
//  Loads the curated devotional pool and selects a passage deterministically
//  by calendar date. The same date always resolves to the same devotional.
//

import Foundation
import Observation

/// Provides daily devotionals with deterministic date-based rotation.
@Observable
@MainActor
final class DevotionalProvider {
    private(set) var pool: [Devotional] = []

    init() {
        load()
    }

    private func load() {
        guard let url = Bundle.main.url(forResource: "devotionals", withExtension: "json"),
              let data = try? Data(contentsOf: url) else {
            pool = []
            return
        }
        pool = (try? JSONDecoder().decode([Devotional].self, from: data)) ?? []
    }

    /// Deterministic day index used to select a devotional.
    /// Combines year and day-of-year so a given calendar date always maps to
    /// the same passage, while different dates spread across the pool.
    private func index(for date: Date) -> Int {
        guard !pool.isEmpty else { return 0 }
        let calendar = Calendar.current
        let dayOfYear = calendar.ordinality(of: .day, in: .year, for: date) ?? 1
        // A large prime keeps the sequence well-distributed across the pool.
        let seed = (dayOfYear &* 2654435761) & 0x7fffffff
        return seed % pool.count
    }

    /// The devotional for the given date (defaults to today).
    func devotional(for date: Date = .now) -> Devotional? {
        guard !pool.isEmpty else { return nil }
        return pool[index(for: date)]
    }

    /// Today's devotional.
    var today: Devotional? { devotional(for: .now) }

    /// A short list of upcoming devotionals for a preview strip.
    func upcoming(days: Int = 7) -> [(date: Date, devotional: Devotional)] {
        let calendar = Calendar.current
        return (1...days).compactMap { offset in
            guard let date = calendar.date(byAdding: .day, value: offset, to: .now),
                  let dev = devotional(for: date) else { return nil }
            return (date, dev)
        }
    }
}
//