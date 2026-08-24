//  AnnoDevotionalLoader.swift
//  Anno
//
//  Deterministic date-rotation engine for Catholic 365-day devotional pool.
//  Matches a calendar date to a devotional entry via day-of-year indexing.
//  Fully supports bilingual English and Vietnamese content.

import Foundation

/// Stateless loader that resolves the devotional for any calendar date.
nonisolated enum AnnoDevotionalLoader {
    /// Loads the devotional pool from the given bundle (defaults to main).
    static func pool(bundle: Bundle = .main) -> [Devotional] {
        guard let url = bundle.url(forResource: "anno_devotional_pool_365", withExtension: "json") ??
                        bundle.url(forResource: "annodevotionals", withExtension: "json"),
              let data = try? Data(contentsOf: url) else {
            return []
        }
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        if let fixture = try? decoder.decode(DevotionalPoolFixture.self, from: data) {
            return fixture.devotionals
        } else if let array = try? decoder.decode([Devotional].self, from: data) {
            return array
        }
        return []
    }

    /// Resolves the devotional for a date using a deterministic day-of-year index.
    static func devotional(for date: Date = .now, bundle: Bundle = .main) -> Devotional? {
        let all = pool(bundle: bundle)
        guard !all.isEmpty else { return nil }
        let dayOfYear = Calendar.current.ordinality(of: .day, in: .year, for: date) ?? 1
        let index = max(0, min(dayOfYear - 1, all.count - 1))
        return all[index]
    }
}
