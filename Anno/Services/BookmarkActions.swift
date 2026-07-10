//  BookmarkActions.swift
//  DailyDevotionKJVForWomen
//
//  Helper operations for creating, toggling and querying bookmarks.
//

import Foundation
import SwiftData

/// Stateless helpers for working with bookmarks via a `ModelContext`.
enum BookmarkActions {
    /// Returns true if a bookmark already exists for the reference.
    static func exists(_ reference: VerseReference, in context: ModelContext) -> Bool {
        let id = reference.id
        var descriptor = FetchDescriptor<Bookmark>(
            predicate: #Predicate { $0.referenceID == id }
        )
        descriptor.fetchLimit = 1
        return (try? context.fetch(descriptor).first) != nil
    }

    /// Toggles a bookmark for the given verse and returns the new state.
    @discardableResult
    static func toggle(reference: VerseReference, text: String, in context: ModelContext) -> Bool {
        let id = reference.id
        var descriptor = FetchDescriptor<Bookmark>(
            predicate: #Predicate { $0.referenceID == id }
        )
        descriptor.fetchLimit = 1
        if let existing = try? context.fetch(descriptor).first {
            context.delete(existing)
            try? context.save()
            return false
        } else {
            context.insert(Bookmark(reference: reference, text: text))
            try? context.save()
            return true
        }
    }

    static func remove(_ bookmark: Bookmark, in context: ModelContext) {
        context.delete(bookmark)
        try? context.save()
    }
}
//