//  SearchHistory.swift
//  DailyDevotionKJVForWomen
//
//  Persists recent search terms to UserDefaults.
//

import Foundation

/// Lightweight recent-search history persisted to UserDefaults.
enum SearchHistory {
    private static let key = "search.recents"
    private static let limit = 8

    static func load() -> [String] {
        UserDefaults.standard.stringArray(forKey: key) ?? []
    }

    /// Adds a term to the front, de-duplicating, and returns the new list.
    @discardableResult
    static func add(_ term: String) -> [String] {
        var list = load().filter { $0.caseInsensitiveCompare(term) != .orderedSame }
        list.insert(term, at: 0)
        if list.count > limit { list = Array(list.prefix(limit)) }
        UserDefaults.standard.set(list, forKey: key)
        return list
    }

    static func clear() {
        UserDefaults.standard.removeObject(forKey: key)
    }
}
//